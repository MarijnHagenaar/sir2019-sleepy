import yaml
import re
import os

import AbstractApplication as Base
from threading import Semaphore

class DialogFlowSampleApplication(Base.AbstractApplication):
    dialog_list = []

    def yaml_open(self, dialog_name):

      print("\033[1;35;40m [!] \x1B[0m playing: "+dialog_name)

      with open(r'dialogs/'+dialog_name) as file:
        output = yaml.load(file, Loader=yaml.FullLoader)

        self.talk(self.get_input(output, "pre_talk"))

        name		= self.get_input(output, "name")
        name = name.replace("_", "")

        DialogFlowSampleApplication.dialog_list.append(name)
        listen_timeout	= self.get_input(output, "listen_timeout")
        lock_timeout	= self.get_input(output, "lock_timeout")

        print("\033[1;35;40m [!] \x1B[0m name: "+name)

        setattr(self, name, None)
        setattr(self, name+"Lock", Semaphore(0))

        self.setEyeColour("blue")
        # self.askreadstoryLock = Semaphore(0)



        self.setAudioContext(name)
        self.startListening()
        print(name)
        # self, name+'Lock'

        # print(self.askreadstoryLock.acquire(timeout=listen_timeout))

        result = getattr(self, name+'Lock')
        # re(timeout=listen_timeout)
        print(result.acquire(timeout=listen_timeout))
        # self.new_lock = name+"Lock"
        # self.new_lock.acquire(timeout=listen_timeout)
        self.stopListening()

        if not getattr(self, name):
            print(result.acquire(timeout=lock_timeout))
          # self.new_lock.acquire(timeout=lock_timeout)

        print(self.get_input(output, "input_none"))
        print(self.get_input(output, "input_max_tries"))

        robot_input = getattr(self, name)
        self.setEyeColour("white")
        
        if "input_success" in output:
          regex_match = self.get_input(output["input_success"], "match")

          if robot_input:
              print("match", regex_match)
              print("input", robot_input)
              match = re.match(regex_match, robot_input)

              if match:
                  print(self.get_input(output["input_success"][True], "return"))
                  print(self.get_goto(self.get_input(output["input_success"][True], "goto")))
              else:
                  print(self.get_input(output["input_success"][False], "return"))
                  print(self.get_goto(self.get_input(output["input_success"][False], "goto")))

          else:
              print(self.get_input(output["input_success"][False], "return"))
              print(self.get_goto(self.get_input(output["input_success"][False], "goto")))

        self.speechLock.acquire()

    def get_goto(self, goto):
        if re.search("(yaml)$", goto):
          self.yaml_open(goto)
        else:
          if goto in dir(os):
            globals()[goto]()

    def get_input(self, arr, name):
        try:
            return(arr[name])
        except:
            print("[!] no "+name+" found in ", arr)
        return ""

    def main(self):
        self.setRecordAudio(True)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()

        # Dialogflow
        self.setDialogflowKey("keyfile.json")
        self.setDialogflowAgent("sleepy-gbdtuq")

        self.get_goto("answer_name.yaml")

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

        if intentName in DialogFlowSampleApplication.dialog_list and len(args) > 0:
            self[intentName] = args[0]
            self[intentName+"Lock"].release()


# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
