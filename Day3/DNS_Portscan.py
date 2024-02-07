import socket

def scan_port(target_host, port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 연결 시도
        sock.connect((target_host, port))
        # 소켓 닫기
        sock.close()
        return True
    except Exception as e:
        return False

def grab_banner(target_host, port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 연결 시도
        sock.connect((target_host, port))
        # 소켓에서 데이터 읽기 (배너 정보)
        banner = sock.recv(1024).decode('utf-8')
        # 소켓 닫기
        sock.close()
        return banner.strip()  # 공백 제거 후 반환
    except Exception as e:
        return None

def port_scanner(target_host, ports):
    for port in ports:
        if scan_port(target_host, port):
            banner = grab_banner(target_host, port)
            if banner:
                print(f"Port {port} is open: {banner}")
            else:
                print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")

if __name__ == "__main__":
    target_host = "192.168.0.48"  # 스캔할 호스트 IP 주소
    ports_to_scan = [53]  # 스캔할 포트 목록

    port_scanner(target_host, ports_to_scan)
