#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil
import sys
import time

def check_aria2c_installed():
    """
    检查 aria2c 是否已安装。
    如果能在 PATH 中找到 aria2c 的可执行文件则返回 True，否则返回 False。
    """
    return shutil.which('aria2c') is not None

def print_install_instructions():
    """
    当检测到 aria2c 未安装时，根据系统平台给出安装指导。
    """
    if sys.platform == 'darwin':  # macOS
        print("aria2c 未安装。请使用以下命令安装或升级：")
        print("  brew install aria2        # 如果未安装")
        print("  brew upgrade aria2        # 如果已安装旧版，进行升级")
    elif sys.platform.startswith('linux'):
        print("aria2c 未安装。请使用以下命令安装：")
        print("  Ubuntu/Debian: sudo apt-get install aria2")
        print("  CentOS/RHEL:   sudo yum install aria2")
    elif sys.platform == 'win32':
        print("aria2c 未安装。请访问以下链接下载安装：\n  https://aria2.github.io/")
    else:
        print("请先安装 aria2c。访问 https://aria2.github.io/ 了解详情")

def main():
    # 1. 检查 aria2c 是否安装
    if not check_aria2c_installed():
        print_install_instructions()
        return

    # 2. 提示用户输入磁力链接
    magnet_link = input("请输入磁力链接（magnet:?xt=urn:btih:...）: ").strip()
    
    if not magnet_link:
        print("未输入磁力链接，退出。")
        return
    
    # 验证磁力链接格式
    if not magnet_link.startswith('magnet:?'):
        print("错误：无效的磁力链接格式。磁力链接应以 'magnet:?' 开头。")
        return

    # 3. 设置默认下载目录
    download_dir = os.path.abspath("./download")
    if not os.path.exists(download_dir):
        try:
            os.makedirs(download_dir, exist_ok=True)
            print(f"创建下载目录：{download_dir}")
        except OSError as e:
            print(f"创建下载目录失败: {e}")
            return

    # 4. 组装 aria2c 的命令参数
    #    注意：已删除 --bt-enable-pex=true，以避免旧版本 aria2c 不识别该选项
    #   下面这些参数可以根据自身需求修改：
    #   --seed-time=0                 下载完成后不继续做种
    #   --continue=true               启用断点续传，若已有部分文件则不会重复下载
    #   --enable-dht/--enable-dht6    启用 DHT/IPv6 DHT，提高找节点能力
    #   --bt-enable-lpd               启用本地节点发现
    #   --bt-enable-pex               启用节点交换功能
    #   --max-connection-per-server   设置每个服务器连接数上限
    #   --max-concurrent-downloads    最大并行任务数
    #   --split                       将单个文件分割成多少个片段以并发下载
    #   --bt-max-open-files           同时允许打开的文件数上限
    aria2c_command_base = [
        "aria2c",
        magnet_link,
        f"--dir={download_dir}",       # 下载保存目录
        "--seed-time=0",
        "--continue=true",             # 断点续传
        "--enable-dht=true",
        "--enable-dht6=true",
        "--bt-enable-lpd=true",
        "--bt-max-open-files=100",
        "--max-concurrent-downloads=5",
        "--max-connection-per-server=5",
        "--split=10",
    ]

    # 添加更多公共 Tracker，提高连接数
    extra_trackers = [
        "udp://tracker.openbittorrent.com:80",
        "udp://open.demonii.com:1337",
        "udp://tracker.opentrackr.org:1337/announce",
        # 可在此处继续添加其它公共 Tracker
    ]
    if extra_trackers:
        trackers_str = ",".join(extra_trackers)
        aria2c_command_base.append(f"--bt-tracker={trackers_str}")

    print("开始下载...")
    print(f"下载目录: {download_dir}")
    
    # 5. 重试机制
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            # 调用 aria2c 命令下载
            process = subprocess.run(
                aria2c_command_base,
                check=True,
                text=True,
                stderr=subprocess.PIPE
            )
            # 如果执行到这里，说明下载成功，无异常抛出
            print("下载完成！")
            break

        except subprocess.CalledProcessError as e:
            # 当 aria2c 的退出码非 0 时，会抛出此异常
            print(f"下载过程中出现错误 (第 {attempt} 次重试): {e}")
            if e.stderr:
                print(f"错误详情: {e.stderr}")
            
            if attempt < max_retries:
                # 等待一段时间后重试，可根据需要调整等待时长
                wait_time = 3
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print("已到达最大重试次数，下载失败。")
        except KeyboardInterrupt:
            # 用户按下 Ctrl+C 等中断操作
            print("\n下载已取消。")
            break
        except Exception as e:
            # 处理除 CalledProcessError、KeyboardInterrupt 以外的其它意外错误
            print(f"发生未知错误: {e}")
            break

    print(f"\n文件保存在: {download_dir}")

if __name__ == "__main__":
    main()
