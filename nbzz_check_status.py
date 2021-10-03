import yaml
from pathlib import Path
import threading
import os
try:
    from nbzz.util.config import load_config
    import eth_keyfile
    from web3 import Web3
    from typing import Dict
    from nbzz.util.default_root import DEFAULT_ROOT_PATH
    from nbzz.rpc.xdai_rpc import connect_w3,get_model_contract,get_proxy_contract,get_glod_contract
except:
    print("nbzz未安装,此脚本需要安装nbzz 然后 . ./activate")
    exit(1)
try:
    import plyvel
except:
    try:
        os.system('pip3 install plyvel')
    except:
        print("plyvel install error ")
        exit(1)
    import plyvel
class nbzz_conract_check:
    check_lock = threading.Lock()

    def __init__(self, model_contract,glod_contract,proxy_contract, address):
        self.model_contract = model_contract
        self.glod_contract = glod_contract
        self.proxy_contract = proxy_contract
        self.address = address

    def _contract_function(self, con_func, args, try_time=3, error_meesage="func error"):
        for i in range(try_time):
                try:
                    with nbzz_conract_check.check_lock:
                        return con_func(*args)
                except:
                    pass
        print(error_meesage)

    def balanceOf(self):
        return self._contract_function(lambda ad: self.proxy_contract.functions.balanceOf(ad).call()/1e18,
                                       (self.address,),
                                       error_meesage="获取nbzz余额失败")

    def pledge_banlance(self):
        return self._contract_function(lambda ad: self.glod_contract.functions.balancesPledge(ad).call()/1e18,
                                       (self.address,),
                                       error_meesage="获取质押状态失败")

    def nbzz_status(self):
        return self._contract_function(lambda ad: (self.model_contract.functions.nodeState(ad).call()),
                                       (self.address,),
                                       error_meesage="获取nbzz状态失败")

def nbzz_status_ithread(i_bee_path,status_dict,status_lock):
    swarm_key=i_bee_path/"keys"/"swarm.key"
    state_store= i_bee_path/"statestore"
    if not state_store.exists():
        print(f"{i_bee_path} 目录下不存在statestore文件,检查是否安装")
        return
    if swarm_key.exists():
        xdai_address=eth_keyfile.load_keyfile(str(swarm_key))["address"]
        xdai_address = Web3.toChecksumAddress("0x"+xdai_address)

        eth_stat=nbzz_conract_check(model_contract,glod_contract,proxy_contract, xdai_address)
        ready,online,_,set_overlay=eth_stat.nbzz_status()
        db=plyvel.DB(str(state_store))
        overlay_address=db.get(b"non-mineable-overlay").decode().strip('"')
        db.close()
        if online:
            stat_info="nbzz已经启动,正在挖矿中"
            with status_lock:
                status_dict["not_initiated"]-=1
                status_dict["running"]+=1
        elif ready and (set_overlay==overlay_address):
            with status_lock:
                status_dict["not_initiated"]-=1
                status_dict["start_wait"]+=1
            stat_info="nbzz已经启动,等待钓鱼节点确认后开始挖矿"
        else:
            stat_info="nbzz未启动"
        print(f"{i_bee_path} {xdai_address} {stat_info}")
    else:
        print(f"{i_bee_path} 目录下不存在keys文件,检查是否安装")

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

config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

w3=connect_w3(config["swap_endpoint"])
model_contract,_ = get_model_contract(w3)
proxy_contract=get_proxy_contract(w3)
glod_contract=get_glod_contract(w3)


all_bee_path=[i for i in bee_install_path.glob(".bee*")]
all_bee_path.sort()
all_thread = []
status_dict={"running":0,"start_wait":0,"not_initiated":len(all_bee_path)}
status_lock=threading.Lock()

for i_bee_path in all_bee_path:
    ithread = threading.Thread(target=nbzz_status_ithread, args=(i_bee_path,status_dict,status_lock))
    all_thread.append(ithread)
    ithread.setDaemon(True)
    ithread.start()

for ithread in all_thread:
    ithread.join()
print(f"挖矿中:{status_dict['running']},已启动等待钓鱼节点确认:{status_dict['start_wait']},未启动:{status_dict['not_initiated']}")

