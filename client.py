import socket
import threading
import cv2
import pickle
import struct

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connection Data for Chat Server
# chat_host = "192.168.1.102"
chat_host ="192.168.1.181"
chat_port = 5050

# Connection Data for Video Stream Server
# video_host = "192.168.1.252"
video_host = "192.168.1.181"
video_port = 9999

# Connecting to Chat Server
chat_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating CHAT client socket
chat_client.connect((chat_host, chat_port))

# Sending Nickname to Chat Server
chat_client.send(nickname.encode('ascii'))

# Receiving Messages from Chat Server
def receive_chat():
    while True:
        try:
            message = chat_client.recv(1024).decode('ascii')
            if message == 'NICK':
                chat_client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Chat Client when an error occurs
            print("Error receiving message from chat server. Closing chat client.")
            chat_client.close()
            break

# Sending Messages to Chat Server
def send_chat():
    while True:
        # message = input()
        # chat_client.send(message.encode('ascii'))

        message = '{}: {}'.format(nickname, input(''))
        chat_client.send(message.encode('ascii'))

# Starting Chat Receive and Send Threads
receive_chat_thread = threading.Thread(target=receive_chat)
receive_chat_thread.start()

send_chat_thread = threading.Thread(target=send_chat)
send_chat_thread.start()

# Connecting to Video Stream Server
video_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creating VIDEO client socket
video_client.connect((video_host, video_port))

# Receiving Video Frames from Video Stream Server
# def receive_video():
#     data = b""
#     payload_size = struct.calcsize("Q")
#     while True:
#         while len(data) < payload_size:
#             packet = video_client.recv(4096)
#             if not packet:
#                 break
#             data += packet
#         packed_msg_size = data[:payload_size]
#         data = data[payload_size:]
#         msg_size = struct.unpack("Q", packed_msg_size)[0]

#         while len(data) < msg_size:
#             data += video_client.recv(4096)
#         frame_data = data[:msg_size]
#         data = data[msg_size:]
#         frame = pickle.loads(frame_data)
#         cv2.imshow("RECEIVING VIDEO", frame)
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('!'):
#             break

def receive_video():
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = video_client.recv(4096)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += video_client.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Video from Server ({})".format(nickname), frame)  # Display video in separate windows for each client
        key = cv2.waitKey(1) & 0xFF
        if key == ord('!'):
            break  # Exit the loop for each client


# Starting Video Receive Thread
receive_video_thread = threading.Thread(target=receive_video)
receive_video_thread.start()

