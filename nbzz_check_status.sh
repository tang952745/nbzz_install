#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_check_status.sh | bash
#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/dev/nbzz_check_status.sh | bash -s dev 

cd nbzz
. ./activate

cd ..
echo $1
export NBZZ_INCOME=$1
if  [ $# == 0 ] ; then
curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_check_status.py | python3
else
curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/dev/nbzz_check_status.py | python3
fi