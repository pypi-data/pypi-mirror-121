###已停用###
import os
import requests
import json

print("PPkg Package Manager 3.0")

# head获取
with open("settings.json", "r") as s:
    sets = json.load(s)
    head = sets["User Agent"]

headers = {
    'User-Agent': head
}


def file_name(file_dir):
    global files
    for root, dirs, files in os.walk(file_dir):
        # 当前路径下所有非目录子文件
        print(files)
    return files


def install():
    with open("pkglist.txt", "r") as f:
        data = f.read().splitlines()
    choi = input("install>")
    num = data.index(choi)
    choName = data[num]
    url1 = "https://gitee.com/yizhigezi_yijiafeiji/pydos/attach_files/828696/download/" + choName
    myFile = requests.get(url1, headers=headers)
    open(choName + ".py", 'wb').write(myFile.content)


def remove():
    cmr = input("remove>")
    upkg = cmr + ".py"
    confirm = input("确认删除？(Y/n)")
    if confirm == "Y":
        ccm = "del " + upkg
        os.system(ccm)
    elif confirm == "n":
        pass


def updatesys():
    url = "https://pydos-1301360149.cos.ap-nanjing.myqcloud.com/update.exe"
    myFile = requests.get(url, headers=headers)
    open("./update.exe", 'wb').write(myFile.content)
    os.system("update.exe")


def reset():
    url = "https://pydos-1301360149.cos.ap-nanjing.myqcloud.com//settings.json"
    res = requests.get(url, headers=headers)
    open("settings.json", "wb").write(res.content)
    print("done")


print("install:安装包\nremove:删除包\nupdatesys:更新软件\nreset:恢复原始设置（下载settings.json）")
cm = input("请选择操作:")

if cm == "install":
    install()
elif cm == "remove":
    remove()
elif cm == "updatesys":
    updatesys()
elif cm == "reset":
    r = input("确认恢复原始设置？(Y/n)")
    if r == "Y":
        reset()
    else:
        pass
