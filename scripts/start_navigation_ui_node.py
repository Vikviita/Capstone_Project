#!/usr/bin/env python3
import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import Point
import tkinter as tk
from tkinter import Listbox
from capstone_project.srv import NavigationServiceMessage,NavigationServiceMessageResponse,NavigationServiceMessageRequest


points=[]
max_count = 10
sub = None

def on_button_pressed():
    rospy.loginfo("Start button pressed!")
    if points.__len__() == 0:
         rospy.loginfo("List is empty")
         return
    request = NavigationServiceMessageRequest()
    request.points_array = points
    start_button.config(state='disabled')
    sub.unregister()
    res = service(request)
    rospy.loginfo(res.message)
    clear_all_goals()
    start_button.config(state='normal')


def on_shutdown():
    root.destroy()
    
def clear_all_goals(is_copy:bool = False):
    i = 1
    global sub
    if is_copy:
        sub.unregister()
    listbox.insert(tk.END, "Clear all points")
    while(i<=max_count):
        rospy.loginfo("deleted")
        point = PointStamped()
        point.header.frame_id = f"map"
        point.header.stamp = rospy.Time.now() + rospy.Duration(i * 0.001)
        point.point.x = -1000
        point.point.y = -1000
        point.point.z = 0
        pub.publish(point)
        i+=1
    if is_copy:
        for point in points:
          pointSt = PointStamped()
          pointSt.header.frame_id = f"map"
          pointSt.header.stamp = rospy.Time.now() + rospy.Duration(i * 0.001) 
          pointSt.point = point 
          pub.publish(pointSt)
    else:
        points.clear()
        rospy.loginfo(f"List size={points.__len__()}")
        listbox.insert(tk.END, "All points are cleared")
    sub = rospy.Subscriber("/clicked_point",PointStamped,on_point_clicked)
    


def on_point_clicked(msg:PointStamped):
        if points.__len__() != max_count:
            point_str = f"({msg.point.x:.2f}, {msg.point.y:.2f}, {msg.point.z:.2f})"
            rospy.loginfo(f"Clicked: {point_str}")
            points.append(msg.point)
            listbox.insert(tk.END, point_str)
        else:
            clear_all_goals(is_copy=True)
            listbox.insert(tk.END,"MAX")

if __name__ == '__main__':
    rospy.init_node('start_button_node', anonymous=True)
    sub = rospy.Subscriber("/clicked_point",PointStamped,on_point_clicked)
    pub = rospy.Publisher("/clicked_point",PointStamped)
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

    
