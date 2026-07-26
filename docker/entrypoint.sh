#!/bin/bash
set -e

# Nạp môi trường ROS 2 Jazzy.
source /opt/ros/jazzy/setup.bash

# Nạp workspace nếu đã được build.
if [ -f "/ros2-ws/install/setup.bash" ]; then
    source /ros2-ws/install/setup.bash
fi

# ==============================================================================
# Tự động phát hiện network interface đang active (WiFi hoặc LAN, bất kể tên
# gì) và sinh file cấu hình Cyclone DDS tương ứng, để không cần sửa tay mỗi
# khi đổi mạng (WiFi <-> LAN, đổi sang WiFi khác, v.v.)
# ==============================================================================
CYCLONEDDS_RUNTIME_CONFIG="/tmp/cyclonedds-runtime.xml"

# Lấy interface đang có "default route" (tức đang thực sự dùng để ra mạng).
DETECTED_IFACE=$(ip route show default 2>/dev/null | awk '/default/ {print $5; exit}')

if [ -z "$DETECTED_IFACE" ]; then
    echo "[entrypoint] Không tìm thấy interface có default route." >&2
    echo "[entrypoint] Fallback sang autodetermine=true." >&2
    IFACE_TAG='<NetworkInterface autodetermine="true" priority="default"/>'
else
    echo "[entrypoint] Phát hiện interface đang active: $DETECTED_IFACE"
    IFACE_TAG="<NetworkInterface name=\"$DETECTED_IFACE\" priority=\"default\"/>"
fi

cat > "$CYCLONEDDS_RUNTIME_CONFIG" <<EOF
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

echo "[entrypoint] Đã sinh file cấu hình Cyclone DDS: $CYCLONEDDS_RUNTIME_CONFIG"

# Ghi đè CYCLONEDDS_URI để dùng đúng file vừa sinh, bất kể giá trị nào đã
# được set sẵn trong docker-compose.yml (ví dụ cyclonedds.pi.xml/pc.xml cũ).
export CYCLONEDDS_URI="file://${CYCLONEDDS_RUNTIME_CONFIG}"

# Thực thi lệnh được truyền từ Dockerfile hoặc Docker Compose.
exec "$@"