import tkinter as tk
import random
 
#Variable Declarations
P1 = 0
P2 = 0
Turn = 1
timeLeft = 80
 
root = tk.Tk()
wordW = tk.Tk()
 
root.title("Pictionary")
 
canvas = tk.Canvas(height = 400, width = 400)
frame = tk.Frame(root)
frame.grid(row = 1, column = 1)
canvas.grid(row=1, column=3)
canvas.create_line(3,0,3,400, tags = "dont_delete")
canvas.create_line(3,397,397,397, tags = "dont_delete")
ccolor = "black"
 
root.resizable(width = False, height = False)
wordW.resizable(width = False, height = False)
 
words = ["Song","Trip","Backbone","Bomb","Treasure","Garbage","Park","Pirate","Ski","Whistle","State","Baseball","Coal","Queen","Photograph","Computer","Hockey","Hot-Dog","iPad","Frog","Cake","Battery","Mailman","Bicycle","Motorcycle","Password","Electrity","Deep","Light Bulb","Brain","Legs","Head","Face","School","Bee","Camera","TV","Plate","Table","Calculator","Juice","Picnic","Tape","Doctor","Ring","Piano","Magnet","YouTube","Seeds","Hug","Snake","School Bus","Storm","Solar System","Compare","Houseboat","Pictionary","Volcano"]
thick = 10
 
 
#Drawing function
def callback(coord):
    try:
        canvas.create_rectangle(coord.x+thick, coord.y-thick, coord.x-thick, coord.y+thick, fill = ccolor, outline = ccolor, tags = "delete")
    except:
        colorEntry.delete(0,tk.END)
        colorEntry.insert(0, "Improper Color!")
 
#Controls for Keyboard
def controls(key): #1=black,2=red,3=green,4=yellow,5=pink,6=purple,7=eraser,8=clear
    global ccolor
    global thick
    if key.char == "1":
        ccolor = "black"
    elif key.char == "2":
        ccolor = "red"
    elif key.char == "3":
        ccolor = "#008000"
    elif key.char == "4":
        ccolor = "yellow"
    elif key.char == "5":
        ccolor = "pink"
    elif key.char == "6":
        ccolor = "blue"
    elif key.char == "7":
        ccolor = "white"
    elif key.char == "q":
        canvas.delete("delete")
    elif key.char == "]":
        thick+=2
    elif key.char == "[":
        thick-=2
    elif key.char == " ":
        pointhandler()
 
#Controls for buttons
def buttcontrols(button):
    global ccolor
    global thick
    if button == "1":
        ccolor = "black"
    elif button == "2":
        ccolor = "red"
    elif button == "3":
        ccolor = "#008000"
    elif button == "4":
        ccolor = "yellow"
    elif button == "5":
        ccolor = "pink"
    elif button == "6":
        ccolor = "blue"
    elif button == "7":
        ccolor = "white"
    elif button == "8":
        canvas.delete("delete")
    elif button == "9":
        thick+=2
    elif button == "10":
        thick-=2
 
#Color Entry Widget      
def colorEnter(x):
    global ccolor
    ccolor = colorEntry.get()
    colorEntry.delete(0,tk.END)
    colorEntry.insert(0, "Color Updated!")
 
#Binds
canvas.bind("<B1-Motion>", callback)
root.bind("<Return>", colorEnter)
root.bind("<Key>", controls)
 
#Widget declarations/packing
guessLabel = tk.Label(frame, text = "Press SPACE when the person guesses it\nIf he can't after the time is over, you can continue\n guessing for fun or just press SPACE to end the round", font = "arial 12 bold italic")
blackB = tk.Button(frame, text = "Black (1)", command = lambda: buttcontrols("1"))
redB = tk.Button(frame, text = "Red (2)", command = lambda: buttcontrols("2"))
greenB = tk.Button(frame, text = "Green (3)", command = lambda: buttcontrols("3"))
yellowB = tk.Button(frame, text = "Yellow (4)", command = lambda: buttcontrols("4"))
pinkB = tk.Button(frame, text = "Pink (5)", command = lambda: buttcontrols("5"))
purpleB = tk.Button(frame, text = "Blue (6)", command = lambda: buttcontrols("6"))
eraserB = tk.Button(frame, text = "Eraser (7)", command = lambda: buttcontrols("7"))
clearB = tk.Button(frame, text = "Clear (Q)", command = lambda: buttcontrols("8"))
increaseB = tk.Button(frame, text = "+Brush Size ]", command = lambda: buttcontrols("9"))
decreaseB = tk.Button(frame, text = "-Brush Size [", command = lambda: buttcontrols("10"))
colorLabel = tk.Label(frame, text = "Enter another color (HEX Code also Supported):")
colorEntry = tk.Entry(frame)
 
