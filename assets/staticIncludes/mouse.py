# Threading  + [Left ,right click ; up,down scroll ]
import cv2 # importing cv2 for camera related works
import mediapipe as mp # Using to detect hand
import pyautogui # to control mouse pointer
import threading
import time
import keyboard
display_width,display_height=pyautogui.size() # getting dispaly size
cap=cv2.VideoCapture(0) # 0 => first video source
detect_hand=mp.solutions.hands.Hands() # getting hand detector
drawing_tools=mp.solutions.drawing_utils # getting drawing tools from mediapipe
gframe=0
ghands=0
start_flag=0
dis_pointer_click=100
    # i ,x y,c ,rc,up,dn
mouse=[0,0,0,80,80,80,80]
action_selector=[0,1,2,3]# click,scrollDown,scrollUp,rightClick
sensi=[20,20,5,3] # sencitivity of ctl action

class VideoCaptureThread(threading.Thread):
    def __init__(self, thread_id=1, device_id=0):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.device_id = device_id
        self.capture = cv2.VideoCapture(self.device_id)
        self.is_running = True

    def run(self):
        print(f"Thread-{self.thread_id}: Starting video capture...")
        global gframe,ghands,start_flag # getting access of global varriables to edit
        while self.is_running:
            ret, frame = self.capture.read()
            if ret:
                frame=cv2.flip(frame,1) # flip the frame on y=1 axis
                rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                output_handInrgb_image=detect_hand.process(rgb_frame)
                hands=output_handInrgb_image.multi_hand_landmarks # getting each hqand containing 21 landmarks
                
                gframe,ghands=frame,hands
                start_flag=1

                # Break the loop and stop capturing if 'q' is pressed
                if (cv2.waitKey(1) & 0xFF == ord('q')) :
                    self.is_running = False
            else:
                print(f"Thread-{self.thread_id}: Error capturing frame")

        self.capture.release()
        cv2.destroyAllWindows()
        print(f"Thread-{self.thread_id}: Video capture thread stopped.")

    def stop(self):
        self.is_running = False

class VideoPlayThread(threading.Thread):
    def __init__(self, thread_id=2, device_id=0):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.device_id = device_id
        global gframe,ghands # getting access of global varriables to edit
        self.frame=gframe
        self.hands=ghands
        self.is_running = True

    def run(self):
        print(f"Thread-{self.thread_id}: Starting video play...")
        # import mediapipe as mp # Using to detect hand
        global gframe,ghands,start_flag,mouse # getting access of global varriables to edit
        while self.is_running :
            try:
                if start_flag:
                    frame=gframe
                    frame_height,frame_width,_=frame.shape # getting height & width of the frame
                    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    output_handInrgb_image=detect_hand.process(rgb_frame)
                    hands=output_handInrgb_image.multi_hand_landmarks # getting each hqand containing 21 landmarks
                    if(hands):
                        mouse[0]=1
                        for hand in hands:
                            drawing_tools.draw_landmarks(frame,hand) # drawing the 21 landmarks of hand on the frame
                            landmarks=hand.landmark
                            for index,landmark_value in enumerate(landmarks): # storing each index and value from arry of landmark
                                x=int(landmark_value.x*frame_width)
                                y=int(landmark_value.y*frame_height)# getting position value in pixel for     MOVEMENT
                                if index==9:# cursor movement buttom of middle finger
                                    mouse[1],mouse[2]=landmark_value.x*display_width,landmark_value.y*display_height
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(255,255,255)) #BGR
                                elif index==4: #point out tip of thumb
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(25,250,25)) #BGR
                                    # drawing on frame ,center =intersection of x & y line ,radious 10 pixel
                                    y_thumb=y
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(25,250,25)) #BGR                              
                                elif index==8: #point out tip of index finger for     CLICK
                                    # drawing on frame ,center =intersection of x & y line ,radious 10 pixel
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(25,250,25)) #BGR
                                    y_index=y
                                    mouse[3]=abs(y_thumb-y)
                                    y=100
                                elif index==12: # middle finger
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(25,250,25)) #BGR
                                    mouse[5]=abs(y_index-y) # scrolll up
                                    y=100
                                elif index==5: # bottom of index 5 pinky finger
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(25,250,25)) #BGR
                                    mouse[6]=abs(y_thumb-y)   # scroll down
                                    y=100
                                elif index==20: # pinky finger
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(25,250,25)) #BGR
                                    mouse[4]=abs(y_thumb-y) # distance between thumb & middle finger for right click
                                    y=100
                    else:
                        mouse[0]=0
                    cv2.imshow(f"Thread-{self.thread_id} Video", frame)
                # Break the loop and stop capturing if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.is_running = False
                    start_flag=0
                    video_thread.stop()
                    control_mouse.stop()
            except:
                self.is_running = False
                video_thread.stop()
                control_mouse.stop()

        cv2.destroyAllWindows()
        print(f"Thread-{self.thread_id}: Video Play thread stopped.")
    def stop(self):
        self.is_running = False

