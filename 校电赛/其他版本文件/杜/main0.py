THRESHOLD = (5, 70, -23, 15, -57, 0) # Grayscale threshold for dark things...
import sensor, image, time, machine
from pyb import LED, Timer
from machine import Pin
import car
from pid import PID

# PID数据
rho_pid = PID(p=0.4, i=0) # 偏移的距离
theta_pid = PID(p=0.001, i=0)

# 数据区
# 小车模式位
mode_pos = 0 # 指示任务当前执行模式
Done_flag = 0 # 完成动作标志位
# 任务模块
task1 = [1, 3, 1]
# task1 = [1, 6, 7, 1, 0]
# task1 = [1, 6, 2, 0]
task2 = [1, 6, 2, 3, 1, 6, 2, 4, 2, 0]
# 距离判断数据
dis_min = 10 # 走进到方块范围内
dis_mid = 90 # 走到赛道中间
dis_max = 70 # 走完赛道全段
# =============================== 超声波模块 ================================ #
Echo = Pin('P5',Pin.IN,Pin.PULL_NONE)
Trig = Pin('P6',Pin.OUT_PP,Pin.PULL_NONE)
distance = 0
# 启动超声波
def Send_Wave():
    Trig.high()
    time.sleep_us(10)
    Trig.low()
# 计算距离
def LCM_Calculate():
    global distance     # 全局变量
    Send_Wave()         # 启动超声波
    pulse_duration = machine.time_pulse_us(Echo, 1, 65535)  # 超声波回波的脉冲宽度
    distance = pulse_duration * 0.0343 / 2  # 根据声速计算距离（声速为343m/s）
# 配置定时器
# 参数：定时器4，频率：2Hz-500ms，调用计算距离函数
# tim = Timer(4,freq=2,callback=LCM_Calculate)
# ========================================================================== #
# =============================== 蜂鸣器模块 ================================ #
Buzz_pin = Pin('P9', Pin.OUT)
def Buzzer_Start():
    Buzz_pin.value(0)  # 拉低引脚触发蜂鸣器
    time.sleep_ms(500)  # 持续一段时间
    Buzz_pin.value(1)  # 恢复高电平停止蜂鸣器
# ========================================================================== #

# 蜂鸣器初始化
Buzz_pin.value(1)  # 恢复高电平停止蜂鸣器
# 指示灯
LED(1).off()
LED(2).off()
LED(3).off()

# ================================ 摄像头初始化 =============================== #
sensor.reset()
# sensor.set_vflip(True)
# sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.
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
def car_fork_xy(img):
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
def Turn_signal():
    sensor.set_framesize(sensor.QVGA)
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot()
    blob_xy=car_fork_xy(img)
    print("方块横纵坐标为：",blob_xy[0],blob_xy[1])
    return blob_xy[0]
# ============================================================================= #

# 测试案例
def Detect(mode_pos, Done_flag):
    change = 0
    LCM_Calculate()

    ## 业务代码
    #if ((mode_pos == 0) or (mode_pos == 3)):
        ## 1 前进, 当超声波检测到 distance < dis_min 时, 认为小车走进到方块范围内，进行蜂鸣或绕过障碍物
        #if(distance < dis_min):
            #change = 1

    #if ((mode_pos == 1) or (mode_pos == 2)):
        ## 4 Done信号，即转弯、蜂鸣器动作完成后
        #if Done_flag: # 检测动作是否完成
            #Done_flag = 0 # 清空标志位
            #change = 1

    # # 拐弯信号
    # if (mode_pos == 0):
    #     value = Turn_signal()
    #     if (value < 65):
    #         change = 1

    # 状态转变
    if change:
        mode_pos += 1 # 完成时应该进入下一个mode
        print('Trans mode')
        car.run(0, 0) # 短停，防止电机反应不过来
    return mode_pos, Done_flag

