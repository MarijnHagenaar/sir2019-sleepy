import yaml
import re
import os

import AbstractApplication as Base
from threading import Semaphore

class DialogFlowSampleApplication(Base.AbstractApplication):
    dialog_list = []
    name = ""

    def yaml_open(self, dialog_name):

        # Open yaml file
        print("\033[1;35;40m [!] \x1B[0m running: "+dialog_name)
        with open(r'dialogs/'+dialog_name) as file:

            # load yaml file
            output = yaml.load(file, Loader=yaml.FullLoader)

            # nao pre talk
            self.talk(self.get_input(output, "pre_talk"))

            # get name, this should correspond to dialogname
            name		= self.get_input(output, "name")
            name_filt   = name.replace("_", "")

            DialogFlowSampleApplication.dialog_list.append(name)

            # load timeouts
            listen_timeout	= self.get_input(output, "listen_timeout")
            lock_timeout	= self.get_input(output, "lock_timeout")


            print("\033[1;35;40m [-] \x1B[0m name: "+name)

            # declare variables
            setattr(self, name_filt, None)
            setattr(self, name_filt+"Lock", Semaphore(0))

            self.setAudioContext(name)

            # set eyecolour to blue, since nao is in listen mode
            self.setEyeColour("blue")
            self.startListening()

            # lock mode for audio
            result = getattr(self, name_filt+'Lock')
            print(result.acquire(timeout=listen_timeout))

            self.stopListening()


            print("\033[1;35;40m [-] \x1B[0m response: "+getattr(self, name_filt))

            if not getattr(self, name_filt):
                print(result.acquire(timeout=lock_timeout))


            print(self.get_input(output, "input_none"))
            print(self.get_input(output, "input_max_tries"))

            robot_input = DialogFlowSampleApplication.name
            print("robot_input", robot_input)
            self.setEyeColour("white")

            if "input_success" in output:
                regex_match = self.get_input(output["input_success"], "match")

                if robot_input:
                  print("match", regex_match)
                  print("input", robot_input)
                  match = re.match(regex_match, robot_input)

                  if match:
                      print("\033[1;35;40m [*] \x1B[0m match 1 ")

                      # Play gesture
                      self.play_gesture(self.get_input(output["input_success"][True], "gesture"))

                      # Talk
                      self.talk(self.get_input(output["input_success"][True], "return"))

                      # Go To next dialog or call a method
                      print(self.get_goto(self.get_input(output["input_success"][True], "gesture")))
                  else:
                      print("\033[1;35;40m [*] \x1B[0m match 2 ")

                      # Play gesture
                      self.play_gesture(self.get_input(output["input_success"][False], "gesture"))

                      # Talk
                      self.talk(self.get_input(output["input_success"][False], "return"))

                      # Go To next dialog or call a method
                      print(self.get_goto(self.get_input(output["input_success"][False], "goto")))
            else:
                print("\033[1;35;40m [*] \x1B[0m match 2 ")

                # Play gesture
                self.play_gesture(self.get_input(output["input_success"][False], "gesture"))

                # Talk
                self.talk(self.get_input(output["input_success"][False], "return"))

                # Go To next dialog or call a method
                print(self.get_goto(self.get_input(output["input_success"][False], "goto")))

            self.speechLock.acquire()
            DialogFlowSampleApplication.name = False


    def get_goto(self, goto):
        if re.search("(yaml)$", goto):
          self.yaml_open(goto)
        else:
          if goto in dir(os):
            globals()[goto]()

    def play_gesture(self, gesturename):

        print("\033[1;35;40m [-] \x1B[0m gesture start: "+name)

        self.gestureLock = Semaphore(0)

        print("\033[1;35;40m [-] \x1B[0m gesture name: "+gesturename)

        self.doGesture(gesturename)
        self.gestureLock.acquire()

        print("\033[1;35;40m [-] \x1B[0m gesture stop")

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
        self.setDialogflowKey("config/keyfile.json")
        self.setDialogflowAgent("sleepy-gbdtuq")

        # name of yaml file, inside dialogs directory
        self.get_goto("meeting_robot.yaml")

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
            # save in DialogFlowSampleApplication.name
            DialogFlowSampleApplication.name = args[0]

            # lock nameLock
            lockfunction = getattr(self, intentName.replace("_", "")+"Lock")
            lockfunction.release()


# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