guessLabel.grid(row = 1, column = 1)
blackB.grid(row = 2, column = 1)
redB.grid(row =3, column = 1)
greenB.grid(row = 4, column = 1)
yellowB.grid(row = 5, column = 1)
pinkB.grid(row = 6, column = 1)
purpleB.grid(row = 7, column = 1)
colorLabel.grid(row = 8, column = 1)
colorEntry.grid(row = 9, column = 1)
eraserB.grid(row = 10, column = 1)
clearB.grid(row = 11, column = 1)
increaseB.grid(row = 12, column = 1)
decreaseB.grid(row = 13, column = 1)
 
timeLabel = tk.Label(root, text = "Time Left: 80", font = "arial 20 underline")
timeLabel.grid(row = 5, column = 1)
Label = tk.Label(root, text = "", font = "arial 20 bold",  bg = "black", fg = "white")
 
countdown = False
 
#Point Handler
def pointhandler():
    global P1
    global P2
    global Turn
    global timeLeft
    global countdown
    countdown = False
    multiplier = 10/80
    if Turn == 1 and timeLeft > 0:
        P1+=int(multiplier*timeLeft)
        P2+=10
        timeLeft = 80
        Turn = 2
        buttcontrols("8")
        updateWords()
        Label.config(text = "Player 2 Turn to Draw!\nP1: "+str(P1)+"\nP2: "+str(P2))
    elif Turn == 1 and timeLeft < 1:
        timeLeft = 80
        Turn = 2
        buttcontrols("8")
        updateWords()
        Label.config(text = "Player 2 Turn to Draw!\nP1: "+str(P1)+"\nP2: "+str(P2))
    elif Turn == 2 and timeLeft > 0:
        P1+=10
        P2+=int(multiplier*timeLeft)
        timeLeft = 80
        Turn = 1
        buttcontrols("8")
        updateWords()
        Label.config(text = "Player 1 Turn to Draw!\nP1: "+str(P1)+"\nP2: "+str(P2))
    elif Turn == 2 and timeLeft < 1:
        Label.config(text = "Player 1 Turn to Draw!\nP1: "+str(P1)+"\nP2: "+str(P2))
        timeLeft = 80
        Turn = 2
        buttcontrols("8")
        updateWords()
        Label.config(text = "Player 1 Turn to Draw!\nP1: "+str(P1)+"\nP2: "+str(P2))
 
#Countdown functions
def time():
    global timeLeft
    global countdown
    if timeLeft > 0 and countdown == True:
        timeLeft-=1
    timeLabel.config(text = "Time Left: " + str(timeLeft), font = "arial 20 underline")
    root.after(1000, time)
 
def time2():
    global timeLeft
    global countdown
    if timeLeft > 0 and countdown == True:
        timeLeft-=1
    timeLabel.config(text = "Time Left: " + str(timeLeft), font = "arial 20 underline")
    root.after(1000, time)
 
#CHOOSE WORD WINDOW
 
wordW.title("Choose a Word")
wordLabel = tk.Label(wordW, text = "Choose a word below:", font = "arial 20 bold", fg = "yellow", bg = "black")
wordLabel.grid(row = 1, column = 1, columnspan = 3)
 
def countdowntoggle():
    global countdown
    countdown = True
    Word1.config(text = "Hidden")
    Word2.config(text = "Hidden")
    Word3.config(text = "Hidden")
 
FirstWord = words[random.randint(0,len(words)-1)]
SecondWord = words[random.randint(0,len(words)-1)]
ThirdWord = words[random.randint(0,len(words)-1)]
Word1 = tk.Button(wordW, text = FirstWord, command = countdowntoggle)
Word2 = tk.Button(wordW, text = SecondWord, command = countdowntoggle)
Word3 = tk.Button(wordW, text = ThirdWord, command = countdowntoggle)
Word1.grid(row = 2, column = 1)
Word2.grid(row = 2, column = 2)
Word3.grid(row = 2, column = 3)
 
def updateWords():
    FirstWord = words[random.randint(0,len(words)-1)]
    SecondWord = words[random.randint(0,len(words)-1)]
    ThirdWord = words[random.randint(0,len(words)-1)]
    Word1.config(text = FirstWord)
    Word2.config(text = SecondWord)
    Word3.config(text = ThirdWord)
 
 
#END OF WORD WINDOW
 
#Countdown/Point calling
time()
Label.config(text = "Player 1 Turn to Draw!\nP1: "+str(P1)+"\nP2: "+str(P2))
Label.grid(row = 6, column = 1)
 
 
root.mainloop()
#https://www.youtube.com/watch?v=Lbfe3-v7yE0
