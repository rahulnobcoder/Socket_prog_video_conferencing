import socket
import threading
import struct
import pickle
import cv2

def audio(client,clients):
    while True:
        audio_data = client.recv(4096)
        for i in clients:
            if i!=client:
                clients[i].send(audio_data)
def video(client,clients):
    while True:
        a=client.recv(1024)
        for i in clients:
            if i!=client:
                clients[i].sendall(a)
def text(client,clients):
    while True:
        msg=client.recv(1024).decode()
        ms,mode=msg.split(':')
        if mode=='all':
            for i in clients:
                if i!=client:
                    clients[i].send(ms.encode())
            print('msg broadcasted')
        else:
            clients[mode].send(ms.encode())
        print(f'msg forwarded: {msg}')
def file(conn,clients):
    while True:
        ms=conn.recv(1024).decode()
        print(ms)
        fil,name,len1=ms.split(':')
        if name=='all':
            for i in clients:
                if i!=conn:
                    clients[i].send(ms.encode())
        else:
            clients[name].send(ms.encode())
        
        len1=int(len1)
        data=conn.recv(len1)
        print('recieved data of size : ',len1)
        if name=='all':
            for i in clients:
                if i!=conn:
                    clients[i].sendall(data)
        else:
            clients[name].sendall(data)
        print(f'sent file data of size - {len1}')

ip=socket.gethostbyname(socket.gethostname())
port_t=5556
port_f=5557
port_v=5558
port_a=5559
addr_v=(ip,port_v)
addr_t=(ip,port_t)
addr_f=(ip,port_f)
addr_a=(ip,port_a)
svideo=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
stext=socket.socket()
sfile=socket.socket()
saudio=socket.socket()
svideo.bind(addr_v)
svideo.listen()
stext.bind(addr_t)
stext.listen()
sfile.bind(addr_f)
sfile.listen()
saudio.bind(addr_a)
saudio.listen()
print('waiting for connection')
print(f'listening at ip : {ip}')
cl_t={}
cl_v={}
cl_f={}
cl_a={}
while True:
    c_t,a_t=stext.accept()
    name=c_t.recv(1024).decode()
    cl_t[name]=c_t
    print(cl_t)
    t_t=threading.Thread(target=text,args=(c_t,cl_t))
    t_t.start()
    print(f'text connection from  {a_t}')
    c_f,a_f=sfile.accept()
    cl_f[name]=c_f
    t_f=threading.Thread(target=file,args=(c_f,cl_f))
    t_f.start()
    print(f'file connection from  {a_f}')
    # c_v,a_v=svideo.accept()
    # cl_v[c_v]=c_v
    # t_v=threading.Thread(target=video,args=(c_v,cl_v))
    # t_v.start()
    # print(f'video connection from  {a_f}')
    # c_a,a_a=saudio.accept()
    # cl_a[c_a]=c_a
    # t_a=threading.Thread(target=audio,args=(c_a,cl_a))
    # t_a.start()
    # print(f'audio connection from  {a_a}')