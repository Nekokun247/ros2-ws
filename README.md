# Customize Terminal
https://github.com/novaspirit/pimpyourterm
# Update
sudo apt update && sudo apt full-upgrade -y
# Install git & gh
sudo apt update && sudo apt install git
sudo apt update && sudo apt install gh
## Setup git
git config --global user.name ""
git config --global user.email ""
git config --list
### Setup gh
gh auth login
gh auth status
# Install tree
sudo apt update && sudo apt install tree
# Install mesa-utils
sudo apt update && sudo apt install mesa-utils
# Install Docker
https://docs.docker.com/engine/install/ubuntu/
# Install NVIDIA Container Toolkit
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.19.1/install-guide.html
<or>
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
# Install ROS2 Jazzy
https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html#install-ros-2
