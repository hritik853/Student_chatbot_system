import warnings

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from tkinter import *
import pyttsx3 as p
import speech_recognition as s
import threading
import os
warnings.filterwarnings("ignore")


engine = p.init()
voices = engine.getProperty('voices')
print(voices)

engine.setProperty('voice',voices[1].id)
def speak(word):
    engine.say(word)
    engine.runAndWait()

bot =ChatBot("my bot",
             logic_adapters=[
        {
          'import_path': 'chatterbot.logic.BestMatch'
        },'chatterbot.logic.MathematicalEvaluation',
           'chatterbot.logic.SpecificResponseAdapter'
         ],
             storage_adapter="chatterbot.storage.SQLStorageAdapter")

trainer =ListTrainer(bot)

for _file in os.listdir('chats'):
    convo=open('chats/' + _file, 'r').readlines()
    trainer.train(convo)


main = Tk()
main.geometry("500x600")
main.title("Geu chatbot")
ima = PhotoImage(file = "geu.png")
PhotoL = Label(main, image=ima)
PhotoL.pack(pady=5)

def take_speak_query():
    sr = s.Recognizer()
    sr.pause_threshold= 1
    print("bot is listening")
    with s.Microphone() as mm:
        try :
            audio = sr.listen(mm)
            query = sr.recognize_google(audio, language='eng-in')
            print(query)
            textf.delete(0,END )
            textf.insert(0, query)
            ask_from_bot()
        except   Exception as e:
            print(e)
            print("not recognize")




def ask_from_bot():
    query=textf.get()
    answer_from_bot=bot.get_response(query)
    msg.insert(END,"You :"+query)
    msg.insert(END,"Bot :"+str(answer_from_bot))
    speak(answer_from_bot)
    textf.delete(0,END)
    msg.yview(END)



frame = Frame(main)
sc = Scrollbar(frame)
msg = Listbox(frame,width=80, height = 20, yscrollcommand = sc.set)
sc.pack(side = RIGHT,fill = Y)
msg.pack(side= LEFT,fill=BOTH,pady=10 )
frame.pack()

# creating text field
textf = Entry(main, font=("verdana",22))
textf.pack(fill=X,pady=10)
bt=Button(main,text="click to ask",font=("verdana",22), command=ask_from_bot)
bt.pack()
#  CREATING THE FUNCTION TO BIND THE ENTER WITH BUTTON
def enter_function(event):
    bt.invoke()

main.bind('<Return>',enter_function)
b ="bot is listening type or speak query!!"
msg.insert(0,b)
def repeat():
    while True:
        take_speak_query()

t= threading.Thread(target=repeat)
t.start()

main.mainloop()
