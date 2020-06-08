import socket, sys
import traceback
from _thread import *
#import threading

try:
    listening_port = int(input("[*] Enter Listening Port Number: "))
except KeyboardInterrupt:
    print("\n[*] User Requested An Interrupt")
    print("[*] Application Exiting...")
    sys.exit()

max_conn = 5
buffer_size = 8192

def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', listening_port))
        s.listen(max_conn)
        print("[*] Inisializing Sockets ... Done")
        print("[*] Sockets Binded Successfully ...")
        print("[*] Server Started Successfully [ {} ]\n".format(listening_port))
    except Exception as e:
        print("[*] Unable to Initialize Socket")
        print(traceback.format_exc())
        sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size).decode('utf-8')
            # print("RECV: {}".format(data))
            if len(data) > 0 :
                start_new_thread(conn_string, (conn,data,addr))
        except KeyboardInterrupt:
            s.close()
            print("\n[*] Proxy Server Shutting Down ...")
            print("[*] Have A Nice Day ... Sergeant !!!")
            sys.exit(1)
    s.close()

def conn_string(conn, data, addr):
    try:
        first_line = data.split('\n')[0]
        # print(first_line)

        url = first_line.split(' ')[1]

        http_pos = url.find("://")
        if(http_pos==-1):
            temp = url
        else:
            temp = url[(http_pos+3):]
        
        port_pos = temp.find(":")

        webserver_pos = temp.find("/")
        if(webserver_pos == -1):
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if(port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        proxy_server(webserver, port, conn, data, addr)
    except Exception as e:
        print("Exception occured...")
        print(traceback.format_exc())

def proxy_server(webserver, port, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data.encode('utf-8'))
        print("DATA:{}\nSent.".format(data.encode('utf-8')))

        while 1:
            reply = s.recv(buffer_size)
            print("RECV:{}".format((reply)))
            if(len(reply) > 0):
                conn.send(reply)

                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                'Print A Custom Message For Request Complete'
                print("[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar)))
            else:
                break
        
        s.close()
        conn.close()
    except socket.error as msg:
        print("Socket Error Occurred")
        print(traceback.format_exc())
        s.close()
        conn.close()
        sys.exit(1)

if __name__ == "__main__":
    start()