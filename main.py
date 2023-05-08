from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT = ("Courier", 70, "bold")
timing = False
MINUTES = 0
SECONDS = 0
extent = 0
reset_value = False
hold_down = True
pressed_down = ""
mode: str
mode_label: Label
canvas2: Canvas
minute_button: Button
seconds_button: Button
upwards_button: Button
downwards_button: Button
count = ""
circle_drawing = ""
reset_pressed = False
real_minute = 0
real_second = 0
real_millisecond = 0



def display(unit):
    if len(str(unit)) == 1:
        return f"0{unit}"
    else:
        return unit


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def reset():
    global time_text, timing, MINUTES, SECONDS, time_text, play_button,\
        extent, reset_value, count, circle_drawing, reset_pressed, real_minute, real_second
    real_minute = 0
    real_second = 0
    if not reset_pressed:
        reset_value = True
        canvas.itemconfig(circle, outline="black")
        canvas.itemconfig(Arc, outline=GREEN, width=1, extent=0)
        extent = 0
        if timing:
            timing = False
            window.after_cancel(count)
            window.after_cancel(circle_drawing)
            canvas.itemconfig(Arc, outline=GREEN, fill=GREEN, extent=0, width=1)
            extent = 0
            window.after_cancel(count)
            count_down(MINUTES, SECONDS)
            play_button_func()

        else:
            global canvas2, upwards_button, downwards_button, mode_label, minute_button, seconds_button, mode
            canvas2 = Canvas(width=200, height=500, bg=RED, highlightthickness=0)
            canvas2.place(x=400, y=0)
            window.minsize(width=640, height=500)

            play_button = Button(image=play_image, bg=GREEN, highlightthickness=0, command=play_button_func)
            play_button.place(x=250, y=400)
            mode = "minute"
            canvas.itemconfig(time_text, text=f"{display(MINUTES)}:{display(SECONDS)}", fill="black", font=FONT)

            seconds_button = Button(text="Seconds")

            minute_button = Button(text="Minute")
            # minute_button.place(x=460, y=480)

            mode_label = Label(text=f"{mode.upper()}", fg=YELLOW, bg=RED, font=("Courier", 25, "italic"))
            mode_label.place(x=430, y=20)

            upwards_button = Button(image=upwards_arrow_image, bg=RED, highlightthickness=0)
            upwards_button.bind('<ButtonPress>', upwards_button_func)
            upwards_button.bind("<ButtonRelease>", long_press_func)
            window.bind("<Up>", upwards_button_func)
            window.bind("<KeyRelease-Up>", long_press_func)
            upwards_button.place(x=430, y=80)

            downwards_button = Button(image=downwards_arrow_image, bg=RED, highlightthickness=0)
            downwards_button.bind("<ButtonPress>", downwards_button_func)
            downwards_button.bind("<ButtonRelease>", long_press_func)
            window.bind("<Down>", downwards_button_func)
            window.bind("<KeyRelease-Down>", long_press_func)
            downwards_button.place(x=430, y=280)

            seconds_button_func("event")
            reset_pressed = True


def play_button_func():
    global timing, SECONDS, MINUTES, reset_pressed
    if MINUTES == 0 and SECONDS == 0:
        return
    if not timing:
        global canvas2, minute_button, seconds_button, upwards_button, downwards_button
        play_button.config(image=pause_image, bg=GREEN)
        try:
            canvas2.destroy()
            minute_button.destroy()
            seconds_button.destroy()
            upwards_button.destroy()
            downwards_button.destroy()
            mode_label.destroy()
            window.minsize(width=440, height=500)

        except:
            pass

        timing = True
        if real_minute == 0 and real_second == 0 and reset_pressed:
            count_down(MINUTES, SECONDS)
        else:
            count_down(real_minute, real_second, real_millisecond)
        draw_circle()

    elif timing:
        play_button.config(image=play_image, bg=GREEN)
        timing = False
        window.after_cancel(count)
        window.after_cancel(circle_drawing)
    reset_pressed = False


def draw_circle():
    global Arc, extent, circle_drawing
    time_in_seconds = MINUTES * 60 + SECONDS
    if timing:
        if extent > -360:
            canvas.itemconfig(Arc, extent=extent, outline=RED, fill=RED, width=8)
            circle_drawing = window.after(1, draw_circle)
            extent -= 360/(1000*time_in_seconds)
        else:
            canvas.itemconfig(circle, outline=RED)

    else:
        if not reset_value:
            canvas.itemconfig(time_text, text=f"{display(0)}:{display(0)}",)
            window.after(400, blink_time)
        else:
            canvas.itemconfig(circle, outline="black")
            canvas.itemconfig(Arc, outline=GREEN, width=1, extent=0)


