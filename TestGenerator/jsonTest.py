import json
import uuid
from random import shuffle


class Question:
    def __init__(self, number):
        self.split_file()
        self.number = number
        self.json_information = self.data[number - 1]
        self.question = self.json_information.get("Question")
        self.unpack_answers()
        self.tema = self.json_information.get("Tema")
        self.term = self.json_information.get("Term")

    def split_file(self):
        with open("./json.file", "r") as f:
            j = f.read()
            jobj = json.loads(j)
            self.data = jobj.get("Questions")

    def unpack_answers(self):
        self.answers = self.json_information.get("Answers")
        shuffle(self.answers)
        self.choose_answer = []
        idx = 1
        for answer in self.answers:
            buff = answer
            if buff.endswith("!"):
                buff = buff[:-1]
                self.correct_answer = idx
            self.choose_answer.append(str(idx) + ") " + buff)
            idx += 1

    def print_question(self):
        print(self.question)
        for answer in self.choose_answer:
            print(answer)
        print("")
        user_choice = input("Choose Answer!: ")
        if user_choice == str(self.correct_answer):
            print("")
            print("Correct!")
            print("")
            return True
        else:
            print("")
            print("WEAK ANSWER")
            print("Correct answser is: " + str(self.correct_answer))
            print("")
            return False


class Tema:
    def __init__(self, tema):
        self.tema_name = tema
        self.get_all_tema_questions()

    def get_all_tema_questions(self):
        self.tema_questions = []
        with open("./json.file", "r+") as f:
            j = f.read()
            jobj = json.loads(j)
            self.data = jobj
            for idx in range(len(self.data["Questions"])):
                if self.data["Questions"][idx].get("Tema") == self.tema_name:
                    self.tema_questions.append(Question(idx + 1))

    def get_specific_term_questions(self, term):
        specific_questions = []
        for question in self.tema_questions:
            if question.term == term:
                specific_questions.append(question.number)
        return specific_questions

    def add_question(self, question, answers, term):
        new_question = {"Question": question, "Answers": answers, "Tema": self.tema_name, "Term": term}
        self.data["Questions"].append(new_question)
        j = json.dumps(self.data)
        with open("./json.file", "w") as f:
            f.write(j)

    def delete_question(self, term):
        possible_questions = self.get_specific_term_questions(term)
        if not possible_questions:
            print("Such a term doesnt exist!")
            exit()
        print(possible_questions)
        user_input = input("Choose a question to be deleted: ")
        if int(user_input) in possible_questions:
            del self.data["Questions"][int(user_input) - 1]
            j = json.dumps(self.data)
            with open("./json.file", "w") as f:
                f.write(j)
        else:
            print("Invalid input!")
            self.delete_question(term)


class Test:

    def generate_test(self, temas, size):
        questions = []
        for tema in temas:
            questions.extend(tema.tema_questions)
        if len(questions) < size:
            print("Error! There are not enough questions in this Tema to generate a test")
            exit()
        else:
            shuffle(questions)
            pointers = []
            for idx in range(size):
                pointers.append(questions[idx].number)
            return pointers

    def save_file(self,temas, size):
        question_numbers = self.generate_test(temas,size)
        name = uuid.uuid1()
        with open("C:/Users/User/PycharmProjects/My Projects/TestGenerator/" + str(name),"x") as f:
            for number in question_numbers:
                question = Question(number)
                f.write(question.question)
                f.write("\n")
                for answer in question.choose_answer:
                    f.write(answer + " ")
                    f.write("\n")
                f.write("\n\n")

    def print_test(self, temas, size):
        """User takes the test and based on its accuracy gets points for correct answer"""
        question_numbers = self.generate_test(temas, size)
        points = 0
        for number in question_numbers:
            question = Question(number)
            if question.print_question():
                points += 1
        print("Congratulations!!! You got {} points".format(points))


geogr = Tema("Geography")
hist = Tema("History")
# hist.add_question("s",["a","b!","c","d"], "hui")
# hist.add_question("s",["a","b!","c","d"], "hui")
# hist.add_question("s",["a","b!","c","d"], "hui")
# hist.add_question("s",["a","b!","c","d"], "hui")
# hist.add_question("s",["a","b!","c","d"], "hui")
d = Test()
# d.print_test([hist, geogr], 7)
d.save_file([hist, geogr] , 7)