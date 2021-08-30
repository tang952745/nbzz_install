try:
    from nbzz.cmds.pledge_funcs import faucet, pledge
    from nbzz.cmds.start import start_cmd
    from nbzz.util.config import load_config
    import eth_keyfile
    from web3 import Web3
    from typing import Dict
    from nbzz.util.default_root import DEFAULT_ROOT_PATH
    from nbzz.util.nbzz_abi import NBZZ_ABI
except:
    print("nbzz未安装,此脚本需要安装nbzz 然后 . ./activate")
    exit(1)
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

env=os.environ
if "NBZZ_RPC" in env:
    os.system(f"sed -i \"/swap_endpoint:  /c\\swap_endpoint:  {env['NBZZ_RPC']} \"  /root/.nbzz/stagenet1/config/config.yaml")

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


class nbzz_conract_check:
    def __init__(self,contract,address):
        #print(tx_receipt.blockNumber)
        self.nbzz_contract = contract
        self.address=Web3.toChecksumAddress("0x"+address)

    def balanceOf(self):
        balance=self.nbzz_contract.functions.balanceOf(self.address).call()
        return balance
    def pledge_banlance(self):
        for i in range(3):
            try:
                balance=self.nbzz_contract.functions.pledgeOf(self.address).call()
                return balance
            except:
                print("获取质押状态失败,重新尝试...")
    def nbzz_status(self):
        for i in range(3):
            try:
                status=self.nbzz_contract.functions.nodeState(self.address).call()
                return status[0]
            except:
                print("获取nbzz状态失败,重新尝试...")

config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

swap_url=config["swap_endpoint"]
if "http" ==swap_url[:4]:
    w3=Web3(Web3.HTTPProvider(swap_url))
elif "ws" ==swap_url[:2]:
    w3=Web3(Web3.WebsocketProvider(swap_url))

nbzz_contract = w3.eth.contract(address=config["network_overrides"]["constants"][config["selected_network"]]["CONTRACT"],abi=NBZZ_ABI)

all_bee_path=[i for i in bee_install_path.glob(".bee*")]
for i_bee_path in tqdm(all_bee_path):
    swarm_key=i_bee_path/"keys"/"swarm.key"
    if swarm_key.exists():
        geth_address=eth_keyfile.load_keyfile(str(swarm_key))["address"]
        eth_stat=nbzz_conract_check(nbzz_contract,geth_address)

        if eth_stat.nbzz_status():
            print(f"{i_bee_path} 已经启动")
            continue
        if eth_stat.pledge_banlance() >=15:
            print(f"{i_bee_path} 已经完成质押")
        else:
            print(f"install bee in {i_bee_path}")
            try:
                faucet(bee_passwd,str(swarm_key))
            except: 
                print(i_bee_path,"打水失败")
            try:
                pledge(15,bee_passwd,str(swarm_key))
            except: 
                print(i_bee_path,"质押并启动失败")
        try:
            os.system(f"nbzz start -p {bee_passwd}  --bee-key-path {str(swarm_key)}")
            print("")
            #start_cmd(None,bee_passwd,str(swarm_key))
        except: 
            print(i_bee_path,"启动失败")

    else:
        print(i_bee_path ,"目录下不存在keys文件,检查是否安装")

