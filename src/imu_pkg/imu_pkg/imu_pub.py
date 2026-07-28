import json
import serial

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class IMUNode(Node):

    def __init__(self):
        super().__init__("imu_node")

        # Cấu hình kết nối Serial
        port = "/dev/ttyACM0"
        baudrate = 500000
        self.serial = serial.Serial(port, baudrate, timeout=0.1)

        # Tạo Publisher gửi tin nhắn IMU (Topic: /imu/4q)
        topic = "/imu/q"
        self.publisher = self.create_publisher(Imu, topic, 10)

        # Vòng lặp timer đọc dữ liệu ở tần số 100Hz
        freq = 100  # Hz
        self.timer = self.create_timer(1.0 / freq, self.read_serial)

    def read_serial(self):
        try:
            # Đọc dòng JSON từ Serial
            line = self.serial.readline().decode("utf-8").strip()
            if not line:
                return

            data = json.loads(line)

            # Khởi tạo tin nhắn IMU chuẩn ROS 2
            msg = Imu()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = "imu_link"

            # Gán dữ liệu Quaternion
            msg.orientation.x = float(data["qx"])
            msg.orientation.y = float(data["qy"])
            msg.orientation.z = float(data["qz"])
            msg.orientation.w = float(data["qw"])

            self.publisher.publish(msg)

            self.get_logger().info(
                f"IMU Q: [{msg.orientation.x:.3f}, "
                f"{msg.orientation.y:.3f}, "
                f"{msg.orientation.z:.3f}, "
                f"{msg.orientation.w:.3f}]"
            )

        except (json.JSONDecodeError, KeyError, ValueError, UnicodeDecodeError):
            # Bỏ qua các chuỗi hỏng / chưa truyền hoàn chỉnh
            pass

    def destroy_node(self):
        # Đảm bảo ngắt kết nối Serial an toàn khi tắt Node
        if hasattr(self, "serial") and self.serial.is_open:
            self.serial.close()

        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = IMUNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
