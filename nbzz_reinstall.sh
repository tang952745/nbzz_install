#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_reinstall.sh | bash
#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/dev/nbzz_reinstall.sh | bash -s dev 
apt install git -y

rm -rf ./nbzz
# Checkout the source and install
git clone https://github.com/LeetSquad/Swarm-nbzz.git nbzz