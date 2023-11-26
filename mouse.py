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
action=[0,1,2,3]# click,scrollDown,scrollUp,rightClick
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
        # self.capture = cv2.VideoCapture(self.device_id)
        global gframe,ghands # getting access of global varriables to edit
        self.frame=gframe
        self.hands=ghands
        self.is_running = True

    def run(self):
        print(f"Thread-{self.thread_id}: Starting video play...")
        # import mediapipe as mp # Using to detect hand
        global gframe,ghands,start_flag,mouse # getting access of global varriables to edit
        while self.is_running :
            # self.frame=gframe
            try:
                if start_flag:
                    # print(self.frame)
                    # if self.hands :
                    #     for hand in self.hands:
                    #         mp.solutions.drawing_utils.draw_landmarks(self.frame,hand) # drawing the 21 landmarks of hand on the frame
                    # cv2.imshow(f"Thread-{self.thread_id} Video", self.frame)
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
                                y=int(landmark_value.y*frame_height)
                                
                                
                                
                                #print("x = ",x,"y = ",y) # getting position value in pixel for     MOVEMENT
                                if index==4: #point out tip of thumb
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(25,250,25)) #BGR
                                    # drawing on frame ,center =intersection of x & y line ,radious 10 pixel
                                    y_thumb=y
                                    mouse[1],mouse[2]=landmark_value.x*display_width,landmark_value.y*display_height
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(25,250,25)) #BGR
                                    # xd,yd=landmark_value.x*display_width,landmark_value.y*display_height
                                    # if(xd<=display_width and yd<=display_height):
                                    #     pyautogui.moveTo(xd,yd)
                                
                                elif index==8: #point out tip of index finger for     CLICK
                                    # drawing on frame ,center =intersection of x & y line ,radious 10 pixel
                                    cv2.circle(img=frame,center=(x,y),radius=10,color=(25,250,25)) #BGR
                                    # dis_pointer_click=abs(y_thumb-y)
                                    y_index=y
                                    mouse[3]=abs(y_thumb-y)
                                    y=100
                                    # mouse[0]=1
                                    # print("index = ",y,"thumb= ",y_thumb ,"diff= ",dis_pointer_click)
                                    # print("Difference between thumb & index = ",dis_pointer_click)
                                    # if(dis_pointer_click<30):
                                    #     print("CLICKED\n")
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

    def run(self):
        print(f"Thread-{self.thread_id}: Starting mouse control...")
        global mouse,sensi
        while self.is_running :
            if keyboard.is_pressed('c'):
                print("Quitting the loop.")
                video_thread.stop()
                video_play_thread.stop()
                control_mouse.stop()
                return

            if(mouse[1]<=display_width and mouse[2]<=display_height and mouse[1]and mouse[2] and mouse[0] ):
                pyautogui.moveTo(mouse[1],mouse[2])
                # print("move ",xd,yd)
                # print(mouse[3])
            if mouse[3]<sensi[0] : # thumb & index
                print("Clicked : ",threading.active_count())
                # time.sleep(0.1)
                pyautogui.click() # click operation
                pyautogui.sleep(0.2)
            elif mouse[4]<sensi[1]: # thumb & pinky
                print("Right Clicked : ",threading.active_count())
                # time.sleep(0.1)
                pyautogui.rightClick() # click operation
                # pyautogui.scroll(-100)
                pyautogui.sleep(0.4)
            elif mouse[5]<sensi[2] and mouse[0] : # index & middle
                print("scroll up",mouse[5])
                pyautogui.scroll(100) # SCROLL UP
                pyautogui.sleep(0.1)
            elif mouse[6]<sensi[3] and mouse[0] : # thumb tip & index buttom   
                print("scroll down",mouse[6])
                pyautogui.scroll(-100) #scroll down
                pyautogui.sleep(0.1)
    # def ctl_pyautogui(self,selector):
        
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
            cap.release()
            cv2.destroyAllWindows()
            return "Virtual Mouse is successfully stopped"
        return "Virtual Mouse is already stopped"
    def update():
        global ctl,action
        return "Updated configurations successfully"    








def start_threads():
    # thread_cap()
    # cap=video_cap() # cv2 not working inside thread
    # Create a VideoCaptureThread
    global video_thread,control_mouse,video_play_thread
    video_thread = VideoCaptureThread(thread_id=1, device_id=0)
    # Start the video capture thread
    video_thread.start()
    # Create a VideoPlayThread
    video_play_thread = VideoPlayThread(thread_id=2, device_id=0)
    # Start the video play thread
    video_play_thread.start()

    # pyautogui
    control_mouse=control_mouse_pointer(thread_id=3, device_id=0)
    # start pyautogui operation
    control_mouse.start()
    # time.sleep(4)
    # stop_threads()

def stop_threads():
    print("calling stop")
    video_thread.stop()
    video_play_thread.stop()
    control_mouse.stop()
    cap.release()
    cv2.destroyAllWindows()

# start_threads()

# class controlVM():
#     def __init__(self):
#         print("hh")
# def start():
#     global video_thread,control_mouse,video_play_thread
#     video_thread = VideoCaptureThread(thread_id=1, device_id=0)
#     video_play_thread = VideoPlayThread(thread_id=2, device_id=0)
#     control_mouse=control_mouse_pointer(thread_id=3, device_id=0)
#     video_thread.start()
#     video_play_thread.start()
#     control_mouse.start()
#     return "Virtual Mouse is successfully started"

