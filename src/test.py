# -*- coding: utf-8 -*-
import os
import sys
from tqdm import tqdm

# 指定要统计的目录，可以修改为你想要的目录，或者使用sys.argv[1]来接收命令行参数
directory = r"E:\GitHub\UnrealEngine-Danta1ion\Engine\Config"

output_log = r"output4.log"

with open(output_log, mode="w", encoding="utf-8") as f:
    f.write("")

file_count = 0
line_count = 0

def logFile(msg: str):
    with open(output_log, mode="a", encoding="utf-8") as f:
        f.write(msg + "\n")

# 遍历目录及其子目录下的所有文件
directories = list(os.walk(directory))
for root, dirs, files in tqdm(directories, total=len(directories)):
    if "Binaries" in root or "Intermediate" in root:
        continue

    for file in files:
        # 拼接文件的完整路径
        file_path = os.path.join(root, file)
        # 打开文件并读取行数
        with open(file_path, encoding="utf-8") as f:
            try:
                lines = len(f.readlines())
            except UnicodeDecodeError:
                logFile(f"{file_path} is binary, skipped.")
                lines = -1
            else:
                logFile(f"{file}: {lines}")
                line_count += lines
                file_count += 1

# 打印结果
print(f"在目录{directory}及其子目录下，共有{file_count}个文件，总共{line_count}行代码。")
print(f"logged in {output_log}")
