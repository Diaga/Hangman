from tkinter import *
from tkinter import ttk
import json
import random
import winsound
from threading import Timer


winsound.PlaySound("Wav\Background.wav", winsound.SND_ASYNC | winsound.SND_FILENAME | winsound.SND_NOSTOP)

Hangman = Tk()
Hangman.title("Hangman")
Hangman.geometry("300x150+500+200")

DummyL1 = ttk.Label(text="Hangman\n[Guess the word!]", justify="center")
DummyL1.place(relx="0.3", rely="0.03")

DummyL2 = ttk.Label(text="Tries: ")
DummyL2.place(relx="0.05", rely="0.45")

AlphabetsC = ttk.Combobox(values=("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"), state="readonly")
AlphabetsC.place(relx="0.27", rely="0.6")

WordLabel = ttk.Label(text="", font=("Courier", "20"))
WordLabel.place(height="40", width="200", relx="0.27", rely="0.25")

Hangman.tries = 5
TriesLabel = ttk.Label(text=Hangman.tries, foreground="Green", font=("Courier", "13"))
TriesLabel.place(relx="0.15", rely="0.441")

def getword():
    length = 10
    while length > 9:
        with open("Json\Words.json", "r") as List_data:
            word = random.choice(list(json.load(List_data).keys()))
            word = word.upper()
            getword.word = word
            print(word)
        length = len(word)
    visiblen = int(length/3)
    i = 0
    visible = list()
    while i != visiblen:
        visibleR = random.randint(0, length - 1)
        if visibleR not in visible:
            visible.append(visibleR)
            i = i + 1
    visible.sort()
    i = 0
    j = 0
    while i != length:
        if i in visible:
            WordLabel.config(text=WordLabel.cget("text") + word[visible[j]])
            j = j + 1
        else:
            WordLabel.config(text=WordLabel.cget("text") + "-")
        i = i + 1


getword()
check = StringVar()


def key(event):
    if event.char.isalpha():
        AlphabetsC.set(value=event.char.upper())
    elif event.keycode == 13:
        check = AlphabetsC.get()
        if check.isalpha():
            if check in getword.word:
                pos = [pos for pos, char in enumerate(getword.word) if char == check]
                if len(pos) == 1:
                    if check not in WordLabel.cget("text"):
                        i = 0
                        while i != len(pos):
                            wordlabel = WordLabel.cget("text")
                            wordlabel = wordlabel[:pos[i]] + getword.word[pos[i]] + wordlabel[pos[i] + 1:]
                            WordLabel.config(text=wordlabel)
                            i = i + 1
                        TriesF("+")
                    else:
                        TriesF("-")
                else:
                    posl = [pos for pos, char in enumerate(WordLabel.cget("text")) if char == check]
                    if len(posl) != len(pos):
                        i = 0
                        while i != len(pos):
                            wordlabel = WordLabel.cget("text")
                            wordlabel = wordlabel[:pos[i]] + getword.word[pos[i]] + wordlabel[pos[i] + 1:]
                            WordLabel.config(text=wordlabel)
                            i = i + 1
                        TriesF("+")
                    else:
                        TriesF("-")
            else:
                TriesF("-")
    if Hangman.tries >= 3:
        TriesLabel.config(foreground="Green")
    else:
        TriesLabel.config(foreground="Red")


def TriesF(operation):
    if Hangman.tries - 1 >= 0:
        if operation == "+":
            if WordLabel.cget("text") != getword.word:
                Hangman.tries = Hangman.tries + 1
                TriesLabel.config(text=Hangman.tries)
                winsound.PlaySound("Wav\Correct.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
                Timer(1.0, winsound.PlaySound, ("Wav\Background.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)).start()
            else:
                winsound.PlaySound("Wav\Win.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
        elif operation == "-":
            Hangman.tries = Hangman.tries - 1
            TriesLabel.config(text=Hangman.tries)
            if Hangman.tries == 0:
                WordLabel.config(text=getword.word)
                winsound.PlaySound("Wav\Lost.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
            else:
                winsound.PlaySound("Wav\Wrong.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)
                Timer(1.0, winsound.PlaySound, ("Wav\Background.wav", winsound.SND_ASYNC | winsound.SND_FILENAME)).start()


Hangman.bind("<KeyRelease>", key)

Hangman.mainloop()
