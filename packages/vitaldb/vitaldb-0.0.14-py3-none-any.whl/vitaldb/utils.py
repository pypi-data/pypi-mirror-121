import os
import errno
import gzip
import numpy as np
import datetime
import tempfile
import shutil
import pandas as pd
from urllib import parse, request
from struct import pack, unpack_from, Struct
import s3fs

unpack_b = Struct('<b').unpack_from
unpack_w = Struct('<H').unpack_from
unpack_s = Struct('<h').unpack_from
unpack_f = Struct('<f').unpack_from
unpack_d = Struct('<d').unpack_from
unpack_dw = Struct('<L').unpack_from
pack_b = Struct('<b').pack
pack_w = Struct('<H').pack
pack_s = Struct('<h').pack
pack_f = Struct('<f').pack
pack_d = Struct('<d').pack
pack_dw = Struct('<L').pack


def unpack_str(buf, pos):
    strlen = unpack_dw(buf, pos)[0]
    pos += 4
    val = buf[pos:pos + strlen].decode('utf-8', 'ignore')
    pos += strlen
    return val, pos


def pack_str(s):
    sutf = s.encode('utf-8')
    return pack_dw(len(sutf)) + sutf


# 4 byte L (unsigned) l (signed)
# 2 byte H (unsigned) h (signed)
# 1 byte B (unsigned) b (signed)
def parse_fmt(fmt):
    if fmt == 1:
        return 'f', 4
    elif fmt == 2:
        return 'd', 8
    elif fmt == 3:
        return 'b', 1
    elif fmt == 4:
        return 'B', 1
    elif fmt == 5:
        return 'h', 2
    elif fmt == 6:
        return 'H', 2
    elif fmt == 7:
        return 'l', 4
    elif fmt == 8:
        return 'L', 4
    return '', 0


