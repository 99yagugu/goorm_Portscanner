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

def Telnet_scan(host):
    port = [23]
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

def SMTP_scan(host):
    port = [25]
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
    port = [53]
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
