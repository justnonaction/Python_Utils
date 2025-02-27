# 编写一个简单的端口扫描器，接受一个IP地址和一个端口范围作为输入，扫描该IP是否开放指定的端口。
import requests
import socket
import re


def ports_handle(ports):
    if re.match(r"\d{1,5}[-~]\d{1,5}", ports):
        ports = ports.split("-") if "-" in ports else ports.split("~")
        ports = range(int(ports[0]), int(ports[1])+1)
        return ports
    elif re.match(r"\d{1,5}", ports):
        return [int(ports)]


def port_scan(ip, ports):
    print(f"正在扫描{ip}存活端口，请稍后...")
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
                s.settimeout(0.4)
                result = s.connect_ex((ip, port))
                if result == 0:
                    print(f"端口{port}可用")
        except socket.error as e:
            print(f"连接错误：{e}")
            continue
    print("扫描结束")

def main():
    ip = input("请输入IP地址：")
    ports = input("请输入端口范围：")
    ports = ports_handle(ports)
    port_scan(ip, ports)
    return

if __name__ == "__main__":
    main()
