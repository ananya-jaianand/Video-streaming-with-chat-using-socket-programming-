# Video streaming with chat using socket programming 
Video streaming with chat using socket programming using socket library in python

This project creates a multi-client chat and video stream application where users can communicate via text and video across different devices in a network. The application uses sockets for network communication and threading to handle multiple clients simultaneously.

## Features
- User entry with nickname selection.
- Real-time chat functionality.
- Real-time video streaming from a server to multiple clients.

## Setup instructions
1. **Install dependencies**
```
    pip install opencv-python imutils
```
2. **Configure IP Addresses**
- Server IP Address: Use your machine's local IP address for the server. You can find your IP address using the following command:
    - Windows: Open Command Prompt and type ipconfig.
    - Linux/Mac: Open Terminal and type ifconfig or ip a.
- Client IP Address: Ensure the clients use the same IP address as the server for both chat and video streaming.
3. **Video Setup**
- By default, the server streams from a video file named vid.mp4. Ensure you have this file in the same directory as your scripts.Change vid = cv2.VideoCapture('vid.mp4') to a new name for changing the video.
4. **Run server**

```
    python server.py

```
5. **Run client**
```
    python client.py
```
