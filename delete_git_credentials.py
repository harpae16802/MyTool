import subprocess

def delete_git_credentials():
    try:
        # 找到Git凭证
        find_git_credentials_cmd = 'cmdkey /list | findstr /C:"git"'
        credentials_output = subprocess.check_output(find_git_credentials_cmd, shell=True, text=True)
        
        # 提取凭证目标名称
        credentials_list = credentials_output.strip().split('\n')
        for cred in credentials_list:
            if 'Target:' in cred:
                target_name = cred.split(':', 1)[1].strip()
                # 删除凭证
                delete_cmd = f'cmdkey /delete:{target_name}'
                subprocess.run(delete_cmd, shell=True, check=True)
        print("Git credentials deleted successfully.")
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    delete_git_credentials()
