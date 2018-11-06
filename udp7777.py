import socket
import select
import time

datalen = 1024 + 1
udp_ip = "192.168.0.169"
udp_port = 7777
message = bytearray(datalen)

print("UDP target IP:  ", udp_ip)
print("UDP target port:", udp_port)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

count = 0
timeouts = 0
damaged = 0

boot = start = time.time()

count = 1

sock.setblocking(False)

while True:
  message[0] = count & 0xFF;
  try:
    sock.recvfrom(datalen) # drop stale data
    print("drop")
  except:
    pass
  sock.sendto(message, (udp_ip, udp_port))
  ready = select.select([sock], [], [], 1)
  
  if ready[0]:
    
    data, addr = sock.recvfrom(datalen)
    if data != message:
      print(f"? len:{len(data)} message[0]:{message[0]} data[0]:{data[0]}")
      damaged += 1
    else:
      if count % 1000 == 0:
        t = time.time()
        runh = int(t - boot) // 3600
        runm = int(t - boot) % 3600 // 60
        
        t -= start
        speed = datalen / t / 1000.0
        errors = (damaged + timeouts) / count * 100
        print(f"Trips: {count:10} {runh:02d}h{runm:02d}m {speed:.3f}MB/s Timeouts: {timeouts} Damaged: {damaged} ({errors:.4f}%)")
        start = time.time()
    
      count += 1
  
  else:
    timeouts += 1
    print(f"Timeout: {timeouts}")

