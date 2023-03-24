import math
from yaml import safe_load
from random import uniform, randint, choice


qsets = {}

def compute_qsets(questions_types_file):    
    global qsets

    with open(questions_types_file) as qfile:
        qsets = safe_load(qfile.read())

def read_values(fp):
    
    values = safe_load(fp.read())
    # functions = values.pop('Functions')
    hidden_vals = values.pop('Hidden')

    return values, hidden_vals

def pick_values_list_set(variable_dict, variable, values):
    if 'tuple' not in variable_dict:
        return compute_function(variable_dict, values)
    
    tpl = variable_dict['tuple']
    #                             lungimea primului elem din dictionar
    picked_index = randint(0, len(tpl[next(iter(tpl))]) - 1)
    for elem in tpl:
        values[elem] = tpl[elem][picked_index]

def pick_value(var_range, variable, values):
    match var_range:
        case int():
            return var_range

        case dict():
            if 'min' not in var_range:
                return pick_values_list_set(var_range, variable, values)
        
            minum = var_range['min']
            maxim = var_range['max']
            # if it's int we return an int
            if var_range['type'] == 'int':
                return(randint (minum, maxim))

            # else we return a float
            precision = var_range['precision']
        
            return round(uniform(minum, maxim), precision)

        case list():
            return choice(var_range)

        case _:
            raise ValueError('var_range is of incorrect type')


def call_lambda_funct(funct, args):
    return eval(funct)(*args)

def compute_function(lambda_function, values):
    var_values = []
    funct_to_call = lambda_function['funct']
    variable_names = lambda_function['variables'] 
    return_values = lambda_function['returns']
    precision = lambda_function['precision']

    for variable in variable_names:
        var_values.append(values[variable])

    answers = call_lambda_funct(funct_to_call, var_values)
    if type(answers) != type(list()):
        # function with only 1 return
        values[return_values[0]] = round(answers, precision)

        return
    
    for answer, var_name in zip(answers, return_values):
        values[var_name] = round(answer, precision)
    
    # return round(answer,precision)
    

def calculate_functions(functions_dict, values):

    for value_name in functions_dict:
        compute_function(functions_dict[value_name], values)


def create_values_from_variable_ranges(variable_ranges):
    values = {}
    for variable in variable_ranges:
        value = pick_value(variable_ranges[variable],variable, values)
        if value:
            values[variable] = value

    return values


def create_question(question, values, is_hidden):
    for value_name in values:
        if value_name in is_hidden:
            print("aici am val hidden: %f %s" % (values[value_name], value_name))
            # ar trb sa iau in calcul val, macar atunci cand generez ala de rasp calculate (gen sa mai trec o data prin noua intrebare doar cu val hidden)
            continue
        name = "{"+value_name+"}"
        question = question.replace(name, str(values[value_name]))
    return question

def add_question_exam(question, fp_values):
    variable_ranges, is_hidden = read_values(fp_values)
    values = create_values_from_variable_ranges(variable_ranges)
    question = create_question(question, values, is_hidden)
    print(question)

   
def create_question_from_text_file(question_file, values_file):
    with open(question_file) as qfile:
        with open (values_file, 'r') as vfile:
            question = qfile.read()
            add_question_exam(question, vfile)

'''
am un dictionar care arata in urmatorul fel:
    { qtype: {problems :[], childs : []}, qtype2 ...}
    in probelme am problemele care apartin tipului acela si in childs am subtipurile acestui tip
'''

def find_suitable_questions(qtype):
    if not qsets[qtype]['childs']:
        return qsets[qtype]['problems']
    
    child_problems = []
    for child in qsets[qtype]['childs']:
        child_problems +=  find_suitable_questions(child)
    return qsets[qtype]['problems'] + child_problems

     
def run_program():
    # quest_types este fisierul in care am stocat tipurile deja creeate in create_question
    compute_qsets('quest_types')
    # for i in range (100 * 20):
    possible_questions = find_suitable_questions('main_type')
    # print(possible_questions)
    # aleg o intrebare si o localizez
    create_question_from_text_file('input_file', 'values_file')
    

run_program()

