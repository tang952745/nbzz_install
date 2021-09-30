from pathlib import Path
import os
import subprocess
import threading
try:
    from tqdm import tqdm
except:
    try:
        os.system('pip3 install tqdm')
    except:
        print("tqdm install error ")
        exit(1)
    from tqdm import tqdm

try:
    from nbzz.util.config import load_config
    from web3 import Web3
    from typing import Dict
    from nbzz.util.default_root import DEFAULT_ROOT_PATH
    import yaml
except:
    print("nbzz未安装,此脚本需要安装nbzz 然后 . ./activate")
    exit(1)
se_lock=threading.Semaphore(10)
def i_thread_nbzz(ii_bee_path):
    swarm_key = ii_bee_path/"keys"/"swarm.key"
    if not swarm_key.exists():
        tqdm.write(f"{ii_bee_path} 目录下不存在keys文件,检查是否安装")
        return
    with se_lock:
        result=subprocess.run(f"nbzz alias show --bee-key-path {str(swarm_key)} ", stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    now_income_address=(((result.stdout.decode().strip("\n")).split(" "))[2]).strip(",")
    #tqdm.write(str(now_income_address))
    now_income_address=Web3.toChecksumAddress(now_income_address)
    if now_income_address == income_address:
        tqdm.write(f"{ii_bee_path} 已经成功设置 收益地址: {now_income_address}")
        return
    with se_lock:
        result=subprocess.run(f"nbzz alias set-address -p {bee_passwd} -a {income_address} --bee-key-path {str(swarm_key)} ", stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    
    if (result.stdout.decode().split())[-1]=="success":
        print(f"{ii_bee_path} 已经设置 收益地址: {now_income_address}")
        return
    else:
        tqdm.write(f"{ii_bee_path} 收益地址设置失败,错误如下: {result.stderr.decode()}")
    

# 修改rpc
env = os.environ

if "NBZZ_INCOME" in env:
    income_address=env["NBZZ_INCOME"]
    print(f"收益地址: {income_address}")
    income_address=Web3.toChecksumAddress(income_address)
else:
    print("未设置收益地址")
    exit(1)

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

# 开始部署
all_bee_path = [i for i in bee_install_path.glob(".bee*")]
all_bee_path.sort()
all_thread = []
for i_bee_path in all_bee_path:
    ithread = threading.Thread(target=i_thread_nbzz, args=(i_bee_path,))
    all_thread.append(ithread)
    ithread.setDaemon(True)
    ithread.start()

for ithread in tqdm(all_thread):
    ithread.join()