class VitalFile:
    def __init__(self, ipath, track_names=None, track_names_only=False, exclude=[]):
        ext = os.path.splitext(ipath)[1]
        if ext == '.vital':
            self.load_vital(ipath, track_names, track_names_only, exclude)
        elif ext == '.parquet':
            if track_names_only:
                raise NotImplementedError
            self.load_parquet(ipath, track_names, exclude)

    def get_samples(self, dtname, interval):
        # 리턴 할 길이
        nret = int(np.ceil((self.dtend - self.dtstart) / interval))

        trk = self.find_track(dtname)
        if trk:
            if trk['type'] == 2:  # numeric track
                ret = np.full(nret, np.nan, dtype=np.float32)  # create a dense array
                for rec in trk['recs']:  # copy values
                    idx = int((rec['dt'] - self.dtstart) / interval)
                    if idx < 0:
                        idx = 0
                    elif idx >= nret:
                        idx = nret - 1
                    ret[idx] = rec['val']
                # if return_pandas:  # 현재 pandas sparse data를 to_parquet 함수에서 지원하지 않음
                #     return pd.Series(pd.arrays.SparseArray(ret))
                return ret
            elif trk['type'] == 5:  # str track
                ret = np.full(nret, np.nan, dtype='object')  # create a dense array
                for rec in trk['recs']:  # copy values
                    idx = int((rec['dt'] - self.dtstart) / interval)
                    if idx < 0:
                        idx = 0
                    elif idx >= nret:
                        idx = nret - 1
                    ret[idx] = rec['val']
                return ret
            elif trk['type'] == 1:  # wave track
                srate = trk['srate']
                recs = trk['recs']

                # 자신의 srate 만큼 공간을 미리 확보
                nsamp = int(np.ceil((self.dtend - self.dtstart) * srate))
                ret = np.full(nsamp, np.nan, dtype=np.float32)

                # 실제 샘플을 가져와 채움
                for rec in recs:
                    sidx = int(np.ceil((rec['dt'] - self.dtstart) * srate))
                    eidx = sidx + len(rec['val'])
                    srecidx = 0
                    erecidx = len(rec['val'])
                    if sidx < 0:  # self.dtstart 이전이면
                        srecidx -= sidx
                        sidx = 0
                    if eidx > nsamp:  # self.dtend 이후이면
                        erecidx -= (eidx - nsamp)
                        eidx = nsamp
                    ret[sidx:eidx] = rec['val'][srecidx:erecidx]

                # gain offset 변환
                if trk['fmt'] > 2:  # 1: float, 2: double
                    ret *= trk['gain']
                    ret += trk['offset']

                # 업샘플
                
                # 다운샘플
                if srate != int(1 / interval + 0.5):
                    ret = np.take(ret, np.linspace(0, nsamp - 1, nret).astype(np.int64))

                return ret

        # 트랙을 찾을 수 없을 때
        return np.full(nret, np.nan)

    def find_track(self, dtname):
        dname = None
        tname = dtname
        if dtname.find('/') != -1:
            dname, tname = dtname.split('/')

        for trk in self.trks.values():  # find track
            if trk['name'] == tname:
                did = trk['did']
                if did == 0 or not dname:
                    return trk                    
                if did in self.devs:
                    dev = self.devs[did]
                    if 'name' in dev and dname == dev['name']:
                        return trk

        return None

    def to_vital(self, opath, compresslevel=1):
        f = gzip.GzipFile(opath, 'wb', compresslevel=compresslevel)

        # save header
        if not f.write(b'VITA'):  # check sign
            return False
        if not f.write(pack_dw(3)):  # version
            return False
        if not f.write(pack_w(10)):  # header len
            return False
        if not f.write(pack_s(self.dgmt)):  # dgmt = ut - localtime
            return False
        if not f.write(pack_dw(0)):  # instance id
            return False
        if not f.write(pack_dw(0)):  # program version
            return False

        # save devinfos
        for did, dev in self.devs.items():
            if did == 0: continue
            ddata = pack_dw(did) + pack_str(dev['name']) + pack_str(dev['type']) + pack_str(dev['port'])
            if not f.write(pack_b(9) + pack_dw(len(ddata)) + ddata):
                return False

        # save trkinfos
        for tid, trk in self.trks.items():
            ti = pack_w(tid) + pack_b(trk['type']) + pack_b(trk['fmt']) + pack_str(trk['name']) \
                + pack_str(trk['unit']) + pack_f(trk['mindisp']) + pack_f(trk['maxdisp']) \
                + pack_dw(trk['col']) + pack_f(trk['srate']) + pack_d(trk['gain']) + pack_d(trk['offset']) \
                + pack_b(trk['montype']) + pack_dw(trk['did'])
            if not f.write(pack_b(0) + pack_dw(len(ti)) + ti):
                return False

            # save recs
            for rec in trk['recs']:
                rdata = pack_w(10) + pack_d(rec['dt']) + pack_w(tid)  # infolen + dt + tid (= 12 bytes)
                if trk['type'] == 1:  # wav
                    rdata += pack_dw(len(rec['val'])) + rec['val'].tobytes()
                elif trk['type'] == 2:  # num
                    fmtcode, fmtlen = parse_fmt(trk['fmt'])
                    rdata += pack(fmtcode, rec['val'])
                elif trk['type'] == 5:  # str
                    rdata += pack_dw(0) + pack_str(rec['val'])

                if not f.write(pack_b(1) + pack_dw(len(rdata)) + rdata):
                    return False

        # save trk order
        if hasattr(self, 'trkorder'):
            cdata = pack_b(5) + pack_w(len(self.trkorder)) + self.trkorder.tobytes()
            if not f.write(pack_b(6) + pack_dw(len(cdata)) + cdata):
                return False

        f.close()
        return True

    save_vital = to_vital

    def to_pandas(self):
        rows = []
        for _, trk in self.trks.items():
            dtname = trk['name']
            dname = ''
            did = trk['did']
            if did in self.devs:
                dev = self.devs[did]
                if 'name' in dev:
                    dname = dev['name']
                    dtname = dname + '/' + dtname  # 장비명을 앞에 붙임

            # 웨이브 트랙이면 대략 1초 단위로 이어붙임
            # parquet 파일에서 특별한 길이 제한은 없음
            newrecs = []
            if trk['type'] == 1 and trk['srate'] > 0:
                srate = trk['srate']
                newrec = {}
                for rec in trk['recs']:
                    if not newrec:  # 첫 샘플
                        newrec = rec
                    elif abs(newrec['dt'] + len(newrec['val']) / srate - rec['dt']) < 1.1 / srate and len(newrec['val']) < srate:
                        # 이전 샘플에서 이어짐
                        newrec['val'] = np.concatenate((newrec['val'], rec['val']))
                    else:  # 이어지지 않음
                        newrecs.append(newrec)
                        newrec = rec
                if newrec:
                    newrecs.append(newrec)
                trk['recs'] = newrecs

            for rec in trk['recs']:
                row = {'tname': dtname, 'dt': rec['dt']}
                if trk['type'] == 1:  # wav
                    vals = rec['val'].astype(np.float32)
                    if trk['fmt'] > 2:  # 1: float, 2: double
                        vals *= trk['gain']
                        vals += trk['offset']
                    row['wval'] = vals.tobytes()
                    row['nval'] = trk['srate']
                elif trk['type'] == 2:  # num
                    # row['val'] = pack_f(np.float32(rec['val']))
                    row['nval'] = rec['val']
                elif trk['type'] == 5:  # str
                    row['sval'] = rec['val']
                rows.append(row)

        df = pd.DataFrame(rows)
        if 'nval' in df:
            df['nval'] = df['nval'].astype(np.float32)
        return df

    def load_parquet(self, ipath, track_names, exclude):
        self.devs = {0: {}}  # did -> devinfo (name, type, port). did = 0 represents the vital recorder
        self.trks = {}  # tid -> trkinfo (name, type, fmt, unit, mindisp, maxdisp, col, srate, gain, offset, montype, did)
        self.dtstart = 0
        self.dtend = 0
        self.dgmt = 0
        
        dname_to_dids = {}
        dtname_to_tids = {}
        df = pd.read_parquet(ipath)
        for _, row in df.iterrows():
            # tname, dt, sval, wval, nval
            dtname = row['tname']
            dname = ''
            did = 0
            tname = dtname
            tid = 0
            if dtname.find('/') >= 0:
                dname, tname = dtname.split('/')

            if dname:
                if dname in dname_to_dids:
                    did = dname_to_dids[dname]
                else:  # 처음 나왔으면
                    did = len(dname_to_dids) + 1
                    dname_to_dids[dname] = did
                    self.devs[did] = {'name': dname, 'type': dname, 'port': ''}

            if dtname:
                if dtname in dtname_to_tids:
                    tid = dtname_to_tids[dtname]
                else:  # 처음 나왔으면
                    tid = len(dtname_to_tids) + 1
                    dtname_to_tids[dtname] = tid
                    if row['wval'] is not None:
                        ntype = 1  # wav
                        srate = row['nval']
                    elif row['sval'] is not None:
                        ntype = 5  # str
                        srate = 0
                    elif row['nval'] is not None:
                        ntype = 2  # num
                        srate = 0
                    else:
                        continue

                    # co2 -> yellow
                    # ecg -> green
                    # art -> red
                    # cvp -> orange
                    # pleth, spo2, vent, vnt -> skyblue
                    # eeg -> plum
                    
                    self.trks[tid] = {'name': tname, 'type': ntype, 'fmt': 1, # float32
                                      'unit': '', 'mindisp': 0, 'maxdisp': 0, 
                                      'col': 0xffffff, # white
                                      'srate': srate, 'gain': 1, 'offset': 0, 
                                      'montype': 0, 'did': did, 'recs': []}

            # 실제 레코드를 읽음
            trk = self.trks[tid]
            rec = {'dt': row['dt']}
            if trk['type'] == 1:  # wav
                rec['val'] = np.frombuffer(row['wval'], dtype=np.float32)
                #rec['val'] = np.array(Struct('<{}f'.format(len(row['wval']) // 4)).unpack_from(row['wval'], 0), dtype=np.float32)
            elif trk['type'] == 2:  # num
                rec['val'] = row['nval']
            elif trk['type'] == 5:  # str
                rec['val'] = row['sval']
            else:
                continue

            trk['recs'].append(rec)

    # track_names: 로딩을 원하는 dtname 의 리스트. track_names가 None 이면 모든 트랙이 읽혀짐
    # track_names_only: 트랙명만 읽고 싶을 때
    # exclude: 제외할 트랙
    def load_vital(self, ipath, track_names=None, track_names_only=False, exclude=[]):
        # 아래 5개 정보만 로딩하면 된다.
        self.devs = {0: {}}  # did -> device info (did = 0 represents the vital recorder)
        self.trks = {}  # tid -> track info
        self.dtstart = 0
        self.dtend = 0
        self.dgmt = 0

        # check if ipath is url
        iurl = parse.urlparse(ipath)
        if iurl.scheme and iurl.netloc:
            if iurl.scheme == 's3':
                fs = s3fs.S3FileSystem(anon=False)
                f = fs.open(iurl.netloc + iurl.path, 'rb')
            else:
                response = request.urlopen(ipath)
                f = tempfile.NamedTemporaryFile(delete=True)
                shutil.copyfileobj(response, f)
                f.seek(0)
        else:
            f = open(ipath, 'rb')

        # 포함할 트랙
        if isinstance(track_names, str):
            if track_names.find(','):
                track_names = track_names.split(',')
            else:
                track_names = [track_names]

        # 제외할 트랙
        exclude = set(exclude)

        # read file as gzip
        f = gzip.GzipFile(fileobj=f)

        # parse header
        if f.read(4) != b'VITA':  # check sign
            return False

        f.read(4)  # file version

        buf = f.read(2)
        if buf == b'':
            return False

        headerlen = unpack_w(buf, 0)[0]
        header = f.read(headerlen)  # skip header
        self.dgmt = unpack_s(header, 0)[0]  # dgmt = ut - localtime

        # parse body
        try:
            sel_tids = set()
            while True:
                buf = f.read(5)
                if buf == b'':
                    break
                pos = 0

                packet_type = unpack_b(buf, pos)[0]; pos += 1
                packet_len = unpack_dw(buf, pos)[0]; pos += 4

                if packet_len > 1000000: # 1개의 패킷이 1MB 이상이면
                    break
                
                buf = f.read(packet_len)
                if buf == b'':
                    break
                pos = 0

                if packet_type == 9:  # devinfo
                    did = unpack_dw(buf, pos)[0]; pos += 4
                    devtype, pos = unpack_str(buf, pos)
                    name, pos = unpack_str(buf, pos)
                    if len(buf) > pos + 4:  # port는 없을 수 있다
                        port, pos = unpack_str(buf, pos)
                    if not name:
                        name = devtype
                    self.devs[did] = {'name': name, 'type': devtype, 'port': port}
                elif packet_type == 0:  # trkinfo
                    did = col = 0
                    montype = unit = ''
                    gain = offset = srate = mindisp = maxdisp = 0.0
                    tid = unpack_w(buf, pos)[0]; pos += 2
                    trktype = unpack_b(buf, pos)[0]; pos += 1
                    fmt = unpack_b(buf, pos)[0]; pos += 1
                    tname, pos = unpack_str(buf, pos)

                    if packet_len > pos:
                        unit, pos = unpack_str(buf, pos)
                    if packet_len > pos:
                        mindisp = unpack_f(buf, pos)[0]
                        pos += 4
                    if packet_len > pos:
                        maxdisp = unpack_f(buf, pos)[0]
                        pos += 4
                    if packet_len > pos:
                        col = unpack_dw(buf, pos)[0]
                        pos += 4
                    if packet_len > pos:
                        srate = unpack_f(buf, pos)[0]
                        pos += 4
                    if packet_len > pos:
                        gain = unpack_d(buf, pos)[0]
                        pos += 8
                    if packet_len > pos:
                        offset = unpack_d(buf, pos)[0]
                        pos += 8
                    if packet_len > pos:
                        montype = unpack_b(buf, pos)[0]
                        pos += 1
                    if packet_len > pos:
                        did = unpack_dw(buf, pos)[0]
                        pos += 4

                    dname = ''
                    if did and did in self.devs:
                        if did and did in self.devs:
                            dname = self.devs[did]['name']
                        dtname = dname + '/' + tname
                    else:
                        dtname = tname

                    matched = False
                    if not track_names:  # 사용자가 특정 트랙만 읽으라고 했을 때
                        matched = True
                    elif dtname in track_names:  # dtname (현재 읽고 있는 트랙명)이 track_names에 지정된 것과 정확히 일치할 때
                        matched = True
                    else:  # 정확히 일치하지는 않을 때
                        for sel_dtname in track_names:
                            if dtname.endswith('/' + sel_dtname) or (dname + '/*' == sel_dtname): # 트랙명만 지정 or 특정 장비의 모든 트랙일 때
                                matched = True
                                break

                    if exclude and matched:  # 제외해야할 트랙이 있을 때
                        if dtname in exclude:  # 제외해야할 트랙명과 정확히 일치할 때
                            matched = False
                        else:  # 정확히 일치하지는 않을 때
                            for sel_dtname in exclude:
                                if dtname.endswith('/' + sel_dtname) or (dname + '/*' == sel_dtname): # 트랙명만 지정 or 특정 장비의 모든 트랙일 때
                                    matched = False
                                    break
                    
                    if not matched:
                        continue
                    
                    sel_tids.add(tid)  # sel_tids 는 무조건 존재하고 앞으로는 sel_tids의 트랙만 로딩한다
                    self.trks[tid] = {'name': tname, 'dtname': dtname, 'type': trktype, 'fmt': fmt, 'unit': unit, 'srate': srate,
                                      'mindisp': mindisp, 'maxdisp': maxdisp, 'col': col, 'montype': montype,
                                      'gain': gain, 'offset': offset, 'did': did, 'recs': []}
                elif packet_type == 1:  # rec
                    if len(buf) < pos + 12:
                        continue

                    infolen = unpack_w(buf, pos)[0]; pos += 2
                    dt = unpack_d(buf, pos)[0]; pos += 8
                    tid = unpack_w(buf, pos)[0]; pos += 2
                    pos = 2 + infolen

                    if self.dtstart == 0 or (dt > 0 and dt < self.dtstart):
                        self.dtstart = dt
                    
                    # TODO: dtrec end 는 다를 수 있음 wav 읽어서 nsamp 로딩해야함
                    if dt > self.dtend:
                        self.dtend = dt

                    if track_names_only:  # track_name 만 읽을 때
                        continue

                    if tid not in self.trks:  # 이전 정보가 없는 트랙이거나
                        continue

                    if tid not in sel_tids:  # 사용자가 트랙 지정을 했는데 그 트랙이 아니면
                        continue

                    trk = self.trks[tid]

                    fmtlen = 4
                    # gain, offset 변환은 하지 않은 raw data 상태로만 로딩한다.
                    # 항상 이 변환이 필요하지 않기 때문에 변환은 get_samples 에서 나중에 한다.
                    if trk['type'] == 1:  # wav
                        fmtcode, fmtlen = parse_fmt(trk['fmt'])
                        if len(buf) < pos + 4:
                            continue
                        nsamp = unpack_dw(buf, pos)[0]; pos += 4
                        if len(buf) < pos + nsamp * fmtlen:
                            continue
                        samps = np.ndarray((nsamp,), buffer=buf, offset=pos, dtype=np.dtype(fmtcode)); pos += nsamp * fmtlen
                        trk['recs'].append({'dt': dt, 'val': samps})
                    elif trk['type'] == 2:  # num
                        fmtcode, fmtlen = parse_fmt(trk['fmt'])
                        if len(buf) < pos + fmtlen:
                            continue
                        val = unpack_from(fmtcode, buf, pos)[0]; pos += fmtlen
                        trk['recs'].append({'dt': dt, 'val': val})
                    elif trk['type'] == 5:  # str
                        pos += 4  # skip
                        if len(buf) < pos + 4:
                            continue
                        s, pos = unpack_str(buf, pos)
                        trk['recs'].append({'dt': dt, 'val': s})
                elif packet_type == 6:  # cmd
                    cmd = unpack_b(buf, pos)[0]; pos += 1
                    if cmd == 6:  # reset events
                        evt_trk = self.find_track('/EVENT')
                        if evt_trk:
                            evt_trk['recs'] = []
                    elif cmd == 5:  # trk order
                        cnt = unpack_w(buf, pos)[0]; pos += 2
                        self.trkorder = np.ndarray((cnt,), buffer=buf, offset=pos, dtype=np.dtype('H')); pos += cnt * 2

        except EOFError:
            pass

        # sorting tracks
        # for trk in self.trks.values():
        #     trk['recs'].sort(key=lambda r:r['dt'])

        f.close()
        return True


