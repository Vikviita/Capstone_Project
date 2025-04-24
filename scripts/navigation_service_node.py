#!/usr/bin/env python3
import rospy
from capstone_project.srv import NavigationServiceMessage,NavigationServiceMessageResponse,NavigationServiceMessageRequest

def requestHandler(request:NavigationServiceMessageRequest):
    list = request.points_array
    for i, point in enumerate(list):
            rospy.loginfo("SENDING TO NAVIGATION %d: x=%.2f, y=%.2f , z=%.2f", i+1, point.x, point.y,point.z)
    resp = NavigationServiceMessageResponse()
    resp.success = True
    resp.message = "Succes"
    return resp



if __name__=="__main__":
    rospy.init_node("navigation_service_node")
    service = rospy.Service("navigation_service",NavigationServiceMessage,requestHandler)
    rospy.spin()
