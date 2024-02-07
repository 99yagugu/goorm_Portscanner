import socket
import telnetlib

def SYN_scan(host, port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 타임아웃 설정

        # SYN 패킷 전송
        result = sock.connect_ex((host, port))

        # 결과 확인
        if result == 0:
            return True  # 포트가 열려있음
        else:
            return False  # 포트가 닫혀있음
    except Exception as e:
        return None  # 예외 발생 시 None 반환
    finally:
        sock.close()

def Telnet_scan(host, port):
    service_name = "Telnet"
    try:
        tn = telnetlib.Telnet(host, port, timeout=5)  # Telnet 객체 생성 및 서버에 연결 (타임아웃 설정)
        banner = tn.read_until(b"\r\n", timeout=5).decode('utf-8').strip()  # 배너 정보 읽기
        tn.close()  # 연결 종료
        return True, service_name, banner
    except ConnectionRefusedError:
        return False, service_name, None  # 연결이 거부되었을 때
    except Exception as e:
        return None, service_name, None  # 그 외 예외 발생 시

def SMTP_scan(host, port):
    service_name = "SMTP"
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 타임아웃 설정

        # SMTP 서버에 연결
        sock.connect((host, port))
        banner = sock.recv(1024).decode('utf-8').strip()  # 배너 정보 읽기
        sock.sendall(b"QUIT\r\n")  # QUIT 명령 전송
        sock.close()  # 연결 종료
        return True, service_name, banner
    except Exception as e:
        return None, service_name, None  # 예외 발생 시

def DNS_scan(host, port):
    try:
        # UDP 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)  # 타임아웃 설정

        # DNS 서버에 데이터 전송
        sock.sendto(b'', (host, port))

        # 데이터 수신 시 포트가 열려 있다고 가정
        # UDP 스캔은 응답이 없어도 포트가 열려 있다고 가정합니다.
        return True, "DNS", None
    except Exception as e:
        return False, "DNS", None
    finally:
        sock.close()

def port_scanner(host, ports_to_scan):
    for port in ports_to_scan:
        if port == 23:
            telnet_result, telnet_service_name, telnet_banner = Telnet_scan(host, port)
            if telnet_result:
                print(f"Port {port} is open for {telnet_service_name} - Banner: {telnet_banner}")
        elif port == 25:
            smtp_result, smtp_service_name, smtp_banner = SMTP_scan(host, port)
            if smtp_result:
                print(f"Port {port} is open for {smtp_service_name} - Banner: {smtp_banner}")
        elif port == 53:
            dns_result, dns_service_name, dns_banner = DNS_scan(host, port)
            if dns_result:
                print(f"Port {port} is open for {dns_service_name}")

if __name__ == "__main__":
    host = "192.168.0.48"  # 스캔할 호스트 IP 주소
    ports_to_scan = [23, 25, 53]  # 스캔할 포트 목록

    port_scanner(host, ports_to_scan)
