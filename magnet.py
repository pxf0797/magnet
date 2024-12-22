#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil
import sys

def check_aria2c_installed():
    """Check if aria2c is installed on the system."""
    return shutil.which('aria2c') is not None

def print_install_instructions():
    """Print instructions for installing aria2c."""
    if sys.platform == 'darwin':  # macOS
        print("aria2c 未安装。请使用以下命令安装：")
        print("brew install aria2")
    elif sys.platform.startswith('linux'):
        print("aria2c 未安装。请使用以下命令安装：")
        print("Ubuntu/Debian: sudo apt-get install aria2")
        print("CentOS/RHEL: sudo yum install aria2")
    elif sys.platform == 'win32':
        print("aria2c 未安装。请访问 https://aria2.github.io/ 下载安装")
    else:
        print("请先安装 aria2c。访问 https://aria2.github.io/ 了解详情")

def main():
    # 检查 aria2c 是否已安装
    if not check_aria2c_installed():
        print_install_instructions()
        return

    # 提示用户输入磁力链接
    magnet_link = input("请输入磁力链接（magnet:?xt=urn:btih:...）: ").strip()
    
    # 如果用户未输入，直接退出
    if not magnet_link:
        print("未输入磁力链接，退出。")
        return
    
    # 验证磁力链接格式
    if not magnet_link.startswith('magnet:?'):
        print("错误：无效的磁力链接格式。磁力链接应以 'magnet:?' 开头。")
        return

    # 默认下载目录（使用绝对路径）
    download_dir = os.path.abspath("./download")
    
    # 如果当前目录下没有 download 文件夹，则自动创建
    if not os.path.exists(download_dir):
        try:
            os.makedirs(download_dir, exist_ok=True)
            print(f"创建下载目录：{download_dir}")
        except OSError as e:
            print(f"创建下载目录失败: {e}")
            return
    
    # 组装 aria2c 的命令参数
    aria2c_command = [
        "aria2c",
        magnet_link,
        f"--dir={download_dir}",
        "--seed-time=0",
        "--continue=true",
        "--max-concurrent-downloads=5",
        "--max-connection-per-server=5",
        "--split=10"  # 单文件最大连接数
    ]
    
    print("开始下载...")
    print(f"下载目录: {download_dir}")
    
    try:
        # 调用 aria2c 命令下载
        process = subprocess.run(
            aria2c_command,
            check=True,
            text=True,
            stderr=subprocess.PIPE
        )
        print("下载完成！")
    except subprocess.CalledProcessError as e:
        print(f"下载过程中出现错误: {e}")
        if e.stderr:
            print(f"错误详情: {e.stderr}")
    except KeyboardInterrupt:
        print("\n下载已取消。")
    except Exception as e:
        print(f"发生未知错误: {e}")
    
    print(f"\n文件保存在: {download_dir}")

if __name__ == "__main__":
    main()
