import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
import cv2


class Tb3_move(Node):
    def __init__(self):
        super().__init__('tb3_move')
        self.qos_profile = QoSProfile(depth = 10)
        self.massage_publisher = self.create_publisher(Twist, 'cmd_vel', self.qos_profile)
        self.timer = self.create_timer(0.1, self.tb3_m_publisher)
        self.count = 0

    def tb3_m_publisher(self):
        msg = Twist()
        msg.linear.x = 0.1
        msg.angular.z = 1.0
        self.massage_publisher.publish(msg)
        self.get_logger().info(f"Publisher message: {msg.linear.x}, {msg.angular.z}")
        self.count += 1


def main(args = None) :
    rclpy.init(args=args)
    capture = cv2.VideoCapture(0)

    node = Tb3_move()
    try :
        frame = capture.read()
        cv2.imshow("VideoFrame", frame)
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt!!!!')
    finally :
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__' :
    main()
