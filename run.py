import socket
from gt.protocol import protocol
from gt.login import login

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("127.0.0.1", 17091))

    loging = login()
    proto = protocol(sock)

    token = loging.get_token(growid="Fazz")
    proto.send_packet(2, f"""protocol|217
                      ltoken|{token}
                      platformID|0,1,1""")  

if __name__ == "__main__":
    main()