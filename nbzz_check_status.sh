#curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/master/nbzz_check_status.sh | bash
#curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/dev/nbzz_check_status.sh | bash -s dev 

cd nbzz
. ./activate

cd ..

if  [ $# == 0 ] ; then
curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/master/nbzz_check_status.py | python3
else
curl  -fsSL https://raw.githubusercontent.com/tang952745/nbzz_install/dev/nbzz_check_status.py | python3
fi