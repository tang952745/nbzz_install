try:
    from nbzz.cmds.pledge_funcs import faucet, pledge
    from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile
    import eth_keyfile
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

os.system("sed -i \"/swap_endpoint: /c\\swap_endpoint:  ws://120.76.247.190:8546 \"  /root/.nbzz/stagenet/config/config.yaml")
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
all_bee_path=[i for i in bee_install_path.glob(".bee*")]

for i_bee_path in tqdm(all_bee_path):
    swarm_key=i_bee_path/"keys"/"swarm.key"
    if swarm_key.exists():
        print(f"install bee in {i_bee_path}")

        geth_address=eth_keyfile.load_keyfile(str(swarm_key))
        print(geth_address)
        exit(1)
        try:
            faucet(bee_passwd,str(swarm_key))
        except: 
            print(i_bee_path,"打水失败")
        try:
            pledge(15,bee_passwd,str(swarm_key))
        except: 
            print(i_bee_path,"质押并启动失败")
    else:
        print(i_bee_path ,"目录下不存在keys文件,检查是否安装")

