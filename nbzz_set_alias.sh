#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_set_alias.sh | bash -s alias 
#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/dev/nbzz_set_alias.sh | bash -s alias dev

cd nbzz
. ./activate

cd ..

#echo $1
export NBZZ_ALIAS=$1

if  [ $# == 1 ] ; then
curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_set_alias.py | python3
else
curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/dev/nbzz_set_alias.py | python3
fi