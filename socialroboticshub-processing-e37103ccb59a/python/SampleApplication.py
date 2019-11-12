import AbstractApplication as Base
from time import sleep

class SampleApplication(Base.AbstractApplication):
    def main(self):
        self.setLanguage('en-US')
        sleep(1)  # wait for the language to change
        self.sayAnimated('Hello, world!')
        sleep(3)  # wait for the robot to be done speaking (to see the relevant prints)

    def onRobotEvent(self, event):
        print(event)

# Run the application
sample = SampleApplication()
sample.main()
sample.stop()
