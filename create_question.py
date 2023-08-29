from yaml import safe_load, dump
from os import mkdir, stat
# ar trebui sa am si un fisier de config in care sa retin unde sa pun interbarile si restul fisierelor
from shutil import rmtree


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

questions_dictionary = {}
path_prefix = "/home/cata/Desktop/Exam_Creator/intrebari/"
questions_path = path_prefix + 'questions_dict'

def set_questions_path():
    global questions_path
    questions_path = path_prefix + 'questions_dict'


actual_question = ''


def check_question(question):
    if not question:
        print("Question name can't be empty")
        return -1
    
    if question not in questions_dictionary:
        print("Question not found in the questions list. Please make sure you"\
                " introduced the corect name")
        return -2

    return 0

def save_dictionary():
    with open(questions_path, "w") as qfile:
        qfile.write(dump(questions_dictionary)) 


def check_exam_dir():
    try:
        stat (path_prefix)
    except FileNotFoundError as e:
        print('Please create a correct exam directory first')
        create_exam_directory()

def create_exam_directory():
    dir_path = input ("Chose exam directory path (absolute):\n")
    try:
        mkdir(dir_path)
    except FileExistsError as e:
        print('loding data from directory "%s"' % dir_path)

    except FileNotFoundError as e:
        print ('failed to create directory "%s"' % dir_path)
        return
    global path_prefix
    if dir_path[len(dir_path)-1] != '/':
        dir_path += '/'
    path_prefix = dir_path
    set_questions_path()
    load_question_dict()


# questions_dictionary e de forma: {q_name: subtipuri_qname}
def load_question_dict():
    global questions_dictionary
    try:
        stat (questions_path)
    except FileNotFoundError as e:
        fp = open (questions_path, "x")
        fp.close()
        

    with open (questions_path, "r") as qfile:
        questions_dictionary = safe_load(qfile.read())
    if not questions_dictionary:
        questions_dictionary = {}
    print(type(questions_dictionary))


def show_question_dict():
    print (questions_dictionary)

def check_prefix_path():
    try:
        stat(path_prefix)
    # fix message to be coding styleble
    except FileNotFoundError as e:
        print ('directory "%s" not found. Modify your settings to an existing'\
            ' directory or create a new problems directory using commnad create_exam_dir' % path_prefix)
        return 1
    return 0


def create_question_directory(question_name):
    if check_prefix_path():
        return 1

    dir_path = path_prefix + question_name

    try:
        mkdir(dir_path)
    except FileExistsError as e:
        print ('name already used')
        return 1

    fp = open(dir_path+"/values.yaml", "x")
    fp.close()
    fp = open(dir_path+"/question_text.tex", "x")
    fp.close()
    return 0


def save_question_to_dict(question_name , tags):
    global actual_question
    actual_question = question_name
    questions_dictionary[question_name] = tags
    save_dictionary()

def create_new_question():

    question_name = input ("Chose question_name:\n")

    if question_name in questions_dictionary:
        print ("name already used")
        # momentan nu facem nimic in cazul asta. Probabil cand o sa fac UX o sa fie ceva cu next care nu te lasa sau idk    
        return
    if not create_question_directory(question_name):
        save_question_to_dict(question_name , ['main'])
    

def open_question_directory():
    global actual_question
    actual_question = ""
    
    question_name = input("What question do you want to open?\n")
    if question_name not in questions_dictionary:
        print("not a valid question")
        return
    actual_question = question_name

def delete_question():
    question_name = input ("Chose question_name to delete:\n")
    answer = input ('Are you sure you want to delete "%s"?(y/n). Deleted files cannot be recovered\n')
    if answer == 'y':
        if question_name not in questions_dictionary:
            print("Question %s not found" % question_name)
            return
        questions_dictionary.pop(question_name)
        rmtree(path_prefix+question_name+'/')
        print('Question deleted sucesfully')

    global actual_question
    actual_question = ""
    save_dictionary()

    
def update_question_text(question, new_text):
    check_question(question)
    check_prefix_path()
    dir_path = path_prefix + question
    try:
        fp = open(dir_path+"/question_text", "w")

    except FileNotFoundError as e:
        print("Question text not found, creating a new file")
        fp = open(dir_path+"/question_text", "x")
    print(new_text, file=fp)
    fp.close()

def modify_text():
    
    if not actual_question:
        print("Question name can't be empty")
        return
    
    text = input ("type new text")
    update_question_text(actual_question, text)

# asta e f grea o facem candva
def update_question_variables(question):
    check_question(question)
    check_prefix_path()
    dir_path = path_prefix + question
    try:
        fp = open(dir_path+"/values.yaml", "r+")

    except FileNotFoundError as e:
        print("Question text not found, creating a new file")
        fp = open(dir_path+"/values.yaml", "x")
    values = safe_load(fp.read())
    fp.close()
    print(values)
    
def modify_variables():
    
    if not actual_question:
        print("Question name can't be empty")
        return
    
    # text = input ("type new vars ig")
    update_question_variables(actual_question)


def update_question_type():
    print ("6")


def invalid():
    print("! Invalid option.")


def menu():
    print(welcome_text)
    check_exam_dir()
    load_question_dict()
    
    switch = {
        "addq": create_new_question,
        "open": open_question_directory,
        "seeq": show_question_dict,
        "create_exam_dir": create_exam_directory,
        "del": delete_question,
        "modt": modify_text,
        "modv": modify_variables,



        "exit": exit
    }


    while True:

        print(options_text)
        if actual_question:
            print("now working on question %s" % actual_question)
        else:
            print("no question selected, please select a question")


        func = switch.get(input(), invalid)
        func()
        print()
 
 
if __name__ == "__main__":
    menu()
