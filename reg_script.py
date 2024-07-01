import os
import subprocess

# 定義要執行的命令
command = r'reg add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve'

try:
    # 使用 subprocess.run 執行命令
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("命令執行成功")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("命令執行失敗")
    print(e.stderr)

# 確保程式在執行後自動關閉
os._exit(0)
