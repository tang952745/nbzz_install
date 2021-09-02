import inspect
import yaml
from pathlib import Path
import threading
import os
import time
try:
    from nbzz.util.config import load_config
    import eth_keyfile
    from web3 import Web3
    from typing import Dict
    from nbzz.util.default_root import DEFAULT_ROOT_PATH
    from nbzz.util.nbzz_abi import NBZZ_ABI
except:
    print("nbzz未安装,此脚本需要安装nbzz 然后 . ./activate")
    exit(1)

class nbzz_conract_check:
    check_lock = threading.Lock()#threading.Semaphore(1)
    check_freq_lock=threading.Lock()
    def __init__(self, contract, address):
        self.nbzz_contract = contract
        self.address = address
    def freq_lock_acquire(self):
        def release_lock(w_time):
            time.sleep(w_time)
            nbzz_conract_check.check_freq_lock.release()
    
        nbzz_conract_check.check_freq_lock.acquire()
        threading.Thread(target=release_lock,args=(0.05,)).start()

    def _contract_function(self, con_func, args, try_time=3, error_meesage="func error"):
        for i in range(try_time):
            with nbzz_conract_check.check_lock:
                #self.freq_lock_acquire()
                try:
                    return con_func(*args)
                except Exception as ex:
                    print(ex)
                    pass
        print(error_meesage)

    def balanceOf(self):
        return self._contract_function(lambda ad: self.nbzz_contract.functions.balanceOf(ad).call(),
                                       (self.address,),
                                       error_meesage="获取nbzz余额失败")

    def pledge_banlance(self):
        return self._contract_function(lambda ad: self.nbzz_contract.functions.pledgeOf(ad).call(),
                                       (self.address,),
                                       error_meesage="获取质押状态失败")

    def nbzz_status(self):
        return self._contract_function(lambda ad: (self.nbzz_contract.functions.nodeState(ad).call())[0],
                                       (self.address,),
                                       error_meesage="获取nbzz状态失败")

def nbzz_status_ithread(i_bee_path):
    swarm_key=i_bee_path/"keys"/"swarm.key"
    if swarm_key.exists():
        geth_address=eth_keyfile.load_keyfile(str(swarm_key))["address"]
        geth_address = Web3.toChecksumAddress("0x"+geth_address)

        eth_stat=nbzz_conract_check(nbzz_contract,geth_address)
        print(f"{i_bee_path} {geth_address} {eth_stat.nbzz_status()}")
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

swap_url=config["swap_endpoint"]
if "http" ==swap_url[:4]:
    w3=Web3(Web3.HTTPProvider(swap_url))
elif "ws" ==swap_url[:2]:
    w3=Web3(Web3.WebsocketProvider(swap_url))

nbzz_contract = w3.eth.contract(address=config["network_overrides"]["constants"][config["selected_network"]]["CONTRACT"],abi=NBZZ_ABI)


all_bee_path=[i for i in bee_install_path.glob(".bee*")]
all_bee_path.sort()
all_thread = []
for i_bee_path in all_bee_path:
    ithread = threading.Thread(target=nbzz_status_ithread, args=(i_bee_path,))
    all_thread.append(ithread)
    ithread.setDaemon(True)
    ithread.start()

for ithread in all_thread:
    ithread.join()


