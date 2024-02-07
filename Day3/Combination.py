import socket
import telnetlib

def SYN_scan(target_host, port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 타임아웃 설정

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

def Telnet_scan(target_host, port):
    service_name = "Telnet"
    try:
        tn = telnetlib.Telnet(target_host, port, timeout=5)  # Telnet 객체 생성 및 서버에 연결 (타임아웃 설정)
        banner = tn.read_until(b"\r\n", timeout=5).decode('utf-8')  # 배너 정보 읽기
        tn.close()  # 연결 종료
        return (True, service_name, banner)  # 성공적으로 연결되면 True와 배너 정보를 반환
    except ConnectionRefusedError:
        return ("Closed", service_name, None)  # 연결이 거부되었을 때 "Closed" 반환
    except Exception as e:
        return (None, service_name, None)  # 그 외 예외 발생 시 None 반환

def SMTP_scan(target_host, port):
    service_name = "SMTP"
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 타임아웃 설정

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

def identify_service(port):
    if port == 23:
        return "Telnet"
    elif port == 25:
        return "SMTP"
    elif port == 53:
        return "DNS"
    else:
        return "Unknown"

def port_scanner(target_host, ports):
    for port in ports:
        # SYN 스캔 수행
        syn_result = SYN_scan(target_host, port)

        # 서비스 스캔 수행
        if port == 23:
            service_result, service_name, banner = Telnet_scan(target_host, port)
        elif port == 25:
            service_result, service_name, banner = SMTP_scan(target_host, port)
        else:
            service_result = scan_port(target_host, port)
            service_name = identify_service(port)
            banner = grab_banner(target_host, port)

        # 결과 출력
        if syn_result is True:
            print(f"Port {port} is open (SYN Scan)")
        elif syn_result is False:
            print(f"Port {port} is closed (SYN Scan)")

        if service_result is True:
            if banner:
                print(f"Port {port} is open for {service_name} - Banner: {banner}")
            else:
                print(f"Port {port} is open for {service_name} (Banner not available)")
        elif service_result == "Closed":
            print(f"Port {port} is closed for {service_name}")
        else:
            print(f"Port {port} status for {service_name} is unknown")

if __name__ == "__main__":
    target_host = "192.168.0.48"  # 스캔할 호스트 IP 주소
    ports_to_scan = [23, 25, 53]  # 스캔할 포트 목록

    port_scanner(target_host, ports_to_scan)