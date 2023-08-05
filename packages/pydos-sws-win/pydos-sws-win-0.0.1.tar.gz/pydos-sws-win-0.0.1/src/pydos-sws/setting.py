import json

print("pydos 设置 0.1")

with open("settings.json", "r") as r:
    settings = json.load(r)
setss = str(settings.keys())
print("进行各项设置:\n" + setss.replace("dict_keys", "").replace("(", "").replace(")", "").replace("[", "").replace("]",
                                                                                                              "").replace(
    "'", ""))
command = input("setting>")
print(settings[command])
set = input("需要修改为:")
yn = input("是否应用？ (Y/n)")
if yn == "Y":
    settings[command] = set
    with open("settings.json", "w") as w:
        json.dump(settings, w)
else:
    pass
