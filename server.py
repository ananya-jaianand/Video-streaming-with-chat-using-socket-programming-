import threading
import socket
import cv2
import pickle
import struct
import imutils

# Connection Data
host = '0.0.0.0'
chat_port = 5050
video_port = 9999

# Starting Chat Server
chat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server.bind((host, chat_port))
chat_server.listen()

# Lists For Chat Clients and Their Nicknames
clients = []
nicknames = []
vidclients=[]



global frame
frame = None

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Chat Clients
def handle(client):
    while True:
        try:
            # Broadcasting Chat Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Chat Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function for Chat Clients
def receive_chat():
    while True:
        # Accept Chat Connection
        client, address = chat_server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to chat server!'.encode('ascii'))

        # Start Handling Thread For Chat Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        print(f"Video stream server is listening on {host}:{video_port}")
        video_accept_thread = threading.Thread(target=accept_video)
        video_accept_thread.start()

# Starting Video Stream Server
video_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
video_server.bind((host, video_port))
video_server.listen()
print("LISTENING AT:", (host, video_port))

# Socket Accept for Video Stream Clients
# def accept_video():
#     while True:
#         client_socket,addr = video_server.accept()
#         print('GOT CONNECTION FROM:', addr)
#         if client_socket:
#             vid = cv2.VideoCapture(0)
#             while(vid.isOpened()):
#                 img, frame = vid.read()
#                 frame = imutils.resize(frame, width=320)
#                 a = pickle.dumps(frame)
#                 message = struct.pack("Q", len(a)) + a
#                 client_socket.sendall(message)

#                 cv2.imshow('TRANSMITTING VIDEO', frame)
#                 key = cv2.waitKey(1) & 0xFF
#                 if key == ord('!'):
#                     client_socket.close()

def accept_video():
    while True:
        try:
            client_socket, addr = video_server.accept()
            print('GOT CONNECTION FROM:', addr)

            vidclients.append(client_socket)

            print(clients)
            print(vidclients)

            
            # vid = cv2.VideoCapture(0)
            vid = cv2.VideoCapture('vid.mp4')
            while vid.isOpened():
                img, frame = vid.read()
                frame = imutils.resize(frame, width=320)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                for client_socket in vidclients:
                    client_socket.sendall(message)

                # cv2.imshow('TRANSMITTING VIDEO', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('!'):
                    client_socket.close()
                    break  # Exit the loop for each client
        except:
            break
            
        vidclients.remove(client_socket)
        client_socket.close()


        

        


# Start Listening Threads for Chat Clients and Video Stream Clients
print(f"Chat server is listening on {host}:{chat_port}")
chat_receive_thread = threading.Thread(target=receive_chat)
chat_receive_thread.start()



