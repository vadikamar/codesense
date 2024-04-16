import speech_recognition as sr
import pyttsx3
import wikipedia
import pyjokes
import cv2
import datetime
import webbrowser
import random
import calendar


vt=input("Enter v for voice or t for type command:")
vt=vt.lower()
listener = sr.Recognizer()
listener1 = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()

name=input("Enter your name:")
line="Hi, "+name+"! How can I help you?"
talk(line)
print(line)

def take_command():
    if vt=='v':
        try:
            with sr.Microphone() as source:
                print('listening...')
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
                command = command.lower()
        except:
            pass
    elif vt=='t':
        command=input("Type.......")
    else:
        print("Wrong choice entered!")
        exit()

    return command


def myname():
    if vt=='v':
        try:
            f=0
            with sr.Microphone() as source:
                print('What is my name...')
                talk('What is my name...')
                v = listener1.listen(source)
                com = listener1.recognize_google(v)
                com = com.lower()
                print(com)
                if 'nebula'==com:
                    f=1
        except:
            pass
    else:
        f=0
        talk('What is my name...')
        print('What is my name...')
        com=input()
        com=com.lower()
        if 'nebula' == com:
            f = 1
    return f

def run_nebula():
    command=take_command()
    print(command)
    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
        print(time)

    elif 'search' in command:
        search = command.replace('search', '')
        webbrowser.open('https://www.google.com/search?q=' + search)

    elif 'calendar' in command:
        yy=int(input("Enter year:"))
        mm=int(input("Enter month:"))
        talk((calendar.month(yy,mm)))
        print((calendar.month(yy,mm)))


    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)


    elif 'joke' in command:
        joke=pyjokes.get_joke()
        talk(joke)
        print(joke)

    elif 'calculator' in command:
        x = int(input("Enter first number:"))
        c = input("Enter operator:")
        y = int(input("Enter second number:"))
        if (c == '+'):
            talk((x + y))
            print(x+y)
        elif (c == '-'):
            talk((x - y))
            print(x-y)
        elif (c == '*'):
            talk((x * y))
            print(x*y)
        elif (c == '/'):
            talk((x / y))
            print(x/y)
        elif (c == '%'):
            talk((x % y))
            print(x%y)
        else:
            talk("Error")
            print("Error")

    elif 'game' in command:
        choice=int(input("Enter number between 1 or 2:"))
        if choice==1:
            while(True):
                a=random.randint(0,9)
                b=int(input("Enter a number in b/w 0-9:"))
                if a==b:
                    print(talk("Congrats! You win."))
                else:
                    talk("Oh No, You lose.")
                    print("Number was ",a)
                q=input("Wanna play again enter r otherwise q:")
                if(q=='q'):
                    exit(1)

        elif choice==2:
            while(True):
                user_action = input("Enter a choice (rock, paper, scissors): ")
                possible_actions = ["r", "p", "s"]
                computer_action = random.choice(possible_actions)
                print(f"\nYou chose {user_action}, computer chose {computer_action}.\n")

                if user_action == computer_action:
                    print(f"Both players selected {user_action}. It's a tie!")
                elif user_action == "r":
                    if computer_action == "s":
                        print("Rock smashes scissors! You win!")
                        talk("Rock smashes scissors! You win!")
                    else:
                        print("Paper covers rock! You lose.")
                        talk("Paper covers rock! You lose.")
                elif user_action == "p":
                    if computer_action == "r":
                        print("Paper covers rock! You win!")
                        talk("Paper covers rock! You win!")
                    else:
                        print("Scissors cuts paper! You lose.")
                        talk("Scissors cuts paper! You lose.")
                elif user_action == "s":
                    if computer_action == "p":
                        print("Scissors cuts paper! You win!")
                        talk("Scissors cuts paper! You win!")
                    else:
                        print("Rock smashes scissors! You lose.")
                        talk("Rock smashes scissors! You lose.")
                q = input("Wanna play again enter r otherwise q:")
                if (q == 'q'):
                    exit(1)
        else:
            talk("Error")
            print("Error")


    else:
        print('Please say the command again.')
        talk('Please say the command again.')

    talk("Press r to continue or q to exit:")
    quit = input("Press r to continue or q to exit:")
    if (quit == 'q'):
        exit(1)
    else:
        run_nebula()



def cam():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
    p = 0
    while True:
        _, frame = cap.read()
        original_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in face:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            face_roi = frame[y:y + h, x:x + w]
            gray_roi = gray[y:y + h, x:x + w]
            smile = smile_cascade.detectMultiScale(gray_roi, 1.3, 25)
            for x1, y1, w1, h1 in smile:
                cv2.rectangle(face_roi, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)
                time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
                file_name = f'selfie-{time_stamp}.png'
                cv2.imwrite(file_name, original_frame)
                webbrowser.open_new_tab('index.html')
                p = 1
        cv2.imshow('cam star', frame)
        if cv2.waitKey(10) == ord('q') or p == 1:
            s="D:\vadik\project\selfie"+time_stamp+".png"
            h = datetime.datetime.now().strftime('%I')
            mm = datetime.datetime.now().strftime('%M')
            break




while True:
    f=myname()
    if f==1:
        run_nebula()
    else:
        cam()
    break








