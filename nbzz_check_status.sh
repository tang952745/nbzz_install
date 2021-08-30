#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_check_status.sh | bash -

cd nbzz
. ./activate

cd ..

curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_check_status.py | python3 -