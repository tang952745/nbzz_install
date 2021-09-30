#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_income_change.sh | bash -s address 
#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/dev/nbzz_income_change.sh | bash -s address dev

cd nbzz
. ./activate

cd ..

#echo $1
export NBZZ_INCOME=$1

if  [ $# == 1 ] ; then
curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_income_change.py | python3
else
curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/dev/nbzz_income_change.py | python3
fi