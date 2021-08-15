apt update -y
apt upgrade -y

# Install Git
apt install git -y

# Checkout the source and install
git clone https://github.com/LeetSquad/Swarm-nbzz.git nbzz
cd nbzz

sh install.sh

. ./activate

cd ..

curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_run.py | python3 -