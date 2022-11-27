from yaml import safe_load
from os import mkdir
# ar trebui sa am si un fisier de config in care sa retin unde sa pun interbarile si restul fisierelor

welcome_text = """Hello, this is the add_question terminal Module."""
options_text = """To add a new question type addq
To open a specyfic question type open <question_name>
After selecting a question or adding a new question:
To modify a question text, type textm
To modify a question variables. type varm
To modify a question answers, type answm
To modify a question type, type typem
To see already defined questions typee seeq
To exit type exit
"""

questions_dictonary = {}
path_prefix = "/home/cata/Desktop/Exam_Creator/intrebari/"


def load_question_dict():
    global questions_dictonary
    with open ('questions_dict') as qfile:
        questions_dictonary = safe_load(qfile.read())
    if not questions_dictonary:
        questions_dictonary = {}
    print(type(questions_dictonary))

def show_question_dict():
    print (questions_dictonary)

def create_folder(qname):
    mkdir(path_prefix+qname)
    
def create_question_directory():
    q_name = input ("Chose question_name:\n")
    if q_name in questions_dictonary:
        print ("name already used")
        # momentan nu facem nimic in cazul asta. Probabil cand o sa fac UX o sa fie ceva cu next care nu te lasa sau idk    
        return
    create_folder(q_name)
    questions_dictonary[q_name] = 'ceva'

def open_question_directory():
    print ("2")


def update_question_text():
    print ("3")



def update_question_variables():
    print ("4")



def update_question_answers():
    print ("5")

def update_question_type():
    print ("6")


def invalid():
    print("! Invalid option.")


def menu():
    print(welcome_text)
    load_question_dict()
    
    while True:

        print(options_text, end='')
        switch = {
            "addq": create_question_directory,
            "open": open_question_directory,
            "seeq": show_question_dict,




            "exit": exit
        }
        func = switch.get(input(), invalid)
        func()
        print()
 
 
if __name__ == "__main__":
    menu()
