#!/bin/bash
set -e

# Nạp môi trường ROS 2 Jazzy.
source /opt/ros/jazzy/setup.bash

# Nạp workspace nếu đã được build.
if [ -f "/ros2-ws/install/setup.bash" ]; then
    source /ros2-ws/install/setup.bash
fi

# Thực thi lệnh được truyền từ Dockerfile hoặc Docker Compose.
exec "$@"
