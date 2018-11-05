const FPS = 60;
const frameTime = 1000/FPS;

let video = document.getElementById("webcam");
let width = video.width;
let height = video.height;
let src = null;
let dst = null;
let cap = null;

//let history = [];
let ws = null;
let ping = 0;
let lastPosLeft, lastPosRight, diffMoveLeft, diffMoveRight;
let lastMessage = 0;
let steps = 0;

let velocity = 1.0;

function startCamera() {
  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
      src = new cv.Mat(height, width, cv.CV_8UC4);
      dst = new cv.Mat(height, width, cv.CV_8UC1);
      cap = new cv.VideoCapture(video);
      setTimeout(processVideo, 0);
    })
    .catch(function(err) {
      console.log("An error occurred! " + err);
    });
}

function processVideo() {
  let begin = Date.now();

  cap.read(src);
  ping++;

  if (lastPosLeft && lastPosRight) {
    if (ping < steps) {
      lastPosLeft[0] += velocity * diffMoveLeft[0];
      lastPosLeft[1] += velocity * diffMoveLeft[1];
      lastPosRight[0] += velocity * diffMoveRight[0];
      lastPosRight[1] += velocity * diffMoveRight[1];
    }

    let p1 = new cv.Point(lastPosLeft[0], lastPosLeft[1]);
    let p2 = new cv.Point(lastPosRight[0], lastPosRight[1]);

    cv.circle(src, p1, 3, [255, 0, 0, 255], -1);
    cv.circle(src, p2, 3, [255, 0, 0, 255], -1);
  }

  cv.imshow("canvasOutput", src);

  let delay = frameTime - (Date.now() - begin);
  setTimeout(processVideo, delay);
}

function connectServer() {
  ws = new WebSocket('ws://localhost:9000');

  ws.onmessage = function (evt) {
    let m = JSON.parse(evt.data);

    //history.push(m);

    let targetPosLeft = [m.leftEye.x, m.leftEye.y];
    let targetPosRight = [m.rightEye.x, m.rightEye.y];

    if (!lastPosLeft) {
      lastPosLeft = targetPosLeft;
    }
    if (!lastPosRight) {
      lastPosRight = targetPosRight;
    }

    let msgFrame = Date.now() - lastMessage;

    if (msgFrame) {
      steps = Math.round(msgFrame / frameTime);
    }

    diffMoveLeft = [(targetPosLeft[0] - lastPosLeft[0]) / steps, (targetPosLeft[1] - lastPosLeft[1]) / steps];
    diffMoveRight = [(targetPosRight[0] - lastPosRight[0]) / steps, (targetPosRight[1] - lastPosRight[1]) / steps];

    ping = 0;
    lastMessage = Date.now();
  };
}

function opencvIsReady() {
  console.log('OpenCV.js is ready');
  startCamera();
  connectServer();
}