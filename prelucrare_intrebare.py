import math
from yaml import safe_load_all, full_load, safe_load
from random import uniform, randint, choice
from json import loads


qsets = {}

def compute_qsets(questions_types_file):
    global qsets

    with open(questions_types_file) as qfile:
        qsets = safe_load(qfile.read())

def read_values(fp):
    # values = munch.Munch()
    
    values = safe_load(fp.read())
    # values.update(munch.munchify(new))

    answers = values.pop('ANSWERS')
    return values, answers

def pick_value(var_range):
    print(var_range)
    match var_range:
        case int():
            return var_range

        case dict():
            minum = var_range['min']
            maxim = var_range['max']

            # if it's int we return an int
            if var_range['type'] == 'int':
                return(randint (minum, maxim))

            # else we return a float
            return uniform(minum, maxim)

        case list():
            return choice(var_range)

        case _:
            raise ValueError('var_range is of incorrect type')


def call_lambda_funct(funct, args):
    return eval(funct)(*args)

def compute_answer(lambda_function, variable_names, values):
    var_values = []

    for variable in variable_names:
        var_values.append(values[variable])

    answer = call_lambda_funct(lambda_function, var_values)
    return answer
    

def calculate_answers(answer_dict, values):

    for answer_name in answer_dict:
        values[answer_name] = compute_answer(answer_dict[answer_name]['funct'], answer_dict[answer_name]['variables'], values)


def create_values_from_variable_ranges(fp):
    variable_ranges, answers = read_values(fp)
    values = {}
    for variable in variable_ranges:
        values[variable] = pick_value(variable_ranges[variable])
    calculate_answers(answers, values)    
    return values


def create_question(question, values):
    for value_names in values:
        name = "{"+value_names+"}"
        question = question.replace(name, str(values[value_names]))
    return question

def add_question_exam(question, fp_values):
    values = create_values_from_variable_ranges(fp_values)
    question = create_question(question, values)
    print(values)
    print(question)

   
def create_question_from_text_file(question_file, values_file):
    with open(question_file) as qfile:
        with open (values_file, 'r') as vfile:
            question = qfile.read()
            print(question)
            add_question_exam(question, vfile)


def find_suitable_questions(qtype):
    if not qsets[qtype]['childs']:
        return qsets[qtype]['problems']
    
    child_problems = []
    for child in qsets[qtype]['childs']:
        child_problems +=  find_suitable_questions(child)
    return qsets[qtype]['problems'] + child_problems

     
def run_program():
    compute_qsets('quest_types')
    possible_questions = find_suitable_questions('main_type')
    print(possible_questions)
    # aleg o intrebare si o localizez
    # create_question_from_text_file('input_file', 'values_file')
    

run_program()

