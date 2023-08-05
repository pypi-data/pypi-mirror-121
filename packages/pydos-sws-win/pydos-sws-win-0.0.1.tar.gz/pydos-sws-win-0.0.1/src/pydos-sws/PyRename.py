import os

print("PyRename  0.0.1 by 一架飞稽")
path = input("请输入文件所在路径:")
srcName = input("请输入需要重命名目标文件或文件夹：")
dstName = input("请输入重命名后目标文件或文件夹：")

srcName = path + "/" + srcName
dstName = path + "/" + dstName

os.rename(srcName , dstName)