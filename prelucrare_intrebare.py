import math
import string
from yaml import safe_load
from random import uniform, randint, choice
from os import path, mkdir, system
qsets = {}

VALUE_FILE = "values.yaml"
INPUT_FILE = "question_text.tex"
BEGIN_LATEX_TEXT = "\\begin{document}"
END_LATEX_TEXT = "\end{document}"
PDF_FILE_NAME = "pdf_files"

ANSWERS_BEG_TEXT = '''\\documentclass{exam}
\\begin{document}
\\begin{center}
\\fbox{\\fbox{\\parbox{5.5in}{\\centering
            \\begin{itemize}
'''

ANSWERS_END_TEXT = '''            \\end{itemize}}}}
\\vspace{0.2cm}
\\end{center}
\end{document}
'''

NEW_ITEM_TEX = '''                \item '''
STANDARD_TEX_EXAM_TEXT = '''% Exam package: Instructions & student name
\documentclass{exam}
\\begin{document}
\\begin{center}
\\fbox{\\fbox{\parbox{5.5in}{\centering
            \\textbf{Read carefully before starting the test:}
            \\begin{itemize}
                \item Answer the questions using
                    a blue or black pen.
                \item You can't use any electronic device.
            \end{itemize}}}}
\\vspace{0.1in}
\end{center}
\makebox[\\textwidth]{\\textsc{Full name:}\enspace\hrulefill}
\\vspace{0.2in}
\makebox[\\textwidth]{\\textsc{DATE:}\enspace\hrulefill}
\end{document}
'''



def compute_qsets(questions_types_file, dir_path):    
    global qsets
    file_name = path.join(dir_path, questions_types_file)
    with open(file_name) as qfile:
        qsets = safe_load(qfile.read())

def read_values(fp):
    
    values = safe_load(fp.read())
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


def create_question(question, values, is_hidden, answer_file, nr):
    answer_file.write("Q" + str(nr + 1) + ": ")
    for value_name in values:
        name = "[*"+value_name+"*]"
        if value_name in is_hidden:
            question = question.replace(name, '\\underline{\\hspace{3cm}}' + '(' + value_name + ')')
            hidden_answer = value_name + " = " +  str(values[value_name]) + "; "
            answer_file.write(hidden_answer)
            continue
        
        question = question.replace(name, str(values[value_name]))
    return question

def add_question_exam(question, fp_values, answer_file, nr):
    variable_ranges, is_hidden = read_values(fp_values)
    values = create_values_from_variable_ranges(variable_ranges)
    question = create_question(question, values, is_hidden, answer_file, nr)
    return question


def trim_document_commands(text):
    start_index = text.find(BEGIN_LATEX_TEXT) + len(BEGIN_LATEX_TEXT)
    end_index = text.find(END_LATEX_TEXT)
    return text[start_index:end_index]

def create_question_from_text_file(question_file, values_file, answer_file, nr):
    with open(question_file) as qfile:
        with open (values_file, 'r') as vfile:
            question = trim_document_commands(qfile.read())
            return add_question_exam(question, vfile, answer_file, nr)

'''
am un dictionar care arata in urmatorul fel:
    { qtype: {problems :[], childs : []}, qtype2 ...}
    in probelme am problemele care apartin tipului acela si in childs am subtipurile acestui tip
'''

def __find_questions(qtype, visited):
    if qtype in visited:
        return []
    
    visited.append(qtype)
    if not qsets[qtype]['childs']:
        return qsets[qtype]['problems']

    child_problems = []
    for child in qsets[qtype]['childs']:
        child_problems +=  __find_questions(child, visited)
    return qsets[qtype]['problems'] + child_problems

# ma mai gandesc aici putin.
# mai am celelate 2 tot
# fac maine asta si dupa scriu lejer repede o noapte 2
def find_suitable_questions(qtypes):
    qproblems = {}
    for name in qtypes.keys():
        questions = []
        for q_type in qtypes[name]:
            questions += __find_questions(q_type, [])
        qproblems[name] = list(set(questions))
    return qproblems

def read_exam_list(file_name):

    with open(file_name) as qfile:
        return safe_load(qfile.read())

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))


def create_exam_file(qexam, dir_path, output_file, exam_filler_text, answer_file, identifier):
    with open(output_file, mode = "x") as ofile:
        end_index = exam_filler_text.find(END_LATEX_TEXT)
        ofile.write(exam_filler_text[:end_index])
        q_list = []
        for i, name in enumerate(qexam.keys()):
            pos_questions = qexam[name]
            while pos_questions:
                q_name = choice(pos_questions)
                if q_name not in q_list:
                    q_list.append(q_name)
                    break   
                pos_questions.remove(q_name)

            if not pos_questions:
                print ("prea putine intrebari, mai adaugati intrebari")
                raise

            input_file = path.join(dir_path, str(q_name), INPUT_FILE)
            values_file = path.join(dir_path, str(q_name), VALUE_FILE)
            ofile.write(create_question_from_text_file(input_file, values_file, answer_file, i))
        # de facut identifier
        # de scris identifier in ambele parti
        # de facut in singur fisier cu identifier + raspunsuri
        ofile.write("\\paragraph{ANSWER IDENTIFIER: " + identifier + "}\n")
        ofile.write(exam_filler_text[end_index:])


def run_program():
    test_output_dir = input("Chose test output_directory:\n")
    if not path.isdir(test_output_dir):
        print ('failed to open directory "%s"' % dir_path)
        return  

    dir_path = input("Chose exam directory path (absolute):\n")
    if not path.isdir(dir_path):
        print ('failed to open directory "%s"' % dir_path)
        return  
    try:
        papers_nr = int(input("Please select how many exam papers should be created:\n"))
    except Exception as e:
        print ("not a number, please retry with a correct number")
        return

    compute_qsets('quest_types', dir_path)
    qeustions = read_exam_list('exam_file')
    possible_questions = find_suitable_questions(qeustions)
    
    test_output_latex_files = path.join(test_output_dir, "latex_files")
    test_output_pdf_files = path.join(test_output_dir, PDF_FILE_NAME)
    mkdir(test_output_latex_files)
    mkdir(test_output_pdf_files)

    answer_file = path.join(test_output_latex_files, "answer_file_" + get_random_string(10) + ".tex")
    with open(answer_file, mode = "x") as afile:
        afile.write(ANSWERS_BEG_TEXT)
        for i in range(papers_nr):
            identifier = get_random_string(10)
            afile.write(NEW_ITEM_TEX)
            afile.write('Identifier ' + identifier + " ")
            output_file = path.join(test_output_latex_files, "exam_file_" + identifier + ".tex")
            create_exam_file(possible_questions, dir_path, output_file, STANDARD_TEX_EXAM_TEXT, afile, identifier)
            afile.write('\n')
        afile.write(ANSWERS_END_TEXT)
    cmd = "cd " + test_output_latex_files + " ; for i in *.tex; do pdflatex -output-directory ../" + PDF_FILE_NAME + " $i; done"
    print(cmd)
    system(cmd)
run_program()