class control_mouse_pointer(threading.Thread):
    def __init__(self, thread_id=2, device_id=0):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.device_id = device_id
        self.is_running = True
        self.action=[
            lambda:(pyautogui.click(),print("Clicked : ",threading.active_count()) ,pyautogui.sleep(0.2)),
            lambda:(pyautogui.scroll(-100),print("scroll down",mouse[6]),pyautogui.sleep(0.1) ),
            lambda:( pyautogui.scroll(100),print("scroll up",mouse[5]),pyautogui.sleep(0.1) ),
            lambda:(pyautogui.rightClick(),print("Right Clicked : ",threading.active_count()),pyautogui.sleep(0.4)),
                     ]    
    def ctl_action(self,selector):
        select=action_selector[selector]
        self.action[select]()
    def run(self):
        print(f"Thread-{self.thread_id}: Starting mouse control...")
        global mouse,sensi
        while self.is_running :
            if keyboard.is_pressed('ctrl+shift+c'):
                print("Quitting the loop.")
                video_thread.stop()
                video_play_thread.stop()
                control_mouse.stop()
                return 0
            if(mouse[1]<=display_width and mouse[2]<=display_height and mouse[1]and mouse[2] and mouse[0] ):
                pyautogui.moveTo(mouse[1],mouse[2])
            if mouse[3]<sensi[0] : # thumb & index                              ctl 0 : default action 0 (click)
                self.ctl_action(0)
            elif mouse[4]<sensi[1]: # thumb & pinky                             ctl 1 : default action 1 (right click)
                self.ctl_action(1)
            elif mouse[5]<sensi[2] and mouse[0] : # index & middle              ctl 2 : default action 2 (scroll up)
                self.ctl_action(2)
            elif mouse[6]<sensi[3] and mouse[0] : # thumb tip & index buttom    ctl 3 : default action 3 (scroll down)
                self.ctl_action(3)
    def stop(self):
        print(f"Thread-{self.thread_id}: mouse control thread stopped.")
        self.is_running = False

class controlVM():
    def __init__(self):
        print("hh")
    def start():
        global video_thread,control_mouse,video_play_thread
        video_thread = VideoCaptureThread(thread_id=1, device_id=0)
        video_play_thread = VideoPlayThread(thread_id=2, device_id=0)
        control_mouse=control_mouse_pointer(thread_id=3, device_id=0)
        video_thread.start()
        video_play_thread.start()
        control_mouse.start()
        return "Virtual Mouse is successfully started"
    def stop():
        global start_flag
        if start_flag:
            print("calling stop")
            video_play_thread.stop()
            video_play_thread.join()
            control_mouse.stop()
            control_mouse.join()
            video_thread.stop()
            video_thread.join() # added last rm if necessory
            cap.release()
            cv2.destroyAllWindows()
            return "Virtual Mouse is successfully stopped"
        return "Virtual Mouse is already stopped"
    def update(action_selected,sensi_selected):
        global action_selector,sensi
        action_selector=action_selected
        sensi=sensi_selected

        print(f"New config      actions: {action_selector}  sensitivity: {sensi_selected}")
        return "Updated configurations successfully"    
