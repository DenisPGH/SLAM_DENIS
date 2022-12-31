import math


def coordinates_from_x_y_distance_and_angle(x_base,y_base,angle,distance):
    """
    :param x_base: where is lidar on x
    :param y_base: where is lidar on y
    :param angle: in degree ,0 is +y
    :param distance: from lidar to the point
    :return: new coordiantes of the found point
    """
    final_x,final_y=0,0
    new_x=distance*math.sin(math.radians(angle))
    new_y=distance*math.cos(math.radians(angle))
    final_x=x_base+new_x
    final_y=y_base+new_y
    final_x=round(final_x,2)
    final_y=round(final_y,2)
    if final_x ==0 or final_x==-0:
        final_x=0
    if final_y ==0 or final_y==-0:
        final_y=0
    return final_x,final_y


a=coordinates_from_x_y_distance_and_angle(-1,1,90,5)
print(a)




