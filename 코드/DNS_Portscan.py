import socket

def DNS_scan(host, port):
    try:
        # UDP 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)  # 타임아웃 설정

        # DNS 서버에 데이터 전송
        sock.sendto(b'', (host, port))

        # 데이터 수신 시 포트가 열려 있다고 가정
        # UDP 스캔은 응답이 없어도 포트가 열려 있다고 가정합니다.
        return True
    except Exception as e:
        return False
    finally:
        sock.close()

def port_scanner(host, port):
    if DNS_scan(host, port):
        print(f"Port {port} is open for DNS")
    else:
        print(f"Port {port} is closed for DNS")

if __name__ == "__main__":
    host = "192.168.0.48"  # 스캔할 호스트 IP 주소
    port_to_scan = 53  # 스캔할 포트 번호

    port_scanner(host, port_to_scan)
