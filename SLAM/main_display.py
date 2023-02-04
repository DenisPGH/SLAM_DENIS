import datetime
import time
from tkinter import *
import tkinter as tk
import os
import sys
USER='Owner'
USER_SERVER='Owner'

class Robo:
    def __init__(self):
        pass
    def robo_test(self,target_node):
        """
        test functon return true if the target is reached
        :return:
        """
        time.sleep(5)
        orientation=90
        return True,orientation

class Display:
    def __init__(self,win):
        self.robo=Robo()
        self.datetime_ = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.fg_buttons = 'White'
        self.bg_buttons = "Black"
        self.size_buttons = 17
        self.font_buttons = 'Areil'

        self.FS_BUTTON_X_BACK = 0
        self.FS_BUTTON_Y_BACK = 0
        self.STRING_BUTTON_BACK = "BACK"
        self.FACK_X=100
        self.FACK_Y=20
        self.interval_refresh_page=2

        self.A_x=50+self.FACK_X
        self.A_y=50+self.FACK_Y
        self.A_text="A"

        self.B_x = 450+self.FACK_X
        self.B_y = 50+self.FACK_Y
        self.B_text = "B"

        self.C_x = 50+self.FACK_X
        self.C_y = 350+self.FACK_Y
        self.C_text = "C"

        self.D_x = 450+self.FACK_X
        self.D_y = 350+self.FACK_Y
        self.D_text = "D"
        self.TIME_X=200
        self.TIME_Y=0

        self.CURRENT_NODE_NAME='A'
        self.CURRENT_NODE_NAME_FG='White'
        self.CURRENT_NODE_NAME_BG='Red'

        self.buttons_color={self.A_text:self.bg_buttons,
                            self.B_text:self.bg_buttons,
                            self.C_text:self.bg_buttons,
                            self.D_text:self.bg_buttons,}



    def clean_screen_function(self,win):
        """
        cleen the screen
        :param win: current windows
        :return:
        """
        for each in win.winfo_children():
            each.destroy()

    def first_screen(self,win):
        """ this function start our first windows view 800x480"""
        self.clean_screen_function(win)
        self.back_button(win)
        #### TIME
        time_label = Label(win, text=self.datetime_, fg=self.fg_buttons, bg=self.bg_buttons, relief="groove", borderwidth=2, bd=0)
        time_label.config(font=(f"{self.datetime_}", 30), text=self.datetime_)
        time_label.pack()
        time_label.place(x=self.TIME_X, y=self.TIME_Y)
        ### Buttons
        A = tk.Button(win, text=self.A_text, fg=self.fg_buttons, bg=self.buttons_color[self.A_text],
                             command=lambda: self.command_to_robo(self.A_text))
        A.config(font=(f"{self.font_buttons}", self.size_buttons))
        A.pack()
        A.place(x=self.A_x, y=self.A_y)

        B = tk.Button(win, text=self.B_text, fg=self.fg_buttons, bg=self.bg_buttons,
                      command=lambda: self.command_to_robo(self.B_text))
        B.config(font=(f"{self.font_buttons}", self.size_buttons))
        B.pack()
        B.place(x=self.B_x, y=self.B_y)

        C = tk.Button(win, text=self.C_text, fg=self.fg_buttons, bg=self.bg_buttons,
                      command=lambda: self.command_to_robo(self.C_text))
        C.config(font=(f"{self.font_buttons}", self.size_buttons))
        C.pack()
        C.place(x=self.C_x, y=self.C_y)

        D = tk.Button(win, text=self.D_text, fg=self.fg_buttons, bg=self.bg_buttons,
                      command=lambda: self.command_to_robo(self.D_text))
        D.config(font=(f"{self.font_buttons}", self.size_buttons))
        D.pack()
        D.place(x=self.D_x, y=self.D_y)


        self._update_function(A,self.A_text,self.buttons_color[self.A_text],self.A_text)
        self._update_function(B,self.B_text,self.buttons_color[self.B_text],self.B_text)
        self._update_function(C,self.C_text,self.buttons_color[self.C_text],self.C_text)
        self._update_function(D,self.D_text,self.buttons_color[self.D_text],self.D_text)
        self._update_function_time(time_label)


    def _update_function(self,button,node_name,color,text):
        """
        function for the update the screens

        :param button: name of the dynamic function
        :param node_name: index in the system for searching
        :param color: back groud color of the node
        :param text: text of the node
        :return:
        """

        """ """

        button.config(text=text,bg=self.buttons_color[node_name])
        button.after(self.interval_refresh_page, self._update_function,button,node_name,color,text)


    def _update_function_time(self,label):
        """
        function for the update the screens
        :param label: name of the dynamic label
        :param text: actual time
        :return:
        """
        """ """
        label.config(text=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        label.after(self.interval_refresh_page, self._update_function_time,label)


    def release_windows(self,win):
        """
        :param win - cur windows
        this have to be last to show the screen
        :return:
        """
        win.mainloop()

    def terminate(self):
        """
        terminate the program, have to add code 1234
        :return:
        """
        sys.exit()


    def back_button(self,win):

        # BACK BUTTON to first screen
        but = tk.Button(win, text=self.STRING_BUTTON_BACK, fg="Red", bg='Black', command=lambda: self.terminate())
        but.config(font=(f"{self.font_buttons}", self.size_buttons))
        but.pack()
        but.place(x=self.FS_BUTTON_X_BACK, y=self.FS_BUTTON_Y_BACK)


    def command_to_robo(self,node_name):
        """
        sent to witch node have to move the robot base
        :param node_name: name of the node
        :return: nothing
        """
        """ send to robo brain"""
        is_reach,orientation=self.robo.robo_test(node_name)
        if is_reach==True:
            print('rotate')
            self.rotation_commands(orientation)
            # change color and location
            self.CURRENT_NODE_NAME=node_name
            self.buttons_color[node_name]=self.CURRENT_NODE_NAME_BG
            for node in self.buttons_color.keys():
                if node !=node_name:
                    self.buttons_color[node] = self.bg_buttons

            print(f"I am on {self.CURRENT_NODE_NAME}")


    def rotation_commands(self,angle):
        """
        set the HDMI display to wished orientation with bash command
        :param angle: 0-360
        :return:
        """
        up_left=340
        up_right=20

        right_up=80
        right_down=100

        down_right=170
        down_left=200

        left_up=280
        left_down=260
        if USER !=USER_SERVER:
            if up_left<=angle==360 or 0<= angle<up_right:
                os.system('xrandr --output HDMI1 --rotate up')

            elif right_up<=angle<=right_down:
                os.system('xrandr --output HDMI1 --rotate left')

            elif down_left<= angle <=down_right:
                os.system('xrandr --output HDMI1 --rotate down')

            elif left_down<=angle<=left_up:
                os.system('xrandr --output HDMI1 --rotate right')
            else:
                os.system('xrandr --output HDMI1 --rotate up')

        else:
            print("rotation here")





if __name__=="__main__":
    """  DISPLAY xrandr --output HDMI1 --rotate right"""
    window = Tk()
    window.geometry("800x480")
    window.configure(background='black')
    window.title("WETTER")
    if USER != USER_SERVER:
        window.attributes("-fullscreen", True)
    gui=Display(window)
    gui.first_screen(window)
    gui.release_windows(window)