from django.http import JsonResponse
from threading import Thread
import mediapipe
import cv2
import time

# Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

# Define the gesture variables globally
action = None
last_action_time = 0
action_interval = 5  # 5 seconds interval

# Use CV2 Functionality to create a Video stream and add some values
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

def start_camera():
    global action, last_action_time
    # Add confidence values and extra settings to MediaPipe hand tracking.
    # As we are using a live video stream this is not a static image mode,
    # confidence values in regards to overall detection and tracking,
    # and we will only let two hands be tracked at the same time.
    # More hands can be tracked at the same time if desired but will slow down the system.
    with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
        # Create an infinite loop which will produce the live feed to our desktop and that will search for hands
        while True:
            ret, frame = cap.read()
            # Uncomment the below line if your live feed is produced upside down
            # flipped = cv2.flip(frame, flipCode=-1)

            # Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
            frame1 = cv2.resize(frame, (640, 480))

            # Produces the hand framework overlay on top of the hand, you can choose the colour here too
            results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

            # In case the system sees multiple hands, this if statement deals with that and produces another hand overlay
            if results.multi_hand_landmarks is not None:
                for handLandmarks in results.multi_hand_landmarks:
                    drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)

                    # Below is added code to find and print to the shell the Location X-Y coordinates of Index Finger, Uncomment if desired
                    for point in handsModule.HandLandmark:
                        normalizedLandmark = handLandmarks.landmark[point]
                        pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(
                            normalizedLandmark.x, normalizedLandmark.y, 640, 480
                        )

                        # Using the Finger Joint Identification Image, we know that point 8 represents the tip of the Index Finger
                        if point == 8:
                            print(point)

                            # Extract Y-coordinates for the TIP of the fingers
                            thumb_tip_y = handLandmarks.landmark[handsModule.HandLandmark.THUMB_TIP].y
                            index_tip_y = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_TIP].y
                            middle_tip_y = handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_TIP].y
                            ring_tip_y = handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_TIP].y
                            pinky_tip_y = handLandmarks.landmark[handsModule.HandLandmark.PINKY_TIP].y

                            # Extract Y-coordinates for DIP/IP of the fingers
                            thumb_ip_y = handLandmarks.landmark[handsModule.HandLandmark.THUMB_IP].y
                            index_dip_y = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_DIP].y
                            middle_dip_y = handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_DIP].y
                            ring_dip_y = handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_DIP].y
                            pinky_dip_y = handLandmarks.landmark[handsModule.HandLandmark.PINKY_DIP].y

                            # Extract Y-coordinates for PIP/MCP of the fingers
                            thumb_mcp_y = handLandmarks.landmark[handsModule.HandLandmark.THUMB_MCP].y
                            index_pip_y = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_PIP].y
                            middle_pip_y = handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_PIP].y
                            ring_pip_y = handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_PIP].y
                            pinky_pip_y = handLandmarks.landmark[handsModule.HandLandmark.PINKY_PIP].y

                            # Extract Y-coordinates for MCP/CMC of the fingers
                            thumb_cmc_y = handLandmarks.landmark[handsModule.HandLandmark.THUMB_CMC].y
                            index_mcp_y = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_MCP].y
                            middle_mcp_y = handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_MCP].y
                            ring_mcp_y = handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_MCP].y
                            pinky_mcp_y = handLandmarks.landmark[handsModule.HandLandmark.PINKY_MCP].y

                            index_tip_x = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_TIP].x
                            index_dip_x = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_DIP].x
                            index_pip_x = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_PIP].x
                            index_mcp_x = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_MCP].x

                            middle_tip_x = handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_TIP].x
                            middle_dip_x = handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_DIP].x
                            middle_pip_x = handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_PIP].x

                            ring_tip_x = handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_TIP].x
                            ring_dip_x = handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_DIP].x
                            ring_pip_x = handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_PIP].x

                            # Check if the fingers are up
                            is_thumb_up = thumb_tip_y < thumb_cmc_y and thumb_tip_y < thumb_ip_y
                            is_index_up = index_tip_y < index_mcp_y and index_tip_y < index_dip_y
                            is_middle_up = middle_tip_y < middle_mcp_y and middle_tip_y < middle_dip_y
                            is_ring_up = ring_tip_y < ring_mcp_y and ring_tip_y < ring_dip_y
                            is_pinky_up = pinky_tip_y < pinky_mcp_y and pinky_tip_y < pinky_dip_y

                            is_index_pointing_left = (
                                index_tip_x > index_dip_x and index_dip_x > index_pip_x and
                                index_tip_x > middle_tip_x and index_tip_x > middle_dip_x and index_dip_x > middle_tip_x and index_dip_x > middle_dip_x and
                                index_tip_x > ring_tip_x and index_tip_x > ring_dip_x and index_dip_x > ring_tip_x and index_dip_x > ring_dip_x
                            )
                            # Check if other fingers are down
                            are_middle_ring_pinky_down = (
                                middle_tip_y > middle_mcp_y and
                                ring_tip_y > ring_mcp_y and
                                pinky_tip_y > pinky_mcp_y
                            )
                            
                            # Check if other fingers are down
                            are_index_ring_pinky_down = (
                                index_tip_y > index_pip_y and
                                ring_tip_y > ring_pip_y and
                                pinky_tip_y > pinky_pip_y
                            )

                            are_all_fingers_up = (
                                is_thumb_up and
                                is_index_up and
                                is_middle_up and
                                is_ring_up and
                                is_pinky_up
                            )

                            is_my_thumb_up = (
                                thumb_tip_y < index_mcp_y and thumb_tip_y < index_dip_y and thumb_tip_y < index_pip_y and thumb_tip_y < index_tip_y and
                                thumb_ip_y < index_mcp_y and thumb_ip_y < index_dip_y and thumb_ip_y < index_pip_y and thumb_ip_y < index_tip_y and

                                thumb_tip_y < middle_mcp_y and thumb_tip_y < middle_dip_y and thumb_tip_y < middle_pip_y and thumb_tip_y < middle_tip_y and
                                thumb_ip_y < middle_mcp_y and thumb_ip_y < middle_dip_y and thumb_ip_y < middle_pip_y and thumb_ip_y < middle_tip_y and

                                thumb_tip_y < ring_mcp_y and thumb_tip_y < ring_dip_y and thumb_tip_y < ring_pip_y and thumb_tip_y < ring_tip_y and
                                thumb_ip_y < ring_mcp_y and thumb_ip_y < ring_dip_y and thumb_ip_y < ring_pip_y and thumb_ip_y < ring_tip_y and

                                thumb_tip_y < pinky_mcp_y and thumb_tip_y < pinky_dip_y and thumb_tip_y < pinky_pip_y and thumb_tip_y < pinky_tip_y and
                                thumb_ip_y < pinky_mcp_y and thumb_ip_y < pinky_dip_y and thumb_ip_y < pinky_pip_y and thumb_ip_y < pinky_tip_y
                            )

                            is_my_pinky_up = (
                                pinky_tip_y < index_mcp_y and pinky_tip_y < index_dip_y and pinky_tip_y < index_pip_y and pinky_tip_y < index_tip_y and
                                pinky_dip_y < index_mcp_y and pinky_dip_y < index_dip_y and pinky_dip_y < index_pip_y and pinky_dip_y < index_tip_y and

                                pinky_tip_y < middle_mcp_y and pinky_tip_y < middle_dip_y and pinky_tip_y < middle_pip_y and pinky_tip_y < middle_tip_y and
                                pinky_dip_y < middle_mcp_y and pinky_dip_y < middle_dip_y and pinky_dip_y < middle_pip_y and pinky_dip_y < middle_tip_y and

                                pinky_tip_y < ring_mcp_y and pinky_tip_y < ring_dip_y and pinky_tip_y < ring_pip_y and pinky_tip_y < ring_tip_y and
                                pinky_dip_y < ring_mcp_y and pinky_dip_y < ring_dip_y and pinky_dip_y < ring_pip_y and pinky_dip_y < ring_tip_y
                            )

                            current_time = time.time()
                            if current_time - last_action_time >= action_interval:
                                if is_middle_up and are_index_ring_pinky_down:
                                    #("Gesture Detected: You are very rude!!!") 
                                    action = 'SHUTDOWN'
                                elif are_all_fingers_up:
                                    #("Gesture Detected: All Fingers Up!")        
                                    action = 'PAUSE'
                                elif is_index_up and are_middle_ring_pinky_down:
                                    #print("Gesture Detected: Index Finger Up!")
                                    action = 'LOGIN'
                                elif is_my_thumb_up:
                                    #("Gesture Detected: Like And Subscribe")   
                                    action = 'PLAY'
                                elif is_pinky_up and is_my_pinky_up:
                                    #("Gesture Detected: Pinky Up!")    
                                    action = 'REFRESH'
                                elif is_index_pointing_left:
                                    #("Gesture Detected: Point Right!")
                                    action = 'SKIP'
                                last_action_time = current_time

            # # Below shows the current frame to the desktop
            # cv2.imshow("Frame", frame1)
            # key = cv2.waitKey(1) & 0xFF

            # # Below states that if the |q| is pressed on the keyboard, it will stop the system
            # if key == ord("q"):
            #     break
            
# Function to start the camera in a new thread
def start_camera_in_background():
    camera_thread = Thread(target=start_camera)
    camera_thread.daemon = True
    camera_thread.start()

# Call this function to start the camera in the background
start_camera_in_background()

def sendGestureData(request):
    global action
    gestureData = action
    print(gestureData)
    
    response_data = {'gesture': gestureData}
    
    # Reset gesture after sending it
    action = None
    
    return JsonResponse(response_data)
