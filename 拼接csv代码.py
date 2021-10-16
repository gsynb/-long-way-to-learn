import pandas as pd
import os
import xlrd
import xlwt
Folder_Path = r'C:\Users\GaoShiyan\Desktop\allindex'
SaveFile_Path = r'C:\Users\GaoShiyan\Desktop\allindex'
SaveFile_Name = r'allin.xls'


os.chdir(Folder_Path)

file_list = os.listdir()

df = pd.read_excel(Folder_Path + '\\' + file_list[0])

# 将读取的第一个CSV文件写入合并后的文件保存
df.to_excel(SaveFile_Path + '\\' + SaveFile_Name, encoding="utf_8_sig", index=False)

for i in range(1, len(file_list)):
    df = pd.read_excel(Folder_Path + '\\' + file_list[i])
    df.to_excel(SaveFile_Path + '\\' + SaveFile_Name, encoding="utf_8_sig", index=False, header=False, mode='a+')