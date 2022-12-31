import math
import numpy as np

##############################################################################################
#######################################   THETA        #######################################
##############################################################################################

class EKFDeniTheta:
    def __init__(self):
        self.A_k_minus_1 = np.array([[1.]])  # Expresses how the state of the system [yaw] changes,identity matrix
        self.process_noise_v_k_minus_1 = np.array([0.01])  # noice by comands, big=big predict error
        self.Q_k = np.array([[1.0]])  # 2.0 #State model noise covariance matrix Q_k,   big believe in measurment
        self.H_k = np.array([[1.0]])  # predicted state estimate at time k, 0.91= is more, 1= is less(estimate positiion)
        self.R_k = np.array([[0.0001]])  # Sensor measurement noise covariance matrix R_k
        self.sensor_noise_w_k = np.array([0.01])

        self.state_estimate_k_minus_1 = np.array([math.radians(0)])  # [ radians] ,start position
        self.control_vector_k_minus_1 = np.array([math.radians(1)])  # [v, yaw_rate] [meters/second, radians/second]
        self.P_k_minus_1 = np.array([[0.3]]) # accuracy of the state estimate at time k
        self.end_position=0
    def getB(self,delta_theta):
        B = np.array([[math.radians(delta_theta)]])
        return B

    def ekf(self,z_k_observation_vector, state_estimate_k_minus_1,
            control_vector_k_minus_1, P_k_minus_1):
        # predict step
        state_estimate_k = self.A_k_minus_1 @ (state_estimate_k_minus_1) + (self.getB(state_estimate_k_minus_1[0])) @ (
            control_vector_k_minus_1) + (self.process_noise_v_k_minus_1)
        #print(f'Before EKF={math.degrees(state_estimate_k):.3f}')
        P_k = self.A_k_minus_1 @ P_k_minus_1 @ self.A_k_minus_1.T + (self.Q_k)
        # update
        measurement_residual_y_k = z_k_observation_vector - ((self.H_k @ state_estimate_k) + (self.sensor_noise_w_k))
        #print(f'Measurment={math.degrees(z_k_observation_vector):.3f}')
        # Calculate the measurement residual covariance
        S_k = self.H_k @ P_k @ self.H_k.T + self.R_k
        K_k = P_k @ self.H_k.T @ np.linalg.pinv(S_k)
        state_estimate_k = state_estimate_k + (K_k @ measurement_residual_y_k)

        # if z_k_observation_vector  > :
        #     state_estimate_k=

        P_k = P_k - (K_k @ self.H_k @ P_k)
        after = math.degrees(state_estimate_k)
        # if after<0:
        #     after=360+after
        #print(f'After EKF={after:.3f}')
        self.end_position=after
        return state_estimate_k, P_k

    def calculate_error_turning(self,z_k):
        """
        get the measured angle and return the corection of the angle with EKF
        :param z_k: np.array[[theta in radians],]
        :return: final position after calculation
        """
        for obs_vector_z_k in z_k:
            #print('Class ekf')
            optimal_state_estimate_k, covariance_estimate_k = self.ekf(math.radians(obs_vector_z_k),
                                                                  self.state_estimate_k_minus_1, self.control_vector_k_minus_1,
                                                                  self.P_k_minus_1, )
            # update matrices
            self.state_estimate_k_minus_1 = optimal_state_estimate_k
            self.P_k_minus_1 = covariance_estimate_k

        return self.end_position



##################################################################################################
#######################################   COORDIANTES      #######################################
##################################################################################################



import math
from math import tan, sin, cos, sqrt, atan2
from filterpy.kalman import MerweScaledSigmaPoints
import numpy as np
from filterpy.kalman import UnscentedKalmanFilter as UKF
from filterpy.stats import plot_covariance_ellipse


class UKFDeni:
    def __init__(self):
        self.dt=1
        self.wheelbase=0.18
        self.end_x=0
        self.end_y=0
        self.end_theta=0
        self.start_x = 0
        self.start_y = 0
        self.start_theta = 0
        self.track=[]
        self.VELOCITY=1.09 # cm/sec ili dist 1.24
        #######
        self.sigma_vel = 0.5,
        self.sigma_steer = np.radians(1)
        self.sigma_range = 200
        self.sigma_bearing = .01
        self.step = 1
        self.ellipse_step = 10

    def pi_to_pi(self,x):
        # x in radians
        """
        convert -180,180 to 0-360

        :param x: angle in radians
        :return:
        """
        x = x % 360
        return x


    def move_steering(self,x, dt, u, wheelbase):
        """
        this is for =>  state transition function f(x).
        imitate the moving of the robot
        :param x: position [x,y]
        :param dt: time interval
        :param u: control motion  u=[v,alpha].T
        :param wheelbase: how wide is the robot base
        :return: robot goes ahead or turning
        """
        hdg = x[2]
        vel = u[0]
        # print(f"vel= {u[1]}")
        steering_angle = u[1]
        dist = vel * dt
        if abs(steering_angle) > 0.001:  # is robot turning?
            beta = (dist / wheelbase) * tan(steering_angle)
            r = wheelbase / tan(steering_angle)  # radius

            sinh, sinhb = sin(hdg), sin(hdg + beta)
            cosh, coshb = cos(hdg), cos(hdg + beta)
            return x + np.array([-r * sinh + r * sinhb, r * cosh - r * coshb, beta])
        else:  # moving in straight line
            return x + np.array([dist * cos(hdg), dist * sin(hdg), 0])

    def move(self,x, dt, u, wheelbase):
        """
        move rotation my car
        this is for =>  state transition function f(x).
        imitate the moving of the robot
        :param x: position [x,y,Theta]
        :param dt: time interval
        :param u: control motion  u=[velcity,alpha].T
        :param wheelbase: how wide is the robot base
        :return: robot goes ahead or turning
        """

        hdg = x[2]  # theta
        vel = u[0]
        steering_angle = u[1]
        dist = vel * dt
        error_turning=3
        # if steering_angle !=0:
        #     steering_angle=math.radians(math.degrees(steering_angle)+error_turning)
        if abs(steering_angle) > 0.001:  # is robot turning?
            # beta = (dist / wheelbase) * tan(steering_angle)
            beta = steering_angle
            r = wheelbase / tan(steering_angle)  # radius
            sinh, sinhb = sin(hdg), sin(hdg)
            cosh, coshb = cos(hdg), cos(hdg)
            # return x + np.array([-r*sinh + r*sinhb, r*cosh - r*coshb, beta])
            # return x + np.array([dist * cos(hdg), dist * sin(hdg), hdg])
            return x + np.array([dist * cos(steering_angle), dist * sin(steering_angle), steering_angle - hdg])

        else:  # moving in straight line
            # print(x + np.array([dist*cos(hdg), dist*sin(hdg), 0]))
            return x + np.array([dist * cos(hdg), dist * sin(hdg), 0])

    def normalize_angle_steering(self,x):
        """
        x: shoud be in radians
        this funktion handle the different 360-1 degre"""
        x = x % (2 * np.pi)  # force in range [0, 2 pi)
        if x > np.pi:  # move to [-pi, pi)
            x -= 2 * np.pi
        return x

    def normalize_angle(self,x):
        """
        x: shoud be in radians
        this funktion handle the different 360-1 degre"""
        x = x % (2 * np.pi)  # force in range [0, 2 pi)
        if x > np.pi:  # move to [-pi, pi)
            x -= 2 * np.pi
        return x

    def residual_h(self,a, b):
        """The state vector has the bearing at index 2, but the measurement vector has it at index 1,
         so we need to write functions to handle each."""
        y = a - b
        # data in format [dist_1, bearing_1, dist_2, bearing_2,...]
        for i in range(0, len(y), 2):
            y[i + 1] = self.normalize_angle(y[i + 1])
        return y

    def residual_x(self,a, b):
        """The state vector has the bearing at index 2, but the measurement vector has it at index 1,
         so we need to write functions to handle each."""
        y = a - b
        y[2] = self.normalize_angle(y[2])
        return y

    def Hx_old(self,x, landmarks):
        """
        x:[x,y,angle]
        landmarks:
        return : [dist_to_1, bearing_to_1, dist_to_2, bearing_to_2, ...].
         takes a state variable and returns the measurement
        that would correspond to that state. """
        hx = []
        for lmark in landmarks:
            px, py = lmark
            dist = sqrt((px - x[0]) ** 2 + (py - x[1]) ** 2)
            angle = atan2(py - x[1], px - x[0])
            hx.extend([dist, self.normalize_angle(angle - x[2])])
        return np.array(hx)

    def Hx(self,x, landmarks):
        """
        x:[x,y,angle]
        landmarks:
        return : [dist_to_1, bearing_to_1, dist_to_2, bearing_to_2, ...].
         takes a state variable and returns the measurement
        that would correspond to that state. """
        hx = []
        for lmark in landmarks:
            px, py = lmark
            # dist = sqrt((px - x[0]) ** 2 + (py - x[1]) ** 2)
            # angle = atan2(py - x[1], px - x[0])
            dist=px
            angle=py
            hx.extend([dist, self.normalize_angle(angle - x[2])])
        return np.array(hx)

    def state_mean(self,sigmas, Wm):
        """

        :param sigmas:
        :param Wm:
        :return:
        """

        x = np.zeros(3)

        sum_sin = np.sum(np.dot(np.sin(sigmas[:, 2]), Wm))
        sum_cos = np.sum(np.dot(np.cos(sigmas[:, 2]), Wm))
        x[0] = np.sum(np.dot(sigmas[:, 0], Wm))
        x[1] = np.sum(np.dot(sigmas[:, 1], Wm))
        x[2] = atan2(sum_sin, sum_cos)
        return x

    def z_mean(self,sigmas, Wm):
        """

        :param sigmas:
        :param Wm:
        :return:
        """
        z_count = sigmas.shape[1]
        x = np.zeros(z_count)

        for z in range(0, z_count, 2):
            sum_sin = np.sum(np.dot(np.sin(sigmas[:, z + 1]), Wm))
            sum_cos = np.sum(np.dot(np.cos(sigmas[:, z + 1]), Wm))

            x[z] = np.sum(np.dot(sigmas[:, z], Wm))
            x[z + 1] = atan2(sum_sin, sum_cos)
        return x

    def localization_correction(self,direction,dist,landmarks):
        """
        :param direction: which direction to go 0-360 degrees
        :param dist: how far in cm
        :param landmarks: [[x,y],[x,y]]
        :return: new x, y ,theta info
        """

        angle_radians = math.radians(direction)

        if dist==0 and direction !=0: # by turning the lidar goes away from the center of turning
            dist+=4
        elif dist==0:
            dist=1

        cmds = [[self.VELOCITY, angle_radians]] * dist
        points = MerweScaledSigmaPoints(n=3, alpha=.01, beta=2, kappa=10,
                                        subtract=self.residual_x)
        ukf = UKF(dim_x=3, dim_z=2 * len(landmarks), fx=self.move, hx=self.Hx,
                  dt=self.dt, points=points, x_mean_fn=self.state_mean,
                  z_mean_fn=self.z_mean, residual_x=self.residual_x,
                  residual_z=self.residual_h)

        ukf.x = np.array([self.start_x, self.start_y, math.radians(self.start_theta)])  # [2, 6, .3] # here is the start position and orientation
        ukf.P = np.diag([4, 4, 0.3]) #4,4,0.3
        ukf.R = np.diag([self.sigma_range ** 2,
                         self.sigma_bearing ** 2] * len(landmarks))
        ukf.Q = np.eye(3) * 0.0001 # 0.0001
        ukf.Q[0,0]= 0.1 #x
        ukf.Q[1,1]= 0.1 # y
        ukf.Q[2,2]= 0.1 # theta


        sim_pos = ukf.x.copy()
        #################
        # if len(landmarks) > 0:
        #     plt.scatter(landmarks[:, 1], landmarks[:, 0], s=30)
        self.track = [] # track the current comand of moving
        for i, u in enumerate(cmds):
            sim_pos = self.move(sim_pos, self.dt, u, self.wheelbase)
            self.track.append(sim_pos)
            if i % self.step == 0:
                ukf.predict(u=u, wheelbase=self.wheelbase)
                if i % self.ellipse_step == 0:
                    pass
                    #plot_covariance_ellipse(
                      #  (ukf.x[1], ukf.x[0]), ukf.P[0:2, 0:2], std=6,
                      #  facecolor='k', alpha=0.3)

                x, y = sim_pos[1], sim_pos[0]
                z = []

                for d,a in landmarks:
                    z.extend([d, a])
                ukf.update(z, landmarks=landmarks)
                if i % self.ellipse_step == 0:
                    pass
                    #plot_covariance_ellipse(
                     #   (ukf.x[1], ukf.x[0]), ukf.P[0:2, 0:2], std=6,facecolor='g', alpha=0.8)

        self.track = np.array(self.track)
        self.end_x=ukf.x[0]
        self.end_y=ukf.x[1]
        self.end_theta=self.pi_to_pi(math.degrees(ukf.x[2]))
        self.start_x = self.end_x
        self.start_y = self.end_y
        self.start_theta = self.end_theta
        return self.end_x, self.end_y, self.end_theta







