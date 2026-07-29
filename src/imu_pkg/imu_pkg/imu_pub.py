# Thư viện Python
import json
import serial

# Thư viện ROS2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu


class IMUPublisher(Node):
    def __init__(self):
        # Tên Node in ra
        super().__init__("IMU_Publisher")

        # Cấu hình kết nối Serial
        port = "/dev/ttyACM0"
        baudrate = 500000
        self.serial = serial.Serial(port, baudrate, timeout=0.1)

        # Tạo Publisher gửi tin nhắn IMU (Topic: /imu/data)
        topic = "/imu/data"
        self.publisher = self.create_publisher(Imu, topic, 10)

        # Vòng lặp timer đọc dữ liệu ở tần số 100Hz
        freq = 100  # Hz
        period = 1.0 / freq
        self.timer = self.create_timer(period, self.read_serial)

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

            # Lấy dữ liệu Roll, Pitch, Yaw
            roll = float(data["Roll"])
            pitch = float(data["Pitch"])
            yaw = float(data["Yaw"])

            self.publisher.publish(msg)

            # self.get_logger().info(
            #     f"IMU Q: [{msg.orientation.x:.3f}, "
            #     f"{msg.orientation.y:.3f}, "
            #     f"{msg.orientation.z:.3f}, "
            #     f"{msg.orientation.w:.3f}]"
            # )
            self.get_logger().info(
                f"Roll: {roll:.2f} | Pitch: {pitch:.2f} | Yaw: {yaw:.2f}"
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
    imu_pub = IMUPublisher()

    try:
        rclpy.spin(imu_pub)
    except KeyboardInterrupt:
        pass
    finally:
        imu_pub.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
