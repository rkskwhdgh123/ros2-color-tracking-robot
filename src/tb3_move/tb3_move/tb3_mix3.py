import rclpy
import cv2
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

class M_sub(Node):
  def __init__(self):
    super().__init__('massage_subscriber')
    self.qos_profile = QoSProfile(depth = 10)
    self.bridge = CvBridge()
    self.cx=0.0
    self.cy=0.0
    self.distance=0.0
    self.helloworld_subscriber2 = self.create_subscription(Float32, 'distance', self.subscriber_distance, self.qos_profile)
    self.helloworld_subscriber = self.create_subscription(CompressedImage, '/camera/image/compressed', self.subscriber_massage, self.qos_profile)
    self.massage_publisher = self.create_publisher(Twist, 'cmd_vel', self.qos_profile)
    self.timer = self.create_timer(0.1, self.tb3_m_publisher)
    self.count = 0

  def subscriber_distance(self, msg):
    self.get_logger().info(f'Recived mesage: {msg.data}')
    self.distance = msg.data

  def subscriber_massage(self, data):
    cv_image = self.bridge.compressed_imgmsg_to_cv2(data, "bgr8")
    rotate = cv2.getRotationMatrix2D((320 / 2, 240 / 2), 90, -1)
    iamge_rotate = cv2.warpAffine(cv_image, rotate, (0,0))
    ycrcb = cv2.cvtColor(iamge_rotate,cv2.COLOR_BGR2YCR_CB)
    find_color = cv2.inRange(ycrcb,(0, 0, 150),(255, 255, 255))
    cv2.imshow("Image window", find_color)
    #cv2.imshow("HSV", ycrcb)

    contours, hierarchy = cv2.findContours(find_color,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # contours= contours+('0',)
    if contours is None:
      pass
    else :
      try:
        M = cv2.moments(contours[0])
        if M['m00'] != 0 :
          self.cx = int(M['m10']/ M['m00'])
          self.cy = int(M['m01']/ M['m00'])
        else:
          self.cx = 0
          self.cy = 0
      except :
           self.cx = 0
           self.cy = 0

    cv2.circle(iamge_rotate,(self.cx,self.cy),3,(0,0,255),-1)

    for cnt in contours:
      cv2.drawContours(iamge_rotate,[cnt],0,(255,0,0),3)

    cv2.imshow("result", iamge_rotate)

    cv2.waitKey(3)

  def tb3_m_publisher(self):
        msg = Twist()
        if  self.cx>=1 and self.cx>=120 :
          msg.angular.z = -0.3
        if self.cx >=1 and self.cx<=200 :
          msg.angular.z = 0.3
        if self.distance >=20 and self.cx<200 and self.cx>120 :
          msg.angular.z = 0.0
          msg.linear.x = 0.15
        if self.cx==0:
          msg.angular.z = 0.0
          msg.linear.x = 0.0
        print(self.cx)

        self.massage_publisher.publish(msg)
        #self.get_logger().info(f"Publisher message: {msg.linear.x}, {msg.angular.z}")
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


