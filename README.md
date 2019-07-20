# E1小车的ROS驱动安装与使用

## 下载安装驱动
下载地址：https://github.com/SJTU-Multicopter/dashgo_e1
将驱动文件从GitHub下载到相应的工作空间（如catkin_ws/src），catkin_make即可，代码均为python文件，无需编译，用时很短。
第一次使用小车，请校准里程计，校准方法见下文。

## 驱动的使用
### 启动小车驱动的两种方式
1. launch文件启动
命令行中输入：
> roslaunch dashgo_driver driver.launch

2. python运行
首先进入驱动程序所在目录：dashgo_e1/dashgo_driver/nodes/
然后命令行中输入：
> python dashgo_driver.py

### 如何控制小车
控制程序发布名为“smoother_cmd_vel”的twist类型的消息即可控制小车。
其中：
twist.linear.x是期望小车的线速度，单位:m/s
twist.angular.z是期望小车的角速度，单位:弧度/s
twist中其他值均取0
【注意】第一次使用，建议将linear和angular的值限制在1以下，避免小车猛冲的危险

### 如何接受小车发布的信息
小车驱动将启动名为“car”的节点，发布的消息也是“car/<具体消息的名称>”的形式，
例如，查看最常用的里程计信息：
> rostopic echo /car/odom

若需要订阅其他消息，请用rostopic list查看，或者直接打开驱动程序dashgo_driver.py查看相应消息的定义


## 其他功能
### PS4手柄控制小车
#### 准备工作：连接手柄至电脑
首先要将手柄连接到电脑（即驱动程序所在的电脑），有两种连接方式：无线和有线。
1. 有线
直接将手柄与电脑USB2.0串口有线连接，PS4手柄指示灯常亮表示连接成功
2. 无线
先按住PS4手柄的share键不放，然后按住手柄的home键（就是手柄中央有PS标志的按键）不放，等待约4s，手柄的指示灯会进入快闪状态，表示蓝牙为待连接状态；
然后打开电脑的蓝牙，连接手柄：
* 如果手柄是第一次连接该电脑，则依次点击电脑上蓝牙标志（Ubuntu16.04是在屏幕右上角）→Bluetooth settings→在界面中按+号→新的界面中点击手柄名称（wireless controller）→next→显示successfully connected即说明连接成功

* 如果手柄之前连接过该电脑，则连接中保留有手柄的信息，则在手柄快闪后→点击电脑上蓝牙标志→点击列表中的手柄名称→点击on→手柄进入常亮状态，即说明连接成功。如果不能成功连接，按照手柄第一次无线连接电脑的方式处理。
#### 启动手柄控制程序
当手柄成功连接电脑后，在命令行中输入
> roslaunch dashgo_driver joy2car.launch

运行后，即可通过手柄的【左摇杆】控制小车运动。

此控制的基本原理是通过手柄的ROS驱动获取手柄的按键命令，然后通过一个名为steady_joy_control.py的程序将手柄的左摇杆信息转换为twist信息发布给小车的ROS驱动程序
（更多关于手柄在ROS中的使用教程，请官方参考文档
http://wiki.ros.org/joy/Tutorials）



### 小车里程计的校正
（此内容部分参考官方文档）
如果小车驱动所在的电脑是第一次控制这台小车，而且你需要获取小车准确的里程计信息，那么一定要校准小车的里程计。
#### 首先校准直线行走1m
1. 确保小车前方至少1m处无障碍
2. 沿小车直线前进方向布置1m卷尺作为刻度参考
3. 启动小车驱动
> roslaunch dashgo_driver driver.launch
4. 接受小车的里程计信息
> roslaunch echo /car/odom
5. 启动小车行走1m的程序
> rosrun dashgo_tools check_linear.py
6. 小车将向前走约1m后停止，这个“1m”是小车里程计认为的1m，并不实际等于1m。假设根据卷尺读出的小车实际直线前进距离为L。
7. 打开文件dashgo_e1/dashgo_driver/config/my_dashgo_params.yaml，找到 “gear_reduction”（减速比）这个参数，修改这个参数。
修改的原则是：假设减速比默认值为g，若L小于1m，则增大g；若L大于1m，则减小g。具体增大与减小多少？推荐第一次调整时用g = g/L 替换默认的g，后续再微调
8. Ctrl+c关闭之前打开的程序
9. 回到1，再次测试小车直线前进的精度，反复2-3次，将误差调整到1%以内

#### 直线校准后，进行旋转360°校准
1. 标记小车启动位置
标记小车转动的起始点，否则转动不宜观察是否回到原点
2. 启动小车驱动
> roslaunch dashgo_driver driver.launch
3. 启动小车转动一圈的程序
> rosrun dashgo_tools check_angular.py
4. 小车将转动约360°后停止，同理，这个角度不精确等于360度
5. 打开文件dashgo_e1/dashgo_driver/config/my_dashgo_params.yaml，找到 “wheel_track”（两轮间距）这个参数，修改这个参数。
修改的原则是：实际转动超过360度就改小，否则就改大，只需要微调（小数点后第三位）
6. Ctrl+c关闭之前打开的程序
7. 回到1，再次测试小车转动一圈的精度，反复2-3次，将误差调整到1%以内


## 小车使用注意事项
### 安全第一
紧急情况下，要停止小车，按下其后部红色按钮。
![593003015f93598e441d4a2b42993f17.png](en-resource://database/528:1)

### 为什么小车不动？
已经打开了小车控制驱动，发送控制指令但小车不动，
硬件方面的可能性从高到低排列有：
1. 小车电源没开→确认一下电源是否打开
2. 小车红色急停按钮处于按下状态——相当于断电→沿着红色急停按钮的箭头方向旋转，按钮跳起则恢复正常状态
3. 小车没电了→充电
软件方面：
1. 驱动信息是否真的发到了小车驱动？通过命令行rostopic echo smoother_cmd_vel来看
2. 小车驱动是不是异常？如果有，命令行终端会有相应的显示

## 说明
说明：此驱动的原始代码由E1的制造商EAI官方提供，官方GitHub驱动网址：https://github.com/EAIBOT/dashgo_e1
实验室中用的是改进的版本。
改进的地方有：
1. 小车的节点名称和发布的topic信息都加上了关键词“car”，便于辨认
2. 在原始驱动基础上开发了新的应用，如手柄控制小车
3. 其他改进

## 更多小车的使用细节，请查阅官方文档dashgo_documents






