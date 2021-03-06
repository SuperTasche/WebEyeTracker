# WebEyeTracker
This app uses a websocket server to obtain webcam images from a client and serve the coordinates of eye positions back to the client. For the computation of eye positions dlib's facial landmark detector is used working on a pre-trained [5-face-landmarks model](http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2).
The app was tested with Python 3.7 and Chrome.

# Setup
Following dependencies have to be installed:  
* SimpleWebsocketServer: `pip install git+https://github.com/dpallot/simple-websocket-server.git`  
* OpenCV: `pip install opencv-python`  
* Dlib: `pip install dlib`  
* imutils: `pip install imutils`  

Start the server on port 9000:  
`python app.py`

Wait for console confirmation.

You can now open the `index.html` in a browser to establish a connection to the server and display the eye positions from your webcam video. Be aware that wearing reflecting glasses will impact detection results!

The project is based on the following articles:  
* [Facial Landmark Detection with OpenCV and Dlib](https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/)  
* [Augmented Reality with OpenCV, Three.js and WebSockets](https://www.smashingmagazine.com/2016/02/simple-augmented-reality-with-opencv-a-three-js/)
