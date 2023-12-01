import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from rclpy.qos import QoSProfile
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 2
GPIO_ECHO = 3

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

# dist = distance()
class M_pub(Node):
  def __init__(self):
    super().__init__('distance_publisher')
    self.qos_profile = QoSProfile(depth = 10)
    self.massage_publisher = self.create_publisher(Float32, 'distance', self.qos_profile)
    self.timer = self.create_timer(1, self.m_publisher)
    self.count = 0

  def m_publisher(self):
    msg = Float32()
    msg.data=distance()
    self.massage_publisher.publish(msg)
    self.get_logger().info(f'distance: {msg.data}')
    self.count += 1


def main(args=None):
  rclpy.init(args=args)
  node = M_pub()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard interrupt!!!!')
  finally:
    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    try:
      main()
    except KeyboardInterrupt:
      print("Measurement stopped by User")
      GPIO.cleanup()
