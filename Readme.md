# dataset.py 用法

--video 视频/图片序列路径

--cache_dir 用于存放视频帧的缓存路径

--dataset 用于存放数据集的路径

--start 在dataset目录中的start位置继续创建目录(0为自动识别)

--scale 对画面进行缩放（例:480x270）

--fps 每秒帧率(默认为8)

--pos 每计算完一组后向后移动pos帧后继续计算(默认16)

--err 容错（默认为2，越低越匀速）

--min 两帧之间的最小差值

--max 两帧之间的最大插值

## 对于min和max的值说明(一般情况下)

  小幅度运动: min=1 max=10 err=1
  
  中幅度: min=10 max=30 err=2
  
  大幅度: min=30 max=65 err=2

# 预览

![im0](https://user-images.githubusercontent.com/68835291/112189929-7a713580-8c3f-11eb-8c3d-4be35f4b22db.png)
![im1](https://user-images.githubusercontent.com/68835291/112189940-7cd38f80-8c3f-11eb-85e5-37e94763340a.png)
![im2](https://user-images.githubusercontent.com/68835291/112189947-7e9d5300-8c3f-11eb-92c3-44bf553fa11a.png)


# 已准备好的数据集

## 中低幅度运动数据(代码自动筛选)

  共 组，大小:G
  
  ### 下载链接:

## 大幅度运动数据(代码自动筛选)

  共 组，大小:G
  
  ### 下载链接:

## 手动挑选大幅度运动数据:

  共 组，大小:G
  
  ### 下载链接:
