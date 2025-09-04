import json
with open('data.json','r')as f:
    data = json.load(f)

def get_gameState()->dict:
    with open('settings.json','r') as f:
        game_state = json.load(f)
    return game_state

def save_gameState(data):
    with open('settings.json','w') as f:
        json.dump(data, f, indent= 4)

def read_question(level, question_mo):
    questions = []
    for ques in data["levels"]:
        if ques["level"] == level:
            questions.append(ques["questions"][question_mo-1])
    return questions[0]

class Question:
    def __init__(self,level,questionNumber):
        data = read_question(level,questionNumber)
        self.question = data['question'] # returns a string like "What is 2 + 3 ?"
        self.option = data['options'] # returns a list of strings like ["4","5","6","7"]
        self.correct = data['correct_answer']# returns currect string from option like "5"
        self.quesNumber = questionNumber
        self.level = level
    
    @staticmethod
    def read_question(level, question_mo):
        questions = []
        for ques in data["levels"]:
            if ques["level"] == level:
                questions.append(ques["questions"][question_mo-1])
        return questions[0]
