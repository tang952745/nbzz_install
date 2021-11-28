#curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/master/nbzz_install.sh | bash
#curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/dev/nbzz_install.sh | bash -s dev 

# Install Git
apt install git -y

rm -rf ./nbzz
# Checkout the source and install
git clone https://github.com/LeetSquad/Swarm-nbzz.git nbzz
cd nbzz

sh install.sh

. ./activate

cd ..
if  [ $# == 0 ] ; then
curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/master/nbzz_run.py | python3
else
curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/dev/nbzz_run.py | python3
fi