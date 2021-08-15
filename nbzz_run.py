try:
    from nbzz.cmds.pledge_funcs import faucet, pledge
except:
    print("nbzz未安装,此脚本需要安装nbzz 然后 . ./activate")
import yaml
from pathlib import Path
import os
try:
    from tqdm import tqdm
except:
    try:
        os.system('pip3 install tqdm')
    except:
            print("tqdm install error ")
            exit(1)
    from tqdm import tqdm

os.system("nbzz init")
#curl  -fsSL https://gitee.com/tousang/nbzz_install/raw/master/nbzz_run.py | python3 -
bee_con_path=Path("config.yaml")
if not bee_con_path.exists():
    print("路径错误,请移动到bee批量安装脚本的启动目录.")
    exit(1)
with bee_con_path.open("r",) as fid :
    bee_con=yaml.safe_load(fid)
bee_install_path=Path(bee_con["bee"]["base_path"])
bee_passwd=bee_con["bee"]["password"]
if not bee_install_path.exists():
    print("bee未安装或者未成功启动")
    exit(1)

for i_bee_path in tqdm(bee_install_path.glob("bee*")):
    print(i_bee_path)
