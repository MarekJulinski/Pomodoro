from tkinter import *
from playsound import playsound
from threading import Thread
import os
# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
TICK = '✔'
DIR = os.path.dirname(os.path.realpath(__file__))
reps = 0
tasks = 0
timer = None

# ------------------------------- COUNT DOWN -------------------------------- #
def play_sound():
    playsound(str(DIR) + '/Bell.wav')

def reset_count_down():
    global reps
    global tasks
    
    reps = 0
    tasks = 0
    
    root.after_cancel(timer)
    
    timer_text.config(text='TIMER', fg=GREEN)
    
    canvas.itemconfigure(countdown, text = '00:00')
    
    change_ticks()

def start_count_down():
    global reps
    global tasks
    global timer
    
    work = WORK_MIN * 60
    short_break = SHORT_BREAK_MIN * 60
    long_break = LONG_BREAK_MIN * 60
    
    if reps % 7 == 0 and reps > 0:
        change_timer_text('BREAK', PINK)
        count(long_break)
        reps = 0
    elif reps % 2 == 0:
        change_timer_text("WORK", RED)
        count(work)
        tasks += 1
        reps += 1
    else:
        change_timer_text("BREAK", GREEN)
        count(short_break)
        reps += 1
    
def count(i):
    global timer
    
    seconds = i % 60
    minutes = int(i / 60)
        
    if minutes < 10:
        minutes = f'0{minutes}'
        
    if seconds < 10:
        seconds = f'0{seconds}'
            
    canvas.itemconfigure(countdown, text = f'{minutes}:{seconds}')
    
    if i >= 0:    
        timer = root.after(1000, count, i-1)
    else:
        thread = Thread(target=play_sound)
        thread.start()
        root.focus_force()
        change_ticks()
        start_count_down()
    
    

# -------------------------------- UI SETUP ------------------------------- #

def main_window():
    root = Tk()
    root.focus_force()
    root.title('POMODORO')
    root.config(background=YELLOW, padx=100, pady=100)
    return root

def create_canvas():
    canvas = Canvas(master=root, width=200, height=224, highlightthickness=0, bg=YELLOW)
    canvas_image = PhotoImage(file = str(DIR) + '/tomato.png')
    canvas.grid(row=1, column=1)
    return canvas, canvas_image

def create_timer_text():
    timer_text = Label(master=root, text='TIMER', font=(FONT_NAME, 70, 'bold'), fg=GREEN)
    timer_text.config(bg=YELLOW, highlightthickness=0)
    timer_text.grid(row=0, column=1)
    return timer_text

def change_timer_text(txt, color):
    timer_text.config(text = txt, fg = color)

def create_buttons():
    start_button = Button(master=root, text='START', font=(FONT_NAME, 30, 'bold'), border=0, command=start_count_down)
    start_button.grid(row=2, column=0)

    reset_button = Button(master=root, text='RESET', font=(FONT_NAME, 30, 'bold'), border=0, command=reset_count_down)
    reset_button.grid(row=2, column=2)
    
    return start_button, reset_button

def create_ticks():
    global reps
    tick_label = Label(master=root, text=TICK*reps, fg=GREEN, background=YELLOW, font=(FONT_NAME, 50, 'bold'))
    tick_label.grid(row=3, column=1)\
        
    return tick_label

def change_ticks():
    global tasks
    tick_label.config(text=TICK*tasks)

#---------------------------------MAIN THREAD---------------------------------#

if __name__ == "__main__":

    root = main_window()

    canvas, canvas_image = create_canvas()
    canvas.create_image(100, 112, image = canvas_image)
    countdown = canvas.create_text(100, 130, text='00:00', font=(FONT_NAME, 45, 'bold'))

    timer_text = create_timer_text()

    start_button, reset_button = create_buttons()

    tick_label = create_ticks()

    root.mainloop()