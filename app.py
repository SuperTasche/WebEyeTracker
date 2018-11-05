from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading
import cv2
import dlib
import json
from imutils import face_utils

# Server code
clients = []
server = None

class SimpleWSServer(WebSocket):
  def handleConnected(self):
    clients.append(self)

  def handleClose(self):
    clients.remove(self)

def run_server():
  global server
  server = SimpleWebSocketServer('', 9000, SimpleWSServer,
                                 selectInterval=(1000.0 / 120) / 1000)
  server.serveforever()

t = threading.Thread(target=run_server)
t.start()

# OpenCV code
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./shape_predictor_5_face_landmarks.dat")

width = 320.0 #640.0
height = 240.0 #480.0
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

print("Server setup complete. Ready to serve, master...")

while True:
  ret, image = cap.read()

  if (ret):
    img_height, img_width, depth = image.shape
    scale = width / img_width
    image = cv2.resize(image, None, fx=scale, fy=scale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
      shape = predictor(gray, rect)
      shape = face_utils.shape_to_np(shape)
     
      #(x, y, w, h) = face_utils.rect_to_bb(rect)

      leftEyeX = int((shape[2][0] + shape[3][0])/2);
      leftEyeY = int((shape[2][1] + shape[3][1])/2);
      rightEyeX = int((shape[0][0] + shape[1][0])/2);
      rightEyeY = int((shape[0][1] + shape[1][1])/2);
      eyes = [[leftEyeX, leftEyeY], [rightEyeX, rightEyeY]];

      for (x, y) in eyes:
        cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
      for client in clients:
        client.sendMessage(str(json.dumps({'leftEye': {'x': leftEyeX, 'y': leftEyeY}, 'rightEye': {'x': rightEyeX, 'y': rightEyeY}})))

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
server.close()
