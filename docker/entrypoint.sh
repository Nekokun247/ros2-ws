#!/bin/bash
set -e

# --- Nạp Môi Trường ROS 2 & Workspace ---
source /opt/ros/jazzy/setup.bash

if [ -f "/ros2-ws/install/setup.bash" ]; then
    source /ros2-ws/install/setup.bash
fi

# --- Cấu Hình Đường Dẫn File CycloneDDS ---
# Ghi đè trực tiếp vào file config cố định để các phiên `docker exec` đều nhận
if [[ "$CYCLONEDDS_URI" == file://* ]]; then
    CYCLONEDDS_CONFIG_PATH="${CYCLONEDDS_URI#file://}"
else
    CYCLONEDDS_CONFIG_PATH="/tmp/cyclonedds-runtime.xml"
    export CYCLONEDDS_URI="file://${CYCLONEDDS_CONFIG_PATH}"
fi

# --- Tự Động Phát Hiện Network Interface Active ---
# Tìm card mạng chính có default route
DETECTED_IFACE=$(ip route show default 2>/dev/null | awk '/default/ {print $5; exit}')

if [ -z "$DETECTED_IFACE" ]; then
    echo "[entrypoint] Không tìm thấy default route -> Fallback: autodetermine" >&2
    IFACE_TAG='<NetworkInterface autodetermine="true" priority="default"/>'
else
    echo "[entrypoint] Interface đang active: $DETECTED_IFACE"
    IFACE_TAG="<NetworkInterface name=\"$DETECTED_IFACE\" priority=\"default\"/>"
fi

# --- Tạo File Cấu Hình CycloneDDS XML ---
cat > "$CYCLONEDDS_CONFIG_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<CycloneDDS xmlns="https://cdds.io/config">
  <Domain Id="any">
    <General>
      <Interfaces>
        $IFACE_TAG
      </Interfaces>
      <AllowMulticast>true</AllowMulticast>
    </General>

    <Tracing>
      <Verbosity>config</Verbosity>
      <OutputFile>/tmp/cyclonedds.log</OutputFile>
    </Tracing>
  </Domain>
</CycloneDDS>
EOF

echo "[entrypoint] Cập nhật CycloneDDS tại: $CYCLONEDDS_CONFIG_PATH"
echo "[entrypoint] CYCLONEDDS_URI: $CYCLONEDDS_URI"

# --- Chuyển Quyền Điều Khiển Cho Tiến Trình Chính Của Container ---
exec "$@"