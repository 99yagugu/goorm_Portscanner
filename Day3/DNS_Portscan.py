import socket

def UDP_scan(target_host, port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)  # 타임아웃 설정

        # UDP 패킷 전송
        sock.sendto(b'', (target_host, port))

        # 결과 확인
        data, addr = sock.recvfrom(1024)
        return True  # 포트가 열려있음
    except Exception as e:
        return False  # 포트가 닫혀있음
    finally:
        sock.close()

def TCP_scan(target_host, port):
    service_name = "DNS"
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 타임아웃 설정

        # DNS 서버에 연결
        sock.connect((target_host, port))
        banner = sock.recv(1024).decode('utf-8')  # 배너 정보 읽기
        sock.close()  # 연결 종료

        # 응답 확인
        if banner:
            return (True, service_name, banner.strip())
        else:
            return (False, service_name, banner.strip())
    except Exception as e:
        return (False, service_name, None)  # 포트가 닫혀있음 또는 예외 발생 시 False 반환

def port_scanner(target_host, ports_to_scan):
    for port in ports_to_scan:
        # UDP 스캔 수행
        udp_result = UDP_scan(target_host, port)

        # TCP 스캔 수행
        tcp_result, service_name, banner = TCP_scan(target_host, port)

        if udp_result is True:
            print(f"Port {port} is open for {service_name} (UDP)")
        elif udp_result is False:
            print(f"Port {port} is closed for {service_name} (UDP)")

        if tcp_result is True:
            print(f"Port {port} is open for {service_name} (TCP) - Banner: {banner}")
        elif tcp_result is False:
            print(f"Port {port} is closed for {service_name} (TCP) - Banner: {banner}")
        else:
            print(f"Port {port} status for {service_name} is unknown")

if __name__ == "__main__":
    target_host = "127.0.0.1"  # 스캔할 호스트 IP 주소
    ports_to_scan = [53]  # 스캔할 포트 목록 (포트 53으로 설정)

    port_scanner(target_host, ports_to_scan)
