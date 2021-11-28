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
    from nbzz.cmds.pledge_funcs import add_pledge
    from nbzz.cmds.start import start_cmd
    from nbzz.util.config import load_config
    import eth_keyfile
    from web3 import Web3
    from typing import Dict
    from nbzz.util.default_root import DEFAULT_ROOT_PATH
    from nbzz.rpc.xdai_rpc import connect_w3,get_model_contract,get_proxy_contract,get_glod_contract
    from nbzz.cmds.start import statestore_dir
except:
    print("nbzz未安装,此脚本需要安装nbzz 然后 . ./activate")
    exit(1)


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


def i_thread_nbzz(ii_bee_path):
    try:
        swarm_key = ii_bee_path/"keys"/"swarm.key"
        state_store= ii_bee_path/"statestore"
        if not swarm_key.exists():
            tqdm.write(f"{ii_bee_path} 目录下不存在keys文件,检查是否安装")
            return
        if not state_store.exists():
            tqdm.write(f"{ii_bee_path} 目录下不存在statestore文件,检查是否安装")
            return

        with statestore_dir(state_store) as statestoredb:
            overlay_address=statestoredb.get_overlay()

        xdai_address = eth_keyfile.load_keyfile(str(swarm_key))["address"]
        xdai_address = Web3.toChecksumAddress("0x"+xdai_address)

        eth_stat = nbzz_conract_check(model_contract,glod_contract,proxy_contract, xdai_address)

        nbzz_status=eth_stat.nbzz_status()
        if nbzz_status[0] and (nbzz_status[3]==overlay_address):
            tqdm.write(f"{ii_bee_path} 已经启动")
            return

        with nbzz_conract_check.check_lock:
            eth_balance = w3.eth.getBalance(xdai_address)/1e18
        if eth_balance < 0.002:
            tqdm.write(
                f"{ii_bee_path} {xdai_address} xdai不足,目前余额: {eth_balance:.4f}")
            return
        pledge_num=eth_stat.pledge_banlance()
        if pledge_num >= 15:
            tqdm.write(f"{ii_bee_path} 已经完成质押 {pledge_num}")
        else:
            tqdm.write(f"{ii_bee_path} 已经质押 {pledge_num}")
            tqdm.write(f"install bee in {ii_bee_path}")
            nbzz_balance=eth_stat.balanceOf()
            if nbzz_balance < 15-pledge_num:
                        tqdm.write(f"{ii_bee_path} 余额{nbzz_balance}小于{15-pledge_num} nbzz, 无法质押")
                        return
            else:
                tqdm.write("nbzz余额充足")
                
            try:
                with nbzz_conract_check.check_lock:
                    add_pledge(15-pledge_num, bee_passwd, str(swarm_key))
            except Exception as ex:
                tqdm.write(f"{ii_bee_path} 质押失败")
                tqdm.write(str(ex))
                return

        try:
            with nbzz_conract_check.check_lock:
                os.system( f"nbzz start -p {bee_passwd}  --bee-key-path {str(swarm_key)} --bee-statestore-path {str(state_store)}")
            tqdm.write("")
            # start_cmd(None,bee_passwd,str(swarm_key))
        except:
            tqdm.write(f"{ii_bee_path} 启动失败")
    finally:
        pbar.update(1)

# 初始化nbzz
os.system("nbzz init")

# 修改rpc
env = os.environ
if "NBZZ_RPC" in env:
    os.system( f"sed -i \"/swap_endpoint:  /c\\swap_endpoint:  {env['NBZZ_RPC']} \"  /root/.nbzz/mainnet1/config/config.yaml")
    print(f"rpc 替换为{ env['NBZZ_RPC'] }")

# 读取createbee配置
bee_con_path = Path("config.yaml")
if not bee_con_path.exists():
    print("路径错误,请移动到bee批量安装脚本的启动目录.")
    exit(1)
with bee_con_path.open("r",) as fid:
    bee_con = yaml.safe_load(fid)

bee_install_path = Path(bee_con["bee"]["base_path"])
bee_passwd = bee_con["bee"]["password"]

if not bee_install_path.exists():
    print("bee未安装或者未成功启动")
    exit(1)

# 读取合约
config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

w3=connect_w3(config["swap_endpoint"])
model_contract = get_model_contract(w3)
proxy_contract=get_proxy_contract(w3)
glod_contract=get_glod_contract(w3)
# 开始部署
all_bee_path = [i for i in bee_install_path.glob(".bee*")]
all_bee_path.sort()
all_thread = []
pbar=tqdm(total=len(all_bee_path))
for i_bee_path in all_bee_path:
    ithread = threading.Thread(target=i_thread_nbzz, args=(i_bee_path,))
    all_thread.append(ithread)
    ithread.setDaemon(True)
    ithread.start()

for ithread in all_thread:
    ithread.join()
