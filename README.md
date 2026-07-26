# Thiết lập môi trường phát triển ROS 2 trên WSL2

Tài liệu này dành cho Ubuntu 24.04 chạy trong WSL2, sử dụng ROS 2 Jazzy và Docker Desktop.

## 1. Cập nhật hệ thống

```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt autoremove -y
```

> Sau khi nâng cấp WSL hoặc kernel, chạy `wsl --shutdown` trong PowerShell rồi mở lại Ubuntu.

## 2. Cài các công cụ cơ bản

```bash
sudo apt install -y \
  ca-certificates \
  curl \
  wget \
  gnupg \
  lsb-release \
  software-properties-common \
  git \
  gh \
  tree \
  unzip \
  zip \
  nano \
  vim \
  htop \
  jq
```

Kiểm tra:

```bash
git --version
gh --version
```

## 3. Cấu hình Git và GitHub CLI

Thay nội dung trong dấu ngoặc kép bằng thông tin của bạn:

```bash
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global init.defaultBranch main
```

Kiểm tra cấu hình:

```bash
git config --global --list
```

Đăng nhập GitHub CLI:

```bash
gh auth login
gh auth status
```
Lệnh Git:

````bash
# Push
git add .
git commit -m ""
git push origin main
# Pull
git pull --rebase origin main
````

## 4. Tùy chỉnh terminal

Tham khảo:

- [Pimp My Term](https://github.com/novaspirit/pimpyourterm)

Các gói thường dùng cho Zsh:

```bash
sudo apt install -y zsh fonts-powerline
```

## 5. Cài công cụ build

```bash
sudo apt install -y \
  build-essential \
  cmake \
  ninja-build \
  pkg-config \
  gdb \
  python3-pip \
  python3-venv \
  python3-dev
```

## 6. Cài công cụ mạng và chẩn đoán DDS

```bash
sudo apt install -y \
  iproute2 \
  iputils-ping \
  net-tools \
  dnsutils \
  traceroute \
  tcpdump \
  socat \
  netcat-openbsd \
  ethtool
```

Các lệnh kiểm tra thường dùng:

```bash
ip -br address
ip route
ping <IP_RASPBERRY_PI>
sudo tcpdump -ni any udp
```

## 7. Cài công cụ đồ họa

```bash
sudo apt install -y \
  mesa-utils \
  vulkan-tools
```

Kiểm tra OpenGL:

```bash
glxinfo -B
```

Kiểm tra Vulkan:

```bash
vulkaninfo --summary
```

## 8. Cài Docker

### Phương án khuyến nghị trên WSL2: Docker Desktop

Cài Docker Desktop trên Windows và bật:

1. **Use the WSL 2 based engine**.
2. **Settings → Resources → WSL Integration**.
3. Bật tích hợp cho bản Ubuntu đang sử dụng.

Tài liệu chính thức:

- [Docker Desktop với WSL2](https://docs.docker.com/desktop/features/wsl/)
- [Hướng dẫn sử dụng Docker trong WSL2](https://docs.docker.com/desktop/features/wsl/use-wsl/)

Kiểm tra trong Ubuntu:

```bash
docker version
docker compose version
docker run --rm hello-world
```
Cấp quyền Docker:
```bash
sudo usermod -aG docker $USER
sudo gpasswd -a $USER docker
newgrp docker
````
> Không cài thêm Docker Engine bên trong Ubuntu nếu đang sử dụng Docker Desktop, nhằm tránh tồn tại hai Docker daemon độc lập.

### Phương án thay thế: Docker Engine cài trực tiếp trong Ubuntu

Chỉ sử dụng phương án này khi không dùng Docker Desktop:

- [Cài Docker Engine trên Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

## 9. NVIDIA GPU trong Docker

### Khi sử dụng Docker Desktop

Docker Desktop với WSL2 đã hỗ trợ NVIDIA GPU thông qua GPU-PV. Không cần chạy `nvidia-ctk runtime configure` bên trong Ubuntu chỉ để cấu hình Docker Desktop.

Yêu cầu:

1. Driver NVIDIA trên Windows hỗ trợ WSL2.
2. WSL được cập nhật.
3. Docker Desktop dùng WSL2 backend.

Kiểm tra từ PowerShell:

```powershell
wsl --update
wsl --shutdown
```

Kiểm tra GPU trong container:

```bash
docker run --rm --gpus all nvidia/cuda:12.6.3-base-ubuntu24.04 nvidia-smi
```

Tài liệu chính thức:

- [GPU support trong Docker Desktop](https://docs.docker.com/desktop/features/gpu/)

### Khi Docker Engine được cài trực tiếp trong Ubuntu

Chỉ trong trường hợp này mới cài NVIDIA Container Toolkit vào Ubuntu:

```bash
sudo apt update
sudo apt install -y --no-install-recommends curl gnupg2

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Tài liệu chính thức:

- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## 10. Cài ROS 2 Jazzy

Thực hiện theo tài liệu chính thức:

- [ROS 2 Jazzy trên Ubuntu bằng Debian packages](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)

Sau khi cài ROS 2, cài thêm các công cụ phát triển:

```bash
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-vcstool \
  python3-argcomplete
```

Khởi tạo `rosdep` một lần:

```bash
sudo rosdep init
rosdep update
```

> Nếu `sudo rosdep init` báo file cấu hình đã tồn tại thì không cần chạy lại.

Nạp môi trường ROS 2 cho Zsh:

```bash
echo 'source /opt/ros/jazzy/setup.zsh' >> ~/.zshrc
source ~/.zshrc
```

Kiểm tra:

```bash
printenv ROS_DISTRO
ros2 --help
```

## 11. Alias build workspace ROS 2

Thêm vào `~/.zshrc`:

```zsh
# === ROS2 Docker ===

# Start container và vào container
alias ros2-start='docker compose -f docker/compose.pc.yaml up -d && docker compose -f docker/compose.pc.yaml exec ros2-pc /bin/zsh'

# Vào container đang chạy
alias ros2-run='docker compose -f docker/compose.pc.yaml exec ros2-pc /bin/zsh'

# Build image và khởi động container
alias ros2-build='docker compose -f docker/compose.pc.yaml up -d --build'

# Build lại image từ đầu
alias ros2-rebuild='docker compose -f docker/compose.pc.yaml down && docker compose -f docker/compose.pc.yaml build --no-cache && docker compose -f docker/compose.pc.yaml up -d'

# Dừng container
alias ros2-stop='docker compose -f docker/compose.pc.yaml down'

# Kiểm tra trạng thái container
alias ros2-status='docker compose -f docker/compose.pc.yaml ps'
```

```zsh
# Build một hoặc nhiều package được chỉ định.
colcon-build() {
    if [[ $# -eq 0 ]]; then
        echo "Usage: colcon-build <package_name> [package_name...]"
        return 1
    fi

    colcon build \
        --symlink-install \
        --packages-select "$@" || return 1

    source install/setup.zsh
}

# Build toàn bộ workspace.
colcon-build-all() {
    colcon build --symlink-install || return 1
    source install/setup.zsh
}
```

Nạp lại cấu hình:

```bash
source ~/.zshrc
```

Ví dụ:

```bash
colcon-build my_package
colcon-build package_a package_b
colcon-build-all
```
