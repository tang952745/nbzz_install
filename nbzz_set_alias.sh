#curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/master/nbzz_set_alias.sh | bash -s alias 
#curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/dev/nbzz_set_alias.sh | bash -s alias dev

cd nbzz
. ./activate

cd ..

#echo $1
export NBZZ_ALIAS=$1

if  [ $# == 1 ] ; then
curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/master/nbzz_set_alias.py | python3
else
curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/dev/nbzz_set_alias.py | python3
fi