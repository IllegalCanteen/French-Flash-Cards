from tkinter import *
import random
import pandas

card = {}
to_learn = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except:
    data = pandas.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global card, timer
    window.after_cancel(timer)
    window.after_cancel(timer)
    card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="Black")
    canvas.itemconfig(card_word, text=card["French"], fill="Black")
    timer = window.after(3000, flip)
    canvas.itemconfig(card_background, image=card_front)


def flip():
    old_image = canvas.itemconfig(card_word, text=card["French"])
    new_image = canvas.itemconfig(card_word, text=card["English"], fill="White")
    new_image = canvas.itemconfig(card_title, text="English", fill="White")
    canvas_image = canvas.create_image(300, 300, image=old_image)
    canvas.itemconfig(card_background, image=card_back)


def correct():
    global card
    try:
        if card in to_learn:
            to_learn.remove(card)
        words_to_learn = pandas.DataFrame(to_learn)
        words_to_learn.to_csv("data/words_to_learn.csv", index=False)
        next_card()
    except IndexError:
        canvas.itemconfig(card_word, text="You have guessed all the words correct", font=("Arial", 24, "normal"))
        canvas.itemconfig(card_title, text="Result")


BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

timer = window.after(3000, flip)

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, command=correct)
known_button.grid(row=1, column=1)

next_card()
window.mainloop()
