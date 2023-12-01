import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from rclpy.qos import QoSProfile

class M_sub(Node):
  def __init__(self):
    super().__init__('distance_subscriber')
    self.qos_profile = QoSProfile(depth = 10)
    self.helloworld_subscriber = self.create_subscription(Float32, 'distance', self.subscriber_massage, self.qos_profile)

  def subscriber_massage(self, msg):
    self.get_logger().info(f'Recived mesage: {msg.data}')

def main(args = None):
  rclpy.init(args=args)
  node = M_sub()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard interrupt!!!!')
  finally:
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
  main()
