#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist



def sendjoyinfo(event):   
    
    global firstrun
    global twist

    if firstrun:
        firstrun = False
    else:
        #print(twist.linear.x,twist.angular.z)
        pub.publish(twist)
    
               
    

def callback(data):

    global twist
    # vertical left stick axis = linear rate
    twist.linear.x = data.axes[1]*0.7
    # horizontal left stick axis = turn rate
    twist.angular.z = data.axes[0]*1.2
    global firstrun
    if firstrun:
        rospy.Timer(rospy.Duration(0.01),sendjoyinfo)

    

def steadyflow():
    global pub
    global firstrun
    global twist
    
    twist = Twist()
    firstrun = True
    pub = rospy.Publisher('smoother_cmd_vel', Twist,queue_size=10)
    rospy.Subscriber("joy", Joy, callback)
    rospy.init_node('steady_joy_control', anonymous=True)    
    rospy.spin()  


if __name__ == '__main__':
    try:
        steadyflow()
    except rospy.ROSInterruptException:
        pass
