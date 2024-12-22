#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

def main():
    # 提示用户输入磁力链接
    magnet_link = input("请输入磁力链接（magnet:?xt=urn:btih:...）: ").strip()
    
    # 如果用户未输入，直接退出
    if not magnet_link:
        print("未输入磁力链接，退出。")
        return
    
    # 默认下载目录
    download_dir = "./download"
    
    # 如果当前目录下没有 download 文件夹，则自动创建
    if not os.path.exists(download_dir):
        os.makedirs(download_dir, exist_ok=True)
    
    # 组装 aria2c 的命令参数
    # --dir 指定下载目录
    # --seed-time=0 下载完成后不继续做种（可按需调整）
    # --continue=true 如果同名文件存在则断点续传
    aria2c_command = [
        "aria2c",
        magnet_link,
        "--dir=" + download_dir,
        "--seed-time=0",
        "--continue=true"
    ]
    
    try:
        # 调用 aria2c 命令下载
        subprocess.run(aria2c_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"下载过程中出现错误: {e}")
    
    print("下载任务结束。")

if __name__ == "__main__":
    main()
