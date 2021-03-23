import os
import shutil
import argparse
import cv2
import numpy as np
import _thread
from queue import Queue, Empty

parser = argparse.ArgumentParser(description='')
parser.add_argument('--video', dest='video', type=str, required=True)
parser.add_argument('--is_dir', dest='is_dir', action='store_true', help='是目录')
parser.add_argument('--cache_dir', dest='cache_dir', type=str, required=True)
parser.add_argument('--dataset', dest='dataset', type=str, required=True)
parser.add_argument('--scale', dest='scale', type=str, default='480x270')
parser.add_argument('--fps', dest='fps', type=int, default=8)
parser.add_argument('--start',dest='start',type=int,default=0)
parser.add_argument('--pos',dest='pos',type=int,default=1)
parser.add_argument('--err', dest='err', type=float, default=3)
parser.add_argument('--min', dest='min', type=float, default=25)
parser.add_argument('--max', dest='max', type=float, default=65)
args = parser.parse_args()

#spilt video into frames
if not args.is_dir:
    cmd = 'ffmpeg -i "{}" -an -s {} -r {} -vf mpdecimate -vsync vfr -f image2 "{}"'.format(args.video,args.scale,args.fps,args.cache_dir) + r"/%09d.png"
    os.system(cmd)
else:
    args.cache_dir = args.video

#读取
frames = [
    cv2.imdecode(
        np.fromfile(os.path.join(args.cache_dir, f), dtype=np.uint8), 1
    )
    for f in os.listdir(args.cache_dir)
]

#写入
def clear_write_buffer(user_args, write_buffer):
    cnt = args.start
    while True:
        item = write_buffer.get()
        if item is None:
            break
        cnt = str(cnt)
        os.mkdir(os.path.join(args.dataset,cnt))
        cv2.imencode('.png', item[0])[1].tofile(os.path.join(args.dataset,cnt,'im0.png'))
        cv2.imencode('.png', item[1])[1].tofile(os.path.join(args.dataset,cnt,'im1.png'))
        cv2.imencode('.png', item[2])[1].tofile(os.path.join(args.dataset,cnt,'im2.png'))
        cnt = int(cnt)
        cnt += 1

write_buffer = Queue(maxsize=10000)
_thread.start_new_thread(clear_write_buffer, (args,write_buffer))

pos = 0
tot = len(frames)

while pos + 2 < tot:
    l = cv2.absdiff(frames[pos],frames[pos+1]).mean()
    r = cv2.absdiff(frames[pos+1],frames[pos+2]).mean()
    f = cv2.absdiff(frames[pos],frames[pos+2]).mean()
    if args.min <= f <= args.max and abs(l - r) <= args.err:
        write_buffer.put([frames[pos],frames[pos+1],frames[pos+2]])
    pos += args.pos

import time
while not write_buffer.empty():
    time.sleep(1)
