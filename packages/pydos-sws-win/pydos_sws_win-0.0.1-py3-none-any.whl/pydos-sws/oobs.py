import json
import os

title = "py-dos 初次配置"


def configFile(mode, connect):
    with open("settings.json", mode) as f:
        if mode == "r":
            data = json.load(f)
            return data
        elif mode == "w":
            json.dump(connect, f)


def license():
    print(title)
    print("请先阅读许可协议(MIT License)")
    os.open("../LICENSE")
    setPython()


def setPython():
    print(title)
    print("请选择py-dos的Python解释器路径：")
    items = {
        "1": "系统路径",
        "2": "内置Python(单独提供的venv,稍后需要联机下载扩展库)"
    }
    for i in items.keys():
        print(i + ":" + items[i])

    cho = input("setPython >")
    if cho == "1":
        data = configFile("r", "")
        data["Python"] = "python.exe"
        configFile("w", data)
    if cho == "2":
        data_1 = configFile("r", "")
        data_1["Python"] = "./venv/Scripts/pytho.exe"
