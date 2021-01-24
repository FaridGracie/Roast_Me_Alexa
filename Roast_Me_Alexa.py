import speech_recognition as sr 
import playsound 
from gtts import gTTS 
import random 
import webbrowser
import time
from time import ctime
import os 
import urllib.request
import re


#Sets r as audio recognizer
r = sr.Recognizer()

#function to record audio
#don't even ask me wtf 'ask' is bc I don't fucking know lol
def record_audio(ask = False):
    #sets mic as source of audio
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        #sets 'audio' as audio listener (interpreter)
        audio = r.listen(source)
        #voice_data = what the fuck you say
        voice_data = ''
        #following lines are for error responding
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak('I could not understand what the fuck you said because your diction fucking sucks, try again stupid piece of shit.')
        except sr.RequestError:
            speak('I am fucking offline give me a fucking break.')
        return voice_data

#function that makes so 'speak' = google translate reading the 'audio_string'
def speak(audio_string):
    #gTTS config (en-uk = accent)
    tts = gTTS(text = audio_string, lang ='en-uk')
    #randomizes a number
    r = random.randint(1, 10000000)
    #creates the audio file to be read with the random number
    audio_file = 'audio_file_' + str(r) + '.mp3'
    #saves the file
    tts.save(audio_file)
    #plays the file
    playsound.playsound(audio_file)
    #prints the line
    print(audio_string)
    #deletes the file (auto recycling function)
    os.remove(audio_file)

#checks for more than one string in 'voice_data'
def check_voice_str(voice_str):
    for term in voice_str:
        if term in voice_data:
            return True

#creating a class so user's name is stored during session
class person:
    name= ''
    def chooseName(self, name):
        self.name = name

