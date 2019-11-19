import AbstractApplication as Base
from threading import Semaphore

class DialogFlowSampleApplication(Base.AbstractApplication):
    def __init__(self, keyfile, agent):
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()
 
        # Dialogflow
        self.setDialogflowKey(keyfile)
        self.setDialogflowAgent(agent)
 
    def askQuestion(self, message):
        self.speechLock = Semaphore(0)
        self.sayAnimated(message)
        self.speechLock.acquire()

    def askName(self):
        cloud_context   = 'answer_name'
        listen_timeout  = 5
        
        self.askQuestion('Hello, what is your name?')

        # Listen for an answer for at most 5 seconds
        self.name = None
        self.nameLock = Semaphore(0)
        self.setAudioContext(cloud_context)
        self.startListening()
        self.nameLock.acquire(timeout=listen_timeout)
        self.stopListening()
        if not self.name:  # wait one more second after stopListening (if needed)
            self.nameLock.acquire(timeout=1)
 
        # Respond and wait for that to finish
        if self.name:
            self.sayAnimated('Nice to meet you ' + self.name + '!')
        else:
            self.sayAnimated('Sorry, I didn\'t catch your name.')
        self.speechLock.acquire()

    def main(self):
        self.askName()
 
    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()
        elif event == 'GestureDone':
            self.gestureLock.release()
 
    def onAudioIntent(self, *args, intentName):
        print(args)
        print(intentName)
        if intentName == 'answer_name' and len(args) > 0:
            self.name = args[0]
            self.nameLock.release()
 
 
# Run the application
sample = DialogFlowSampleApplication("keyfile.json", "sleepy-gbdtuq")
sample.main()
sample.stop()
