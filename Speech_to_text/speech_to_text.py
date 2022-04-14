import speech_recognition as sr
import pyttsx3
#Please above library first
r = sr.Recognizer()
def speak1(text):                               
        speaker = pyttsx3.init()               
        speaker.setProperty('rate',150)          
        speaker.say(text)                       
        speaker.runAndWait()
def write1(text):                               
        f = open("newtext.txt",mode='a')   
        f.writelines(mytext+"\n")
        f.close()
while True:
        try:
                with sr.Microphone() as source1:
                        print("Say Anything !!!!!!!!!!!!!")
                        r.adjust_for_ambient_noise(source1,duration=1)
                        audio1 = r.listen(source1)
                        mytext = r.recognize_google(audio1)
                        mytext = mytext.lower()
                        print("You said ",mytext)
                        write1(mytext)
                        speak1(mytext)
        except sr.RequestError as e:            
                print(e)
        except sr.UnknownValueError:
                print("Unkown value error")
                break
