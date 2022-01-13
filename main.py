#from __future__ import division
from tkinter import *
import sys
import tkinter as tk
import time
#import Adafruit_PCA9685
from threading import Thread
import random
import tkinter.scrolledtext as st


'''
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
pulse=1935
def move_to_initial():
    #move to initial position
    pulse=1935
    pwm.set_pwm(0, pulse, 4096-pulse)
    time.sleep(0.1)
    pwm.set_pwm(1, pulse, 4096-pulse)
    time.sleep(0.1)
    pwm.set_pwm(2, pulse, 4096-pulse)
    time.sleep(0.1)
    pwm.set_pwm(3, pulse, 4096-pulse)
    time.sleep(0.1)
move_to_initial()  
'''

#global variables

choice=""
speed=50
t=0
same_arm_time=1.15
diff_arm_time=0.525
waiting_time=0.4
running=False
seconds=0
minutes=0
begin=False
enterd_combination=""
learning_combos=[]

'''
def servo():
    global waiting_time
    global same_arm_time
    global diff_arm_time
    global running
    global learning_combos
    if choice=="s":
        combos=[]
        with open('combos.txt') as file:
            lines=file.readlines()
        
        for line in lines:
            combos.append(line)
        
        file.close()
    
        choices=random.choices(combos,k=len(combos))
        previous=0
        while True:
            for moves in choices:
                moves=moves.strip("\n")
                channels=moves.split(",")
                for i in channels:
                    if i==previous:
                        time.sleep(same_arm_time)
                    else:
                        time.sleep(diff_arm_time)
                    if not running:
                        break
                    pwm.set_pwm(int(i)-1, 2000, 4096-2000)
                    time.sleep(waiting_time)
                    pwm.set_pwm(int(i)-1, pulse, 4096-pulse)
                    previous=i
                if not running:
                    move_to_initial()
                    break
            if not running:
                    move_to_initial()
                    break
    elif choice=="c":
        previous=0
        while True:
            for moves in learning_combos:
                for i in channels:
                    if i==previous:
                        time.sleep(same_arm_time)
                    else:
                        time.sleep(diff_arm_time)
                    if not running:
                        break
                    pwm.set_pwm(int(i)-1, 2000, 4096-2000)
                    time.sleep(waiting_time)
                    pwm.set_pwm(int(i)-1, pulse, 4096-pulse)
                    previous=i
                if not running:
                    move_to_initial()
                    break
            if not running:
                    move_to_initial()
                    break
                
'''

# shutdown the gui
def shutdown():
    sys.exit();
    #pass


def press_spar():
    global choice
    choice="s"
    main_page.pack_forget()
    page2.pack()


def press_combo():
    global choice
    choice="c"
    main_page.pack_forget()
    page5.pack()


def increase_speed():
    global speed
    global same_arm_time
    global diff_arm_time
    global waiting_time
    if speed <= 90:
        waiting_time -= 0.022
        same_arm_time -= 0.185
        diff_arm_time -= 0.105
        speed += 10
    speed_label.config(text=str(speed) + "%")


def decrease_speed():
    global speed
    global same_arm_time
    global diff_arm_time
    global waiting_time
    if speed > 10:
        waiting_time += 0.022
        same_arm_time += 0.185
        diff_arm_time += 0.105
        speed -= 10
    speed_label.config(text=str(speed) + "%")


def select_speed():
    page2.pack_forget()
    page3.pack()


def go_home():
    global t
    global running
    global seconds
    global speed
    global begin
    begin=False
    t = 0
    speed = 50
    seconds = 0
    running = False
    speed_label.config(text="50%")
    reset()
    page2.pack_forget()
    page3.pack_forget()
    page4.pack_forget()
    page5.pack_forget()
    main_page.pack()


def set_timer():
    global t
    global speed
    t = v.get()
    page3.pack_forget()
    page4.pack()
    page4.speed_label.config(text="Speed: " + str(speed) + "%")




def update():
    global seconds
    global minutes
    global running
    global begin
    global t
    if not begin:
        begin=True
    else:
        time.sleep(1)
    if seconds == 60:
        seconds = 0
        minutes += 1
    minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
    seconds_string = f'{seconds}' if seconds > 9 else f'0{seconds}'
    page4.stopwatch_label.config(text=minutes_string + ':' + seconds_string)
    if running and int(minutes_string) != t:
        seconds += 1
        
        update()
    elif int(minutes_string)==t:
        time.sleep(2)
        seconds=0
        minutes=0
        begin=False
        start_button.place(x=140, y=180)
        running = False
    elif running==False:
        start_button.place(x=140, y=180)
        running = False

