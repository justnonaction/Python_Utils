import threading
import socket
import re
import os
import ipaddress
import subprocess

def ports_handle(ports):
    # ports handle
    pattern_ports = re.compile(r"\d+[-~]\d+")
    if pattern_ports.match(ports):
        ports = ports.split("-") if "-" in ports else ports.split("~")
    if ports == "common":
        ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389, 8080]
    return ports



def ips_handle(ips):
    # ips handle
    pattern_ip = re.compile(r"^(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$")
    pattern_ips = re.compile(
        r"^(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)/([0-9]|[1-2]\d|3[0-2])$")
    res = []
    if pattern_ip.match(ips):
        ip_list = [ips]
        return ip_list
    elif pattern_ips.match(ips):
        ip_list = generate_ips(ips)
        return ip_list
    else:
        print("❌ 请检查输入，重新输入正确的 IP 地址！")
        return None


def generate_ips(ips):
    ip_list = []
    try:
        ips = ipaddress.ip_network(ips, strict=False)
        for ip in ips.hosts():
            ip_list.append(ip)
    except:
        print("❌ 生成地址列表失败，请检查输入地址！")
        return None
    return ip_list



def ip_scan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        if result == 0:
            print(f"✅ {ip}:{port} 端口开放\n")
        else:
            print(f"❌ {ip}:{port} 端口关闭\n")
    except Exception as e:
        print(f"❌ {ip}:{port} 端口扫描失败！\n")


def ip_ping(ip, res):
    if os.name == "nt":  # Windows
        command = ["ping", "-n", "1", "-w", "1000", str(ip)]
    else:  # Linux/Unix
        command = ["ping", "-c", "1", "-W", "1", str(ip)]

    try:
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = process.stdout.lower()

        if os.name == "nt":
            # Windows: 检查"TTL="是否在输出中
            is_alive = "ttl=" in output
        else:
            # Linux: 检查" 0% packet loss"是否在输出中
            is_alive = " 0% packet loss" in output
        if is_alive:
            res.append(str(ip))
        # else:
        #     print(f"❌ {ip} 不可达\n")
    except Exception as e:
        print(f"❌ {ip} ping失败: {str(e)}\n")



def multi_threading(ips, ports, module):
    ## 端口扫描
    if module == "1":
        Threads = []
        for port in ports:
            t = threading.Thread(target=ip_scan, args=(str(ips), port))
            t.start()
            Threads.append(t)
        for t in Threads:
            t.join()
    ### ping
    if module == "2":
        Threads_ping = []
        res = []
        for ip in ips:
            t_p = threading.Thread(target=ip_ping, args=(ip,res))
            t_p.start()
            Threads_ping.append(t_p)
        for t_p in Threads_ping:
            t_p.join()
        ##排序
        for ip in sorted(res, key=lambda ip: ipaddress.ip_address(ip)):
            print(f"✅ {ip} 存活！")

def main():
    res = [] #获取返回存活ip进行后续数据处理
    module = input("请输入扫描模式（1: 端口扫描，2: ping）：")
    ips = input("请输入 IP 地址或地址段：")
    if module == "2":
        ips = ips_handle(ips)
        if ips:
            multi_threading(ips, None, module)

    if module == "1":
        ports = input("请输入端口号（支持范围和常用端口）：")
        ports = ports_handle(ports)
        if ips and ports:
            multi_threading(ips, ports, module)

if __name__ == "__main__":
    # 工程版，未优化完全。
    main()