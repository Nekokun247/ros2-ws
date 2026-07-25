# === ROS 2 Create Package ===

# Tạo ROS 2 package dùng ament_cmake và Apache-2.0.
ros2-pkg-create-cmake() {
    if [[ -z "$1" ]]; then
        echo "Usage: ros2-pkg-create-cmake <package_name>"
        return 1
    fi

    ros2 pkg create \
        --build-type ament_cmake \
        --license Apache-2.0 \
        "$1"
}

# Tạo ROS 2 package dùng ament_python và Apache-2.0.
ros2-pkg-create-python() {
    if [[ -z "$1" ]]; then
        echo "Usage: ros2-pkg-create-python <package_name>"
        return 1
    fi

    ros2 pkg create \
        --build-type ament_python \
        --license Apache-2.0 \
        "$1"
}
