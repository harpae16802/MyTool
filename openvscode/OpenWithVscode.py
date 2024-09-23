import os
import winreg as reg
import subprocess
import sys
import ctypes

# 定义消息框函数，弹出不同类型的消息框
def show_message_box(title, message, style):
    ctypes.windll.user32.MessageBoxW(0, message, title, style)

def find_vscode_path():
    # 定义可能的 VSCode 安装路径
    possible_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft VS Code\Code.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft VS Code\Code.exe")
    ]

    # 检查路径是否存在
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def add_vscode_to_context_menu(vscode_path):
    try:
        # 打开/创建注册表项 HKEY_CLASSES_ROOT\Directory\Background\shell\Open with VSCode
        key_path = r"Directory\\Background\\shell\\Open with VSCode"
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path) as key:
            # 设置菜单显示名称
            reg.SetValue(key, '', reg.REG_SZ, "Open with VSCode")
        
        # 打开/创建子项 HKEY_CLASSES_ROOT\Directory\Background\shell\Open with VSCode\command
        command_key_path = key_path + r"\\command"
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_key_path) as command_key:
            # 设置 command 的默认值为 vscode 的启动命令
            command = f'"{vscode_path}" "%V"'
            reg.SetValue(command_key, '', reg.REG_SZ, command)
        
        show_message_box("成功", f"已成功將 VSCode 新增至滑鼠右側選單，路徑為：{vscode_path}", 64)  # 信息图标
        print(f"已成功將 VSCode 新增至滑鼠右側選單，路徑為：{vscode_path}")
    
    except Exception as e:
        show_message_box("錯誤", f"寫入註冊表錯誤: {e}", 16)  # 错误图标
        print(f"寫入註冊表時出錯: {e}")

def main():
    # 弹出提示框，告知用户正在查找 VSCode 路径
    show_message_box("提示", "正在尋找 VSCode 安裝路徑...", 64)  # 信息图标

    # 找到 VSCode 的路径
    vscode_path = find_vscode_path()

    if vscode_path:
        show_message_box("成功", f"找到 VSCode 安装路徑：{vscode_path}", 64)  # 信息图标
        print(f"找到 VSCode 安装路徑：{vscode_path}")
        # 将 VSCode 添加到右键菜单
        add_vscode_to_context_menu(vscode_path)
    else:
        show_message_box("錯誤", "無法找到 VSCode 請確認已經安裝。", 16)  # 错误图标
        print("無法找到 VSCode 請確認已經安裝。")

if __name__ == "__main__":
    # 确保以管理员权限运行
    if not os.name == 'nt':
        sys.exit("該程式只能在 Windows 系统上使用。")
    
    try:
        # 使用管理员权限运行脚本
        if ctypes.windll.shell32.IsUserAnAdmin():
            main()
        else:
            show_message_box("提示", "需要以系統管理員權限使用此程式", 48)  # 警告图标
            print("需要以系統管理員權限使用此程式")
            # 重新以管理员权限运行
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    except Exception as e:
        show_message_box("錯誤", f"執行出錯: {e}", 16)  # 错误图标
        print(f"執行出錯: {e}")
