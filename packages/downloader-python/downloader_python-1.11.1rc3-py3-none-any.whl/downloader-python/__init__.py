import sys
import os
import time
print(f"Can't import,you can found this path:'{sys.executable[:-10]}Lib\\site-pakages\\downloader-python\\main.py',and then,use python to run it.")
print(os.system(f'{sys.executable} {sys.executable[:-10]}Lib\\site-pakages\\downloader-python\\main.py'))
ac = time.time()
ac = time.struct_time(ac)
nye = int(time.strftime('%Y',ac))
