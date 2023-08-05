import os

repo = " -i https://pypi.tuna.tsinghua.edu.cn/simple"
pkglist = ["requests", "pygame", "pillow", "pymediainfo", "pycryptodome", "psutil"]
print("开始安装依赖包")
try:
    for i in pkglist:
        os.system("pip install " + i + " -i https://pypi.tuna.tsinghua.edu.cn/simple")
    print("安装完成")
except:
    print("安装失败")

os.system("pause")