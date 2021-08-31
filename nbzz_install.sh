#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_install.sh | bash
#dev curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/dev/nbzz_install.sh  | xargs bash  dev 
echo $1
exit 0
apt update -y
apt upgrade -y

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
curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_run.py | python3
else
curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/dev/nbzz_run.py | python3