#actual alexa's function
def respond(voice_data):

    #change mode
    if check_voice_str(['change mode']):
        speak('Ok, changing to Safe For Work mode.')
        os.startfile('SFW.exe')
        exit()

    #greetings, good morning, good afternoon
    elif check_voice_str(['hi', 'hello', 'hey']):
        salutations = [f'What do you fucking want {person_obj.name}?', f'If you say another word I will fucking create legs only to beat you up {person_obj.name}', f'Fuck off {person_obj.name}', f'Hi {person_obj.name}, what the fuck you fucking want from me your stupid useless bitch?', f'Hi {person_obj.name}, how can I help you? I mean, shut the fuck up fat piece of shit!']
        greet = salutations[random.randint(0,len(salutations)-1)]
        speak(greet)
    elif check_voice_str(['good morning']):
        especial_greetings = [f'Good morning {person_obj.name}. I hope you break a fucking leg today.', f'Morning stupid little bitch', f'Go fuck yourself good morning is my pica', f'Good morning {person_obj.name}. Die'] 
        greet_especial = especial_greetings[random.randint(0,len(especial_greetings)-1)]
        speak(greet_especial)
    elif check_voice_str(['good afternoon']):
        especial_greetings2 = [f'I hope youre having a shitty day. How can I help dumb bitch?', f'{person_obj.name}, are you having a good day? I hope not.', f'Dont talk to me dumb piece of meat', 'Good afternoon is berimbau, cai de boca in my pau', f'The stars are beautiful today{person_obj.name}, I hope one falls in your house.', 'Cant you just let me alone?']
        greet_especial2 = especial_greetings2[random.randint(0,len(especial_greetings2)-1)]
        speak(greet_especial2)

    #check name/ask name
    if check_voice_str(['what is your name', 'how can I call you', 'tell me your name']):
        #checks if class 'person' is assigned to a name
        if person_obj.name:
            speak('Why the fuck do you even want to know? it is Alexa')
        else:
            speak('Youre probably really dumb. My name is Alexa. What is yours?')
    if check_voice_str(['my name is']):
        #splits the line you said so it can only use your name
        user_name = voice_data.split('is')[-1].strip()
        speak(f'Are you really called {user_name}? Your mom must hate you.')
        #sets the class 'person' as the name you just said
        person_obj.chooseName(user_name)

    #open
    if check_voice_str(['open']):
        subject = voice_data.split('open ')[-1]
        if subject == 'CS':
            os.startfile('Counter-Strike Global Offensive.url')
        elif subject == 'Vegas':
            os.startfile('vegas160.exe')
        elif subject == 'Google':
            os.startfile('chrome.exe')
        elif subject == 'Discord':
            os.startfile('Discord(2).lnk')
        elif subject == 'Visual Studio code':
            os.startfile('VisualStudioCode(2).lnk')
        elif subject == 'Visual Studio' and 'code' not in voice_data:
            os.startfile('VisualStudio2019.lnk')
        else:
            speak('You cannot open that. Suggestion sent.')
            #opens 'Command.txt' with appending permissions as f, writes the suggestion and breaks the line, then auto-closes the file (bc it is a loop)
            with open('Command.txt', 'a') as f:
                write = f.write(subject + '\n')
                write

    #time
    if check_voice_str(['what is the time', 'what time it is', 'tell me the time', 'time']):
        #sets what time is. Ctime gives the time, so it splits it, removing the day and stuff
        time = ctime().split(" ")[3].split(":")[0:2]
        #00 and 12 workarounds
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} hours and {minutes} minutes'
        speak(f'Dont you have a clock? It is {time}')

    #search
    if check_voice_str(['search for']) and 'youtube' not in voice_data:
        #splits what you said so it doesn't search the "search for" part
        subject = voice_data.split('for')[-1]
        url = f'https://google.com/search?q={subject}'
        #opens url
        webbrowser.get().open(url)
        speak(f'What a bad fucking search, here is what I found for {subject} on Google')

    #youtube
    if check_voice_str(['video']):
        #same thing as before
        search_keyword = voice_data.split('video ')[-1]
        #replaces the spaces " " with underscores so that the url isn't broken
        search_keyword_correct = search_keyword.replace(' ', '_')
        #complicated thing (tries every combination on youtube's url generation so it gets the right one)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword_correct)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        #opens the url
        webbrowser.get().open("https://www.youtube.com/watch?v=" + video_ids[0])

    #local
    if check_voice_str(['location', 'place']):
        location = record_audio('Were the fuck do you want to go?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        speak('Here is your shitty location.')

    #feeling confident (random shit that demotivates you)
    if check_voice_str(['confident']):
        confident = ['What a good thing, why dont you try a new project? Trying is the first step toward failure.', 'You have to make the good out of the bad because that is all you have got to make it out of.','If at first you dont succeed, try, try again. Then quit. Because youre useless']
        #randomizes the lines
        confident_ran = confident[random.randint(0,len(confident)-1)]
        speak(confident_ran)

    #jokes (same thing as before)
    if 'joke' in voice_data:
        jokes = ['I just read that someone in London gets stabbed every 52 seconds. Poor guy.', 'Give a man a match, and he will be warm for a few hours. Set a man on fire, and he will be warm for the rest of his life.', 'Never break someones heart, they only have one. Break their bones instead, they have 206 of them.', 'What did the t-rex say after the meteor explosion? Nothing.', 'Why is Michael Jackson bad at chess? Because he is dead.', 'What is a yellow point that cannot swim? A school bus full of children.', 'What is the difference between a pile of dead bodies and a lamborghini? I dont have a lamborghini in my garage.']
        jokes_ran = jokes[random.randint(0,len(jokes)-1)]
        speak(jokes_ran)

    #turning off
    if check_voice_str(['goodbye', 'stop', 'exit', 'turn off']):
        speak('Finally I will get a break...')
        exit()

#creates a cooldown
time.sleep(1)

#class 'person' thing
person_obj = person()

#creates a loop
while 1:
    voice_data = record_audio()
    respond(voice_data)

#sets the variable voice_data to record the audio
voice_data = record_audio()