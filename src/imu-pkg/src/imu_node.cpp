#include <chrono>
#include <fcntl.h>
#include <stdexcept>
#include <string>
#include <termios.h>
#include <unistd.h>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class Stm32ImuNode : public rclcpp::Node {
public:
  Stm32ImuNode() : Node("stm32_imu_node") {
    port_ = declare_parameter<std::string>("port", "/dev/ttyACM0");
    topic_ = declare_parameter<std::string>("topic", "/imu/mcu_json");

    publisher_ = create_publisher<std_msgs::msg::String>(topic_, 10);

    open_serial();

    timer_ = create_wall_timer(std::chrono::milliseconds(2), std::bind(&Stm32ImuNode::read_serial, this));
  }

  ~Stm32ImuNode() override {
    if (serial_fd_ >= 0) {
      close(serial_fd_);
    }
  }

private:
  void open_serial() {
    serial_fd_ = open(port_.c_str(), O_RDONLY | O_NOCTTY | O_NONBLOCK);

    if (serial_fd_ < 0) {
      RCLCPP_FATAL(get_logger(), "Khong mo duoc cong %s", port_.c_str());
      throw std::runtime_error("Serial open failed");
    }

    termios tty{};

    if (tcgetattr(serial_fd_, &tty) != 0) {
      close(serial_fd_);
      serial_fd_ = -1;
      throw std::runtime_error("tcgetattr failed");
    }

    cfmakeraw(&tty);
    cfsetispeed(&tty, B921600);
    cfsetospeed(&tty, B921600);

    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8 | CLOCAL | CREAD;
    tty.c_cflag &= ~(PARENB | CSTOPB | CRTSCTS);
    tty.c_cc[VMIN] = 0;
    tty.c_cc[VTIME] = 0;

    if (tcsetattr(serial_fd_, TCSANOW, &tty) != 0) {
      close(serial_fd_);
      serial_fd_ = -1;
      throw std::runtime_error("Serial configuration failed");
    }

    tcflush(serial_fd_, TCIFLUSH);

    RCLCPP_INFO(get_logger(), "Dang doc %s tai 921600 baud va publish len %s", port_.c_str(), topic_.c_str());
  }

  void read_serial() {
    char buffer[256];
    ssize_t count = read(serial_fd_, buffer, sizeof(buffer));

    if (count <= 0) {
      return;
    }

    receive_buffer_.append(buffer, static_cast<std::size_t>(count));

    std::size_t newline_position;

    while ((newline_position = receive_buffer_.find('\n')) != std::string::npos) {
      std::string line = receive_buffer_.substr(0, newline_position);
      receive_buffer_.erase(0, newline_position + 1);

      if (!line.empty() && line.back() == '\r') {
        line.pop_back();
      }

      if (line.empty()) {
        continue;
      }

      std_msgs::msg::String message;
      message.data = line;
      publisher_->publish(message);
    }
  }

  std::string port_;
  std::string topic_;
  std::string receive_buffer_;

  int serial_fd_ = -1;

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Stm32ImuNode>());
  rclcpp::shutdown();

  return 0;
}