def Detect_1(mode_pos, Done_flag):
    change = 0
    LCM_Calculate()

    # 业务代码
    if (mode_pos == 0):
        # 1 前进, 当超声波检测到 distance < dis_min 时, 认为小车走进到方块范围内，进行蜂鸣或绕过障碍物
        if(distance < dis_min):
            change = 1

    ## 2 后退, 当超声波检测到 distance > dis_mid 时, 认为小车走到赛道中间
    #if(distance > dis_mid):
        #change = 1

    if (mode_pos == 2):
        # 3 后退, 当超声波检测到 distance > dis_max 时, 认为小车后退走完赛道全段
        if(distance > dis_max):
            change = 1

    if (mode_pos == 1):
        # 4 Done信号，即转弯、蜂鸣器动作完成后
        if Done_flag: # 检测动作是否完成
            Done_flag = 0 # 清空标志位
            change = 1
    # 5 拐弯信号

    # 状态转变
    if change:
        mode_pos += 1 # 完成时应该进入下一个mode
        print('Trans mode')
        car.run(0, 0) # 短停，防止电机反应不过来
    return mode_pos, Done_flag

def Detect_2(mode_pos, Done_flag):
    change = 0
    LCM_Calculate()

    # 业务代码


    # 状态转变
    if change:
        mode_pos += 1 # 完成时应该进入下一个mode
        print('Trans mode')
        car.run(0, 0) # 短停，防止电机反应不过来
    return mode_pos, Done_flag


def Run(mode):
    Done_flag = 0
    # 0 停止
    if mode == 0:
        car.run(0, 0)
    # 1 前进 2 后退
    elif mode == 1 or mode == 2:
        clock.tick()
        img = sensor.snapshot().binary([THRESHOLD])
        line = img.get_regression([(100,100)], robust = True)
        if (line):
            rho_err = abs(line.rho())-img.width()/2
            if line.theta()>90:
                theta_err = line.theta()-180
            else:
                theta_err = line.theta()
            img.draw_line(line.line(), color = 127)
            # print(rho_err,line.magnitude(),rho_err)
            if line.magnitude()>8:
                #if -40<b_err<40 and -30<t_err<30:
                rho_output = rho_pid.get_pid(rho_err,1)
                theta_output = theta_pid.get_pid(theta_err,1)
                output = rho_output+theta_output
                if mode == 1:
                    output_l = 50+output
                    output_r = 50-output
                elif mode == 2:
                    output_l = -(50+output)
                    output_r = -(50-output)
                car.run(output_l, output_r)
            else:
                car.run(0,0)
        else:
            car.run(50,-50)
            pass
     # 3 左前转弯
    # 3 左转弯
    elif mode == 3:
        car.turn_left(90)
        Done_flag = 1
    # 4 右转弯
    elif mode == 4:
        car.turn_right(90)
        Done_flag = 1
    # 5 180°转弯
    elif mode == 5:
        car.turn_right(180)
        Done_flag = 1
    # 6 蜂鸣器
    elif mode == 6:
        Buzzer_Start()
        Done_flag = 1
    # 7 绕过障碍物
    elif mode == 7:
        # 右转
        car.turn_right(60)
        car.run(0, 0) # 短停，防止电机反应不过来
        # 前进一小段
        for i in range(60000):
            car.run(20,20)
        car.run(0, 0) # 短停，防止电机反应不过来
        # 左转
        car.turn_left(60)
        car.run(0, 0) # 短停，防止电机反应不过来
        # 前进一小段
        for i in range(100000):
            car.run(20,20)
        car.run(0, 0) # 短停，防止电机反应不过来
        # 左转
        car.turn_left(60)
        car.run(0, 0) # 短停，防止电机反应不过来
        # 前进一小段
        for i in range(60000):
            car.run(20,20)
        car.run(0, 0) # 短停，防止电机反应不过来
        # 右转
        car.turn_right(60)
        # car.run(0, 0) # 短停，防止电机反应不过来
        Done_flag = 1

    #if(not(mode == 0) or not(mode == 1) or not(mode == 2)): # Done信号产生 有bug
        #Done_flag = 1
    return Done_flag

while True:
    mode_pos, Done_flag = Detect(mode_pos, Done_flag)  # 判断当前模式的触发条件是否满足
    if mode_pos < len(task1):
        Done_flag = Run(task1[mode_pos]) # 执行当前模式的操作
        # print(task1[mode_pos])
    # sensor.snapshot()
    print(distance)
#while True:
    #LCM_Calculate()
    #print(distance)
