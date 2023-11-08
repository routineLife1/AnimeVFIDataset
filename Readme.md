# dataset.py 用法

--mode 1/2 模式1/2

--video 视频/图片序列路径

--cache_dir 用于存放视频帧的缓存路径

--dataset 用于存放数据集的路径

--start 在dataset目录中的start位置继续创建目录(0为自动识别)

--scale 对画面进行缩放（例:480x270）

--fps 每秒帧率(默认为12)

--pos 每计算完一组后向后移动pos帧后继续计算(默认16)

--err 容错（默认为2，越低越匀速）

--min 两帧之间的最小差值

--max 两帧之间的最大插值

## 对于min和max的值说明(一般情况下)

  小幅度运动: min=1 max=10 err=1
  
  中幅度: min=10 max=30 err=2
  
  大幅度: min=30 max=65 err=2

# 预览

![ezgif com-gif-maker](https://user-images.githubusercontent.com/68835291/112470075-30a25f80-8da5-11eb-8205-efcd30d10a9c.gif)
![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/68835291/112470102-3730d700-8da5-11eb-92e1-ee250ea3a669.gif)
![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/68835291/112470108-3a2bc780-8da5-11eb-810c-ff07286c469e.gif)
![ezgif com-gif-maker (3)](https://user-images.githubusercontent.com/68835291/112470150-46b02000-8da5-11eb-80bc-9a06014253bb.gif)
