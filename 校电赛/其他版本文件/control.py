THRESHOLD = (5, 70, -23, 15, -57, 0) # Grayscale threshold for dark things...
import sensor, image, time, machine
from pyb import LED, Timer
from machine import Pin
import car
from module import Buzz
from pid import PID


# 测试用
def Detect(mode_pos, Done_flag):
    if Done_flag: # 检测动作是否完成
        mode_pos += 1 # 完成时应该进入下一个mode
        Done_flag = False # 清空标志位
        car.run(0, 0) # 短停，防止电机反应不过来
    return mode_pos, Done_flag

def Run(mode):
    Done_flag = False
    # 0 停止
    if mode == 0:
        car.run(0, 0)
    # 1 前进
    # 2 后退
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
    elif mode == 3:
        car.turn_left(90)
    elif mode == 4:
        car.turn_right(90)
    elif mode == 6: # 蜂鸣器
        buzz.Buzzer_Start()
        print('ok')
    elif mode == 10: # 绕过障碍物
        # 右转
        car.turn_right(60)
        car.run(0, 0) # 短停，防止电机反应不过来

        # 前进一小段
        for i in range(50000):
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
        for i in range(50000):
            car.run(20,20)
        car.run(0, 0) # 短停，防止电机反应不过来

        # 右转
        car.turn_right(60)
        # car.run(0, 0) # 短停，防止电机反应不过来

    if((mode != 0) or (mode != 1) or (mode !=2)):
        Done_flag = True
    return Done_flag