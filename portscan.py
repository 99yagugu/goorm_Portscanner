import ftplib

def FTP_conn(target_host, port, username, password):
    service_name = "FTP"
    try:
        ftp = ftplib.FTP(target_host, timeout=5)  # FTP 객체 생성 및 서버에 연결 (타임아웃 설정)
        ftp.login(user=username, passwd=password)  # 로그인 시도
        banner = ftp.getwelcome()  # 배너 정보 가져오기
        ftp.quit()  # 연결 종료
        return (True, service_name, banner)  # 성공적으로 연결되면 True와 배너 정보를 반환
    except ftplib.error_perm as e:
        return ("Closed", service_name, None)  # 권한 오류 발생 시 "Closed" 반환
    except Exception as e:
        return (None, service_name, None)  # 그 외 예외 발생 시 None 반환

def port_scanner(target_host, ports_to_scan, username, password):
    for port in ports_to_scan:
        result, service_name, banner = FTP_conn(target_host, port, username, password)
        if result is True:
            if banner:
                print(f"Port {port} is open for {service_name} - Banner: {banner}")
            else:
                print(f"Port {port} is open for {service_name} (Banner not available)")
        elif result == "Closed":
            print(f"Port {port} is closed for {service_name}")
        else:
            print(f"Port {port} status for {service_name} is unknown")

if __name__ == "__main__":
    target_host = "127.0.0.1"  # 스캔할 호스트 IP 주소
    ports_to_scan = [23, 25, 53]  # 스캔할 포트 목록
    username = "your_username"  # FTP 로그인에 사용할 사용자 이름
    password = "your_password"  # FTP 로그인에 사용할 비밀번호

    port_scanner(target_host, ports_to_scan, username, password)
