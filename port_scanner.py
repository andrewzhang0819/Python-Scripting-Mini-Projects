# Port Scanner: 
# - Multi-threading
# - Be able to scan a range of ports
# - Have version detection

import socket
import argparse
import re
import sys
import concurrent.futures

def parse_arguments():
    # initalize the parser
    parser = argparse.ArgumentParser(description="Port Scanner")
    # Required IP address to target
    parser.add_argument("target", help="The IP address or hostname you want to scan")
    # Optional port range
    parser.add_argument("-p", "--ports", default="1-1024", 
                        help="Specify a port range (e.g., '1-100' or 'all'). Default is 1-1024.")
    # Optional flags
    parser.add_argument("-sV", "--version", action="store_true", 
                        help="Enable version/service detection on open ports")

    return parser.parse_args()

def valid_ip(ip_address):
    # xxx.xxx.xxx.xxx
    is_valid_chars = bool(re.match(r"^[0-9.]+$", ip_address))
    if not is_valid_chars:
        return False
    parts = ip_address.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        if not 0 <= int(part) <= 255:
            return False
    return True

def check_ip_range(port_string):
    is_valid_range = bool(re.match(r"^\d+-\d+$", port_string))
    if not is_valid_range:
        return (0,0)
    parts = port_string.split("-")
    if len(parts) != 2:
        return (0,0)
    
    if 1 <= int(parts[0]) <= 65535 and 1 <= int(parts[1]) <= 65535:
        if int(parts[0]) <= int(parts[1]):
            return (int(parts[0]), int(parts[1]))
            
    return (0,0)

def scan_port(port, ip_address, version):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((ip_address, port))
        if version:
            try:
                banner_bytes = sock.recv(1024)
                banner = banner_bytes.decode('utf-8', errors='ignore').strip()
                if banner:
                    print(f"[+] Port {port} is open | Banner: {banner}")
                else:
                    print(f"[+] Port {port} is open | Banner: No banner received")
            except:
                print(f"[+] Port {port} is open | Banner: Timed out")
        else:
            print(f"[+] Port {port} is open")
        sock.close()
    except:
        pass

def main():
    args = parse_arguments()
    start = 1
    end = 1024
    if not valid_ip(args.target):
        sys.exit("Please enter a valid ip")
        
    if args.target:
        port_range = check_ip_range(args.ports)
        if port_range == (0,0):
            sys.exit("Please enter a valid port range")
        else:
            start = port_range[0]
            end = port_range[1]
    
    # You can adjust this number. 100-500 is usually a safe sweet spot for port scanning.
    max_threads = 100 
    
    print(f"[*] Starting scan on {args.target} with {max_threads} active threads...")

    # The 'with' statement automatically handles cleanup and waiting (joining)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for port in range(start, end + 1):
            # We "submit" the function and its arguments to the pool
            executor.submit(scan_port, port, args.target, args.version)
            
    print("[*] Scan complete.")

if __name__ == "__main__":
    main()