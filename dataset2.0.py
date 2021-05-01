import os
import cv2
import _thread
from queue import Queue, Empty
import shutil
import skvideo.io

vpath = "D:/dataset/video"  # 视频存放路径
dataset = "E:/dataset/train_set"  # 存放数据集的目录
bufsize = 1000  # 一次吞入量
min_vec = 3  # 最小运动幅度
min_diff = 15  # 最小被筛选的运动幅度
err = 0.5  # 允许误差
start = 0  # 从start序号开始准备数据集（0为自动）

pre = 0
# 恢复dataset中的位置
if start == 0:
    maxc = 0
    for f in os.listdir(dataset):
        tempcnt = int(os.path.splitext(f)[0])
        if tempcnt > maxc:
            maxc = tempcnt
    cnt = maxc + 1
    pre = cnt
else:
    cnt = start

# 写入
def clear_write_buffer(user_args, write_buffer):
    while True:
        item = write_buffer.get()
        if item is None:
            break
        cn = str(item[3])
        os.mkdir(os.path.join(dataset, cn))
        cv2.imencode('.png', item[0])[1].tofile(
            os.path.join(dataset, cn, 'im0.png'))
        cv2.imencode('.png', item[1])[1].tofile(
            os.path.join(dataset, cn, 'im1.png'))
        cv2.imencode('.png', item[2])[1].tofile(
            os.path.join(dataset, cn, 'im2.png'))


write_buffer = Queue(maxsize=10000)
_thread.start_new_thread(clear_write_buffer, (0, write_buffer))

Cvideo = [os.path.join(vpath, f) for f in os.listdir(vpath)]
for video in Cvideo:
    vframes = cv2.VideoCapture(video).get(7)
    inputparameters = {"-hwaccel": "auto"}
    outputparameters = {"-s": "1280x720","-vframes":str(int(vframes))}
    reader = skvideo.io.FFmpegReader(video,
                inputdict=inputparameters,
                outputdict=outputparameters).nextFrame()
    while True:
        data = []
        for nf in range(bufsize):
            try:
                frame = reader.__next__()
            except:
                break
            data.append(frame[..., ::-1])
        if len(data) != 0:
            scene = {}
            scene[0] = [data[0]]
            scn = 0
            for x in range(0, len(data)-1):
                if cv2.absdiff(data[x], data[x+1]).mean() < 40:
                    scene[scn].append(data[x+1])
                else:
                    scn += 1
                    scene[scn] = []
            for sc in scene:
                x = 0
                select = []
                ls = len(scene[sc])
                if ls == 0:
                    break
                while x < ls:
                    l = scene[sc][x]  # x帧
                    try:
                        x += 1
                        r = scene[sc][x]  # x+1帧
                    except:
                        break
                    Cframes = []
                    while cv2.absdiff(l, r).mean() < min_diff:
                        Cframes.append(r)
                        try:
                            x += 1
                            r = scene[sc][x]  # x+2 - x+n帧
                        except:
                            break
                    min_err = 10 ** 3
                    current_frame = None
                    for m in Cframes:
                        l1 = cv2.absdiff(m, l).mean()  # 中间和前一帧
                        r1 = cv2.absdiff(m, r).mean()  # 中间和后一帧
                        ae = abs(l1-r1)
                        if ae < err and l1 > min_vec and r1 > min_vec:
                            zlr = ae
                            if zlr < min_err:
                                min_err = zlr
                                current_frame = m
                    if not current_frame is None:
                        select.append([l, current_frame, r])  # 放入该场景中所有满足条件的组
                # 再进行一次绝对中间值筛选
                min_err = 10 ** 3
                sel_item = 0
                for s in select:
                    l = s[0]
                    m = s[1]
                    r = s[2]
                    mm = cv2.absdiff(l, r).mean() / 2
                    left = cv2.absdiff(m, l).mean()
                    right = cv2.absdiff(m, r).mean()
                    ml = abs(mm-left)
                    mr = abs(mm-right)
                    ae = ml + mr
                    if ae < min_err and ml < 5:
                        min_err = ae
                        sel_item = s
                # 加入至写入缓存区
                if sel_item != 0:
                    write_buffer.put([sel_item[0], sel_item[1], sel_item[2], cnt])
                    cnt += 1
                    print("输出第:{}组".format(cnt-1))
        else:
            break
    os.remove(video)