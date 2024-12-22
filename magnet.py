#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import libtorrent as lt

def download_magnet(magnet_link: str, download_path: str = "./download") -> None:
    """
    使用 libtorrent 下载磁力链接

    :param magnet_link:  磁力链接，如 "magnet:?xt=urn:btih:xxxxx"
    :param download_path: 文件保存路径，默认当前目录下的 "download" 文件夹
    """
    # 创建会话（session）
    session = lt.session()
    
    # 设置会话的监听端口
    session.listen_on(6881, 6891)
    
    # 添加种子
    params = {
        "save_path": download_path,
        "storage_mode": lt.storage_mode_t.storage_mode_sparse,
        # 磁力链接会产生一个临时的 torrent_handle 对象
        "paused": False,
        "auto_managed": True,
        "duplicate_is_error": True
    }
    
    # 添加磁力链接到会话
    handle = lt.add_magnet_uri(session, magnet_link, params)
    
    # 等待 metadata（种子信息）下载完成
    print("正在获取元数据 (metadata)，请稍候...")
    while not handle.has_metadata():
        status = handle.status()
        print(f"  已下载大小: {status.total_done} 字节", end="\r")
        time.sleep(1)
    
    print("\n元数据获取完成，开始下载...")
    
    # 开始下载
    while True:
        status = handle.status()
        
        # 下载完成后退出循环
        if status.state == lt.torrent_status.seeding:
            print("\n下载完成！")
            break
        
        # 显示下载进度、速度等信息
        s = (
            f"\r进度: {status.progress * 100:.2f}% "
            f"下载速度: {status.download_rate / 1000:.1f} kB/s "
            f"上传速度: {status.upload_rate / 1000:.1f} kB/s "
            f"已下载: {status.total_done / 1024:.1f} KB "
            f"连接数: {status.num_peers}"
        )
        
        print(s, end="")
        sys.stdout.flush()
        
        time.sleep(1)

def main():
    # 如果通过命令行传入： python download_magnet.py <magnet_link> <download_path>
    if len(sys.argv) < 2:
        print("用法: python download_magnet.py <magnet_link> [download_path]")
        sys.exit(1)

    magnet_link = sys.argv[1]
    
    if len(sys.argv) > 2:
        download_path = sys.argv[2]
    else:
        download_path = "./download"  # 默认下载到当前目录的 ./download 文件夹
    
    download_magnet(magnet_link, download_path)

if __name__ == "__main__":
    main()
