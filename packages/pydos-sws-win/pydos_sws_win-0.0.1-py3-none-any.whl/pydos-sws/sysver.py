import sys, platform, time, socket, psutil

# 版本信息
sysVer = "PyDOS 0.3 Fe  PyKernel 2.0 Cheetah  Build at 2021.8.14"
print(sysVer)
a = sys.version_info
print("Python Runtime Ver: {a[0]}.{a[1]}.{a[2]}".format(a=a))
print("")
print("")
print("*Official website: https://gitee.com/yizhigezi_yijiafeiji/py-dos")
print("*Feedback: https://gitee.com/yizhigezi_yijiafeiji/py-dos/issues")
print("")
print("*System info update at " + time.strftime('%Y-%m-%d', time.localtime(time.time())))
print("")

ret = {}
# 系统检测
plat_form = platform.platform()
if "Linux" in plat_form:
    ret["plat_form"] = "Linux"
elif "Windows" in plat_form:
    ret["plat_form"] = "Windows"
else:
    ret['plat_form'] = "Mac"

ret["version"] = platform.version()
ret['version_bit'] = platform.architecture()[0][0:2]

# IP检测
hostname = socket.gethostname()
IPA = socket.gethostbyname(hostname)

# CPU信息
cpu_percent = psutil.cpu_percent(interval=1)
cpu_info = "CPU Use：%i%%" % cpu_percent

# 内存检测
phymem = psutil.virtual_memory()
line = "Memory: %5s%% %6s/%s" % (
    phymem.percent,
    str(int(phymem.used / 1024 / 1024)) + "M",
    str(int(phymem.total / 1024 / 1024)) + "M"
)

print("Platform OS:{ret[plat_form]}".format(ret=ret))
print("Platform OS Version: {ret}".format(ret=ret['version'].split(" ")[0]))
print("{ret[version_bit]}Bit OS".format(ret=ret))

print("Host Name: " + hostname)
print("IP Address: " + IPA)

print("CPU Core:" + str(psutil.cpu_count()))

print(cpu_info)

print(line)

print("本项目基于MTI开源协议")
