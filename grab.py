import socket
import threading

def grab_banner(s):
    """Retrieve the banner from the socket if available."""
    try:
        banner = s.recv(1024).decode().strip()
        return banner
    except:
        return None

def scan_port(target, port):
    """Scan a single port on the target IP."""
    s = socket.socket()
    s.settimeout(0.5)  # Set a timeout for the connection attempt
    try:
        s.connect((target, port))
        banner = grab_banner(s)
        if banner:
            print(f"Port {port} is open on {target}: {banner}")
        else:
            print(f"Port {port} is open on {target}")
    except (socket.timeout, ConnectionRefusedError):
        pass  # Ignore closed ports
    except Exception as e:
        print(f"Error scanning port {port} on {target}: {e}")
    finally:
        s.close()

def banner_grabbing_port_scan(targets, port_range):
    """Scan multiple targets and ports using threads."""
    threads = []
    for target in targets:
        for port in range(*port_range):
            t = threading.Thread(target=scan_port, args=(target, port))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()  # Wait for all threads to complete

# Example usage:
if __name__ == "__main__":
    target_ips = ['192.168.1.1', '192.168.1.2']  # Replace with your target IPs
    port_range = (1, 1024)  # Scan ports from 1 to 1024
    banner_grabbing_port_scan(target_ips, port_range)
