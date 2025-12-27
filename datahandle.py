import json
import random as r
def read_data():
    with open('data1.json','r')as f:
        data = json.load(f)
    return data

def get_gameState()->dict:
    with open('settings.json','r') as f:
        game_state = json.load(f)
    return game_state

def save_gameState(data):
    with open('settings.json','w') as f:
        json.dump(data, f, indent= 4)


class Question:
    INDEX_LIST = [i for i in range(0,30)]
    data = read_data()
    def __init__(self):
        ques = self.__class__.read_question()
        self.question = ques['question'] # returns a string like "What is 2 + 3 ?"
        self.option = ques['options'] # returns a list of strings like ["4","5","6","7"]
        self.correct = ques['correct_answer']# returns currect string from option like "5"
    
    @classmethod
    def read_question(cls):
        r.shuffle(cls.INDEX_LIST)
        ques = cls.data[cls.INDEX_LIST[0]]
        cls.INDEX_LIST.pop(0)
        return ques
    
    def next_question(self):
        if not len(self.__class__.INDEX_LIST):
            raise IndexError("No More Question Left")
        ques = self.__class__.data[self.__class__.INDEX_LIST[0]]
        self.question = ques['question'] # returns a string like "What is 2 + 3 ?"
        self.option = ques['options'] # returns a list of strings like ["4","5","6","7"]
        self.correct = ques['correct_answer']# returns currect string from option like "5"
        self.__class__.INDEX_LIST.pop(0)
    
    @classmethod
    def reload_data(cls):
        cls.data = read_data()
        cls.INDEX_LIST = [i for i in range(0,29)]
        cls.read_question()

if __name__ == "__main__":
    q = Question()
    print(q.question)
    print(q.correct)
    q.next_question()
    print(q.question)
    print(q.correct)