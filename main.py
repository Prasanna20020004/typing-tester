import random as rnd
import math
from tkinter import *
from tkinter import messagebox
from word import word_list

TIMER = 10
number_of_words = 3
words = ""
user_total = ""
word_total = ""


def timer_set():
    global TIMER
    TIMER = int(set_timer.get())
    set_timer.config(state="disabled")
    set_button.config(state="disabled")


def generate_words():
    global number_of_words
    random_word = ""
    for i in range(number_of_words):
        random_word = random_word + " " + rnd.choice(word_list)

    return random_word.strip()


def start():
    global words
    start_button.config(state="disabled")
    words = generate_words()
    canvas.itemconfig(test_text, text=words)
    user_input.config(state="normal")
    user_input.focus()
    count_down(TIMER)


def count_down(time_left):
    time_sec = time_left % 60
    time_min = math.floor(time_left / 60)

    if time_sec < 10:
        timer_text.config(text=f"Timer: {time_min}:0{time_sec}")
    else:
        timer_text.config(text=f"Timer: {time_min}:{time_sec}")

    if time_sec == 0 and time_min == 0:
        check(time_left)
        start_button.config(state="normal")
        user_input.delete(0, END)
        user_input.config(state="disabled")
        set_timer.config(state="normal")
        set_timer.delete(0, END)
        set_button.config(state="normal")
        canvas.itemconfig(test_text, text="Click start to start the test.")

    if time_left > 0:
        window.after(1, check, time_left)
        window.after(1000, count_down, time_left - 1)


def check(rtime):
    global words, user_total, word_total

    user_text = user_input.get()
    if len(words) == len(user_text):
        user_total = user_total + " " + user_text
        word_total = word_total + " " + words
        words = generate_words()
        user_input.delete(0, END)
        canvas.itemconfig(test_text, text=words)

    if rtime == 0:
        user_total = user_total + " " + user_input.get()
        word_total = word_total + " " + words[0:len(user_input.get())]
        speed = len(user_total.strip().split(" ")) * (60 / TIMER)
        accuracy = get_accuracy(user_total.strip(), word_total.strip())
        messagebox.showinfo(title="Result",
                            message=f"Your typing results are:\nSpeed: {speed} WPM\nAccuracy: {accuracy}%")


def get_accuracy(user, word):
    counter = 0

    for i in range(len(user)):
        if user[i] == word[i]:
            counter += 1

    try:
        accuracy = (counter / len(user)) * 100
    except ZeroDivisionError:
        return 0
    else:
        return f"{accuracy: .2f}"


window = Tk()
window.minsize(700, 500)
window.title("Typing Tester")
window.config(pady=100, padx=100)

set_label = Label(text="Set timer default 10sec (type number of seconds):")
set_label.grid(column=2, row=0)
set_timer = Entry()
set_timer.grid(column=2, row=1)
set_button = Button(text="Set", command=timer_set)
set_button.grid(column=2, row=2)

timer_text = Label(text="Timer: 00:00", font=("Arial", 24, "bold"), fg="red")
timer_text.grid(column=2, row=3)

canvas = Canvas(height=100, width=700)
canvas.grid(column=2, row=4, columnspan=2)
canvas.config(bg="black")
test_text = canvas.create_text(350, 50,
                               width=600,
                               text="Click start to start the test.",
                               fill="white",
                               font=("Arial", 15, "bold"))  # width, height

user_input = Entry(width=63, font=("Helvetica", 15))
user_input.config(state="disabled")
user_input.grid(column=2, row=5, columnspan=2)

start_button = Button(text="Start the test", bg="green", font=("Arial", 15, "bold"), command=start)
start_button.grid(column=2, row=6)

window.mainloop()
