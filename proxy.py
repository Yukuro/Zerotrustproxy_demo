import socket
import sys
import threading
import queue
import logging
from datetime import datetime, timedelta

def start(listening_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info('Inisializing Sockets ... Done')

        s.bind(('', listening_port))
        logging.info('Sockets Binded Successfully ...')

        s.listen(max_conn)
        logging.info('Server Started Successfully [ {} ]\n'.format(listening_port))
    except Exception as e:
        logging.exception('Unable to Initialize Socket...')
        sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size).decode('utf-8')
            conn_time_now = datetime.now()

            logging.debug('RECV data: {}'.format(data))

            if len(data) > 0 :
                t = threading.Thread(target=conn_string, args=(conn,data,addr,conn_time_now))
                t.start()
        except KeyboardInterrupt:
            logging.info('\nProxy Server Shutting Down ...')
            s.close()
            sys.exit(1)
    s.close()

def conn_string(conn, data, addr, conn_time_now):
    try:
        first_line = data.split('\n')[0]

        url = first_line.split(' ')[1]

        http_pos = url.find('://')
        if(http_pos==-1):
            temp = url
        else:
            temp = url[(http_pos+3):]
        
        port_pos = temp.find(':')

        webserver_pos = temp.find('/')
        if(webserver_pos == -1):
            webserver_pos = len(temp)
        webserver = ''
        port = -1
        if(port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        logging.debug('Entry conn_string | PEER:{} / SOCK:{}'.format(conn.getpeername, conn.getsockname))

        proxy_server(webserver, port, conn, data, addr, conn_time_now)
    except Exception:
        logging.exception('Exception occurred...')

def proxy_server(webserver, port, conn, data, addr, conn_time_now):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))

        s.send(data.encode('utf-8'))
        logging.debug('DATA:{}\nSent -> {}:{}.'.format(data.encode('utf-8'), webserver, port))

        while 1:
            reply = s.recv(buffer_size)
            logging.debug('RCV reply:{}'.format(reply))
            if(len(reply) > 0): # can through only HTTP
                conn.send(reply)

                logging.debug('Conn_time_now: {} / from IP: {}'.format(conn_time_now, s.getsockname()))

                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = '%.3s' % (str(dar))
                dar = '%s KB' % (dar)
                'Print A Custom Message For Request Complete'
                logging.info('Request Done: %s => %s <=' % (str(addr[0]), str(dar)))

                global pt # one last Request
                if(conn_time_now != pt):
                    send_queue((conn_time_now, s.getsockname()[0], data))

                # calculate trust score
                trust_data_now = calc_trust()

                if trust_data_now:
                    logging.info('[*] Trust Score: {} from {}'.format(trust_data_now[0], trust_data_now[1]))

                pt = conn_time_now
            else:
                break
        
        s.close()
        conn.close()
    except socket.error as msg:
        logging.info('Socket Error occurred...')
        s.close()
        conn.close()
        sys.exit(1)

def send_queue(trustdata):
    q.put(trustdata)
    logging.debug('{} => queue sent.'.format(trustdata))

def calc_trust():
    q_len = q.qsize()
    logging.debug('queue length: {}'.format(q_len))

    if q_len < 2:
        return None

    logging.debug('ready to calculate...')

    # TODO: more smart method
    f_access_time, f_from_ip, _ = q.get()
    s_access_time, s_from_ip, _ = q.get()

    logging.debug('{} from {} -> {} from {}'.format(f_access_time, f_from_ip, s_access_time, s_from_ip))

    global trust_score
    if f_from_ip == s_from_ip:
        if _evaluate(f_access_time, s_access_time):
            trust_score -= 1

    return (trust_score, f_from_ip)

def _evaluate(first_time, second_time):
    # TODO: more smart method
    delta = second_time - first_time

    if timedelta(microseconds=0) < delta < timedelta(microseconds=2000000):
        return True
    return False



def main():
    try:
        listening_port = int(input('[-] Enter Listening Port Number: '))
    except KeyboardInterrupt:
        logging.info('User Requested An Interrupt')
        logging.info('Application Exiting...')
        sys.exit()

    start(listening_port)

if __name__ == '__main__':
    # global variables
    # TODO remove
    trust_score = 0
    pt = datetime.now()
    max_conn = 5
    buffer_size = 2048
    q = queue.Queue()

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    main()