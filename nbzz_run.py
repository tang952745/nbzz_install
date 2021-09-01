import inspect
import yaml
from pathlib import Path
import threading
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
# store builtin print
old_print = print
def new_print(*args, **kwargs):
    # if tqdm.tqdm.write raises error, use builtin print
    try:
        tqdm.write(*args, **kwargs)
    except:
        old_print(*args, ** kwargs)
# globaly replace print with new_print
inspect.builtins.print = new_print

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
#print=new_print
class nbzz_conract_check:
    check_semaphore=threading.Semaphore(5)
    def __init__(self,contract,address):
        self.nbzz_contract = contract
        self.address=address
    def _contract_function(func,args):
        pass
    def balanceOf(self):
        balance=0
        for i in range(3):
            nbzz_conract_check.check_semaphore.acquire()
            try:
                balance=self.nbzz_contract.functions.balanceOf(self.address).call()
                break
            except:
                print("获取余额失败,重新尝试...")
            finally:
                nbzz_conract_check.check_semaphore.release()
        return balance
        

    def pledge_banlance(self):
        balance=0
        for i in range(3):
            nbzz_conract_check.check_semaphore.acquire()
            try:
                balance=self.nbzz_contract.functions.pledgeOf(self.address).call()
                break
            except:
                print("获取质押状态失败,重新尝试...")
            finally:
                nbzz_conract_check.check_semaphore.release()
        return balance
    def nbzz_status(self):
        for i in range(3):
            nbzz_conract_check.check_semaphore.acquire()
            try:
                status=(self.nbzz_contract.functions.nodeState(self.address).call())[0]
                return status
            except:
                pass        
            finally:
                nbzz_conract_check.check_semaphore.release()
        print("获取nbzz状态失败,重新尝试...")
        

def i_thread_nbzz(ii_bee_path):
    swarm_key=ii_bee_path/"keys"/"swarm.key"
    if not swarm_key.exists():
        tqdm.write(f"{ii_bee_path} 目录下不存在keys文件,检查是否安装")
        return 
        
    geth_address=eth_keyfile.load_keyfile(str(swarm_key))["address"]
    geth_address=Web3.toChecksumAddress("0x"+geth_address)

    eth_stat=nbzz_conract_check(nbzz_contract,geth_address)
    eth_balance=w3.eth.getBalance(geth_address)/1e18
    
    if eth_balance<0.002:
        tqdm.write(f"{ii_bee_path} {geth_address} geth不足,目前余额: {eth_balance:.4f}")
        return

    if eth_stat.nbzz_status():
        tqdm.write(f"{ii_bee_path} 已经启动")
        return

    if eth_stat.pledge_banlance() >=15:
        tqdm.write(f"{ii_bee_path} 已经完成质押")
    else:
        tqdm.write(f"install bee in {ii_bee_path}")
        if eth_stat.balanceOf() <15:
            run_semaphore.acquire()
            try:
                faucet(bee_passwd,str(swarm_key))
            except: 
                tqdm.write(f"{ii_bee_path} 打水失败")
                return
            finally:
                run_semaphore.release()
        else:
            tqdm.write("nbzz余额充足")
        run_semaphore.acquire()
        try:
            pledge(15,bee_passwd,str(swarm_key))
        except: 
            tqdm.write(f"{ii_bee_path} 质押失败")
            return
        finally:
            run_semaphore.release()

    run_semaphore.acquire()
    try:
        os.system(f"nbzz start -p {bee_passwd}  --bee-key-path {str(swarm_key)}")
        tqdm.write("")
        #start_cmd(None,bee_passwd,str(swarm_key))
    except: 
        tqdm.write(f"{ii_bee_path} 启动失败")
    finally:
        run_semaphore.release()


run_semaphore=threading.Semaphore(1)
#初始化nbzz
os.system("nbzz init")

#修改rpc
env=os.environ
if "NBZZ_RPC" in env:
    os.system(f"sed -i \"/swap_endpoint:  /c\\swap_endpoint:  {env['NBZZ_RPC']} \"  /root/.nbzz/stagenet1/config/config.yaml")

#读取createbee配置
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

#读取合约
config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

swap_url=config["swap_endpoint"]
if "http" ==swap_url[:4]:
    w3=Web3(Web3.HTTPProvider(swap_url))
elif "ws" ==swap_url[:2]:
    w3=Web3(Web3.WebsocketProvider(swap_url))

nbzz_contract = w3.eth.contract(address=config["network_overrides"]["constants"][config["selected_network"]]["CONTRACT"],abi=NBZZ_ABI)

#开始部署
all_bee_path=[i for i in bee_install_path.glob(".bee*")]
all_bee_path.sort()
all_thread=[]
for i_bee_path in tqdm(all_bee_path,ncols=80):
    ithread=threading.Thread(target=i_thread_nbzz,args=(i_bee_path,))
    all_thread.append(ithread)
    ithread.setDaemon(True)
    ithread.start()

for ithread in all_thread:
    ithread.join()