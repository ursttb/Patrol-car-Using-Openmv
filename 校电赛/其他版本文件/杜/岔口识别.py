import sensor, image, time, math
sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

GRAYSCALE_THRESHOLD = [(-125, 20, -21, 13, -28, 14)]#巡线的阈值
ROIS = [
        (0, 90, 160, 20, 0.7),
        (100, 150, 140, 20, 0.4),
        (100, 210, 140, 20, 0.05)
       ]#三个区域
weight_sum = 0
range_stop=[390,190,100]#停止线像素最小值
range_wait=[60,40,0]    #等待停止线像素最小值
for r in ROIS: weight_sum += r[4]
blob_xy=[0,0]   # 方块的xy坐标

def find_max(blobs):
    max_size=[0,0]
    max_ID=[-1,-1]
    for i in range(len(blobs)):
        if blobs[i].pixels()>max_size[0]:
            max_ID[1]=max_ID[0]
            max_size[1]=max_size[0]
            max_ID[0]=i
            max_size[0]=blobs[i].pixels()
        elif blobs[i].pixels()>max_size[1]:
            max_ID[1]=i
            max_size[1]=blobs[i].pixels()
    return max_ID

def car_fork():
    centroid_sum = [0,0]
    left_center=[-1,-1,-1]
    right_center=[-1,-1,-1]
    for r in range(3):
        blobs = img.find_blobs(GRAYSCALE_THRESHOLD, roi=ROIS[r][0:4], merge=True,area_threshold=100,margin=3)
        if blobs:
            max_ID=[-1,-1]#保存两个最大色块的ID
            max_ID=find_max(blobs)
            img.draw_rectangle(blobs[max_ID[0]].rect())
            img.draw_cross(blobs[max_ID[0]].cx(),
                           blobs[max_ID[0]].cy())
            if max_ID[1]!=-1:#如果识别到两个色块
                img.draw_rectangle(blobs[max_ID[1]].rect())
                img.draw_cross(blobs[max_ID[1]].cx(),
                               blobs[max_ID[1]].cy())
                #区分左边和右边
                if blobs[max_ID[0]].cx()<blobs[max_ID[1]].cx():
                    left_center[r]=blobs[max_ID[0]].cx()
                    right_center[r]=blobs[max_ID[1]].cx()
                else:
                    left_center[r]=blobs[max_ID[1]].cx()
                    right_center[r]=blobs[max_ID[0]].cx()
            else:
                left_center[r]=right_center[r]=blobs[max_ID[0]].cx()
                centroid_sum[0] += left_center[r] * ROIS[r][4]
                centroid_sum[1] += right_center[r] * ROIS[r][4]
    center_pos =[0,0]
    center_pos[0] = (centroid_sum[0] / weight_sum)
    center_pos[1] = (centroid_sum[1] / weight_sum)
    deflection_angle = [0,0]
    deflection_angle[0] = -math.atan((center_pos[0]-80)/60)
    deflection_angle[1] = -math.atan((center_pos[1]-80)/60)
    #使用的QQVGA像素是160*120，因此中心点是（80,60）
    deflection_angle[0] = math.degrees(deflection_angle[0])
    deflection_angle[1] = math.degrees(deflection_angle[1])
    if center_pos[0]==center_pos[1]==0:
        deflection_angle[1]=deflection_angle[0]=0
    A=[int(deflection_angle[0])+90,int(deflection_angle[1])+90]

    return A

def car_fork_xy():
    blob_catchxy=[[0,0],[0,0],[0,0]]        # 收集采样数据
    blob_xy=[0,0]                           # 采样数据计算结果，取平均
    for r in range(3):
        blobs = img.find_blobs(GRAYSCALE_THRESHOLD, roi=ROIS[r][0:4], merge=True,area_threshold=100,margin=3)
        if blobs:
            max_ID=[-1,-1]#保存两个最大色块的ID
            max_ID=find_max(blobs)
            blob_x = (blobs[max_ID[0]].cx()+blobs[max_ID[1]].cx())/2
            blob_y = (blobs[max_ID[0]].cy()+blobs[max_ID[1]].cy())/2
            blob_catchxy[r][0]=blob_x
            blob_catchxy[r][1]=blob_y
    blob_xy[0]=(blob_catchxy[0][0]+blob_catchxy[1][0]+blob_catchxy[2][0])/3
    blob_xy[1]=(blob_catchxy[0][1]+blob_catchxy[1][1]+blob_catchxy[2][1])/3
    return  blob_xy

while True:
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot()  # Take a picture and return the image.
    angle=car_fork()
    car_fork_xy()
    blob_xy=car_fork_xy()
    print("方块横纵坐标为：",blob_xy[0],blob_xy[1])
    # print(angle)
    # to the IDE. The FPS should increase once disconnected.
