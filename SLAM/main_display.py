from tkinter import *
import tkinter as tk
import sys
USER='Owner'
USER_CLIENT='nanorobo'

class Display:
    def __init__(self,win):
        self.fg_buttons = 'White'
        self.bg_buttons = "Black"
        self.size_buttons = 17
        self.font_buttons = 'Areil'

        self.FS_BUTTON_X_BACK = 0
        self.FS_BUTTON_Y_BACK = 0
        self.STRING_BUTTON_BACK = "BACK"
        self.FACK_X=100
        self.FACK_Y=20

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
        ### Buttons
        A = tk.Button(win, text=self.A_text, fg=self.fg_buttons, bg=self.bg_buttons,
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

        # LINEs
        # canvas = Canvas(win)
        # canvas.create_line(100, 200, 200, 35, fill="green", width=2)
        # canvas.pack()


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
        print(node_name)



if __name__=="__main__":
    """  DISPLAY """
    window = Tk()
    window.geometry("800x480")
    window.configure(background='black')
    window.title("WETTER")
    if USER == USER_CLIENT:
        window.attributes("-fullscreen", True)
    gui=Display(window)
    gui.first_screen(window)
    gui.release_windows(window)