import struct

class protocol:
    def __init__(self, sock):
        self.sock = sock

    def send_packet(self, type, payload):
        data = (
            type.to_bytes(4, "little") +  # 4 byte header type
            payload.encode("utf-8") + 
            b"\x00"
        )
        print(f"Sending packet: Type={type}, Payload={payload[:100]}...")
        print(f"[DEBUG] Raw data: {data}")
        self.sock.send(struct.pack("<I", len(data)) + data)
