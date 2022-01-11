import rospy
from std_msgs.msg import Float64
import sys, select, termios, tty
import rospy
from geometry_msgs.msg import Twist
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
msg = """
Reading from the keyboard  
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

q/z : increase/decrease max speeds by 1 unit

anything else : stop

CTRL-C to quit
"""

moveBindings = {
        'i':(1,0),
        'j':(0,1),
        'l':(0,-1),
        ',':(-1,0,0), 
    }

speedBindings={
        'q':(1),
        'z':(-1),
    }

def getKey():
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key
def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)
if __name__=="__main__":
    rospy.init_node('vel_Publisher')
    settings = termios.tcgetattr(sys.stdin)
    vel = Twist()
    x_linear=0
    z_angular=0
    pub.publish(vel)
    print(msg)
    while(1):
            key = getKey()
            if key in moveBindings.keys():
                x_linear = moveBindings[key][0]
                z_angular = moveBindings[key][1]
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]
                print(vels(speed,turn))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15
            else:
                x_linear = 0
                z_angular = 0
                if (key == '\x03'):
                    break
            vel.linear.x = x_linear*speed; 
            vel.angular.z = z_angular*turn
            pub.publish(vel)
		
