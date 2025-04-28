#!/usr/bin/env python3
import rospy
import actionlib
from capstone_project.srv import NavigationServiceMessage,NavigationServiceMessageResponse,NavigationServiceMessageRequest
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PointStamped

def requestHandler(request:NavigationServiceMessageRequest):
    list = request.points_array
    for goal in list:
        x = goal.x
        y = goal.y
        send_goal(x, y)
            
    resp = NavigationServiceMessageResponse()
    resp.success = True
    resp.message = "Succes"
    return resp


def send_goal(x, y):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    client.wait_for_result()


if __name__=="__main__":
    rospy.init_node("navigation_service_node")
    service = rospy.Service("navigation_service",NavigationServiceMessage,requestHandler)
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("Waiting for move_base action server...")
    client.wait_for_server()
    rospy.loginfo("Connected to move_base.")
    rospy.spin()
