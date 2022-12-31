import math


class Helfer:
    def __init__(self):
        pass
    def update_new_coordinates_from_theta_and_dist(self,orientation,x,y,theta,distance):
        
        """
        for update line of the robot path in Plot
        :param orientation: which dir in the world
        :param x: act x position
        :param y: act y position
        :param theta: degree diference last postion
        :param distance: distance in cm from last until new position
        :return: new x,new y
        """
        
        new_x,new_y=self.coordinates_new_pos_car(x,y,theta,distance)
        return new_x,new_y



    def coordinates_from_x_y_distance_and_angle(self,orientation_angle,x_base, y_base, angle, distance):
        """
        :param orientation_angle: which direction in the world is oriented the robot
        :param x_base: where is lidar on x
        :param y_base: where is lidar on y
        :param angle: in degree ,0 is +y
        :param distance: from lidar to the point
        :return: new coordiantes of the found point
        """

        new_x = distance * math.sin(math.radians(angle+orientation_angle))
        new_y = distance * math.cos(math.radians(angle+orientation_angle))




        final_x = x_base + new_x
        final_y = y_base + new_y
        final_x = round(final_x, 2)
        final_y = round(final_y, 2)
        if final_x == 0 or final_x == -0:
            final_x = 0
        if final_y == 0 or final_y == -0:
            final_y = 0
        return final_x, final_y

    
    def coordinates_new_pos_car(self,x_base, y_base, angle, distance):
        """
        :param orientation_angle: which direction in the world is oriented the robot
        :param x_base: where is lidar on x
        :param y_base: where is lidar on y
        :param angle: in degree ,0 is +y
        :param distance: from lidar to the point
        :return: new coordiantes of the found point
        """

        new_x = distance * math.sin(math.radians(angle))
        new_y = distance * math.cos(math.radians(angle))
        final_x = x_base + new_x
        final_y = y_base + new_y
        final_x = round(final_x, 2)
        final_y = round(final_y, 2)
        if final_x == 0 or final_x == -0:
            final_x = 0
        if final_y == 0 or final_y == -0:
            final_y = 0
        return final_x, final_y



# a=Helfer()
# b=a.coordinates_from_x_y_distance_and_angle(45,0,0,0,5)
# print(f" x= {b[0]} | y= {b[1]}")