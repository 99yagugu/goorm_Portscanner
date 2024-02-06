import socket

def SYN_scan(target_host, port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 타임아웃 설정

        # SYN 패킷 전송
        result = sock.connect_ex((target_host, port))

        # 결과 확인
        if result == 0:
            return True  # 포트가 열려있음
        else:
            return False  # 포트가 닫혀있음
    except Exception as e:
        return None  # 예외 발생 시 None 반환
    finally:
        sock.close()

def SMTP_scan(target_host, port):
    service_name = "SMTP"
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 타임아웃 설정

        # SMTP 서버에 연결
        sock.connect((target_host, port))
        banner = sock.recv(1024).decode('utf-8')  # 배너 정보 읽기
        sock.sendall(b"QUIT\r\n")  # QUIT 명령 전송
        sock.close()  # 연결 종료

        # 응답 확인
        if banner.startswith("220"):
            return (True, service_name, banner.strip())
        else:
            return (False, service_name, banner.strip())
    except Exception as e:
        return (None, service_name, None)  # 예외 발생 시 None 반환

def port_scanner(target_host, ports_to_scan):
    for port in ports_to_scan:
        # SYN 스캔 수행
        syn_result = SYN_scan(target_host, port)

        # SMTP 스캔 수행
        smtp_result, service_name, banner = SMTP_scan(target_host, port)

        if syn_result is True:
            print(f"Port {port} is open (SYN Scan)")
        elif syn_result is False:
            print(f"Port {port} is closed (SYN Scan)")

        if smtp_result is True:
            print(f"Port {port} is open for {service_name} - Banner: {banner}")
        elif smtp_result is False:
            print(f"Port {port} is closed for {service_name} - Banner: {banner}")
        else:
            print(f"Port {port} status for {service_name} is unknown")

if __name__ == "__main__":
    target_host = "192.168.0.48"  # 스캔할 호스트 IP 주소
    ports_to_scan = [25]  # 스캔할 포트 목록 (포트 25로 설정)

    port_scanner(target_host, ports_to_scan)
