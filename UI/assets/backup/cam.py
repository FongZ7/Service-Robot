
import cv2


cap = cv2.VideoCapture(2)


if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:

    ret, frame = cap.read()


    if not ret:
        print("Error: Could not read frame.")
        break

    cv2.imshow('Camera Feed', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

# import cv2

# def check_video_devices():
#     for index in range(6):  # Assuming you have up to /dev/video5
#         cap = cv2.VideoCapture(index)
#         if cap.isOpened():
#             print(f"Successfully opened /dev/video{index}")
#             ret, frame = cap.read()
#             if ret:
#                 cv2.imshow(f'Camera Feed - /dev/video{index}', frame)
#                 cv2.waitKey(0)  # Press any key to close the window
#                 cv2.destroyAllWindows()
#             cap.release()
#         else:
#             print(f"Could not open /dev/video{index}")

# check_video_devices()


import cv2

def find_available_cameras(max_index=1000):
    available_cameras = []
    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"Camera found at index: {index}")
            available_cameras.append(index)
            cap.release()  # Release the camera after checking
        else:
            print(f"No camera at index: {index}")
    return available_cameras

# Set the maximum index to check (adjust as needed)
available_cams = find_available_cameras(100)
print("Available cameras:", available_cams)
