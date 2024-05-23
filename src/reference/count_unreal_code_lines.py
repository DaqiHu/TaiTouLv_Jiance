# -*- coding: utf-8 -*-
import os
import sys
from tqdm import tqdm
# from numba import njit

def logFile(file, msg: str):
    with open(file, mode="a", encoding="utf-8") as f:
        f.write(msg + "\n")

# @njit
def count(directory: str, log_file_name: str) -> tuple[int, int]:
    file_count = 0
    line_count = 0

    

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
                    logFile(log_file_name, f"{file_path} is binary, skipped.")
                    lines = -1
                else:
                    logFile(log_file_name, f"{file}: {lines}")
                    line_count += lines
                    file_count += 1
    
    return file_count, line_count

def main():
    # 指定要统计的目录，可以修改为你想要的目录，或者使用sys.argv[1]来接收命令行参数
    directories = [
        r"E:\GitHub\UnrealEngine\Engine\Source\Developer",
        r"E:\GitHub\UnrealEngine\Engine\Source\Editor",
        r"E:\GitHub\UnrealEngine\Engine\Source\Programs",
        r"E:\GitHub\UnrealEngine\Engine\Source\Runtime",
        r"E:\GitHub\UnrealEngine\Engine\Config",
        r"E:\GitHub\UnrealEngine\Engine\Plugins",
    ]

    file_name = r"output4.log"

    with open(file_name, mode="w", encoding="utf-8") as f:
        f.write("")

    results = [count(directory, file_name) for directory in directories]
    
    file_total = 0
    line_total = 0
    
    for index, directory in enumerate(directories):
        file_count, line_count = results[index]
        # 打印结果
        print(f"在目录{directory}及其子目录下，共有{file_count}个文件，总共{line_count}行代码。")
        print(f"logged in {file_name}")
        
        file_total += file_count
        line_total += line_count
    
    print("============================================================================================")
    print(f"共计{file_total}个文件，{line_total}行代码。")

if __name__ == "__main__":
    main()