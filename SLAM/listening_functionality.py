import speech_recognition as sr

from LOGIC import SlamMainLogic,Places
from speak_functionality import Voice
import re


class ListeningComands:
    def __init__(self):
        self.stimme = Voice()
        self.r = sr.Recognizer()
        self.code_word='go' # Go to 1!
        self.pattern_regex= "(?P<number>([0-9]+))"
        self.loc_question='you' # Where are you?
        self.logic=SlamMainLogic()
        self.dict_places={'a':'0' , 'b':'1' ,'c':'5'} # name:node
        self.finish='bye'
        self.place_to_node=Places.PLACES

    def __regex_helfer(self,sentence):
        """
        :param sentence: come sentence 'Go to 1!'
        :return: 1:number int
        """
        number = 0
        result=re.finditer(self.pattern_regex,sentence)
        for num in result:
            number=num.group("number")
        if int(number) !=0:
            return int(number)


    def listening(self):
        """
        This function listen from the microphone and recognise the voice ONLINE with help from google
        :return: Only the NUMBER (the key for walking 'Go to {node_name}!.')
        """
        try:
            while True:
                with sr.Microphone() as source:
                    self.r.adjust_for_ambient_noise(source, duration=0.7)  # 0.7
                    print("Speak Anything :")
                    audio = self.r.listen(source)
                    try:
                        text = self.r.recognize_google(audio)
                        print(text)
                        self.stimme.speak_this(text)
                        sentence = text.lower()
                        for each_word,node_number in self.place_to_node.items():
                            if each_word in sentence:
                                return node_number # return number

                        # if self.code_word in sentence:
                        #     #action => moving from current node, where the robot is to the target node!!!!
                        #     return self.__regex_helfer(sentence)
                        #     #return 2
                        if self.loc_question in sentence: # on which node I am
                            self.logic.where_are_you()

                        elif self.finish in sentence:
                            return 100
                        # else: # return node, but I said code word==> 'bad','livingroom', etc..
                        #     for word in self.dict_places.keys():
                        #         if word in sentence:
                        #             return self.dict_places['a']
                    except:
                        a="Sorry I could not recognize what you said!!"
                        print(a)
                        #self.stimme.speak_this(a)

        except KeyboardInterrupt:
            end="Program Finish!!!"
            print(end)
            self.stimme.speak_this(end)