def start():
    global running
    if not running:
        running = True
        start_button.place_forget()
        pause_button.place(x=400, y=180)
        if __name__ == '__main__':
            #a=Thread(target=servo)
            b = Thread(target=update)
            #a.start()
            b.start()

def pause():
    global running
    global seconds
    global begin
    if running:
        start_button.place(x=140, y=180)
        pause_button.place_forget()
        begin=False
        seconds-=1
        running = False

def reset():
    global running
    running=False
    # set variables back to zero
    global minutes
    global seconds
    minutes = 0
    seconds = 0
    # set label back to zero
    page4.stopwatch_label.config(text="00:00")

def one_clicked():
    global enterd_combination
    enterd_combination+="1"

def two_clicked():
    global enterd_combination
    enterd_combination+="2"


def three_clicked():
    global enterd_combination
    enterd_combination+="3"


def four_clicked():
    global enterd_combination
    enterd_combination+="4"


def enter_clicked():
    global enterd_combination
    global learning_combos
    learning_combos.append(int(enterd_combination))
    combos_selected.insert(tk.INSERT,enterd_combination+ ", ")
    enterd_combination=""



master = tk.Tk()
main_page = tk.Frame(master)
page2 = tk.Frame(master)
page3 = tk.Frame(master)
page4 = tk.Frame(master)
page5 = tk.Frame(master)

#--------------------------------------------page1, select mode---------------------------------------------------------
canvas = Canvas(main_page, width=728, height=455)
canvas.pack(fill="both", expand=True)

img_background = PhotoImage(file=r'Picture/new.png')
canvas.create_image(0, 0, anchor="nw", image=img_background)

img_name = PhotoImage(file=r'Picture/name.png')
canvas.create_image(40, 40, anchor="nw", image=img_name)

myFont = ("Roboto", 30, "bold")

img_mode =PhotoImage(file=r'Picture/select_mode.png')
canvas.create_image(150, 160, anchor="nw", image=img_mode)

# button that brings the user to the speed page
spar = Button(main_page, text="Combo", command=lambda: press_combo(), width=8, bg='#357EC7', fg='#ffffff')

combo = Button(main_page, text="Spar", command=lambda: press_spar(), width=8, bg='#357EC7', fg='#ffffff')

# button to shutdown the raspbery pi
img_quit = PhotoImage(file=r'Picture/button_shut-down (4).png')
main_page.img_quit = img_quit
quit = Button(main_page, image=img_quit, command=lambda: shutdown(), borderwidth=0)
quit.place(x=150, y=350)


# modfies the font of the button
combo['font'] = myFont
spar['font'] = myFont

# adjusts the position of the buttons
spar.place(x=100, y=240)
combo.place(x=450, y=240)

main_page.pack()

#-----------------------------------------second page choose speed increment--------------------------------------------
img_background2=PhotoImage(file=r'Picture/bg_timer.png')
myFont = ("Roboto", 25, "bold")
myFont_speed= ("Roboto",50, "bold")
canvas2 = Canvas(page2, width=728, height=455)
canvas2.pack(fill="both", expand=True)
canvas2.create_image(0, 0, anchor="nw", image=img_background2)
canvas2.create_image(40, 40, anchor="nw", image=img_name)
img_speed = PhotoImage(file=r'Picture/speed2 (1).png')
canvas2.create_image(160, 140, anchor="nw", image=img_speed)


img_home = PhotoImage(file=r'Picture/button_start-over (1).png')
page2.img_home= img_home
home = Button(page2, image=img_home, command=lambda: go_home(), borderwidth=0)
home.place(x=150, y=350)

decrease = Button(page2, text="Decrease", command=lambda: decrease_speed(), width=8, bg='#357EC7', fg='#ffffff')
increase = Button(page2, text="Increase", command=lambda: increase_speed(), width=8, bg='#357EC7', fg='#ffffff')
speed_label = Label(page2, text=str(speed) + "%", width=4,fg='#1545d4', bg='#000000')
select_speed_button = Button(page2, text="Set Speed", command=lambda: select_speed(), width=8, bg='#357EC7',
                             fg='#ffffff')

decrease['font'] = myFont
increase['font'] = myFont
speed_label['font'] = myFont_speed
select_speed_button['font'] = myFont
# adjusts the position of the buttons
decrease.place(x=40, y=230)
increase.place(x=280, y=230)
speed_label.place(x=410, y=125)
select_speed_button.place(x=510, y=230)



