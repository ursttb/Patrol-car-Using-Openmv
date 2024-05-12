import car

mode_pos = 0 # 用于记录小车跑图阶段 || 指示任务当前执行模式
mode = 0 # 小车运作模式
dis_min = 0
dis_mid = 0
dis_max = 0
# 模式编码
# 0 停止
# 1 前进
# 2 后退
# 3 左转弯
# 4 右转弯
# 5 180°转弯
# 6 打开蜂鸣器，等待2秒响应，关闭蜂鸣器
# 7 绕过障碍物
# 8 左转信号后前进一小段左转
# 9 右转信号后前进一小段右转
# 10 识别到转弯信号前进一小段停止
# 常用判断模式，即检测到以下情况时应该进入下一个跑图阶段，切换模式
# 1 前进, 当超声波检测到 distance < dis_min 时, 认为小车走进到方块范围内，进行蜂鸣或绕过障碍物
# if distance < dis_min:
#     change = 1
# 2 后退, 当超声波检测到 distance > dis_mid 时, 认为小车走到赛道中间
# if distance > dis_mid:
#     change = 1
# 3 后退, 当超声波检测到 distance > dis_max 时, 认为小车后退走完赛道全段
# if distance > dis_max:
#     change = 1
# 4 Done信号，即转弯、蜂鸣器动作完成后
# if Done_flag:  # 检测动作是否完成
#     Done_flag = 0  # 清空标志位
#     change = 1
# 5 拐弯信号
# if (mode_pos == 0):
# value = Turn_signal(img)
# if value == 1:
# change = 1


# 任务一
# mode=1 前进，要求distance<5时切换mode
# mode=6 打开蜂鸣器，等待2秒响应，关闭蜂鸣器 切换mode
# mode=5 180°转弯完成后前进
# mode=1 前进，要求无巡线转弯信号时切换mode
# mode=10 识别到转弯信号前进一小段切换mode
# mode=1 前进，要求无巡线转弯信号时切换mode
# mode=10 识别到转弯信号前进一小段停止
# mode=0 停止
task1 = [1, 6, 5, 1, 10, 1, 10, 0]
def Detect_1(mode_pos, Done_flag):
    change = 0
    LCM_Calculate()

    # 业务代码
    if mode_pos == 0:
        # 1 前进, 当超声波检测到 distance < dis_min 时, 认为小车走进到方块范围内，进行蜂鸣或绕过障碍物
        if distance < dis_min:
            change = 1

    if mode_pos == 1 or mode_pos == 2 or mode_pos == 4 or mode_pos == 6:
        # 4 Done信号，即转弯、蜂鸣器动作完成后
        if Done_flag: # 检测动作是否完成
            Done_flag = 0 # 清空标志位
            change = 1

    if mode_pos == 3 or mode_pos == 5:
        value = Turn_signal(img)
        if value == 1:
            change = 1

    # 状态转变
    if change:
        mode_pos += 1 # 完成时应该进入下一个mode
        print('Trans mode')
        car.run(0, 0) # 短停，防止电机反应不过来
    return mode_pos, Done_flag

# 任务二
# mode=1 前进，要求distance<5时切换mode
# mode=6 打开蜂鸣器，等待2秒响应，关闭蜂鸣器 切换mode
# mode=5 180°转弯完成后前进
# mode=1 前进，要求识别到右转信号时切换mode
# mode=9 右转信号后前进一小段右转
# mode=1 前进，要求distance<5时切换mode
# mode=6 打开蜂鸣器，等待2秒响应，关闭蜂鸣器 切换mode
# mode=5 180°转弯完成后切换状态
# mode=1 前进，要求识别到右转信号时切换mode
# mode=9 右转信号后前进一小段右转
# mode=1 前进，要求无巡线时切换mode
# mode=10 识别到转弯信号前进一小段停止
# mode=0 停止
task2 = [1, 6, 5, 1, 9, 1, 6, 5, 1, 9, 1, 10, 0]
def Detect_2(mode_pos, Done_flag):
    change = 0
    LCM_Calculate()

    # 业务代码
    if mode_pos == 0 or mode_pos == 5:
        if distance < dis_min:
            change = 1

    if mode_pos == 1 or mode_pos == 2 or mode_pos == 4 or mode_pos == 6 or mode_pos == 7 or mode_pos== 9 or mode_pos == 11:
        # 4 Done信号，即转弯、蜂鸣器动作完成后
        if Done_flag: # 检测动作是否完成
            Done_flag = 0 # 清空标志位
            change = 1

    if mode_pos == 3 or mode_pos == 8 or mode_pos == 10:
        value = Turn_signal(img)
        if value == 1:
            change = 1

    # 状态转变
    if change:
        mode_pos += 1 # 完成时应该进入下一个mode
        print('Trans mode')
        car.run(0, 0) # 短停，防止电机反应不过来
    return mode_pos, Done_flag

# 任务三
# mode=1 前进，要求识别到左转信号时切换mode0
# mode=8 左转信号后前进一小段左转1
# mode=1 前进，要求识别到识别到障碍物(distan<10)时切换mode2
# mode=7 绕过障碍物3
# mode=1 前进，要求识别到左转信号时切换mode4
# mode=8 左转信号后前进一小段左转5
# mode=1 前进，要求distance<5时切换mode6
# mode=6 打开蜂鸣器，等待2秒响应，关闭蜂鸣器 切换mode7
# mode=5 180°转弯完成后前进8
# mode=1 前进，要求distance<5时切换mode9
# mode=6 打开蜂鸣器，等待2秒响应，关闭蜂鸣器 切换mode10
# mode=5 180°转弯完成后前进11
# mode=1 前进，要求识别到左转信号时切换mode12
# mode=8 左转信号后前进一小段左转13
# mode=1 前进，要求识别到识别到障碍物(distan<10)时切换mode14
# mode=7 绕过障碍物15
# mode=1 前进，要求识别到右转信号时切换mode16
# mode=9 右转信号后前进一小段右转17
# mode=1 前进，要求无巡线时切换mode18
# mode=10 识别到转弯信号前进一小段停止19
# mode=0 停止20

# 任务四
# mode=1 前进，要求识别到左转信号时切换mode0
# mode=8 左转弯，完成时切换mode1
# mode=1 前进，要求识别到识别到障碍物(distan<10)时切换mode2
# mode=7 绕过障碍物3
# mode=1 前进，要求识别到左转信号时切换mode4
# mode=8 左转信号后前进一小段左转5

# 判断有无目标物
    # 无目标物时mode=5 180°转弯
    # 有目标物时L2R_flag=1 使后面右转弯变左转弯
# if distance > 180:
#     car.turn_right(190)
#     L2R_flag = 1

# mode=1 前进，要求distance<5时切换mode6
# mode=6 打开蜂鸣器，等待2秒响应，关闭蜂鸣器 切换mode7
# mode=5 180°转弯完成后前进8
# mode=1 前进，要求识别到右转/左转信号时切换mode，这里右转还是左转取决于之前有无设置L2R_flag标志位9
# 假设没有目标物时L2R_flag=0 执行右转
# 反之，L2R_flag=1 执行左转
# mode=9-L2R_flag 转弯，完成时切换mode10

# =========== 回家路线 =========== #
# mode=1 前进，要求识别到识别到障碍物(distan<10)时切换mode11
# mode=7 绕过障碍物12
# mode=1 前进，要求识别到右转信号时切换mode13
# mode=9 右转信号后前进一小段右转14
# mode=1 前进，要求无巡线时切换mode15
# mode=10 识别到转弯信号前进一小段停止16
# mode=0 停止17
