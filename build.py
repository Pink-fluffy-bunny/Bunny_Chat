"""
项目打包脚本
使用PyInstaller创建可执行文件
"""

import os
import sys
import subprocess

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # 构建命令
    cmd = [
        "pyinstaller",
        "--name=AI_Chat_可可",
        "--windowed",  # 无控制台窗口
        "--add-data=assets;assets",
        "--add-data=config;config",
        "--add-data=.env;.",
        "--hidden-import=pyttsx3.drivers",
        "--hidden-import=pyttsx3.drivers.sapi5",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("构建完成！")
        print("可执行文件位于 dist/AI_Chat_可可.exe")
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")

def main():
    print("AI角色对话系统打包工具")
    print("=" * 30)
    
    # 安装PyInstaller
    install_pyinstaller()
    
    # 构建可执行文件
    build_executable()
    
    print("打包完成！")

if __name__ == "__main__":
    main()