def blink_time():
    if not reset_value:
        canvas.itemconfig(time_text, text=f"")
        window.after(400, draw_circle)
    else:
        canvas.itemconfig(circle, outline="black")
        canvas.itemconfig(Arc, outline=GREEN, width=1, extent=0)


def count_down(minute, second, millisecond=1000):
    global timing, time_text, reset_value, play_button, time_text, count, real_minute, real_second, real_millisecond
    canvas.itemconfig(time_text, text=f"{display(minute)}:{display(second)}")
    reset_value = False
    real_minute = minute
    real_second = second
    real_millisecond = millisecond
    if timing:
        if minute == 0 and second == 0 and millisecond == 0:
            canvas.itemconfig(time_text, text=f"{display(minute)}:{display(second)}")
            play_button_func()
            play_button.destroy()
            blink_time()

        elif millisecond > 0:
            count = window.after(1, count_down, minute, second, millisecond-1)

        elif second > 0:
            count = window.after(1, count_down, minute, second-1, 999)
        else:
            count = window.after(1, count_down, minute - 1, 59, 999)


def minute_button_func(event):
    global mode, seconds_button, mode_label
    if mode == "seconds":
        mode = "minute"
        minute_button.destroy()
        mode_label.config(text=f"{mode.upper()}")
        seconds_button = Button(text="Seconds", command=lambda: seconds_button_func("event"))
        window.bind("<space>", seconds_button_func)
        seconds_button.place(x=460, y=450)


def seconds_button_func(event):
    global mode, minute_button, mode_label
    if mode == "minute":
        mode = "seconds"
        seconds_button.destroy()
        mode_label.config(text=f"{mode.upper()}")
        minute_button = Button(text="Minute", command=lambda: minute_button_func("event"))
        window.bind("<space>", minute_button_func)
        minute_button.place(x=460, y=450)


def upwards_button_func(event):
    global MINUTES, SECONDS, hold_down, pressed_down
    hold_down = True
    if hold_down:
        if mode == "minute":
            MINUTES += 1
        elif mode == "seconds":
            if SECONDS == 59:
                SECONDS = 0
                MINUTES += 1
            else:
                SECONDS += 1
        pressed_down = window.after(200, upwards_button_func, event)
        canvas.itemconfig(time_text, text=f"{display(MINUTES)}:{display(SECONDS)}")


def downwards_button_func(event):
    global MINUTES, SECONDS, pressed_down

    if mode == "minute":
        if MINUTES == 0:
            return
        MINUTES -= 1
    elif mode == "seconds":
        if MINUTES == 0 and SECONDS == 0:
            return
        if SECONDS == 0:
            SECONDS = 59
            MINUTES -= 1
        else:
            SECONDS -= 1

    canvas.itemconfig(time_text, text=f"{display(MINUTES)}:{display(SECONDS)}")
    pressed_down = window.after(200, downwards_button_func, event)


def long_press_func(event):
    global pressed_down
    window.after_cancel(pressed_down)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Count Down Timer")
window.config(bg=GREEN)
window.minsize(width=440, height=500)
pause_image = PhotoImage(file="pause.png")

upwards_arrow_image = PhotoImage(file="upwarded arrow.png")
downwards_arrow_image = PhotoImage(file="downward_arrow.png")
canvas = Canvas(width=350, height=350, bg=GREEN, highlightthickness=0)
canvas.place(x=50, y=20)
circle = canvas.create_oval(20, 20, 320, 320, width=5, )
Arc = canvas.create_arc(320, 20, 20, 320, extent=extent, outline=GREEN, start=90, style="arc")
# lines = canvas.create_arc(150, 20, 450, 320, width=5)
# circle = canvas.create_oval(150, 20, 450, 320, width=5)
# canvas3 = Canvas(width=350, height=350, bg=)
# canvas3.place(x=50, y=20)
time_text = canvas.create_text(170, 185, text=f"{display(MINUTES)}:{display(SECONDS)}", font=FONT)


# Label
# time_label = Label(text=f"{display(minute)}:{display(second)}", bg=GREEN, font=FONT)
# time_label.place(x=70, y=165)

# Button
clock_image = PhotoImage(file="clock.png")
clock_button = Button(image=clock_image, bg=GREEN, highlightthickness=0, command=reset)
clock_button.place(x=80, y=370)

play_image = PhotoImage(file="play.png")
play_button = Button(image=play_image, bg=GREEN, highlightthickness=0, command=play_button_func)
play_button.place(x=250, y=400)


window.mainloop()
