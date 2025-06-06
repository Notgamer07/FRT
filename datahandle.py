import json

with open('data.json','r')as f:
    data = json.load(f)

def read_question(level, question_mo):
    questions = []
    for ques in data["levels"]:
        if ques["level"] == level:
            questions.append(ques["questions"][question_mo-1])
    return questions[0]

class Question:
    def __init__(self,level,questionNumber):
        data = read_question(level,questionNumber)
        self.question = data['question']
        self.option = data['options']
        self.currect = data['correct_answer']
    
    @classmethod
    def read_question(level, question_mo):
        questions = []
        for ques in data["levels"]:
            if ques["level"] == level:
                questions.append(ques["questions"][question_mo-1])
        return questions[0]

if __name__ == "__main__":
    q = Question(1,1)
    print(q.currect)