import rclpy
import cv2
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Twist
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

class M_sub(Node):
  def __init__(self):
    super().__init__('massage_subscriber')
    self.qos_profile = QoSProfile(depth = 10)
    self.bridge = CvBridge()
    self.helloworld_subscriber = self.create_subscription(CompressedImage, '/camera/image/compressed', self.subscriber_massage, self.qos_profile)

    self.massage_publisher = self.create_publisher(Twist, 'cmd_vel', self.qos_profile)
    self.timer = self.create_timer(0.1, self.tb3_m_publisher)
    self.count = 0

  def subscriber_massage(self, data):
    cv_image = self.bridge.compressed_imgmsg_to_cv2(data, "bgr8")
    rotate = cv2.getRotationMatrix2D((320 / 2, 240 / 2), 90, -1)
    iamge_rotate = cv2.warpAffine(cv_image, rotate, (0,0))
    cv2.imshow("Image window", iamge_rotate)
    cv2.waitKey(3)

  def tb3_m_publisher(self):
        msg = Twist()
        msg.linear.x = 0.1
        msg.angular.z = 1.0
        self.massage_publisher.publish(msg)
        self.get_logger().info(f"Publisher message: {msg.linear.x}, {msg.angular.z}")
        self.count += 1

def main(args = None):
  rclpy.init(args=args)
  node = M_sub()
  try :
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard interrupt!!!!')
  finally :
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':

  main()
