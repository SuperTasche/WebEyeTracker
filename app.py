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

while True:
  ret, image = cap.read()

  if (ret):
    img_height, img_width, depth = image.shape
    scale = width / img_width
    #height = img_height * scale
    #image = imutils.resize(image, width=540)
    image = cv2.resize(image, None, fx=scale, fy=scale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces
    rects = detector(gray, 1)

    # loop over face detections
    for (i, rect) in enumerate(rects):
      # determine the facial landmarks for the face region, then
      # convert the facial landmark (x, y)-coordinates to a NumPy
      # array
      shape = predictor(gray, rect)
      shape = face_utils.shape_to_np(shape)
     
      # convert dlib's rectangle to a OpenCV-style bounding box
      # [i.e., (x, y, w, h)], then draw the face bounding box
      #(x, y, w, h) = face_utils.rect_to_bb(rect)
      #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
     
      # show the face number
      # cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
      #   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

      leftEyeX = int((shape[2][0] + shape[3][0])/2);
      leftEyeY = int((shape[2][1] + shape[3][1])/2);
      rightEyeX = int((shape[0][0] + shape[1][0])/2);
      rightEyeY = int((shape[0][1] + shape[1][1])/2);

      print("leftEye(%d,%d) | rightEye(%d,%d)" % (leftEyeX, leftEyeY, rightEyeX, rightEyeY))

      eyes = [[leftEyeX, leftEyeY], [rightEyeX, rightEyeY]];
      # loop over the (x, y)-coordinates for the facial landmarks
      # and draw them on the image
      #for (x, y) in shape:
      #   cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
      for (x, y) in eyes:
        cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
      for client in clients:
        client.sendMessage(unicode(json.dumps({'leftEye': {'x': leftEyeX, 'y': leftEyeY}, 'rightEye': {'x': rightEyeX, 'y': rightEyeY}})))

    cv2.imshow("Output", image)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
server.close()