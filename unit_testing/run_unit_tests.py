import math
import string
from yaml import safe_load
from random import uniform, randint, choice, seed
from os import path, mkdir, system





def run_program():
    seed_nr = int(input("Please decide seed\n"))
    seed(seed_nr)
    exactvalue = 6
    intervalint = randint(15,70)
    intervalfloat = round(uniform(5, 7), 3)
    valuelist = choice([1,2,34,56,100])
    elem1 = [1,2,3,4,5,6,7]
    elem2 = [2,4,6,8,10,12,14]
    elem3 = [3,6,9,12,15,18,21]
    index_tuplu = randint (0, len(elem1) - 1)
    elem1 = elem1[index_tuplu]
    elem2 = elem2[index_tuplu]
    elem3 = elem3[index_tuplu]
    hidAnsw = 4

    answer1 = round(exactvalue + intervalint, 3)
    answer2 = round(elem1 - intervalfloat, 3)
    answer3 = round(valuelist - elem3, 3)

    to_echo = 'exactvalue {}; intervalint {}; intervalfloat {}; valuelist {}; elem1 {}; elem2 {}; elem3 {}; hidAnsw {}; answer1 {}; answer2 {}; answer3 {};'.format(
           exactvalue,    intervalint,    intervalfloat,    valuelist,    elem1,    elem2,    elem3,    hidAnsw,    answer1,    answer2,    answer3)
    system('echo "{}" > expected_rez'.format(to_echo))

run_program()