def vital_recs(ipath, track_names=None, interval=None, return_timestamp=False, return_datetime=False, return_pandas=False, exclude=[]):
    '''
    interval: 데이터 추출 간격, None 이면 최대 해상도. wave 트랙이 없으면 0.002 초 (500Hz)
    '''
    # 만일 SNUADC/ECG_II,Solar8000 형태의 문자열이면?
    if isinstance(track_names, str):
        if track_names.find(',') != -1:
            track_names = track_names.split(',')
        else:
            track_names = [track_names]

    vf = VitalFile(ipath, track_names, exclude=exclude)
    if not track_names:
        track_names = [trk['dtname'] for trk in vf.trks.values()]
    
    # remove duplicates
    track_names = list(dict.fromkeys(track_names))
    
    # 안전을 위한 체크
    if not interval:
        # interval 이 지정되지 않으면 최대 해상도로 데이터 추출
        max_srate = max([trk['srate'] for trk in vf.trks.values()])
        interval = 1 / max_srate
    if not interval:  # 500 Hz
        interval = 0.002
    if vf.dtend <= vf.dtstart:
        return []

    ret = []
    for dtname in track_names:
        col = vf.get_samples(dtname, interval)
        ret.append(col)
    if not ret:
        return []

    # return time column
    if return_datetime: # in this case, numpy array with object type will be returned
        tzi = datetime.timezone(datetime.timedelta(minutes=-vf.dgmt))
        ret.insert(0, datetime.datetime.fromtimestamp(vf.dtstart, tzi) + np.arange(len(ret[0])) * datetime.timedelta(seconds=interval))
        track_names = ['Time'] + track_names
    elif return_timestamp:
        ret.insert(0, vf.dtstart + np.arange(len(ret[0])) * interval)
        track_names = ['Time'] + track_names

    if return_pandas:
        # ret = np.transpose(ret)
        # return pd.DataFrame(ret, columns=track_names)
        return pd.DataFrame({
            track_names[i] : ret[i] for i in range(len(track_names))
            }, columns=track_names)

    ret = np.transpose(ret)
    return ret

def vital_trks(ipath):
    # 트랙 목록만 읽어옴
    ret = []
    vf = VitalFile(ipath, track_names_only=True)
    for trk in vf.trks.values():
        tname = trk['name']
        dname = ''
        did = trk['did']
        if did in vf.devs:
            dev = vf.devs[did]
            if 'name' in dev:
                dname = dev['name']
        ret.append(dname + '/' + tname)
    return ret


if __name__ == '__main__':
    vals = vital_recs("https://vitaldb.net/samples/00001.vital", return_timestamp=True, return_pandas=True)
    print(vals)