# ---------------------------------------------Third page (set time)-----------------------------------------------------
myFont = ("Roboto", 25, "bold")
canvas3 = Canvas(page3, width=728, height=455)
canvas3.pack(fill="both", expand=True)
canvas3.create_image(0, 0, anchor="nw", image=img_background2)
canvas3.create_image(40, 40, anchor="nw", image=img_name)

home2 = Button(page3, image=img_home, command=lambda: go_home(), borderwidth=0)
home2.place(x=150, y=350)

v = DoubleVar()


myFont_time = ("Roboto", 18, "bold")
select_time = Label(page3, text="Selected Time: 1 minute(s)",width=20,bg='#000000', fg='#ffffff')
select_time['font'] = myFont_time
select_time.place(x=230, y=120)

def cmd(v):
    select_time.config(text="Selected Time: " + str(v) + " minute(s)")


myFont_timer = ("Roboto", 15, "bold")
timer=Scale(page3,variable = v, from_=1 , to=6,tickinterval=1, command=cmd,orient=HORIZONTAL,
            fg="black",bg="#DC143C",troughcolor="#F08080",width=40, length=600)
timer['font']=myFont_timer
timer.place(x=60,y=160)

myFont = ("Roboto", 25, "bold")
set_time = Button(page3, text="Set Time", command=lambda: set_timer(), width=8, bg='#357EC7', fg='#ffffff')
set_time['font'] = myFont
# adjusts the position of the buttons
set_time.place(x=280, y=270)

# ------------------------------------------------Fourth page (timer, start motors)----------------------------------------
myFont = ("Roboto", 25)
canvas4 = Canvas(page4, width=728, height=455)
canvas4.pack(fill="both", expand=True)
canvas4.create_image(0, 0, anchor="nw", image=img_background2)

home2 = Button(page4, image=img_home, command=lambda: go_home(), borderwidth=0)
home2.pack(pady=30)
home2.place(x=130, y=350)

myFont = ("Roboto", 33)
page4.stopwatch_label = Label(page4, text='00:00', font=("Roboto", 80))
page4.stopwatch_label.place(x=220, y=50)
page4.stopwatch_label.config(background='black')
page4.stopwatch_label.config(foreground='white')

'''
page4.time_label = Label(page4, text=str(t) + "minutes", font=("Roboto", 40))
page4.time_label.place(x=50, y=300)
'''

l_font=("Roboto", 30, 'bold')
page4.speed_label = Label(page4, text="Speed: " + str(speed) + "%", font=l_font, bg="black", fg="red")
page4.speed_label.place(x=230, y=10)

img_start = PhotoImage(file=r'Picture/start.png')
page4.img_start = img_start
start_button = Button(page4, image=img_start, command=lambda: start(), borderwidth=0)
start_button.place(x=140, y=180)



img_pasue = PhotoImage(file=r'Picture/pause (1).png')
page4.img_pasue = img_pasue
pause_button = Button(page4, image=img_pasue, command=lambda: pause(), borderwidth=0)

# ------------------------------------------------Fifth page (Spar Mode)----------------------------------------
myFont = ("Roboto", 20)
canvas5 = Canvas(page5, width=728, height=455)
canvas5.pack(fill="both", expand=True)
canvas5.create_image(0, 0, anchor="nw", image=img_background2)
canvas5.create_image(40, 40, anchor="nw", image=img_name)

home3 = Button(page5, image=img_home, command=lambda: go_home(), borderwidth=0)
home3.place(x=150, y=350)

one = Button(page5, text="1", command=lambda: one_clicked(), width=5, bg='#357EC7', fg='#ffffff')
two = Button(page5, text="2", command=lambda: two_clicked(), width=5, bg='#357EC7', fg='#ffffff')
three = Button(page5, text="3", command=lambda: three_clicked(), width=5, bg='#357EC7', fg='#ffffff')
four = Button(page5, text="4", command=lambda: four_clicked(), width=5, bg='#357EC7', fg='#ffffff')
enter = Button(page5, text="Enter", command=lambda: enter_clicked(), width=7, bg='#357EC7', fg='#ffffff')
one['font'] = myFont
two['font'] = myFont
three['font'] = myFont
four['font'] = myFont
enter['font'] = myFont
one.place(x=480,y=130)
two.place(x=600,y=130)
three.place(x=480,y=200)
four.place(x=600,y=200)
enter.place(x=520,y=270)


combos_selected= st.ScrolledText(page5,width=20,height=5,font=("Roboto",25),bg="black", fg="red")
combos_selected.place(x=50, y=130)
combos_selected.insert(tk.INSERT,"Combos Selected: ")

#run program
mainloop()
