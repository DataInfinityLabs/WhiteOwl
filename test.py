import cv2

# Replace the URL with your IP camera's URL
url = 'http://192.168.29.99:8080/video'

# Open the video stream from the IP camera
capture = cv2.VideoCapture(url)

# Check if the video stream is opened successfully
if not capture.isOpened():
    print("Cannot open camera")
    exit()

# Set the window name and size
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video", 640, 480)

while True:
    # Read a frame from the video stream
    ret, frame = capture.read()

    # Check if a frame is successfully read
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the frame in a window
    cv2.imshow("Video", frame)

    # Press 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video stream and close the window
capture.release()
cv2.destroyAllWindows()