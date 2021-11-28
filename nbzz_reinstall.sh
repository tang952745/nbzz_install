#curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/master/nbzz_reinstall.sh | bash
#curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/dev/nbzz_reinstall.sh | bash -s dev 
apt install git -y

rm -rf ./nbzz
# Checkout the source and install
git clone https://github.com/LeetSquad/Swarm-nbzz.git nbzz