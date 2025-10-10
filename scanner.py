import nmap

# Point directly to your nmap executable (use raw string or double backslashes)
NMAP_EXE = r"C:\Program Files (x86)\Nmap\nmap.exe"

# Create PortScanner with explicit path
nm = nmap.PortScanner(nmap_search_path=[NMAP_EXE])

def discover_devices(network="192.168.1.0/24", fast_ping=True):
    args = "-sn" if fast_ping else ""
    nm.scan(hosts=network, arguments=args)

    devices = []
    for host in nm.all_hosts():
        if nm[host].state() != "up":
            continue
        info = {"ip": host}
        addrs = nm[host].get("addresses", {})
        if "mac" in addrs:
            info["mac"] = addrs["mac"]
        try:
            hostname = nm[host].hostname()
            if hostname:
                info["name"] = hostname
        except:
            info["name"] = ""
        devices.append(info)
    return devices

if __name__ == "__main__":
    print(discover_devices("192.168.1.0/24"))
