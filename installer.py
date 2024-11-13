import os
import platform
from tqdm import tqdm
import requests
import zipfile
import shutil

os.system('cls')
print('''  __  __    ____   ____    __  __                                               
 |  \/  |  / ___| / ___|  |  \/  |   __ _   _ __     __ _    __ _    ___   _ __ 
 | |\/| | | |     \___ \  | |\/| |  / _` | | '_ \   / _` |  / _` |  / _ \ | '__|
 | |  | | | |___   ___) | | |  | | | (_| | | | | | | (_| | | (_| | |  __/ | |   
 |_|  |_|  \____| |____/  |_|  |_|  \__,_| |_| |_|  \__,_|  \__, |  \___| |_|   
                                                            |___/               
  ___                 _             _   _               
 |_ _|  _ __    ___  | |_    __ _  | | | |   ___   _ __ 
  | |  | '_ \  / __| | __|  / _` | | | | |  / _ \ | '__|
  | |  | | | | \__ \ | |_  | (_| | | | | | |  __/ | |   
 |___| |_| |_| |___/  \__|  \__,_| |_| |_|  \___| |_| 

 + MCSM 安装器 0.1 版，
 + 著佐权所有 © 2024 cygbs@BugCraft
 + https://github.com/cygbs/mcsm-installer
''')

# 程序设置
class 配置:
    URL = 'https://awwa.cc/mcsm/win'
    运行路径 = os.path.dirname(os.path.abspath(__file__))
    用户目录 = os.environ['USERPROFILE']
    文件路径 = 运行路径 + '/mcsm.zip'
    解压路径 = 运行路径 + '/mcsm'
    安装路径 = 'C:\Program Files\MCSManager'
    自启目录 = 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp'

# 确保在 Windows 上安装
if platform.system() == 'Windows':
    print('您正在使用 Windows，安装程序可以继续。')
else:
    print('您不是在 Windows 上启动安装，这个版本的安装程序不支持其它操作系统。')
    exit

# 下载函数
def 下载安装包():
    返回内容 = requests.get(url=配置.URL, stream=True)
    当前进度 = int(返回内容.headers.get("content-length", 0))
    with tqdm(total=当前进度, unit='B', unit_scale=True) as 进度条:
        with open(配置.文件路径, 'wb') as 文件:
            for 数据 in 返回内容.iter_content(1024):
                进度条.update(len(数据))
                文件.write(数据)
    if 当前进度 != 0 and 进度条.n != 当前进度:
        print('无法下载。')
    return os.path.isfile(配置.文件路径)

# 确保安装包存在
if not os.path.isfile(配置.文件路径):
    print('找不到安装包，开始下载。')
    是否下载成功 = 下载安装包()
    if 是否下载成功 == False:
        print('下载出现错误。')
        exit
    else:
        print('下载完成，可以继续。')
else:
    print('在本地找到安装包，跳过下载。')

# 调整安装文件
if os.path.exists(配置.解压路径):
    print('正在清空解压路径。')
    shutil.rmtree(配置.解压路径)
print('正在解压，稍等。')
with zipfile.ZipFile(配置.文件路径, 'r') as 压缩包:
    压缩包.extractall(配置.解压路径)
print('整理安装文件……')
shutil.rmtree(配置.解压路径 + '/__MACOSX')
os.remove(配置.解压路径 + '/Github.url')

# 安装
if os.path.exists(配置.安装路径):
    print('清理安装目录……')
    shutil.rmtree(配置.安装路径)
print('复制文件……')
os.rename(配置.解压路径, 配置.安装路径)
print('配置启动脚本……')
启动脚本 = 配置.用户目录 + '/Desktop/start-mcsm.cmd'
if os.path.isfile(启动脚本): os.remove(启动脚本)
with open(启动脚本, 'w') as 文件:
    文件.write('cd ' + 配置.安装路径)
    文件.write('\ncall start.bat')
print('配置开机自启动……')
if os.path.isfile(配置.自启目录 + '/start-mcsm.cmd'): os.remove(配置.自启目录 + '/start-mcsm.cmd')
os.rename(启动脚本, 配置.自启目录 + '/start-mcsm.cmd')
with open(启动脚本, 'w') as 文件:
    文件.write('cd ' + 配置.安装路径)
    文件.write('\ncall start.bat')
print('安装完成！')

# 清理
input('\n如果您需要自动删除安装器和安装包，\n按下回车键，否则直接关闭安装程序即可。')
if os.path.isfile(配置.用户目录 + '/Desktop/clean.cmd'): os.remove(配置.用户目录 + '/Desktop/clean.cmd')
with open(配置.用户目录 + '/Desktop/clean.cmd', 'w') as 文件:
    文件.write('ping localhost\n')
    文件.write('rmdir /s /q "' + 配置.运行路径 + '"\n')
    文件.write('del /f /s /q %~dp0clean.cmd')
os.system('start cmd /c ' + 配置.用户目录 + '/Desktop/clean.cmd')
