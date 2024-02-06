import socket
import telnetlib

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

def port_scanner(target_host, ports_to_scan):
    for port in ports_to_scan:
        # SYN 스캔 수행
        syn_result = SYN_scan(target_host, port)

        # Telnet 스캔 수행
        telnet_result, service_name, banner = Telnet_scan(target_host, port)

        if syn_result is True:
            print(f"Port {port} is open (SYN Scan)")
        elif syn_result is False:
            print(f"Port {port} is closed (SYN Scan)")

        if telnet_result is True:
            if banner:
                print(f"Port {port} is open for {service_name} - Banner: {banner.strip()}")
            else:
                print(f"Port {port} is open for {service_name} (Banner not available)")
        elif telnet_result == "Closed":
            print(f"Port {port} is closed for {service_name}")
        else:
            print(f"Port {port} status for {service_name} is unknown")

if __name__ == "__main__":
    target_host = "192.168.0.48"  # 스캔할 호스트 IP 주소
    ports_to_scan = [23]  # 스캔할 포트 목록 (포트 23로 설정)

    port_scanner(target_host, ports_to_scan)