# def stop():
#     global start_flag
#     if start_flag:
#         print("calling stop")
#         video_play_thread.stop()
#         video_play_thread.join()
#         control_mouse.stop()
#         control_mouse.join()
#         video_thread.stop()
#         cap.release()
#         cv2.destroyAllWindows()
#         return "Virtual Mouse is successfully stopped"
#     return "Virtual Mouse is already stopped"
# ctl=controlVM()
# start()
# time.sleep(5)
# stop()
def move_cursor(frame,hands) :  
    frame_height,frame_width,_=frame.shape # getting height & width of the frame
    if(hands):
        for hand in hands:
            drawing_tools.draw_landmarks(frame,hand) # drawing the 21 landmarks of hand on the frame
            landmarks=hand.landmark
            for index,landmark_value in enumerate(landmarks): # storing each index and value from arry of landmark
                #print("x = ",x,"y = ",y) # getting fractional value [left Most=0,1=right Most in frame] but we need pixel / position respect to the frame to draw
                x=int(landmark_value.x*display_width)# position along x axis
                y=int(landmark_value.y*display_height)# along y axis
                
                #print("x = ",x,"y = ",y) # getting position value in pixel for     MOVEMENT
                if index==4: #point out tip of thumb
                    y_thumb=y
                    if(x<=display_width and y<=display_height):
                        pyautogui.moveTo(x,y)
                if index==8: #point out tip of index finger for     CLICK
                    click=40 # clicking distance between two points
                    dis_pointer_click=abs(y_thumb-y)
                    print("index = ",y,"thumb= ",y_thumb ,"diff= ",dis_pointer_click)
                    if(dis_pointer_click<click):
                        print("CLICKED\n")
                        pyautogui.click() # click operation
                        pyautogui.sleep(0.1)
    

def video_cap() : 
    ignore,frame=cap.read()
    frame=cv2.flip(frame,1) # flip the frame on y=1 axis
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    output_handInrgb_image=detect_hand.process(rgb_frame)
    hands=output_handInrgb_image.multi_hand_landmarks # getting each hqand containing 21 landmarks
    global gframe,ghands,ggg # getting access of global varriables to edit
    gframe,ghands=frame,hands
    ggg=888
    return frame,hands

def show_frames(frame,hands) : 
    frame_height,frame_width,_=frame.shape # getting height & width of the frame
    if(hands):
        for hand in hands:
            drawing_tools.draw_landmarks(frame,hand) # drawing the 21 landmarks of hand on the frame
            landmarks=hand.landmark
            for index,landmark_value in enumerate(landmarks): # storing each index and value from arry of landmark
                x_frac=landmark_value.x # position along x axis
                y_frac=landmark_value.y # along y axis
                x=int(x_frac*frame_width)
                y=int(y_frac*frame_height)
                
                #print("x = ",x,"y = ",y) # getting position value in pixel for     MOVEMENT
                if index==4: #point out tip of thumb
                    # drawing on frame ,center =intersection of x & y line ,radious 10 pixel
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(255,50,25)) #BGR
                if index==8: #point out tip of index finger for     CLICK
                    # drawing on frame ,center =intersection of x & y line ,radious 10 pixel
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(255,50,25)) #BGR
    cv2.imshow('Virtual mouse',frame)


def thread_cap():
    import cv2
    import mediapipe as mp # Using to detect hand
    cap=cv2.VideoCapture(0) # 0 => first video source
    detect_hand=mp.solutions.hands.Hands() # getting hand detector
    while True:
        get_frame,get_hands=video_cap()

def thread_show():
    while True:
        global gframe,ghands,ggg
        if(gframe and ghands):
            show_frames(gframe,ghands)
        else:
            print("waiting\n",ggg)
            time.sleep(0.2)
def thread_move():
    while True:
        move_cursor(gframe,ghands)

def manual():
    while True:
        get_frame,get_hands=video_cap()
        show_frames(gframe,ghands)
        move_cursor(get_frame,get_hands)
        exit = cv2.waitKey(1) & 0xFF
        if exit ==ord('x'):
            break
        elif exit ==ord('q'):
            break
# run only one of below
# manual()



cap.release()
cv2.destroyAllWindows()




class control_mouse_pointer1(threading.Thread): # low speed
    def __init__(self, thread_id=2, device_id=0):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.device_id = device_id
        # self.capture = cv2.VideoCapture(self.device_id)
        global gframe,ghands,start_flag # getting access of global varriables to edit
        self.frame=gframe
        self.hands=ghands
        self.is_running = True

    def run(self):
        print(f"Thread-{self.thread_id}: Starting mouse control...")
        while self.is_running :
            global gframe,ghands,start_flag,ghands # getting access of global varriables to edit
            self.frame=gframe
            # print("mcotrl")
            if start_flag:
                frame=self.frame
                frame_height,frame_width,_=frame.shape # getting height & width of the frame
                hands=ghands
                if(hands):
                    for hand in hands:
                        landmarks=hand.landmark
                        for index,landmark_value in enumerate(landmarks): 
                            x=int(landmark_value.x*frame_width)
                            y=int(landmark_value.y*frame_height)
                            
                            #print("x = ",x,"y = ",y) # getting position value in pixel for     MOVEMENT
                            if index==4: #point out tip of thumb
                                # drawing on frame ,center =intersection of x & y line ,radious 10 pixel
                                y_thumb=y
                            if index==8: #point out tip of index finger for     CLICK
                                dis_pointer_click=abs(y_thumb-y)
                                if(dis_pointer_click<30):
                                    print("CLICKED hdhtg\n")


    def stop(self):
        print(f"Thread-{self.thread_id}: mouse control thread stopped.")
        self.is_running = False
