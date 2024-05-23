import os
import shutil
from tqdm import tqdm
directory = r"E:\GitHub\UnrealEngine-Danta1ion\Engine\Plugins"

directories = list(os.walk(directory))
print(len(directories))

for root, dirs, files in tqdm(directories, total=len(directories)):
    if root.endswith("Intermediate"):
        shutil.rmtree(root)
