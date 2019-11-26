import AbstractApplication as Base
from threading import Semaphore
import time

class DialogFlowSampleApplication(Base.AbstractApplication):
    def meetingRobot(self):
        self.talk("Hello, I am Sleepy")

    def askingName(self):
        cloud_context   = 'answer_name'
        listen_timeout  = 5

        self.talk('What is your name?')

        self.name = None
        self.nameLock = Semaphore(0)
        self.setAudioContext(cloud_context)
        self.startListening()
        self.nameLock.acquire(timeout=listen_timeout)
        self.stopListening()
        if not self.name:  # wait one more second after stopListening (if needed)
            self.nameLock.acquire(timeout=1)

        print(self.name)
        # Respond and wait for that to finish
        if self.name:
            self.sayAnimated('Nice to meet you ' + self.name + '!')
        else:
            self.sayAnimated('Sorry, I didn\'t catch your answer.')
            self.askingName()
        self.speechLock.acquire()

    def readStory(self):
        cloud_context   = 'ask_read_story'
        listen_timeout  = 5

        self.talk('Do you want me to read a story?')

        self.read_story = None
        self.read_storyLock = Semaphore(0)
        self.setAudioContext(cloud_context)
        self.startListening()

        self.read_storyLock.acquire(timeout=listen_timeout)
        self.stopListening()
        print(self.read_story)
        if not self.read_story:  # wait one more second after stopListening (if needed)
            self.read_storyLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.read_story:
            if "no" in self.read_story:
               self.sayAnimated('Your answer is no')
               print("your answer is no")
               self.sayAnimated('Why don\'t you want to hear a story?')

            else:
              self.sayAnimated('Nice I will read a story.')
        else:
            self.sayAnimated('Sorry, I didn\'t catch your answer.')
            self.readStory()
        self.speechLock.acquire()

    def favoriteAnimal(self):
        cloud_context   = 'favorite_animal'
        listen_timeout  = 5

        self.talk('What is your favorite animal')

        self.animal = None
        self.animalLock = Semaphore(0)
        self.setAudioContext(cloud_context)
        self.startListening()
        self.animalLock.acquire(timeout=listen_timeout)
        self.stopListening()
        print("-", self.animal)

        if not self.animal:  # wait one more second after stopListening (if needed)
            self.animalLock.acquire(timeout=1)

        # Respond and wait for that to finish
        print(self.animal)

        if self.animal:
            self.sayAnimated('Oh nice, my favorite animal is '+self.animal+' too')
            self.readStory()
        else:
            self.sayAnimated('Sorry, I didn\'t understand.')
            time.sleep(2)
            self.favoriteAnimal()
        self.speechLock.acquire()


    def personalInterest(self):
        cloud_context   = 'personal_interest'
        listen_timeout  = 5

        self.talk('Do you like to play footbal?')

        self.personal_story = None
        self.personal_storyLock = Semaphore(0)
        self.setAudioContext(cloud_context)
        self.startListening()
        self.read_storyLock.acquire(timeout=listen_timeout)
        self.stopListening()

        if not self.personal_story:  # wait one more second after stopListening (if needed)
            self.personal_storyLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.personal_story:
            self.sayAnimated('ohh')
        else:
            self.sayAnimated('Sorry, I didn\'t understand.')
            self.personalInterest()
        self.speechLock.acquire()

    def main(self):
        self.setRecordAudio(True)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()

        # Dialogflow
        self.setDialogflowKey("keyfile.json")
        self.setDialogflowAgent("sleepy-gbdtuq")

        # self.meetingRobot()
        # self.askingName()
        self.favoriteAnimal()
        self.readStory()

#        self.personalInterest()

    def talk(self, message):
        self.speechLock = Semaphore(0)
        self.sayAnimated(message)
        self.speechLock.acquire()

    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()
        elif event == 'GestureDone':
            self.gestureLock.release()

    def onAudioIntent(self, *args, intentName):
        print("args", args)
        print("intentname", intentName)
        if intentName == 'answer_name' and len(args) > 0:
            self.name = args[0]
            self.nameLock.release()

        if intentName == 'ask_read_story' and len(args) > 0:
            self.read_story = args[0]
            self.read_storyLock.release()

        if intentName == 'personal_interest' and len(args) > 0:
            self.personal_story = args[0]
            self.personal_storyLock.release()

        if intentName == 'favorite_animal' and len(args) > 0:
            self.animal = args[0]
            self.animalLock.release()


# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
