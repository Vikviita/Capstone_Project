#!/usr/bin/env python3
import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import PointStamped
import tkinter as tk
from tkinter import Listbox
from capstone_project.srv import NavigationServiceMessage,NavigationServiceMessageResponse,NavigationServiceMessageRequest


points=[]

def add_point(msg:PointStamped):
    points.append(msg.point)
    point = PointStamped()
    point.header.frame_id = f"map"
    point.header.stamp = rospy.Time.now()
    point.point.x = msg.point.x
    point.point.y = msg.point.y
    point.point.z = msg.point.z
    pub.publish(point)

def on_button_pressed():
    rospy.loginfo("Start button pressed!")
    request = NavigationServiceMessageRequest()
    request.points_array = points
    service(request)
    sub.unregister()
    root.destroy()


def on_shutdown():
    root.destroy()
    

def on_point_clicked(msg:PointStamped):
    if points.__len__() != 10:
        point_str = f"({msg.point.x:.2f}, {msg.point.y:.2f}, {msg.point.z:.2f})"
        rospy.loginfo(f"Clicked: {point_str}")
        add_point(msg)
        listbox.insert(tk.END, point_str)
    else:
        listbox.insert(tk.END,"MAX")

if __name__ == '__main__':
    rospy.init_node('start_button_node', anonymous=True)
    sub = rospy.Subscriber("/clicked_point",PointStamped,on_point_clicked)
    pub = rospy.Publisher("/point_stamped",PointStamped,queue_size=20)
    service = rospy.ServiceProxy("navigation_service",NavigationServiceMessage)
    


    root = tk.Tk()
    root.title("Rviz Point Viewer")
    
    listbox = Listbox(root, width=40, height=15)
    listbox.pack(pady=10)

    start_button = tk.Button(root, text="Start", command=on_button_pressed, height=5, width=20)
    start_button.pack(pady=20)
    
    rospy.loginfo("GUI ready. Waiting for button press.")
    rospy.on_shutdown(on_shutdown)
    root.mainloop()
    rospy.spin()

    
