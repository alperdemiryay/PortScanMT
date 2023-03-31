import socket
import threading
import time

# Define the IP address and the range of ports to scan
ip_address = "10.220.12.10"
start_port = 1
end_port = 10000
threads = []
timeCounter  = 0
jobFinishCount = 0
openPorts= []

# Define a function to scan a range of ports
def scan_ports(start_port, end_port):
    global jobFinishCount
    # Loop through the range of ports and attempt to connect to each one
    for port in range(start_port, end_port + 1):
        # Create a new socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout of 1 second
        sock.settimeout(0.1)
        # Attempt to connect to the remote host on the current port
        result = sock.connect_ex((ip_address, port))
        # If the connection was successful, the port is open
        if result == 0:
            print(f"Port {port} is open")
            openPorts.append(port)
        # Close the socket
        sock.close()
    jobFinishCount += 1

def countTime():
    global timeCounter
    while jobFinishCount < 20:
        time.sleep(1)
        timeCounter += 1
        if timeCounter % 10 == 0:
            print('{} seconds passed.'.format(timeCounter))
    print('Open port count: ', len(openPorts))
    print('Open ports are: ',openPorts)
    print('Time spent: ', timeCounter, ' seconds.')

# Create multiple threads to scan different ranges of ports
for i in range(20):
    start = start_port + (i * ((end_port - start_port + 1) // 20))
    end = start_port + ((i+1) * ((end_port - start_port + 1) // 20)) - 1
    thread = threading.Thread(target=scan_ports, args=(start, end))
    threads.append(thread)
    thread.start()

thread = threading.Thread(target=countTime)
threads.append(thread)
thread.start()