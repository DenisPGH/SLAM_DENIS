import pyttsx3

class Voice:
    def __init__(self):
        self.talking=pyttsx3.init()
        self.speaker = self.talking
        

    def speak_this(self,text:str):
        """
        :param text: the message which have to be spoken and say it,done!
        :return: nothing
        """
        self.speaker.setProperty("rate", 140)
        self.speaker.setProperty("voice", 'Bulgarian+m2')

        self.speaker.say(text)
        self.speaker.runAndWait()
        return