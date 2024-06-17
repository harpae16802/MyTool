import subprocess

def kill_node():
    try:
        # 使用subprocess呼叫taskkill命令
        subprocess.run('taskkill /im node.exe /F', check=True, shell=True)
        print("Node.js process has been terminated successfully.")
    except subprocess.CalledProcessError:
        print("Failed to terminate Node.js process. It might not be running.")

if __name__ == '__main__':
    kill_node()
