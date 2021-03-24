import os
import shutil
import argparse
import cv2
import numpy as np
import _thread
from queue import Queue, Empty

parser = argparse.ArgumentParser(description='动漫补帧数据集制作')
parser.add_argument('--video', dest='video', type=str, required=True,help='视频/文件夹路径')
parser.add_argument('--cache_dir', dest='cache_dir', type=str, required=True,help='存放缓存的目录')
parser.add_argument('--dataset', dest='dataset', type=str, required=True,help='存放数据的目录')
parser.add_argument('--scale', dest='scale', type=str, default='480x270',help='缩放')
parser.add_argument('--fps', dest='fps', type=int, default=8,help='对动漫进行掉帧处理（尽可能一拍一）')
parser.add_argument('--start',dest='start',type=int,default=0,help='从start开始创建目录，0为自动')
parser.add_argument('--pos',dest='pos',type=int,default=8,help='选出一组后往后推pos帧后继续选择（减少重复场景）')
parser.add_argument('--err', dest='err', type=float, default=2,help='容错，越低运动越均匀')
parser.add_argument('--min', dest='min', type=float, default=30,help='识别最小值')
parser.add_argument('--max', dest='max', type=float, default=65,help='识别最大值')
args = parser.parse_args()

is_dir = False
if os.path.isdir(args.video):
    is_dir = True

if not is_dir and os.path.exists(args.cache_dir):
    try:
        shutil.rmtree(args.cache_dir)
        os.mkdir(args.cache_dir)
    except:
        print('')

if not is_dir:
    cmd = 'ffmpeg -i "{}" -an -s {} -r {} -vf mpdecimate -vsync vfr -f image2 "{}"'.format(args.video,args.scale,args.fps,args.cache_dir) + r"/%09d.png"
    os.system(cmd)
else:
    args.cache_dir = args.video

frames = [
    cv2.imdecode(
        np.fromfile(os.path.join(args.cache_dir, f), dtype=np.uint8), 1
    )
    for f in os.listdir(args.cache_dir)
]

#恢复dataset中的位置
if args.start == 0:
    maxc = 0
    for f in os.listdir(args.dataset):
        tempcnt = int(os.path.splitext(f)[0])
        if tempcnt > maxc:
            maxc = tempcnt
    if maxc == 0:
        maxc = 1
    cnt = maxc + 1
else:
    cnt = args.start

#写入
def clear_write_buffer(user_args, write_buffer):
    while True:
        item = write_buffer.get()
        if item is None:
            break
        cn = str(item[3])
        os.mkdir(os.path.join(args.dataset,cn))
        cv2.imencode('.png', item[0])[1].tofile(os.path.join(args.dataset,cn,'im0.png'))
        cv2.imencode('.png', item[1])[1].tofile(os.path.join(args.dataset,cn,'im1.png'))
        cv2.imencode('.png', item[2])[1].tofile(os.path.join(args.dataset,cn,'im2.png'))

write_buffer = Queue(maxsize=10000)
_thread.start_new_thread(clear_write_buffer, (args,write_buffer))

pos = 0
tot = len(frames)
while pos + 2 < tot:            
    l = cv2.absdiff(frames[pos],frames[pos+1]).mean()
    r = cv2.absdiff(frames[pos+1],frames[pos+2]).mean()
    f = cv2.absdiff(frames[pos],frames[pos+2]).mean()
    if args.min <= f <= args.max and abs(l - r) <= args.err:
        write_buffer.put([frames[pos],frames[pos+1],frames[pos+2],cnt])
        cnt += 1
        pos += args.pos - 1
    pos += 1

#等待最后一帧写入
import time
while not os.path.exists(os.path.join(args.dataset,str(cnt-1),'im2.png')):
    time.sleep(1)
print('已找出{}组数据'.format(cnt))
