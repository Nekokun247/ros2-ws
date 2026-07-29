import math
import tf_transformations
from tf_transformations import euler_from_quaternion

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class IMUSubscriber(Node):
    def __init__(self):
        super().__init__("IMU_Subcriber")
        topic = "/imu/data"
        self.subscription = self.create_subscription(Imu, topic, self.imu_callback, 10)
        self.subscription

    def imu_callback(self, msg: Imu):
        qx = msg.orientation.x
        qy = msg.orientation.y
        qz = msg.orientation.z
        qw = msg.orientation.w

        euler = tf_transformations.euler_from_quaternion([qx, qy, qz, qw])

        # Đổi từ radian sang độ để so sánh trực quan với dữ liệu firmware gốc
        roll = math.degrees(euler[0])
        pitch = math.degrees(euler[1])
        yaw = math.degrees(euler[2])

        self.get_logger().info(
            f"Roll: {roll:.2f}° | Pitch: {pitch:.2f}° | Yaw: {yaw:.2f}°"
        )


def main(args=None):
    rclpy.init(args=args)
    imu_sub = IMUSubscriber()

    try:
        rclpy.spin(imu_sub)
    except KeyboardInterrupt:
        pass
    finally:
        imu_sub.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
