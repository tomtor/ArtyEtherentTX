import socket
import time

UDP_IP = "192.168.0.169"
UDP_PORT = 7777
MESSAGE = bytearray(1024)

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

count= 0

start = time.time()
while True:
  count += 1
  sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  if data != MESSAGE:
    print("?")
  if count % 1000 == 0:
    t= time.time() - start
    speed= len(MESSAGE) / t / 1000.0
    print(f"Trips: {count:10} {t:.3f}s {speed:.3f}MB/s")
    start = time.time()

