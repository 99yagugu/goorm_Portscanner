import socket
import ftplib

def SYN_scan(target_host, port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 타임아웃 설정

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

def port_scanner(target_host, ports_to_scan, username, password):
    for port in ports_to_scan:
        # SYN 스캔 수행
        syn_result = SYN_scan(target_host, port)

        # FTP 포트 스캔 결과 확인
        ftp_result, service_name, banner = FTP_conn(target_host, port, username, password)

        if syn_result is True:
            print(f"Port {port} is open (SYN Scan)")
        elif syn_result is False:
            print(f"Port {port} is closed (SYN Scan)")

        if ftp_result is True:
            if banner:
                print(f"Port {port} is open for {service_name} - Banner: {banner}")
            else:
                print(f"Port {port} is open for {service_name} (Banner not available)")
        elif ftp_result == "Closed":
            print(f"Port {port} is closed for {service_name}")
        else:
            print(f"Port {port} status for {service_name} is unknown")

if __name__ == "__main__":
    target_host = "127.0.0.1"  # 스캔할 호스트 IP 주소
    ports_to_scan = [23, 25, 53]  # 스캔할 포트 목록
    username = "your_username"  # FTP 로그인에 사용할 사용자 이름
    password = "your_password"  # FTP 로그인에 사용할 비밀번호

    port_scanner(target_host, ports_to_scan, username, password)

