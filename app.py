import os
import matplotlib
from collections.abc import Callable
import re
from re import L
from math import e
import sys


# Denis Model

# TODO:
# ls: include parantheses
# all karnaugh map stuff/default to original functions

##################################
updated_on = '09/05/25 @ 2:00 AM'
##################################

# All App Layer Modules
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn3, venn3_circles
import numpy as np 
import random
import time
import os
import string
from datetime import datetime, timedelta

################################################################################
# All Web App Modules
import matplotlib
import io, base64, uuid
matplotlib.use("Agg")  # headless backend
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from textwrap import dedent

app = Flask(__name__) # This is initializing my flask app 
app.config['SECRET_KEY'] = 'pq569'  

#copy pasta
# save matplot diagram to a png

def fig_to_static_url(fig, subdir="q"):
    """Save fig under static/subdir/<id>.png and return its URL."""
    img_id = f"{uuid.uuid4()}.png"
    dir_path = os.path.join(app.static_folder, subdir)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, img_id)
    fig.savefig(file_path, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return url_for("static", filename=f"{subdir}/{img_id}")

def build_queue(skills, ask_list, shuffle=False):
    q = []
    for s, c in zip(skills, ask_list):
        q.extend([s] * int(c))
    if shuffle:
        random.shuffle(q)
    return q



################################################################################
# globals
DNF_OPS = ['n', 'u']
DNF_VARS = ['A', 'B', 'C']
QUESTION_TUPLE = ('abc', 'num', 'nums')

choice_list = ['all',
              'as','vb','vd','bd','db','so','rn','ca','ps','dm','sb','ss','v1','v2','v3',
              'al','ls','pt','kp','pk','cp', 'ct', 'ck', 'pe']

def clean_dnf(dnf):
  # this function will get the answer for randomly generated dnf
  clean_dnf = dnf.replace("__", "")

  return clean_dnf

# single notation
def list_to_bit_strings(abc_region, bit_streams):

  ans_list = []

  for key, val in bit_streams.items():
    if key == abc_region:
      ans_list = val

  #ans_list will equal the complement of whatever
  #convert list to string

  bit_strings = []

  for i in range(len(ans_list)):
    bit_strings.append(list_to_string(ans_list[i]))

  return bit_strings

def create_stuff(notation, ques_type):

  weight_s = {'rn': [.1, .4, .5],
            'ca': [.2, .6, .2],
            'dm': [.3, .6, .1],
            'ps': [.2, .6, .2],
            'pt': [.5, .5]}

  choices = [1, 2, 3]

  if notation == 'logic':
    logic = ['P', 'Q']
    n_or_v = ['^', 'v'] #'->', '<->']
    choices = [1, 2]
  elif notation == 'dnf':
    abc = ['A', 'B', 'C']
    u_or_n = ['u', 'n']

  compliment = ['_', '__', '']

  notations = []

  # loop twice to get 2 expressions
  for _ in range(2):

    selection = int(random.choices(choices, weights=weight_s[ques_type])[0])

    region_l = []
    chosen = []

    while len(region_l) < selection:

      # This is for having duplicates and no sorting
      #index = random.randint0, len(logic) - 1) if notation == 'logic' else random.randint(0, len(abc) - 1)
      #region_l.appendlogic[index] if notation == 'logic' else abc[index])

      # this is not allowing duplicates and sorting
      # we can change this later and allow duplicates
      if notation == 'logic':
        index = random.randint(0, len(logic) - 1)
        #if logic[index] not in region_l:
          #region_l.append(logic[index])
        region_l.append(logic[index])

        if logic[index] == 'P':
          weight_s[ques_type] = [.3, .7]
        else:
          weight_s[ques_type] = [.7, .3]

#        print(f"QUES_TYPE: {weight_s[ques_type]}")

      else:
        index = random.randint(0, len(abc) - 1)
        #if abc[index] not in region_l:
          #region_l.append(abc[index])
        region_l.append(abc[index])

      region_l.sort()

    compliment_list = [compliment[int(random.choices([0, 1, 2], weights=[0.4, 0.1, 0.5])[0])] for _ in range(selection)]
    #print(f"LIST: {compliment_list}")

    u_or_n_list = [random.choice(n_or_v) if notation == 'logic' else random.choice(u_or_n) for _ in range(selection - 1)]

    u_or_n_list.append('')

    dnf_notation = ""

    for i in range(selection):
      dnf_notation = f"{dnf_notation}{compliment_list[i]}{region_l[i]}{u_or_n_list[i]}"

    inc_parantheses = f"({dnf_notation})"

    distribute = 10
    if distribute == 10:
      inc_parantheses = f"_{inc_parantheses}"

    notations.append(inc_parantheses)
    #printf"inc_parantheses: {inc_parantheses}")
    #notations.appenddnf_notation)

    # Trying to create a logical statement w/ two expressions

    if notation == 'logic' and len(notations) == 2:
      always_n_v = ['^', 'v', '->', '<->']
      select_one = int(random.choices([0, 1, 2, 3], weights=[.4, .4, .1, .1])[0])
      middle_operation = always_n_v[select_one]
      two_expressions = f"{notations[0]}{middle_operation}{notations[1]}"

      # I want to create a statement that does negation distributing and one that uses demorgans law.
    elif notation == 'dnf' and len(notations) == 2:
      always_u_n = ['u', 'n']
      select_one = int(random.choices([0, 1], weights=[.5, .5])[0])
      middle_operation = always_u_n[select_one]
      two_expressions = f"{notations[0]}){middle_operation}({notations[1]})"

    # How to retrieve the answer from the statement?

    # if we get _P^Q)v(_PvQ)
    # convert to a list
    # ['_', '', 'P', '^', 'Q', ')', 'v', '(', '_', 'P', 'v', 'Q', ')']

  return notations, two_expressions, middle_operation
  #return dnf_notation

def list_to_string(ans_list):

  new_string = ""

  for i in range(len(ans_list)):
    new_string = f"{new_string}{ans_list[i]}"

  return new_string


################################################################################

# venn 1 set
#from IPython.display import Image, display
import glob

def v1_create():
  # use venn2 to create venn1

  U = random.randint(60, 100)
  A = random.randint(1, U - 1)
  _A = U - A

  fig, ax = plt.subplots()
  v = venn2(subsets=(A, 0, 0), set_labels=('', ''), ax=ax)

  v.get_patch_by_id('10').set_color('skyblue')
  shift_x = 0.15

  # remove B circle
  select_question = random.randint(0, 2)
  regions = ['01', '11'] if select_question != 1 else ['10', '01', '11']

  for region in regions:
    if region == '01' or region == '11':
      if v.get_patch_by_id(region): v.get_patch_by_id(region).set_visible(False)
    if v.get_label_by_id(region): v.get_label_by_id(region).set_visible(False)
  # hide the B label
  if v.set_labels[1]: v.set_labels[1].set_visible(False)


  circles = venn2_circles(subsets=(A, 0, 0), ax=ax, linewidth=2)
  # venn2_circles returns a list of circle object
  # circles[0] == 'A'
  if circles[0]:
    cx, cy = circles[0].center # each circle has an obj 'center' that gives (x, y)
    circles[0].set_center((cx + shift_x, cy))  # we provide a tuple of new coords n move the circle outline
    v.get_patch_by_id('10').set_center((shift_x, 0))  # move filled region of circle

  label = v.get_label_by_id('10')
  label.set_position((shift_x, 0)) # move the value

  #plt.title("Venn Diagram")
  plt.text(0, 0.7, 'Venn Diagram')
  plt.text(-0.7, 0.7, f'U = {U}')
  plt.text(0.9, -0.7, _A)

  plt.show()
  # types of questions
  person = 'person'
  select_question = random.randint(0, 2)

  if select_question == 0:
    question = f'How many possible bit streams are there? '
    answer = 2

  elif select_question == 1:
    v.get_label_by_id('10').set_visible(False)
    question = f'{U} people got tested for COVID. {_A} {person if _A == 1 else "people"} tested negative. How many people have COVID? '
    answer = A

  elif select_question == 2:
    question = f'{A} people were positive for COVID and {_A} people tested negative. How many people have tested for COVID? '
    answer = U
  

  return question, answer

  # venn 2 stuff
def generate_random_values_venn2():
  U = random.randint(78, 148)  # if universe is = to arbitrary #, we can calc the rest
  # every 7 we increment Universe by
  # +2 to intersectoins (AnB, AnC, BnC), and +4 to whole sections (A, B, C)

  a_or_b_bigger = random.randint(0, 1)
  base_U = 78
  base_A = 28
  base_B = 39
  if a_or_b_bigger == 1:
    base_A = 39
    base_B = 28
  base_AnB = 8

  U_diff = U - base_U
  increments = U_diff // 7

  A = base_A
  B = base_B
  AnB = base_AnB

  for i in range(increments):
    A += 4
    B += 4
    AnB += 2

  whole_circle = A + B - AnB

  An_B = A - AnB
  _AnB = B - AnB

  _An_B = U - whole_circle

  return U, A, B, AnB, An_B, _AnB, _An_B

def generateQuestion_venn2():
  global streak # an idea to give students harder questions if they are on a specific streak (10 ina row or something)

  random_int = random.randint(0, 4) # usin rand value to pick question type

  U, A, B, AnB, An_B, _AnB, _An_B = generate_random_values_venn2()

  if random_int <= 0:
    # ask for _An_B
    question = f"{U} students were surveyed, {A} students took calculus, {B} students took physics, and {AnB} students took both. \nHow many students took neither?"
    return U, A, B, AnB, An_B, _AnB, _An_B, question, _An_B

  elif random_int == 1:
    # ask for An_B + _AnB

    An_Bu_AnB = _AnB + An_B

    question = f"{A} students took calculus, {B} students took physics, {_AnB} students took only physics, and {_An_B} students took neither. \nHow many students took at least one class? "
    return U, A, B, AnB, An_B, _AnB, _An_B, question, An_Bu_AnB

  elif random_int == 2:
    # find A

    question = f"{An_B} students took only calculus, {_AnB} students took only physics, {AnB} students took both calculus and physics, and {_An_B} students took neither. \nHow many students took calculus? "
    return U, A, B, AnB, An_B, _AnB, _An_B, question, A

  elif random_int == 3:
    # find B
    question = f"{An_B} students took only calculus, {_AnB} students took only physics, {AnB} students took both calculus and physics, and {_An_B} students took neither. \nHow many students took physics? "
    return U, A, B, AnB, An_B, _AnB, _An_B, question, B

  elif random_int == 4:
    # find AnB
    question = f"{U} students were surveyed, {An_B} students took only calculus, {_AnB} students took only physics, and {_An_B} students took neither. \nHow many students took both calculus and physics? "
    return U, A, B, AnB, An_B, _AnB, _An_B, question, AnB

# under construction
#  elif random_int == 5 and streak >= 5: # this can be changed
#    U = random.randint(1050, 1200)
#    A = random.randint(550, 650)
#    B = random.randint(350, 450)
#    AnB = random.randint(100, 200)
#
#    An_B = A - AnB
#    #_An_B = U - whole_circle
#
#    answer = An_B + _An_B
#
#    question = f"{U} participants surveyed. {A} people have diabetes. {B} people have diarrhea and {AnB} have both diabetes and diarrhea. Find how many people have no condition, plus the amount of people that have only diarrhea. "
#
#    return question, answer
#
  #return values to access later
  return U, A, B, AnB, An_B, _AnB, _An_B

def venn_2_diagram(venn_labels_list,venn_type='elements'):
  font_size = 8

  An_B  = venn_labels_list[4]  # 100/a
  _AnB  = venn_labels_list[5]  # 010/b
  AnB = venn_labels_list[3]  # 001/c
  _An_B  = venn_labels_list[6]  # 001/c

  U = venn_labels_list[0]

  size_list = (An_B, _AnB, AnB, _An_B)
  bit_list = ('10','01','11','00')

  v = venn2(subsets=(An_B,_AnB,AnB,_An_B), set_labels=('A','B'))

  for text in v.set_labels:
    text.set_fontweight('bold')

  venn2_circles(subsets=(size_list),
                linestyle="solid",
                linewidth=2)

  for text in v.subset_labels:
    text.set_fontsize(font_size)

  #add text at (x, y)
  plt.text(-0.2,0.55,'Venn Diagram')
  plt.text(-0.7,0.52,f'U = {U}').set_fontsize(font_size)        # Universe
  plt.text(0.55,-0.45, str(_An_B).replace('[','').replace(']','').replace("'",'')).set_fontsize(font_size)  # 000/h

  # Change Backgroud
  plt.gca().set_facecolor('lightgray')
  plt.gca().set_axis_on()
  plt.show()

def venn_2():

  U, A, B, AnB, An_B, _AnB, _An_B, question, answer = generateQuestion_venn2()
  venn_labels_list = [U, A, B, AnB, An_B, _AnB, _An_B, question, answer]

  venn_2_diagram(venn_labels_list, '')
  # get the diagram

  return question, answer

################################################################################
# This venn_3 is for v3 only


def generate_venn3_questions():

  U = random.randint(122, 230) # this will be the # of positive results for problem

  # only *decent* way I can figure out how to create valid values for venn
  # open for suggestions

  # why not
  base_universe = 149
  base_positive = 122 # patients w/ positive results
  base_A = 73
  base_B = 52
  base_C = 62
  base_AnB = 26
  base_AnC = 31
  base_BnC = 23

  # find difference from universe to base
  # this will be a arithmetic sequence with a difference of 7

  # for each term in the sequence we:
  # +4 to whole sections (A, B, C), and +2 to intersectoins (AnB, AnC, BnC)

  diff_U = U - base_positive

  # find number of times we incremented by 7
  total_increments = diff_U // 7

  total_U = base_universe
  A = base_A
  B = base_B
  C = base_C
  AnB = base_AnB
  AnC = base_AnC
  BnC = base_BnC

  for i in range(total_increments):
    total_U += 8
    A += 4
    B += 4
    C += 4
    AnB += 2
    AnC += 2
    BnC += 2

  AnBnC = ( AnB + AnC + BnC) - (A + B + C) + U
  _An_Bn_C = total_U - U

  AnBn_C = AnB - AnBnC
  _AnBnC = BnC - AnBnC
  An_BnC = AnC - AnBnC

  _AnBn_C = B - (AnBn_C + _AnBnC + AnBnC)
  #

  An_Bn_C = A - (AnBn_C + An_BnC + AnBnC)
  _An_BnC = C - (_AnBnC + An_BnC + AnBnC)

  random_choice = random.randint(1, 9)

  # planning on creating harder questions if user has high streak

  if random_choice == 1:

    question = f"""New drugs (Albanine, Betroxin, and Cepterol) were given to {total_U} patients. \n{U} patients showed a positive reaction.\nAlbanine produced {A} positive reactions.\nBetroxin produced {B} positive reactions.
\nCepterol produced {C} positive reations.
\nAll cases where Albanine and Betroxin were used together produced {AnB} positive reactions.
\nAll cases where Albanine and Cepterol were used together produced {AnC} postive reations.
\nAll cases where Betroxin and Cepterol were used together produced {BnC} positive reations.
\nWhat were the results for Betroxin only?"""

    question_type = 1
    answer = _AnBn_C

    return total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer

  elif random_choice == 2:

    greatest_drug = max(An_Bn_C, _AnBn_C, _An_BnC)
    greatest_combination = max(AnBnC, AnBn_C, An_BnC, _AnBnC)

    answer = max(greatest_drug, greatest_combination)

    question = f"""New drugs (Albanine, Betroxin, and Cepterol) were given to {total_U} patients. \n{U} patients showed a positive reaction.\nAlbanine produced {A} positive reactions.\nBetroxin produced {B} positive reactions.\nCepterol produced
    {C} positive reations.\nAll cases where Albanine and Betroxin were used together
    produced {AnB} positive reactions.\nAll cases where Albanine and Cepterol were
    used together produced {AnC} positive reations.\nAll cases where Betroxin and
    Cepterol were used together produced {BnC} positive reations.\nWhat drug or combination of drugs produced the highest positive results?"""

    question_type = 2

    return total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer

  elif random_choice == 3:

    lowest_drug = min(An_Bn_C, _AnBn_C, _An_BnC)
    lowest_combination = min(AnBnC, AnBn_C, An_BnC, _AnBnC)

    answer = min(lowest_drug, lowest_combination)

    question = f"""New drugs (Albanine, Betroxin, and Cepterol) were given to {total_U} patients. \n{U} patients showed a positive reaction.\nAlbanine produced {A} positive
    reactions.\nBetroxin produced {B} positive reactions.\nCepterol produced
    {C} positive reations.\nAll cases where Albanine and Betroxin were used together
    produced {AnB} positive reactions.\nAll cases where Albanine and Cepterol were
    used together produced {AnC} positive reations.\nAll cases where Betroxin and
    Cepterol were used together produced {BnC} positive reations.\nWhat drug or combination of drugs produced the lowest positive results?"""

    question_type = 3

    return total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer

  elif random_choice == 4:

    answer = AnBnC

    question = f"""New drugs (Albanine, Betroxin, and Cepterol) were given to {total_U} patients. \n{U} patients showed a positive reaction.\nAlbanine produced {A} positive reactions.\nBetroxin produced {B} positive reactions.\nCepterol produced {C} positive reations.\nAll cases where Albanine and Betroxin were used together produced {AnB} positive reactions.\nAll cases where Albanine and Cepterol were used together produced {AnC} positive reations.\nAll cases where Betroxin and Cepterol were used together produced {BnC} positive reations.\nWhat were the results for the combination of all three drugs?"""

    question_type = 4

    return total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer

  elif random_choice == 5:

    answer = AnBn_C

    question = f"""New drugs (Albanine, Betroxin, and Cepterol) were given to {total_U} patients. \n{U} patients showed a positive reaction.\nAlbanine produced {A} positive
reactions.\nBetroxin produced {B} positive reactions.\nCepterol produced {C} positive reations.\nAll cases where Albanine and Betroxin were used together produced {AnB} positive reactions.\nAll cases where Albanine and Cepterol were used together produced {AnC} positive reations.\nAll cases where Betroxin and Cepterol were used together produced {BnC} positive reations.\nWhat were the results for the combination of only Albanine and Betroxin?"""

    question_type = 5

    return total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer

  elif random_choice == 6:

    answer = An_BnC

    question = f"""New drugs (Albanine, Betroxin, and Cepterol) were given to {total_U} patients. \n{U} patients showed a positive reaction.\nAlbanine produced {A} positive
reactions.\nBetroxin produced {B} positive reactions.\nCepterol produced {C} positive reations.\nAll cases where Albanine and Betroxin were used together produced {AnB} positive reactions.\nAll cases where Albanine and Cepterol were used together produced {AnC} positive reations.\nAll cases where Betroxin and Cepterol were used together produced {BnC} positive reations.\nWhat were the results for the combination of only Albanine and Cepterol?"""

    question_type = 6

    return total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer

  elif random_choice == 7:

    answer = _AnBnC

    question = f"""New drugs (Albanine, Betroxin, and Cepterol) were given to {total_U} patients. \n{U} patients showed a positive reaction.\nAlbanine produced {A} positive
reactions.\nBetroxin produced {B} positive reactions.\nCepterol produced {C} positive reations.\nAll cases where Albanine and Betroxin were used together produced {AnB} positive reactions.\nAll cases where Albanine and Cepterol were used together produced {AnC} positive reations.\nAll cases where Betroxin and Cepterol were used together produced {BnC} positive reations.\nWhat were the results for the combination of only Betroxin and Cepterol?"""

    question_type = 7

    return total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer

  elif random_choice == 8:

    answer = _An_BnC

    question = f"""New drugs (Albanine, Betroxin, and Cepterol) were given to {total_U} patients. \n{U} patients showed a positive reaction.\nAlbanine produced {A} positive reactions.\nBetroxin produced {B} positive reactions.\nCepterol produced {C} positive reations.\nAll cases where Albanine and Betroxin were used together produced {AnB} positive reactions.\nAll cases where Albanine and Cepterol were used together produced {AnC} positive reations.\nAll cases where Betroxin and Cepterol were used together produced {BnC} positive reations.\nWhat were the results for Cepterol only?"""

    question_type = 8

    return total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer

  elif random_choice == 9:

    answer = An_Bn_C

    question = f"""New drugs (Albanine, Betroxin, and Cepterol) were given to {total_U} patients. \n{U} patients showed a positive reaction.\nAlbanine produced {A} positive reactions.\nBetroxin produced {B} positive reactions.\nCepterol produced {C} positive reations.\nAll cases where Albanine and Betroxin were used together produced {AnB} positive reactions.\nAll cases where Albanine and Cepterol were used together produced {AnC} positive reations.\nAll cases where Betroxin and Cepterol were used together produced {BnC} positive reations.\nWhat were the results for Albanine only?"""
    question_type = 9

    return total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer


def venn_3_v3():
  font_size = 8

  total_U, U, A, B, C, AnB, AnC, BnC, AnBn_C, An_BnC, _AnBnC, An_Bn_C, _AnBn_C, _An_BnC, AnBnC, _An_Bn_C, question, question_type, answer = generate_venn3_questions()
  venn_labels = [An_Bn_C,_AnBn_C,_An_BnC,AnBn_C,An_BnC,_AnBnC,AnBnC,_An_Bn_C]

  venn_set_labels = ('A','B','C')
  bit_list = ('100','010','001','110','101','011','111')

  size_list = [30, 30, 20, 30, 20, 20, 10]

  v = venn3(subsets=(size_list),
            set_labels=(venn_set_labels))

  for text in v.set_labels:
    text.set_fontweight('bold')

  venn3_circles(subsets=(size_list),
                linestyle="solid",
                linewidth=2)

  # manually override subsets since we assigned it to size_list for appearance
  for i, label in enumerate(bit_list):
    if v.get_label_by_id(label):
      v.get_label_by_id(label).set_text(venn_labels[i])

  for text in v.subset_labels:
    text.set_fontsize(font_size)

  #add text at (x, y)
  plt.text(-0.2,0.69,'Venn Diagram')
  plt.text(-0.70,0.64,f'U = {U}').set_fontsize(font_size) # Universe
  plt.text(0.55,-0.7, str(_An_Bn_C).replace('[','').replace(']','').replace("'",'')).set_fontsize(font_size)  # 000/h

  # Change Backgroud
  plt.gca().set_facecolor('lightgray')
  plt.gca().set_axis_on()

  plt.show()

  return question, answer


################################################################################
# This venn_3 is for all of Set Theory besides v3

def venn_3(venn_labels_list, venn_type='elements'):
    font_size = 8

    # (your existing values)
    An_Bn_C = 30; _AnBn_C = 30; AnBn_C = 30; _An_BnC = 20
    An_BnC = 20; _AnBnC = 20; AnBnC = 10

    size_list = [An_Bn_C,_AnBn_C,_An_BnC,AnBn_C,An_BnC,_AnBnC,AnBnC]
    venn_set_labels = ('A','B','C')
    bit_list = ('100','010','001','110','101','011','111')

    # Universe label
    if venn_type == 'elements':
        element_list = []
        for sublist in venn_labels_list:
            for element in sublist:
                element_list.append(element)
        element_list.sort()
        U = str(element_list).replace("'",'').replace('[','{').replace(']','}')
    elif venn_type in ('dnf','bit'):
        U = ''
    else:
        U = '1'

    # unpack provided labels
    An_Bn_C  = venn_labels_list[0]
    _AnBn_C  = venn_labels_list[1]
    _An_BnC  = venn_labels_list[2]
    AnBn_C   = venn_labels_list[3]
    An_BnC   = venn_labels_list[4]
    _AnBnC   = venn_labels_list[5]
    AnBnC    = venn_labels_list[6]
    _An_Bn_C = venn_labels_list[7]

    fig, ax = plt.subplots(figsize=(6, 6))
    v = venn3(subsets=size_list, set_labels=venn_set_labels, ax=ax)

    if v.set_labels:
        for text in v.set_labels:
            text.set_fontweight('bold')

    for i in range(len(venn_labels_list)-1):
        lbl = v.get_label_by_id(bit_list[i])
        if lbl:
            lbl.set_text(str(venn_labels_list[i]).replace('[','').replace(']','').replace("'",""))

    patch = v.get_patch_by_id('111')
    if patch:
        patch.set_color('white')

    venn3_circles(subsets=size_list, linestyle="solid", linewidth=2, ax=ax)

    if v.subset_labels:
        for text in v.subset_labels:
            if text: text.set_fontsize(font_size)

    ax.text(-0.2, 0.75, 'Venn Diagram')
    ax.text(-0.7, 0.65, f'U = {U}').set_fontsize(font_size)
    ax.text(0.4, -0.7, str(_An_Bn_C).replace('[','').replace(']','').replace("'",'')).set_fontsize(font_size)

    ax.set_facecolor('lightgray')
    ax.set_axis_on()

    return fig_to_static_url(fig)   # <-- return a /static URL

#def venn_3(venn_labels_list,venn_type='elements'):
#
#  font_size = 8
#  # initialize number of elements by section to scale diagram properly
#  An_Bn_C = 30  # 100/a (/)
#  _AnBn_C = 30  # 010/b (/)
#  AnBn_C  = 30  # 001/c -> 110
#  _An_BnC = 20  # 110/d -> 001
#
#  An_BnC  = 20  # 101/e (/)
#  _AnBnC  = 20  # 011/f (/)
#  AnBnC   = 10  # 111/g (/)
#  # _An_Bn_C = 0  # 000/h
#
#  #print(f"venn_labels_list {venn_labels_list}")
#
# # An_Bn_C = len(venn_labels_list[0])
# # _AnBn_C = len(venn_labels_list[1])
# # AnBn_C  = len(venn_labels_list[2])
# # _An_BnC = len(venn_labels_list[3])
# # An_BnC  = len(venn_labels_list[4])
# # _AnBnC  = len(venn_labels_list[5])
# # AnBnC   = len(venn_labels_list[6])
#
#  # the size_list is for scaling purposes. Do not change the size_list.
#  size_list = [An_Bn_C,_AnBn_C,_An_BnC,AnBn_C,An_BnC,_AnBnC,AnBnC]
#  #print(f"size_list {size_list}")
#
#  venn_set_labels = ('A','B','C')
#
#  dnf_list = ('An_Bn_C','_AnBn_C','_An_BnC','AnBn_C','An_BnC','_AnBnC','AnBnC')
#  bit_list = ('100','010','001','110','101','011','111')
#  abc_list = ('a','b','c','d','e','f','g')
#
#  # implement later
#  # dnf_var = [An_Bn_C,_AnBn_C,_An_BnC,AnBn_C,An_BnC,_AnBnC,AnBnC,_An_Bn_C]
#  # for i in range(len(dnf_var)):
#  #   dnf_var[i] = venn_labels_list[i]
#
#  An_Bn_C  = venn_labels_list[0]  # 100/a
#  _AnBn_C  = venn_labels_list[1]  # 010/b
#  _An_BnC  = venn_labels_list[2]  # 001/c
#  AnBn_C   = venn_labels_list[3]  # 110/d
#  An_BnC   = venn_labels_list[4]  # 101/e
#  _AnBnC   = venn_labels_list[5]  # 011/f
#  AnBnC    = venn_labels_list[6]  # 111/g
#  _An_Bn_C = venn_labels_list[7]  # 000/h
#
#  venn_labels = [An_Bn_C,_AnBn_C,_An_BnC,AnBn_C,An_BnC,_AnBnC,AnBnC,_An_Bn_C]
#
#  if venn_type == 'cardinality':
#    element_count = 0
#    for sublist in venn_labels_list:
#        for element in sublist:
#            element_count += element
#    U = element_count  # total number of elements
#
#  elif venn_type == 'elements':
#    element_list = []
#
#    for sublist in venn_labels_list:
#        for element in sublist:
#            element_list.append(element)
#    element_list.sort()
#    U = str(element_list).replace("'",'').replace('[','{').replace(']','}')
#
#  elif venn_type == 'fractions':
#    U = '1'
#
#  elif venn_type == 'decimals':
#    U = '1.000'
#
#  elif venn_type == 'percents':
#    U = '100%'
#
#  elif venn_type == 'dnf':
#    U = ''
#
#  elif venn_type == 'bit':
#    U = ''
#
#  else:
#    print('Invalid Venn Type')
#    return None
#
#  # depict venn diagram
#
#  fig, ax = plt.subplots(figsize=(6, 6))                                   
#  v = venn3(subsets=size_list, set_labels=venn_set_labels, ax=ax)          
#
# # v = venn3(subsets=(size_list),
# #           set_labels=(venn_set_labels))
#
#
#  for text in v.set_labels:
#    text.set_fontweight('bold')
#
#  # set text to defined label id
#  for i in range(len(venn_labels_list)-1):
#    lbl = v.get_label_by_id(bit_list[i])                                 
#    if lbl:
#      lbl.set_text(str(venn_labels_list[i]).replace('[','').replace(']','').replace("'",''))
#    #v.get_label_by_id(bit_list[i]).set_text(str(venn_labels_list[i]).replace('[','').replace(']','').replace("'",''))
#
#  # set color to defined path id
#
#  patch = v.get_patch_by_id('111')                                         
#  if patch:
#      patch.set_color('white')
#
#  #v.get_patch_by_id('111').set_color('white')
#
#  # add outline
# # venn3_circles(subsets=(size_list),
# #               linestyle="solid",
# #               linewidth=2)
#
#  venn3_circles(subsets=size_list, linestyle="solid", linewidth=2, ax=ax)  
#
#  for text in v.subset_labels:
#    text.set_fontsize(font_size)
#
#  #add text at (x, y)
##  plt.text(-0.2,0.75,'Venn Diagram')
##  plt.text(-0.7,0.65,f'U = {U}').set_fontsize(font_size)        # Universe
##  plt.text(0.4,-0.7, str(_An_Bn_C).replace('[','').replace(']','').replace("'",'')).set_fontsize(font_size)  # 000/h
##
##  # Change Backgroud
##  plt.gca().set_facecolor('lightgray')
##  plt.gca().set_axis_on()
##
##  plt.show()
#  
#  ax.text(-0.2, 0.75, 'Venn Diagram')                                      
#  ax.text(-0.7, 0.65, f'U = {U}').set_fontsize(font_size)                  
#  ax.text(0.4, -0.7, str(_An_Bn_C).replace('[','').replace(']','').replace("'",'')).set_fontsize(font_size)  
#
#  # Change Background
#  # plt.gca().set_facecolor('lightgray')                                   
#  # plt.gca().set_axis_on()                                                
#  ax.set_facecolor('lightgray')                                            
#  ax.set_axis_on()                                                         
#
#  # plt.show()                                                             
#  # return None                                                            
#  return fig_to_data_url(fig)                                             

################################################################################
 # working function sort of...

def venn3_display_shuffle_diagram(venn_type):
    min_elements, max_elements = 1, 24
    min_num_elements, max_num_elements = 1, 3
    num_of_regions = 8

    if venn_type == 'num':
        region_list = [[str(i+1)] for i in range(num_of_regions)]
    elif venn_type == 'nums':
        region_list = []
        while len(region_list) < num_of_regions:
            random_list = [
                random.randint(min_elements, max_elements)
                for _ in range(random.randint(min_num_elements, max_num_elements))
            ]
            if not any(el in sub for sub in region_list for el in random_list):
                region_list.append(list(set(random_list)))
    else:
        region_list = ['a','b','c','d','e','f','g','h']  # fallback

    random.shuffle(region_list)
    img_url = venn_3(region_list, venn_type='elements')
    return region_list, img_url


#def venn3_display_shuffle_diagram(venn_type):
#
#    min_elements = 1
#    max_elements = 24
#    min_num_elements = 1
#    max_num_elements = 3
#
#    num_of_regions = 8
#
#    region_list = ['a','b','c','d','e','f','g','h']
#
#    # elements = True   # (unused) -> remove
#
#    if venn_type == 'num':
#        count = 0
#        region_list = []
#        for i in range(num_of_regions):
#            count += 1
#            region_list.append([str(count)])
#
#    elif venn_type == 'nums':
#        region_list = []
#        while len(region_list) < num_of_regions:
#            random_list = [
#                random.randint(min_elements, max_elements)
#                for _ in range(random.randint(min_num_elements, max_num_elements))
#            ]
#            # no duplicate elements across sublists
#            if not any(element in sub for sub in region_list for element in random_list):
#                region_set = set(random_list)  # de-dupe within sublist
#                region_list.append(list(region_set))
#
#    random.shuffle(region_list)
#
#    img_url = venn_3(region_list, venn_type='elements')
#
#    return region_list, img_url

#def venn3_display_shuffle_diagram(venn_type):
#
#  min_elements = 1
#  max_elements = 24
#  min_num_elements = 1
#  max_num_elements = 3
#
#  num_of_regions = 8
#
#  region_list = ['a','b','c','d','e','f','g','h']
#
#  elements = True
#
#  if venn_type == 'num':
#    count = 0
#    region_list = []
#    for i in range(num_of_regions):
#      count += 1
#      region_list.append([str(count)])
#
#  elif venn_type == 'nums':
#    region_list = []
#
#    while len(region_list) < num_of_regions:
#      random_list = [random.randint(min_elements, max_elements) for _ in range(random.randint(min_num_elements, max_num_elements))]
#
#      if not any(element in sub for sub in region_list for element in random_list): # no duplicate elements in any other sublist in region_list
#        region_set = set(random_list) # no duplicates in the random_list
#        region_list.append(list(region_set))
#
#
#  random.shuffle(region_list)
#
#  venn_3(region_list, venn_type='elements')
#
#  return region_list

################################################################################

################################################################################

# my function imports

def create(ques_type: str, condition: int) -> str:
  # change condition later to: sorted: bool ???
  # currying & partials

  # weight are adjustable
  weight_s = {'rn': [.2, .4, .4],
            'ca': [.2, .6, .2],
            'dm': [.2, .8, 0],
            'ps': [.2, .6, .2]}

  # (_AnBu_C)

  abc = ['A', 'B', 'C']
  compliment = ['_', '__', '']
  u_or_n = ['u', 'n']

  abc_select = random.choices([1, 2, 3], weights=weight_s[ques_type])

  abc_int = int(abc_select[0]) # cast the abc_select to int

  #abc_index = random.randint0, len(abc) - 1)
  #count = abc_index

  region_abc = []
  used = []

  while len(region_abc) < abc_int:

    abc_index = random.randint(0, len(abc) - 1)
    count = abc_index

    if condition == 2:
      # no duplicates & sorted
      if abc[count] not in used:
        used.append(abc[count])
        region_abc.append(abc[count])
        region_abc.sort()

    else:
      region_abc.append(abc[count])

  compliment_list = [random.choice(compliment) for _ in range(abc_int)]
  u_or_n_list = [random.choice(u_or_n) for _ in range(abc_int - 1)]
  u_or_n_list.append('')

  dnf_notation = ""

  for i in range(abc_int):
    dnf_notation = f"{dnf_notation}{compliment_list[i]}{region_abc[i]}{u_or_n_list[i]}"

  return dnf_notation

################################################################################

# Set Theory Functions
# Skills, Generator (diagram, questions, answer), Check

# individual skill functions

def venn3_to_dnf():
    dnf_list = ['An_Bn_C','_AnBn_C','_An_BnC','AnBn_C','An_BnC','_AnBnC','AnBnC','_An_Bn_C']
    bit_list = ['100','010','001','110','101','011','111','000']

    index = random.randint(0,7)
    diagram_index = random.choice(QUESTION_TUPLE)  # e.g., 'bit' or 'nums'

    if diagram_index == 'bit':
        region_list = bit_list
        img_url = venn_3(region_list, 'bit')
    else:
        region_list, img_url = venn3_display_shuffle_diagram(diagram_index)

    if diagram_index == 'nums':
        question = f"What is disjunctive normal form for elements {str(region_list[index]).replace('[','{').replace(']','}')}?"
    else:
        question = f"What is disjunctive normal form for region {str(region_list[index]).replace('[','').replace(']','')}?"

    answer = dnf_list[index]
    return question, answer, img_url


#def venn3_to_dnf():
#  dnf_list = ['An_Bn_C','_AnBn_C','_An_BnC','AnBn_C','An_BnC','_AnBnC','AnBnC','_An_Bn_C']
#  bit_list = ['100','010','001','110','101','011','111','000']
#
#  index = random.randint(0,7)
#  diagram_index = random.choice(QUESTION_TUPLE)
#
#  if diagram_index == 'bit':
#    region_list = bit_list
#    venn_3(region_list, 'bit')
#  else:
#    region_list, img_url = venn3_display_shuffle_diagram(diagram_index)
#
#  #time.sleep(2)
#
#  if diagram_index == 'nums':
#    question = f"What is disjunctive normal form for elements {str(region_list[index]).replace('[','{').replace(']','}') }? "
#  else:
#    question = f"What is disjunctive normal form for region {str(region_list[index]).replace('[','').replace(']','')}?"
#
#  answer = dnf_list[index]
#
#  return question, answer, img_url

################################################################################

def venn3_to_bit():
  bit_list = ['100','010','001','110','101','011','111','000']

  index = random.randint(0,7)
  region_list, img_url = venn3_display_shuffle_diagram('abc')

  #time.sleep(1)
  question = f"What is bit stream form for region {str(region_list[index]).replace('[','').replace(']','')}?"
  answer = bit_list[index]

  return question, answer, img_url

################################################################################
def venn3_dnf_to_bit():
  bit_list = ['100','010','001','110','101','011','111','000']
  region_list = ['An_Bn_C','_AnBn_C','_An_BnC','AnBn_C','An_BnC','_AnBnC','AnBnC','_An_Bn_C']

  index = random.randint(0, 7)

  img_url = venn_3(region_list, 'dnf')

  #time.sleep(1)
  question = f"What is bit stream form for region {str(region_list[index]).replace('[','').replace(']','')}?"
  answer = bit_list[index]

  return question, answer, img_url

################################################################################

def venn3_bit_to_dnf():
  dnf_list = ['An_Bn_C','_AnBn_C','_An_BnC','AnBn_C','An_BnC','_AnBnC','AnBnC','_An_Bn_C']
  region_list = ['100','010','001','110','101','011','111','000']

  index = random.randint(0, 7)

  img_url = venn_3(region_list, 'bit')

  #time.sleep(1)
  question = f"What is Disjunctive Normal Form form for region {str(region_list[index]).replace('[','').replace(']','')}?"
  answer = dnf_list[index]

  return question, answer, img_url

################################################################################


################################################################################

def venn3_set_operators():
  # denote union, intersection, and compliment

  # dont mess with order
  union_types = ("A union B","A union C", "B union C")
  u_answer = ('AuB', 'AuC', 'BuC')

  intersection_types = ("A intersection B","A intersection C", "B intersection C")
  i_answer = ('AnB', 'AnC', 'BnC')

  compliment_types = ("A compliment B","A compliment C", "B compliment C")
  c_answer = ('_AnB', '_AnC', '_BnC')

  question_types = (union_types, intersection_types, compliment_types)
  answers = (u_answer, i_answer, c_answer)

  select_random = random.randint(0, len(question_types) - 1)

  select_question = question_types[select_random]
  select_answer = answers[select_random]

  pick_index = random.randint(0, len(select_question) - 1)

  question = f"How do you denote {select_question[pick_index]}?"
  answer = select_answer[pick_index]

  # dont need region_list for this func
  region_list, img_url = venn3_display_shuffle_diagram('abc')

  return question, answer, img_url


### new imports from my own version of the_program 08/29 @ 4:33 PM ###

def clean_conditionals_str(expr_list: list) -> list:
  # expr_list should come in cleaned (simplified)
      
  # l = [1, 2, 3, 4, 5, 6]
  # i = 1
  # i want to remove 2-5
  # del l[i:i+4]
  
  i = 0
  while i < len(expr_list):
    if expr_list[i] == '<':
      #biconditional
      del expr_list[i:i+3]
      expr_list.insert(i, '<->')
      i += 1

    elif expr_list[i] == '-' and expr_list[i + 1] == '>' and expr_list[i - 1] != '<':
      # conditional
      del expr_list[i:i+2]
      expr_list.insert(i, '->')
      i += 1

    elif expr_list[i] == '+' and expr_list[i + 1] == 'o':
      del expr_list[i:i+2]
      expr_list.insert(i, '+o')
      i += 1

    else:
      i += 1

  return expr_list

def create_ls_expr():
  
  var = ['P', 'Q', 'R']
  ops = ['_', '^', 'v', '+o', '->', '<->']

  var_percents = [0.33, 0.33, 0.33]
  ops_percents = [0.2125, 0.2125, 0.2125, 0.2125, 0.075, 0.075]
  amount_of_vars = 5

  new_str = ''
  for i in range(amount_of_vars):
    ops_choice = random.choices(ops, weights=ops_percents)[0]
    var_choice = random.choices(var, weights=var_percents)[0]

    negation = True if ops_choice == '_' else False # checking if first choice is a negation

    negation_str = '_'
    prefix = ops[random.randint(1, len(ops) - 3)] if negation and i < amount_of_vars - 2 else ''

    if i != amount_of_vars - 1:
      new_str = f"{new_str}{(negation_str if negation else '')}{var_choice}{prefix}{ops_choice if not negation and i < amount_of_vars - 2 else ''}"

   # if i == 0:
   #   #_Q+o^R+oPvP<->P
   #   new_str = f"{new_str}{(negation_str if negation else '')}{var_choice}{prefix if negation else ops_choice}"
   # elif i == 1:
   #   new_str = f"{new_str}{}{var_choice}{}"
   # else:
   #   new_str = f"{new_str}{prefix}{ops_choice}{var_choice}"
      
    # update da ops percents | we dont need this, might take it out
    for j in range(len(ops)):
      if ops[j] == ops_choice:
        ops_percents[j] = 0

     #   if ops[j] in ('<->', '->'):
     #     ops_percents[j] = 0
     #   if ops[j] not in ('<->', '->'):
     #     ops_percents[j] = max(0, ops_percents[j] - 0.15)
     #   else:
     #     ops_percents[j] += 0.03
      
    # change the odds
    for k in range(len(var)):
      if var[k] == var_choice:
        var_percents[k] = max(0, var_percents[k] - 0.20)
      else:
        var_percents[k] += 0.10

  return new_str

def logic_symbols():

  expr = ['_P^QvR+oP<->P^Q', 'P^QvP^_Q', 'Pv_Q^RvP+oR']
  # create another typa LOGIC generation function. this one should be geared towards logic symbols (not many duplicates)

  n = create_ls_expr()
  clean_expr = list_to_string(list(n))

  # need to figure out how to put parentheses in the correct spots to explicitly show order
  # Pv_Q^R+oP<->R->Q

  #P^_QvR+oP'
  #(((P^(_Q))vR)+oP)

  prec_dic = {
      '_': 1,
      '^': 2,
      'v': 3,
      '+o': 4,
      '->': 5,
      '<->': 6
  }

  type_of_question = 1

  #l = list(expr[random.randint(0, len(expr) - 1)])
  l = list(n)
  r = clean_conditionals_str(l)
  
  symbols_in_expr = []
  for i in range(len(r)):
    if r[i] in prec_dic.keys():
      symbols_in_expr.append(r[i])
   
  old_order = symbols_in_expr
  for i in range(len(symbols_in_expr)):
    for j in range(len(symbols_in_expr) - 1):
      if prec_dic[symbols_in_expr[j]] > prec_dic[symbols_in_expr[j+1]]:
        symbols_in_expr[j], symbols_in_expr[j+1] = symbols_in_expr[j+1], symbols_in_expr[j]
  
  if 'v' in l and '+o' in l:
    a, b = 'v', '+o'
    i, j = r.index(a), r.index(b)  
    k, p = symbols_in_expr.index(a),  symbols_in_expr.index(b)

    if i < j:
      # this means OR comes first
      if k < p:
        pass
      else:
        symbols_in_expr[k], symbols_in_expr[p] = symbols_in_expr[p], symbols_in_expr[k] 

    if i > j:
      if k > p:
        pass
      else:
        symbols_in_expr[k], symbols_in_expr[p] = symbols_in_expr[p], symbols_in_expr[k] 
    
  if type_of_question == 0:
    pass
    
  elif type_of_question == 1:

    num_of_ops = random.randint(0, len(symbols_in_expr) - 1)
    num_grammar = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh']
    question = f'When parentheses are not present, what is {num_grammar[num_of_ops]} symbol in precedence? {clean_expr}'

    answer = symbols_in_expr[num_of_ops]

    return question, answer

  elif type_of_question == 2:

    # need to fix this mess.

    i = 0
    first_found = False
    first_index = 0
    inner = 0

    para_reached = 0
    answer = []

    while para_reached < len(symbols_in_expr):

      # [(_Q)], [(^R)]
      # (Pv((_Q)^R))

      # how do I create something that:
      # can take: 'Pv_Q^R+oP<->R->Q'

      if symbols_in_expr[i] == r[j] and first_found == False:

        #print(j)
        #print(f'len(r) = {len(r)}')
        inner = j # we will make the placement of other parentheses depend on this
        if symbols_in_expr[0] == '_':
          first = f'({r[j]}{r[j+1]})'
          r.insert(j, first)

          inner = j
          curr_index = j
          del r[j+1:j+3]
         # answer.append(first)
          first_found = True

        i += 1
        para_reached += 1

        #print(f'R: {r}')

      if first_found and symbols_in_expr[i] == r[j]:
        if symbols_in_expr[i] not in ('<->', '->'):
          if j > inner: # this statement is on the right side
            # ((_Q)^P
            r.insert(inner, '(')
            curr_index = j + 3
            r.insert(curr_index, ')')
            #print(r)
            i += 1
            #print(i)
          elif j < inner:
            r.insert(j, '(')
            r.insert(curr_index, ')')
            #print(r)
            i += 1
        elif symbols_in_expr[i] == '<->':
          i += 1
        elif symbols_in_expr[i] == '->':
          r.insert(j, '(')
          r.insert(j+1, ')')
          i += 1

        new_str = ''
        for n in r:
          new_str = f'{new_str}{n}'
        #print(new_str)

      j += 1
      if j == len(r) - 1:
        j = 0

def split_on_main_op(s: str):
  
  # we pass in a s: str that typically has no '(' or ')' and no outside negation in the str
  # depth will track how many open '(' your currently inside
  depth = 0

  for i, ch in enumerate(s):
      # incase we do pass in something like (..)vP
      if   ch == '(': depth += 1
      elif ch == ')': depth -= 1
      elif ch in ('^','v') and depth == 0:
         # print(f's[:i] {s[:i]}')
         # print(f's[i+1] {s[i+1]}')

         # _P^P 
         # s[:i] _P
         # s[i+1] P

         # _PvQ
         # s[:i] _P
         # s[i+1] Q
         # this works since our current iteration is on the operation
          return s[:i], ch, s[i+1:]

  if '^' not in s and 'v' not in s:
    print('Error. No operation')

def toggle_neg(term: str) -> str:
  # remove one underscore if present, else prepend one
  # either _(_P) or _(P)
  # when string enters this function it'll be _P or P
  # if starts with _ that means we get rid of the negation '_(_P)' -> P
  # if it doesnt then that means we have '_(P)' -> _P
  return term[1:] if term.startswith('_') else '_' + term

def simplify_logic_expr():

  expr_list, _, mid_op = create_stuff('logic', 'pt')
  results = []

  for curr in expr_list:
      # not negating expression. we can keep it the same 
      if not curr.startswith('_'):
          results.append(curr.strip('()'))
          continue

      # strip the leading '_' and outer parentheses
      inner = curr[1:] 
      if inner.startswith('(') and inner.endswith(')'):
          inner = inner[1:-1]

      # if it has NO operator, it's just a literal negation
      if '^' not in inner and 'v' not in inner:
          # toggle exactly one underscore
          results.append(toggle_neg(inner))
          continue

      # otherwise apply demorgans 
      left, op, right = split_on_main_op(inner)
      flipped_op = '^' if op=='v' else 'v'
      results.append(f"{toggle_neg(left)}{flipped_op}{toggle_neg(right)}")
  # pre_str _(Qv_Q)v_(_PvQ)
  # answer (_Q^Q)v(P^_Q)
  # mid_op v
  pre_str = f'{expr_list[0]}{mid_op}{expr_list[1]}'
  ans_str = f'({results[0]}){mid_op}({results[1]})'

  return pre_str, ans_str, mid_op

def get_truth_table(first_expr, second_expr):


  # first_expr = P
  # second_expr = PvQ
  truth_dic = {
      'P': ['T', 'T', 'F', 'F'],
      'Q': ['T', 'F', 'T', 'F'],
      '_P': ['F', 'F', 'T', 'T'],
      '_Q': ['F', 'T', 'F', 'T']
  }

  P = ['T', 'T', 'F', 'F']
  _P = ['F', 'F', 'T', 'T']
  Q = ['T', 'F', 'T', 'F']
  _Q = ['F', 'T', 'F', 'T']
  

  # we can loop over this twice to do both lists
  combined_lists = [first_expr, second_expr]

  answers = []
  for i in range(len(combined_lists)):
    curr = combined_lists[i]   
  
    first_one = []
    first_one_done = False
    first_op = ''
    first_two = []

    if 'v' in curr or '^' in curr:
      for i in range(len(curr)):
        if first_one_done == False:
          if curr[i] not in ('v', '^'):
            first_one.append(curr[i])
          else:
            first_one_done = True
            first_op = curr[i]
            continue
        else:
          first_two.append(curr[i])
    else:

      # singular 
      for key, val in truth_dic.items():
        if list_to_string(curr) == key:
          answers.append(val)
          continue

    for key, val in truth_dic.items():
      if list_to_string(first_one) == key:
        first_one = val
      if list_to_string(first_two) == key:
        first_two = val
    
    first_ans = []

    if first_op in ('^', 'v'):
      if first_op == '^':
        for i in range(len(first_one)):
          if first_one[i] == 'T' and first_two[i] == 'T':
            first_ans.append('T')
          else:
            first_ans.append('F')

      elif first_op == 'v':
        for i in range(len(first_one)):
          if first_one[i] == 'T' or first_two[i] == 'T':
            first_ans.append('T')
          else:
            first_ans.append('F')
  
      answers.append(first_ans)
  #print(f'answers: {answers}')
  return answers


def get_truth_ls():

  # pre_str _(_P)^_(P^Q)
  # answer (P)^(_Pv_Q)
  # mid_op ^

  pre_str, answer, mid_op = simplify_logic_expr()
   # pre_str _(_P)v_(_P^_Q)
   # answer (P)v(PvQ)
   # mid_op v
  answer_l = list(answer)

  first_expr = []
  second_expr = []
  first_expr_done = False

  for i in range(len(answer_l)):

    if answer_l[i] != '(' and first_expr_done == False:
      if answer_l[i] == ')':
        first_expr_done = True
        this_index = i
 #       mid_op = answer_l[i + 1]
      else:
        first_expr.append(answer_l[i])
      
    if first_expr_done:
      if i != this_index + 1:
        if answer_l[i] not in ('(', ')', '-', '>'):
          second_expr.append(answer_l[i])

  truth_tables = get_truth_table(first_expr, second_expr)
  # need to get the truth table of each expr
  truth_table = []
  
 # for key, val in truth_table_dic.items():
 #   if key == list_to_string(first_expr):
 #     first_expr = val

 #   if key == list_to_string(second_expr):
 #     second_expr = val

  first_expr = truth_tables[0]
  second_expr = truth_tables[1]

  
#  print(f'mid_op: {mid_op}')
#  print(f'first_expr {first_expr}')
#  print(f'second_expr {second_expr}')

  if mid_op == 'v':
    for i in range(len(first_expr)):
      if first_expr[i] == 'T' or second_expr[i] == 'T':
        truth_table.append('T')
      else:
        truth_table.append('F')

  elif mid_op == '^':
    for i in range(len(first_expr)):
      if first_expr[i] == 'T' and second_expr[i] == 'T':
        truth_table.append('T')
      else:
        truth_table.append('F')

  elif mid_op == '->':
    for i in range(len(first_expr)):
      # we can simplify these if statements with or's later
      if first_expr[i] == 'T' and second_expr[i] == 'T':
        truth_table.append('T')
      elif first_expr[i] == 'F' and second_expr[i] == 'T':
        truth_table.append('T')
      elif first_expr[i] == 'F' and second_expr[i] == 'F':
        truth_table.append('T')
      else:
        truth_table.append('F')
  
  elif mid_op == '<->':
    for i in range(len(first_expr)):
      if first_expr[i] == 'T' and second_expr[i] == 'T':
        truth_table.append('T')
      elif first_expr[i] == 'F' and second_expr[i] == 'F':
        truth_table.append('T')
      else:
        truth_table.append('F')
  
  #print(f'TRUTH TABLE: {truth_table}')

  return pre_str, list(truth_table)

def fig_circ(logic_statement='PvQ'):

  circuits = {
 # \\ for spacing

    #---------------------------------------------------------------------
    #                                SINGLE
    #---------------------------------------------------------------------

    'P^Q': """
    P--------\\
            AND----OUTPUT
    Q--------/
    """,

   'PvQ': """
    P--------\\
             OR----OUTPUT
    Q--------/
    """,

    '_P^Q': """
    P--NOT---\\
             AND----OUTPUT
    Q--------/
    """,

    '_PvQ': """
    P--NOT---\\
             OR----OUTPUT
    Q--------/
    """,

    'P^_Q': """
    P--------\\
             AND----OUTPUT
    Q--NOT---/
    """,

    'Pv_Q': """
    P--------\\
             OR----OUTPUT
    Q--NOT---/
    """,

    '_P^_Q': """
    P--NOT---\\
             AND----OUTPUT
    Q--NOT---/
    """,

    '_Pv_Q': """
    P--NOT---\\
             OR----OUTPUT
    Q--NOT---/
    """,

    #---------------------------------------------------------------------
    #                                DOUBLE
    #---------------------------------------------------------------------

    '(P^_Q)v(_P^_Q)': """
    P--------\\
              AND---------\\
    Q---NOT--/             \\
                            OR----OUTPUT
    P---NOT--\             /
              AND---------/
    Q---NOT--/
    """,

    '(_P^Q)v(_P^_Q)': """
    P---NOT--\\
              AND---------\\
    Q--------/             \\
                            OR----OUTPUT
    P---NOT--\              /
              AND----------/
    Q---NOT--/
    """,

    '(P^Q)v(_P^_Q)': """
    P--------\\
              AND---------\\
    Q--------/             \\
                            OR----OUTPUT
    P---NOT--\             /
              AND---------/
    Q---NOT--/
    """,

    '(_P^Q)v(P^_Q)': """
    P---NOT--\\
              AND---------\\
    Q--------/             \\
                            OR----OUTPUT
    P--------\             /
              AND---------/
    Q---NOT--/
    """,

    '(_P^Q)v(_P^_Q)': """
    P---NOT--\\
              AND---------\\
    Q--------/             \\
                            OR----OUTPUT
    P---NOT--\             /
              AND---------/
    Q---NOT--/
    """,

    #---------------------------------------------------
    #-----------------TRIPLES---------------------------
    #---------------------------------------------------

    '(P^_Q)v(_P^Q)v(_P^_Q)': """
    P--------\\
              AND----\\
    Q---NOT--/        \\
                       OR-----\\
    P---NOT--\        /        \\
              AND----/          \\
    Q--------/                   OR----OUTPUT
                                /
    P---NOT--\                 /
              AND-------------/
    Q---NOT--/
    """,

    '(P^Q)v(_P^Q)v(_P^_Q)': """
    P--------\\
              AND----\\
    Q--------/        \\
                       OR-----\\
    P---NOT--\        /        \\
              AND----/          \\
    Q--------/                   OR----OUTPUT
                                /
    P---NOT--\                 /
              AND-------------/
    Q---NOT--/
    """,

    '(P^Q)v(P^_Q)v(_P^_Q)': """
    P--------\\
              AND----\\
    Q--------/        \\
                       OR-----\\
    P--------\        /        \\
              AND----/          \\
    Q---NOT--/                   OR----OUTPUT
                                /
    P---NOT--\                 /
              AND-------------/
    Q---NOT--/
    """,

    '(P^Q)v(P^_Q)v(_P^Q)': """
    P--------\\
              AND----\\
    Q--------/        \\
                       OR-----\\
    P--------\        /        \\
              AND----/          \\
    Q---NOT--/                   OR----OUTPUT
                                /
    P---NOT--\                 /
              AND-------------/
    Q--------/
    """,

    #---------------------------------------------------
    #-----------------QUAD------------------------------
    #---------------------------------------------------

    '(P^Q)v(P^_Q)v(_P^Q)v(_P^_Q)': """
    P--------\\
              AND----\\
    Q--------/        \\
                       OR-----\\
    P--------\        /        \\
              AND----/          \\
    Q---NOT--/                   OR----\\
                                /       \\
    P---NOT--\                 /         OR----OUTPUT
              AND-------------/         /
    Q--------/                         /
                                      /
    P---NOT--\                       /
              AND-------------------/
    Q---NOT--/
    """,
  }

  diagram = circuits[logic_statement]
  print(f'\n{diagram}\n')

  return None

def fig_tru(x='FFFF'):
  import pandas as pd

  df = pd.DataFrame({
      ' P': [' T',' T',' F',' F'],
      ' Q': [' T', ' F',' T',' F'],
      '_P': ['F','F','T','T'],
      '_Q': ['F','T','F','T'],
      'a': [' F',' F',' F',' F'],
      'b': [' F',' F',' F',' T'],
      'c': [' F',' F',' T',' F'],
      'd': [' F',' F',' T',' T'],
      'e': [' F',' T',' F',' F'],
      'f': [' F',' T',' F',' T'],
      'g': [' F',' T',' T',' F'],
      'h': [' F',' T',' T',' T'],
      'i': [' T',' F',' F',' F'],
      'j': [' T',' F',' F',' T'],
      'k': [' T',' F',' T',' F'],
      'l': [' T',' F',' T',' T'],
      'm': [' T',' T',' F',' F'],
      'n': [' T',' T',' F',' T'],
      'o': [' T',' T',' T',' F'],
      'p': [' T',' T',' T',' T'],
  })

  print(df.to_markdown(tablefmt='github',index=False))

  return df 

def pt_to_truth():
  pre_str, truth = get_truth_ls()

  answer_dic = {
      'a': ['F','F','F','F'],
      'b': ['F','F','F','T'],
      'c': ['F','F','T','F'],
      'd': ['F','F','T','T'],
      'e': ['F','T','F','F'],
      'f': ['F','T','F','T'],
      'g': ['F','T','T','F'],
      'h': ['F','T','T','T'],
      'i': ['T','F','F','F'],
      'j': ['T','F','F','T'],
      'k': ['T','F','T','F'],
      'l': ['T','F','T','T'],
      'm': ['T','T','F','F'],
      'n': ['T','T','F','T'],
      'o': ['T','T','T','F'],
      'p': ['T','T','T','T'],
  }

  df = fig_tru()
  question = f'What is the correct truth table for {pre_str}'
  answer = 'a'

  for key, val in answer_dic.items():
    if truth == val:
      answer = key

  return question, answer

def select_circ():

  truth_table_dic = {
    'P': ['T','T','F','F'],
    'Q': ['T','F','T','F'],
    '_P': ['F','F','T','T'],
    '_Q': ['F','T','F','T'],
    'P^Q': ['T','F','F','F'],
    'PvQ': ['T','T','T','F'],
    '_P^Q': ['F','F','T','F'],
    '_PvQ': ['T','F','T','T'],
    'P^_Q': ['F','T','F','F'],
    'Pv_Q': ['T','T','F','T'],
    '_P^_Q': ['F','F','F','T'],
    '_Pv_Q': ['F','T','T','T'],
    '(P^_Q)v(_P^_Q)': ['F','T','F','T'], # XOR
    '(_P^Q)v(_P^_Q)': ['F','F','T','T'],
    '(P^Q)v(_P^_Q)': ['T', 'F', 'F', 'T'],
    '(_P^Q)v(P^_Q)': ['F', 'T', 'T', 'F'],
    '(_P^Q)v(_P^_Q)': ['F', 'F', 'T', 'T'],
    '(P^_Q)v(_P^Q)v(_P^_Q)': ['F', 'T', 'T', 'T'],
    '(P^Q)v(_P^Q)v(_P^_Q)': ['T', 'F', 'T', 'T'],
    '(P^Q)v(P^_Q)v(_P^_Q)': ['T', 'T', 'F', 'T'],
    '(P^Q)v(P^_Q)v(_P^Q)': ['T', 'T', 'T', 'F'],
    '(P^Q)v(P^_Q)v(_P^Q)v(_P^_Q)': ['T', 'T', 'T', 'T']
  }


  all_logic = ['P^Q', 'PvQ', '_P^Q','_PvQ', 'P^_Q', 'Pv_Q', 'Pv_Q', '_P^_Q', '_Pv_Q', '(P^_Q)v(_P^_Q)', '(_P^Q)v(_P^_Q)', '(P^Q)v(_P^_Q)', '(_P^Q)v(P^_Q)', '(_P^Q)v(_P^_Q)', '(P^_Q)v(_P^Q)v(_P^_Q)', '(P^Q)v(_P^Q)v(_P^_Q)', '(P^Q)v(P^_Q)v(_P^_Q)', '(P^Q)v(P^_Q)v(_P^Q)', '(P^Q)v(P^_Q)v(_P^Q)v(_P^_Q)']

  # Simplify Truth Table
  

  # I'm going to have to create a dictionary of this to have the corresponding truth values
  # This will allow us to use circuits in a much higher magnitude of problems

  ran_index = random.randint(0, len(all_logic) - 1)
  statement = all_logic[ran_index]

  return statement

def circ_to_tru():

  df_dic = {
      ' P': ['T','T','F','F'],
      ' Q': ['T','F','T','F'],
      '_P': ['F','F','T','T'],
      '_Q': ['F','T','F','T'],
      'a': ['F','F','F','F'],
      'b': ['F','F','F','T'],
      'c': ['F','F','T','F'],
      'd': ['F','F','T','T'],
      'e': ['F','T','F','F'],
      'f': ['F','T','F','T'],
      'g': ['F','T','T','F'],
      'h': ['F','T','T','T'],
      'i': ['T','F','F','F'],
      'j': ['T','F','F','T'],
      'k': ['T','F','T','F'],
      'l': ['T','F','T','T'],
      'm': ['T','T','F','F'],
      'n': ['T','T','F','T'],
      'o': ['T','T','T','F'],
      'p': ['T','T','T','T'],
  }

  # the statements wont match
  # we will need to match truth tables instead
  df = fig_tru()
    
  # pick a random statement
  statement = select_circ()
  # get the truth table to that statement

  truth_table_circuit = {
    'P': ['T','T','F','F'],
    'Q': ['T','F','T','F'],
    '_P': ['F','F','T','T'],
    '_Q': ['F','T','F','T'],
    'P^Q': ['T','F','F','F'],
    'PvQ': ['T','T','T','F'],
    '_P^Q': ['F','F','T','F'],
    '_PvQ': ['T','F','T','T'],
    'P^_Q': ['F','T','F','F'],
    'Pv_Q': ['T','T','F','T'],
    '_P^_Q': ['F','F','F','T'],
    '_Pv_Q': ['F','T','T','T'],
    '(P^_Q)v(_P^_Q)': ['F','T','F','T'], # XOR
    '(_P^Q)v(_P^_Q)': ['F','F','T','T'],
    '(P^Q)v(_P^_Q)': ['T', 'F', 'F', 'T'],
    '(_P^Q)v(P^_Q)': ['F', 'T', 'T', 'F'],
    '(_P^Q)v(_P^_Q)': ['F', 'F', 'T', 'T'],
    '(P^_Q)v(_P^Q)v(_P^_Q)': ['F', 'T', 'T', 'T'],
    '(P^Q)v(_P^Q)v(_P^_Q)': ['T', 'F', 'T', 'T'],
    '(P^Q)v(P^_Q)v(_P^_Q)': ['T', 'T', 'F', 'T'],
    '(P^Q)v(P^_Q)v(_P^Q)': ['T', 'T', 'T', 'F'],
    '(P^Q)v(P^_Q)v(_P^Q)v(_P^_Q)': ['T', 'T', 'T', 'T']
  }

  truth_table_statement = truth_table_circuit[statement]

  # display circuit
  fig_circ(statement)
  question = f"Which table matches the circuit?"
  
  for key, val in df_dic.items():
    if val == truth_table_circuit[statement]:
      correct_table = key

  #print(f"correct_table: {correct_table}")

  return question, correct_table

def circ_to_propositional_logic():
  # get logic statement
  # use truth table to check answer

  all_logic = ['P^Q', 'PvQ', '_P^Q','_PvQ', 'P^_Q', 'Pv_Q', 'Pv_Q', '_P^_Q', '_Pv_Q', '(P^_Q)v(_P^_Q)', '(_P^Q)v(_P^_Q)', '(P^Q)v(_P^_Q)', '(_P^Q)v(P^_Q)', '(_P^Q)v(_P^_Q)', '(P^_Q)v(_P^Q)v(_P^_Q)', '(P^Q)v(_P^Q)v(_P^_Q)', '(P^Q)v(P^_Q)v(_P^_Q)', '(P^Q)v(P^_Q)v(_P^Q)', '(P^Q)v(P^_Q)v(_P^Q)v(_P^_Q)']
  
  random_logic = []

  for i in range(5):
    random_statement = all_logic[random.randint(0, len(all_logic) - 1)]
    random_logic.append(random_statement)
    all_logic.remove(random_statement)
  
  question = f'''Which of these statements match the circuit above?
a. {random_logic[0]}
b. {random_logic[1]}
c. {random_logic[2]}
d. {random_logic[3]}
e. {random_logic[4]}
  '''
  
  select_random_index = random.randint(0, len(random_logic) - 1)
  select_statement = random_logic[select_random_index]

  ans_dic = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e'
  }       

  fig_circ(select_statement)
  ans = ans_dic[select_random_index]

  return question, ans 

def proof_by_equivalence():

  pre_str, answer_tru = get_truth_ls()
  #print(f'PRE_STR {pre_str}')
  #print(f'answer_TRU {answer_tru}')

  truth_table_dic = {
    'P': ['T', 'T', 'F', 'F'],
    'Q': ['T', 'F', 'T', 'F'],
    '_P': ['F','F', 'T', 'T'],
    '_Q': ['F', 'T', 'F', 'T'],
    'P^Q': ['T', 'F', 'F', 'F'],
    'P^_Q': ['F', 'T', 'F', 'F'],
    '_P^Q': ['F', 'F', 'T', 'F'],
    '_P^_Q': ['F', 'F', 'F', 'T'],
    '(P^Q)v(_P^_Q)': ['T', 'F' 'F', 'T'], # xor
    'PxorQ': ['F', 'T', 'T', 'F'],
    'PvQ': ['T', 'T', 'T', 'F'],
    'Pv_Q': ['T', 'T', 'F', 'T'],
    '_PvQ': ['T', 'F', 'T', 'T'],
    '_Pv_Q': ['F', 'T', 'T', 'T'],
    'Qv_Q': ['T', 'T', 'T', 'T'],
    'Pv_P': ['T', 'T', 'T', 'T'],
    'Q^_Q': ['F', 'F', 'F', 'F'],
    'P^_P': ['F', 'F', 'F', 'F']
    }
  
  equivalent_l = []
  equivalent = 0
  false_or_true = random.randint(0, 9)
  
  if false_or_true < 9:
    for key, val in truth_table_dic.items():
      if val == answer_tru:
        #print(f'VAL: {val}')
        equivalent_l.append(key)
        equivalent = 1
      if key == 'P^_P' and equivalent == 0: # we reached the end w no match
        equivalent_l.append(random.choice(list(truth_table_dic)))

  elif false_or_true == 9:
    # getting unequivalent answer
    for key, val in truth_table_dic.items():
      if val != answer_tru:
        equivalent_l.append(key)
        equivalent = 0

  question = f"Is {pre_str} equivalent to {equivalent_l[random.randint(0, len(equivalent_l) - 1)]} y/n"

  ans = 'y' if equivalent == 1 else 'n'

  return question, ans    

 # the answer is a yes/no. so we can return y/n from user
 # if equivalent == 1:
 #   print(f"They are equivalent")
 # else:
 #   print(f"They are not equivalent")

 # print(false_or_true)

 ## karnaugh map stuff ##

def fig_kmap2(kmap_type="all"):
  if kmap_type == "all":
    print('a      Q  | _Q      |   b      Q  | _Q      |   c      Q  | _Q      |   d      Q  | _Q   ')
    print('    + - - + - - +   |       + - - + - - +   |       + - - + - - +   |       + - - + - - +')
    print('  P |  F  |  F  |   |     P |  F  |  F  |   |     P |  F  |  F  |   |     P |  F  |  F  |')
    print('  - + - - + - - +   |     - + - - + - - +   |     - + - - + - - +   |     - + - - + - - +')
    print(' _P |  F  |  F  |   |    _P |  F  |  T  |   |    _P |  T  |  F  |   |    _P |  T  |  T  |')
    print('    + - - + - - +   |       + - - + - - +   |       + - - + - - +   |       + - - + - - +')
    print('                    |                       |                       |                    ')
    print('--------------------+-----------------------+-----------------------+--------------------')
    print('                    |                       |                       |                    ')
    print('e      Q  | _Q      |   f      Q  | _Q      |   g      Q  | _Q      |   h      Q  | _Q   ')
    print('    + - - + - - +   |       + - - + - - +   |       + - - + - - +   |       + - - + - - +')
    print('  P |  F  |  T  |   |     P |  F  |  T  |   |     P |  F  |  T  |   |     P |  F  |  T  |')
    print('  - + - - + - - +   |     - + - - + - - +   |     - + - - + - - +   |     - + - - + - - +')
    print(' _P |  F  |  F  |   |    _P |  F  |  T  |   |    _P |  T  |  F  |   |    _P |  T  |  T  |')
    print('    + - - + - - +   |       + - - + - - +   |       + - - + - - +   |       + - - + - - +')
    print('                    |                       |                       |                    ')
    print('--------------------+-----------------------+-----------------------+--------------------')
    print('                    |                       |                       |                    ')
    print('i      Q  | _Q      |   j      Q  | _Q      |   k      Q  | _Q      |   l     Q  | _Q    ')
    print('    + - - + - - +   |       + - - + - - +   |       + - - + - - +   |       + - - + - - +')
    print('  P |  T  |  F  |   |     P |  T  |  F  |   |     P |  T  |  F  |   |     P |  T  |  F  |')
    print('  - + - - + - - +   |     - + - - + - - +   |     - + - - + - - +   |     - + - - + - - +')
    print(' _P |  F  |  F  |   |    _P |  F  |  T  |   |    _P |  T  |  F  |   |    _P |  T  |  T  |')
    print('    + - - + - - +   |       + - - + - - +   |       + - - + - - +   |       + - - + - - +')
    print('                    |                       |                       |                    ')
    print('--------------------+-----------------------+-----------------------+--------------------')
    print('                    |                       |                       |                    ')
    print('m      Q  | _Q      |   n      Q  | _Q      |   o      Q  | _Q      |   p      Q  | _Q   ')
    print('    + - - + - - +   |       + - - + - - +   |       + - - + - - +   |       + - - + - - +')
    print('  P |  T  |  T  |   |     P |  T  |  T  |   |     P |  T  |  T  |   |     P |  T  |  T  |')
    print('  - + - - + - - +   |     - + - - + - - +   |     - + - - + - - +   |     - + - - + - - +')
    print(' _P |  F  |  F  |   |    _P |  F  |  T  |   |    _P |  T  |  F  |   |    _P |  T  |  T  |')
    print('    + - - + - - +   |       + - - + - - +   |       + - - + - - +   |       + - - + - - +')
  else:
    print('       Q  | _Q')
    print(f'    + - - + - - +')
    print(f'  P |  {kmap_type[0]}  |  {kmap_type[1]}  |')
    print(f'  - + - - + - - +')
    print(f' _P |  {kmap_type[2]}  |  {kmap_type[3]}  |')
    print(f'    + - - + - - +')

  return None

def karnaugh_to_propositional():
  questions = [# Karnaugh-2 Maps to Unsimplified Propositional Logic
      ['What is the logic equation for the Karnaugh map in terms of P? (Use _ for NOT, v for OR, and ^ for AND)','P^_P',fig_kmap2,'FFFF'],
      ['What is the logic equation for the Karnaugh map in terms of Q? (Use _ for NOT, v for OR, and ^ for AND)','Q^_Q',fig_kmap2,'FFFF'],
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','_P^_Q',fig_kmap2,'FFFT'],
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','_P^Q',fig_kmap2,'FFTF'],
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(_P^Q)v(_P^_Q)',fig_kmap2,'FFTT'], # Simplified: _P
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','P^_Q',fig_kmap2,'FTFF'],
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^_Q)v(_P^_Q)',fig_kmap2,'FTFT'], # Simplified: _Q
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^_Q)v(_P^Q)',fig_kmap2,'FTTF'],
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^_Q)v(_P^Q)v(_P^_Q)',fig_kmap2,'FTTT'], # Simplified: _Qv_P^Q
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','P^Q',fig_kmap2,'TFFF'],
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^Q)v(_P^_Q)',fig_kmap2,'TFFT'],
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^Q)v(_P^Q)',fig_kmap2,'TFTF'], # Simplified: Q
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^Q)v(_P^Q)v(_P^_Q)',fig_kmap2,'TFTT'], # Simplified: Qv_P^_Q
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^Q)v(P^_Q)',fig_kmap2,'TTFF'], # Simplified: P
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^Q)v(P^_Q)v(_P^_Q)',fig_kmap2,'TTFT'], # Simplified: P^Qv_Q
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^Q)v(P^_Q)v(_P^Q)',fig_kmap2,'TTTF'], # Simplified: Pv_P^Q
      ['What is the logic equation for the Karnaugh map? (Use _ for NOT, v for OR, and ^ for AND)','(P^Q)v(P^_Q)v(_P^Q)v(_P^_Q)',fig_kmap2,'TTTT'],
      ['What is the logic equation for the Karnaugh map in terms of P? (Use _ for NOT, v for OR, and ^ for AND)','Pv_P',fig_kmap2,'TTTT'],
      ['What is the logic equation for the Karnaugh map in terms of Q? (Use _ for NOT, v for OR, and ^ for AND)','Qv_Q',fig_kmap2,'TTTT']]

  random_int = random.randint(0, len(questions) - 1)
  question = questions[random_int][0]
  ans = questions[random_int][1]

  #display function
  fig_kmap2(questions[random_int][3])

  return question, ans


def propositional_logic_to_karnaugh():

  questions = [# Propositional Logic to Karnaugh-2 Map
      ['Which Karnaugh map is the equivalent to the equation: F?','a',fig_kmap2,'all'],                           # FFFF
      ['Which Karnaugh map is a contradiction?','a',fig_kmap2,'all'],                                             # ^
      ['Which Karnaugh map is the equivalent to the equation: P^_P?','a',fig_kmap2,'all'],                        # ^
      ['Which Karnaugh map is the equivalent to the equation: Q^_Q?','a',fig_kmap2,'all'],                        # ^
      ['Which Karnaugh map is the equivalent to the equation: (PvQ)^(Pv_Q)^(_PvQ)^(_Pv_Q)?','a',fig_kmap2,'all'], # ^      # New equation another F representation
      ['Which Karnaugh map is the equivalent to the equation: _P^_Q?','b',fig_kmap2,'all'],                       # FFFT
      ['Which Karnaugh map is the equivalent to the equation: _(_P->Q)?','b',fig_kmap2,'all'],                    # ^      # New equation using ->
      ['Which Karnaugh map is the equivalent to the equation: _P^Q?','c',fig_kmap2,'all'],                        # FFTF
      ['Which Karnaugh map is the equivalent to the equation: _(_P->_Q)?','c',fig_kmap2,'all'],                   # ^      # New equation using ->
      ['Which Karnaugh map is the equivalent to the equation: (_P^Q)v(_P^_Q)?','d',fig_kmap2,'all'],              # FFTT
      ['Which Karnaugh map is the equivalent to the equation: _P?','d',fig_kmap2,'all'],                          # ^
      ['Which Karnaugh map is the equivalent to the equation: P^_Q?','e',fig_kmap2,'all'],                        # FTFF
      ['Which Karnaugh map is the equivalent to the equation: _(P->Q)?','e',fig_kmap2,'all'],                     # ^      # New equation using ->
      ['Which Karnaugh map is the equivalent to the equation: (P^_Q)v(_P^_Q)?','f',fig_kmap2,'all'],              # FTFT
      ['Which Karnaugh map is the equivalent to the equation: _Q?','f',fig_kmap2,'all'],                          # ^
      ['Which Karnaugh map is the equivalent to the equation: (P^_Q)v(_P^Q)?','g',fig_kmap2,'all'],               # FTTF
      ['Which Karnaugh map is the equivalent to the equation: _P<->Q?','g',fig_kmap2,'all'],                      # ^      # New equation using <->
      ['Which Karnaugh map is the equivalent to the equation: P<->_Q?','g',fig_kmap2,'all'],                      # ^      # New equation using <->
      ['Which Karnaugh map is the equivalent to the equation: (P^_Q)v(_P^Q)v(_P^_Q)?','h',fig_kmap2,'all'],       # FTTT
      ['Which Karnaugh map is the equivalent to the equation: _Pv_Q?','h',fig_kmap2,'all'],                       # ^      # Changed from _Qv_P to _Pv_Q
      ['Which Karnaugh map is the equivalent to the equation: P->_Q?','h',fig_kmap2,'all'],                       # ^      # New equation using ->
      ['Which Karnaugh map is the equivalent to the equation: P^Q?','i',fig_kmap2,'all'],                         # TFFF   # Change from equivalvnt to equivalent
      ['Which Karnaugh map is the equivalent to the equation: _(P->_Q)?','i',fig_kmap2,'all'],                    # ^      # New equation using ->
      ['Which Karnaugh map is the equivalent to the equation: (P^Q)v(_P^_Q)?','j',fig_kmap2,'all'],               # TFFT
      ['Which Karnaugh map is the equivalent to the equation: P<->Q?','j',fig_kmap2,'all'],                       # ^      # New equation using <->
      ['Which Karnaugh map is the equivalent to the equation: _P<->_Q?','j',fig_kmap2,'all'],                     # ^      # New equation using <->
      ['Which Karnaugh map is the equivalent to the equation: (P^Q)v(_P^Q)?','k',fig_kmap2,'all'],                # TFTF
      ['Which Karnaugh map is the equivalent to the equation: Q?','k',fig_kmap2,'all'],                           # ^
      ['Which Karnaugh map is the equivalent to the equation: (P^Q)v(_P^Q)v(_P^_Q)?','l',fig_kmap2,'all'],        # TFTT
      ['Which Karnaugh map is the equivalent to the equation: _PvQ?','l',fig_kmap2,'all'],                        # ^      # Changed V to v
      ['Which Karnaugh map is the equivalent to the equation: P->Q?','l',fig_kmap2,'all'],                        # ^      # New equation using ->
      ['Which Karnaugh map is the equivalent to the equation: (P^Q)v(P^_Q)?','m',fig_kmap2,'all'],                # TTFF
      ['Which Karnaugh map is the equivalent to the equation: P?','m',fig_kmap2,'all'],                           # ^
      ['Which Karnaugh map is the equivalent to the equation: (P^Q)v(P^_Q)v(_P^_Q)?','n',fig_kmap2,'all'],        # TTFT
      ['Which Karnaugh map is the equivalent to the equation: Pv_Q?','n',fig_kmap2,'all'],                        # ^      # Changed from P_Q to Pv_Q
      ['Which Karnaugh map is the equivalent to the equation: _P->_Q?','n',fig_kmap2,'all'],                      # ^      # New equation using ->
      ['Which Karnaugh map is the equivalent to the equation: (P^Q)v(P^_Q)v(_P^Q)?','o',fig_kmap2,'all'],         # TTTF
      ['Which Karnaugh map is the equivalent to the equation: PvQ?','o',fig_kmap2,'all'],                         # ^      # Changed V to v
      ['Which Karnaugh map is the equivalent to the equation: _P->Q?','o',fig_kmap2,'all'],                       # ^      # New equation using ->
      ['Which Karnaugh map is the equivalent to the equation: (P^Q)v(P^_Q)v(_P^Q)v(_P^_Q)?','p',fig_kmap2,'all'], # TTTT
      ['Which Karnaugh map is the equivalent to the equation: Pv_P?','p',fig_kmap2,'all'],                        # ^      # New equation another T representation
      ['Which Karnaugh map is the equivalent to the equation: Qv_Q?','p',fig_kmap2,'all'],                        # ^      # New equation another T representation
      #['Which Karnaugh map is the equivalent to the equation: Tautology?','p',fig_kmap2,'all'],                           # ^
      ['Which Karnaugh map is a tautology?','p',fig_kmap2,'all']]
    
  # 1: ques 2: answer 3: func 4: all kmap
  random_int = random.randint(0, len(questions) - 1)
  question = questions[random_int][0]
  ans = questions[random_int][1]

  #display function
  fig_kmap2()

  return question, ans  

def circuit_to_kmap():

  # logic: circuit
  # kmap: logic

  question = 'What Karnaugh map corresponds to the circuit above?'

  # display all KMAP
  fig_kmap2()

  contradiction = random.randint(0, 12)

  if contradiction == 12:

    circuit = {

      'P^_P': """
      P--------\\
              AND----OUTPUT
     _P--------/
      """,

      'Q^_Q': """
      Q--------\\
              AND----OUTPUT
     _Q--------/
      """
    }
  
    contradiction_l = ['P^_P', 'Q^_Q']
    random_statement = contradiction_l[random.randint(0, 1)]
    print(circuit[random_statement])

    ans = 'a'

  else:

    circ_to_kmap = {
      'P^Q': 'i',
      'PvQ': 'o',
      '_P^Q': 'c',
      '_PvQ': 'l',  
      'P^_Q': 'e',
      'Pv_Q': 'n',  
      '_P^_Q': 'b',
      '_Pv_Q': 'h',
      '(P^_Q)v(_P^_Q)': 'f',  # XOR
      '(_P^Q)v(_P^_Q)': 'd',
      '(P^Q)v(_P^_Q)': 'j',
      '(_P^Q)v(P^_Q)': 'g',
      '(P^_Q)v(_P^Q)v(_P^_Q)': 'h',
      '(P^Q)v(_P^Q)v(_P^_Q)': 'l',
      '(P^Q)v(P^_Q)v(_P^_Q)': 'n',
      '(P^Q)v(P^_Q)v(_P^Q)': 'o',
      '(P^Q)v(P^_Q)v(_P^Q)v(_P^_Q)': 'p' # tautology
    }

    select_random_index = random.randint(0, len(circ_to_kmap) - 1)
    select_statement = list(circ_to_kmap.keys())[select_random_index]
    
    fig_circ(select_statement)

    ans = circ_to_kmap[select_statement]

  return question, ans

################################################################################

def sort_sublists(l):

  new_list = []

  for sublist in l:
    for item in sublist:
      new_list.append(item)

  new_list.sort()

  return new_list

################################################################################
# this is not the answer

#def venn3_roster_notation():
#  roster_question_types = ('num', 'nums')
#  # this will use num and nums types
#
#  region_list = venn3_display_shuffle_diagram(roster_question_types[random.randint(0, len(roster_question_types) -1)])
#  # order -> 100, 010, 001, 110, 101, 011, 111, 000
#
#  U = [region_list]
#  #A = [region_list[0], region_list[3], region_list[]]
#  # compliments
#  notA_list = [region_list[1],region_list[2],region_list[5],region_list[7]]
#  notB_list = [region_list[0],region_list[2],region_list[4],region_list[7]]
#  notC_list = [region_list[0],region_list[1],region_list[3],region_list[7]]
#
#  # unions
#  AuB_list =  [region_list[0], region_list[1], region_list[3], region_list[4], region_list[5], region_list[6]]
#  AuC_list =  [region_list[0], region_list[2], region_list[3], region_list[4], region_list[5], region_list[6]]
#  BuC_list =  [region_list[1], region_list[2], region_list[3], region_list[4], region_list[5], region_list[6]]
#
#  # intersections
#  AnB_list =  [region_list[3], region_list[6]]
#  AnC_list =  [region_list[4], region_list[6]]
#  BnC_list =  [region_list[5], region_list[6]]
#
#  #'An_Bn_C', '_AnBn_C', '_An_BnC', 'AnBn_C', 'An_BnC', '_AnBnC', 'AnBnC', '_An_Bn_C')
#
#  roster_notations = ('_A', '_B', '_C', 'AuB', 'AuC', 'BuC', 'AnB', 'AnC', 'BnC')
#  roster_lists = (notA_list, notB_list, notC_list, AuB_list, AuC_list, BuC_list, AnB_list, AnC_list, BnC_list)
#
#  select_roster = random.randint(0, len(roster_notations) - 1)
#  #roster_answers = ()
#
#  countin_commas = ['{', '}']
#  question = f"What are the elements for {roster_notations[select_roster]}?"
#  answer = f"{countin_commas[0]}{sort_sublists(roster_lists[select_roster])}{countin_commas[1]}".replace('[','').replace(']','')
#
#  return question, answer
#
################################################################################

# refactor at some point
def get_bits_dnf(question_type, manual):

  # works for now
  # *dont read* unless necessary

  # might get rid of manual parameter asp
  # asp = at some point i just created a new abbreviation
  # it should catch on

  if manual:
    dnf_l = list(manual)
    #print('manual')
  else:
    #print('not manual')
    dnf = create(question_type, 2)
    c_dnf = clean_dnf(dnf)
    dnf_l = list(c_dnf)

  pos_bit_streams = {
      "A": [[1, 0, 0], [1, 1, 0], [1, 0, 1], [1, 1, 1]],
      "B": [[0, 1, 0], [1, 1, 0], [0, 1, 1], [1, 1, 1]],
      "C": [[0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
      }

  neg_bit_streams = {
      "A": [[0, 1, 0], [0, 0, 1], [0, 1, 1], [0, 0, 0]],
      "B": [[1, 0, 0], [0, 0, 1], [1, 0, 1], [0, 0, 0]],
      "C": [[1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 0]]
     }

  num_operations = 0
  for i in range(len(dnf_l)):
    if dnf_l[i] in DNF_OPS:
      num_operations += 1

  if num_operations == 0:
    if dnf_l[0] == '_':
      # negate
      #print("negate")
      for key, val in neg_bit_streams.items():
        if key == dnf_l[1]:
          bit_streams = val
          abc_region = key
    else:
      # no negate
      for key, val in pos_bit_streams.items():
        if key == dnf_l[0]:
          bit_streams = val
          abc_region = key

    bit_strings = []
    for i in range(len(bit_streams)):
      bit_strings.append(list_to_string(bit_streams[i]))

    final_ans = bit_strings
   # print(f"DNF: {dnf}")
   # print(f"ANS: {bit_streams}")
   # print(f"STR: {bit_strings}")

  elif num_operations == 1:

    # we have 2 variables
    # one operations

    f_h_appended = False
    s_h_appended = False
    first_half = []
    second_half = []

    for i in range(len(dnf_l)):
      if dnf_l[i] in DNF_OPS:
        op_index = i
        operation = dnf_l[i]

    # we know where the middle operation is

    for i in range(len(dnf_l)):
      if i < op_index:
        # we are before the op
        if dnf_l[i] == '_':
          # we are negating
          first_half.append(neg_bit_streams[dnf_l[i + 1]])
          f_h_appended = True

        elif dnf_l[i] != '_' and f_h_appended == False:
          first_half.append(pos_bit_streams[dnf_l[i]])
          f_h_appended = True

      elif i > op_index:
        # we are after the op
        if dnf_l[i] == '_':
          # we are negating
          #print('s_h negate')
          second_half.append(neg_bit_streams[dnf_l[i + 1]])
          s_h_appended = True

        elif dnf_l[i] != '_' and s_h_appended == False:
          #print('s_h non_negate')
          second_half.append(pos_bit_streams[dnf_l[i]])
          s_h_appended = True

    string_f_h = []
    string_s_h = []

    #print(len(first_half[0]))

    for i in range(len(first_half[0])):
      string_f_h.append(list_to_string(first_half[0][i]))

    for i in range(len(second_half[0])):
      string_s_h.append(list_to_string(second_half[0][i]))

   # print(f"DNF: {dnf}")
   # print(f"First_Half: {string_f_h}")
   # print(f"Second_Half: {string_s_h}")

    if operation == 'n':
      final_ans = set(string_f_h).intersection(set(string_s_h))
    elif operation == 'u':
      final_ans = set(string_f_h).union(set(string_s_h))

    #print(f"Final-List {list(final_ans)}")

    #question = f"What is the roster notation for {dnf}?"

  elif num_operations == 2:

    # apologies
    # i thought i was onto something
    # and then this happened...

    DNF_OPS_l = {}
    DNF_OPS_index = []

    first_exp = []
    second_exp = []
    third_exp = []

    n_occur = 0
    u_occur = 0

    for i in range(len(dnf_l)):
      if dnf_l[i] in DNF_OPS:
        DNF_OPS_l[dnf_l[i]] = i
        DNF_OPS_index.append(i)

        if dnf_l[i] == 'n':
          n_occur += 1
        else:
          u_occur += 1

    found_first_op = False

    found_first_exp = False
    found_second_exp = False
    found_third_exp = False

    #print(f"dnf_length {len(dnf_l)}")
    #print(f"dnf {c_dnf}")

    for i in range(len(dnf_l)):
      if i < DNF_OPS_index[0]:
        # first expresson
        if dnf_l[i] == '_':
          # we know its a negation
          first_exp.append(neg_bit_streams[dnf_l[i+1]])
          found_first_exp = True
        elif dnf_l[i] != '_' and found_first_exp == False:
          # non negation
          first_exp.append(pos_bit_streams[dnf_l[i]])
          found_first_exp = True

      elif i > DNF_OPS_index[0] and i < DNF_OPS_index[1]:
        # we are on the second exp

        if dnf_l[i] == '_':
          # we know its a negation
          second_exp.append(neg_bit_streams[dnf_l[i+1]])
          found_second_exp = True

        elif dnf_l[i] != '_' and found_second_exp == False:
          # non negation
          second_exp.append(pos_bit_streams[dnf_l[i]])
          found_second_exp = True

      elif i > DNF_OPS_index[1] and i <= len(dnf_l) - 1:
        # AnBnC
        #i: [1, 3]
        #len(dnf_l) - 1: 4

        DNF_VARS = ['A', 'B', 'C']
        #print(f"current problem: {dnf_l[i]}")

        if dnf_l[i] == '_':
          # we know its a negation
          third_exp.append(neg_bit_streams[dnf_l[i+1]])
          found_third_exp = True

        elif dnf_l[i] in DNF_VARS and found_third_exp == False:
          # non negation
          third_exp.append(pos_bit_streams[dnf_l[i]])
          found_third_exp = True

    # clean our lists
    # we can do some if statements to check if exp lists are same length
    # EX: if they are all the same length, we can use only 1loop

    string_first = []
    string_second = []
    string_third = []

   # print(f"First_Exp = {first_exp}")
   # print(f"Second_Exp = {second_exp}")
   # print(f"Third_Exp = {third_exp}")

   # this looks gross
   # will fix later

    for i in range(len(first_exp[0])):
      string_first.append(list_to_string(first_exp[0][i]))

    for i in range(len(second_exp[0])):
      string_second.append(list_to_string(second_exp[0][i]))

    for i in range(len(third_exp[0])):
      string_third.append(list_to_string(third_exp[0][i]))

    if n_occur == 2:
      # two intersections
      final_ans = set(string_first).intersection(set(string_second)).intersection(set(string_third))
      if len(final_ans) == 0:
        # no intersection
        list(final_ans)
      #print(f"Final Answer: {final_ans}")

    elif u_occur == 2:
      final_ans = set(string_first).union(set(string_second)).union(set(string_third))
      #print(f"Final Answer: {final_ans}")

    else:
      # one union, one intersection
      # 1 or 0
      # 0 = intersection comes first
      # 1 = intersection comes second

      first = 0
      for i in range(len(dnf_l)):
        if dnf_l[i] == 'n':
          first = 0
          break
        elif dnf_l[i] == 'u':
          first = 1
          break

      if first == 0:
        final_ans = set(string_first) & (set(string_second)) | (set(string_third))

      elif first == 1:
        final_ans = set(string_first) | (set(string_second)) & (set(string_third))

      #print(f"Final Answer: {final_ans}")

   # print(f"First_Exp = {string_first}")
   # print(f"Second_Exp = {string_second}")
   # print(f"Third_Exp = {string_third}")

  if manual:
    return list(final_ans)
  else:
    return c_dnf, list(final_ans)

def sum_regions(region_list, statement_bits):

  answer = []

  ans_dic = {
      "100": region_list[0],
      "010": region_list[1],
      "001": region_list[2],
      "110": region_list[3],
      "101": region_list[4],
      "011": region_list[5],
      "111": region_list[6],
      "000": region_list[7]
  }

  for key, val in ans_dic.items():
    if key in statement_bits:
      answer.append(val)

  return answer

def rn_create():

  #c_dnf = clean dnf form ex: (AnB)
  #truth = bit streams that makes up ex: (AnB)
  c_dnf, bits = get_bits_dnf('rn', '')

  select_question_type = QUESTION_TUPLE[random.randint(0, len(QUESTION_TUPLE) - 1)]

  diagram_selection = select_question_type
  region_list, img_url = venn3_display_shuffle_diagram(select_question_type)

  # we know that region_list = [100, 010, 001, 110, 101, 110, 111, 000]

  answer = sum_regions(region_list, bits)

  new_answer = []
  used = []

  for i in range(len(answer)):
    for j in range(len(answer[i])):
      if answer[i][j] not in used:
        used.append(answer[i][j])
        new_answer.append(answer[i][j])

  # right now. every set will have '' for each element
  # we can change this type of formatting in the future

  for i in range(len(new_answer)):
    new_answer[i] = f'{new_answer[i]}'

  question = f"What is the roster notation for {c_dnf}?: "

  return question, set(new_answer), img_url


def get_cardinality_dnf(region_list, bits):
  answer = sum_regions(region_list, bits)

  total_used = []
  total = 0
  for i in range(len(region_list)):
    for j in range(len(region_list[i])):
      if region_list[i][j] not in total_used:
        total_used.append(region_list[i][j])
        total += 1

  count = 0
  used = []
  for i in range(len(answer)):
    for j in range(len(answer[i])):
      #print(answer[i][j])
      if answer[i][j] not in used:
        used.append(answer[i][j])
        count += 1

  return count, total

def ca_create():

  #'abc', 'num', 'nums', 'bit'

  selection = QUESTION_TUPLE[random.randint(0, len(QUESTION_TUPLE) - 1)]
  c_dnf, bits = get_bits_dnf('rn', '')

  diagram_selection = selection
  region_list, img_url = venn3_display_shuffle_diagram(selection)

  count, total = get_cardinality_dnf(region_list, bits)

  list_dnf = list(c_dnf)
  var_count = 0
  for i in range(len(list_dnf)):
    if list_dnf[i] in DNF_VARS:
      var_count += 1

  # same typa questions. thought i'd spice it up
  selection = random.randint(1, 3)
  question = f"What is the cardinality of {c_dnf}?"
  if selection == 2 | selection == 3 & var_count == 3:
    question = f"What is the cardinality of |{c_dnf}|?"
  elif selection == 3 and var_count <= 2:
    question = f"What is the cardinality of |_({c_dnf})|?"
    count = total - count

  print(f"COUNT: {count}")

  return question, count, img_url

def ps_create():

  selection = QUESTION_TUPLE[random.randint(0, len(QUESTION_TUPLE) - 1)]
  c_dnf, bits = get_bits_dnf('ps', '')

  diagram_selection = selection
  region_list, img_url = venn3_display_shuffle_diagram(selection)

  count, total = get_cardinality_dnf(region_list, bits)

 # get the dnf from q
 # this is kinda jank but it works
 # ps is just 2^ca
 # l_q = list(q)
 # new_string = ""
 # expression_starts = False

 # lol this was so bad
 # I was using ca_create to try n finesse it and this is how I got a dnf from a question string
 # for i in range(len(q)):
 #   if q[i] == '_':
 #     new_string = f"{new_string}_"
 #     expression_starts = i
 #   elif q[i] in DNF_VARS and i > expression_starts:
 #     new_string = f"{new_string}{c_dnf[i]}"
 #     expression_starts = True
 #   elif q[i] in DNF_OPS and expression_starts:
 #     new_string = f"{new_string}{c_dnf[i]}"

  question = f"How many sets are in the power set {c_dnf}?"
  answer = 2**count

  if answer <= 8 and selection != 'abc':

    # we cannot create a set datatype {{}, {1}}
    # since elements within a set are supposed to be immutable
    # if we have {} and {1} in a set these are mutable since they are sets themselves (subsets)
    # also python uses a hashtable to store elements and python can't guarantee the hash will stay the same

    # solution: use lists

    # we can make the user write it out, just make sure its >= 8
    # once we have that we can create all the combinations of that set
    # [[2], [1]]
    # {2, 1}

    # [2, 1]
    # [[2], [1], [2, 1]]

    combine_elements = [] #lol
    question = f"Write out all the subsets in the power set {c_dnf}?"
    answer = sum_regions(region_list, bits)

    print('we have <= 8 ps')

    ps_list = []
    for i in range(len(answer)):
      curr_l = answer[i]
      for j in range(len(curr_l)):
        combine_elements.append(int(curr_l[j]))

    # [2, 1, 6]
    # [[], [2], [1], [6], [2,1], [2, 6], [1,6], [2, 1, 6]]

    from itertools import combinations
    subsets = [list(subset) for r in range(len(combine_elements) + 1) for subset in combinations(combine_elements, r)]

               # + 1 to skip the empty set
               # when r = 1
               # [2], [1], [6]
               # when r = 2
               # [2, 1], [2, 6], [1, 6]
               # when r = 3
               # [2, 1, 6]

    print(f"set_list: {subsets}")
    for i in range(len(subsets)):
      curr = subsets[i]
      for _ in range(len(curr) - 1):
        for j in range(len(curr) - 1):
          if curr[j] > curr[j + 1]:
            curr[j], curr[j + 1] = curr[j + 1], curr[j]

    answer = sorted(subsets)
    # subsets = [[], [17], [6], [1], [17, 6], [17, 1], [6, 1], [17, 6, 1]]

  print(f'ANSWER: {answer}')

  return question, answer, img_url

# under construction
# need better 'dm' questions
def dm_create():

  selection = QUESTION_TUPLE[random.randint(0, len(QUESTION_TUPLE) - 1)]
  c_dnf, bits = get_bits_dnf('dm', '')

  diagram_selection = selection
  region_list, img_url = venn3_display_shuffle_diagram(selection)

  comb = ['000', '001', '010', '011', '100', '101', '110', '111']

  answer = []
  for bit in bits:
    for item in comb:
      if item not in bits:
        answer.append(item)

  answer = sum_regions(region_list, answer)

  count, total = get_cardinality_dnf(region_list, bits)
#  print(f'count: {count}')
#  print(f'total: {total}')

  cardinality_or_sets = [0.2, 0.8]
  select_question = random.choices([0, 1], cardinality_or_sets)[0]
  #print(f'select_question: {select_question}')

  if select_question == 1:

    question = f"What is the roster notation for _({c_dnf})?"

    new_answer = []
    used = []
    for i in range(len(answer)):
      for j in range(len(answer[i])):
        if answer[i][j] not in used:
          used.append(answer[i][j])
          new_answer.append(answer[i][j])

    # right now. every set will have '' for each element
    # we can change this type of formatting in the future

    for i in range(len(new_answer)):
      new_answer[i] = f'{new_answer[i]}'

    return question, set(new_answer), img_url

  else:
    question = f"What is the cardinality for _({c_dnf})?"
    return question, total - count, img_url

def sb_create():
  img_url="" # no img required for this question

  natural_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

 # s_set = random.choices([natural_nums, abc], weights=[0, 1])[0]
 # s_region = random.choices(['A', 'B', 'C'], weights=[.33, .33, .33])[0]
#
#  num_print = random.choice(("Natural", "Whole", "Integer"))
#  less_or_more = 'less' if random.randint(0, 1) == 0 else 'more'
#  num_used = random.randint(3, 10)
#
#  if less_or_more == 'less':
#    question = f'Write the set of {num_print} numbers that is {less_or_more}
#    than {num_used} in set builder notation.'
#
#  else:
#    # we need to find less than or equal to the more number
#    max_num = num_used + random.randint(1, 4)
#    question = f'Write the set of {num_print} numbers that is {less_or_more}
#    than {num_used} and less than {max_num} in set builder notation.'


  #if s_set == abc:
  # s = select
  s_set = random.choices([natural_nums, abc], weights=[.5, .5])[0]
  s_region = random.choices(['A', 'B', 'C'], weights=[.33, .33, .33])[0]

  starting_index = random.randint(0, 4)
  ending_index = len(s_set) - 1 - random.randint(0, 3)

  set_l = s_set[starting_index]
  last_set_l = s_set[ending_index]

  countin_commas = ["{", "}"]
  question = f"Given {s_region} = {countin_commas[0]}xEN | {set_l} <= x <= {last_set_l}{countin_commas[1]}, what is the roster form?"

  difference = ending_index - starting_index + 1
  answer = []

  for i in range(difference):
    answer.append(s_set[starting_index + i])

  return question, str(answer), img_url


################################################################################

def print_notation():

  p_notation = '''
  #################################################################
  Set Theory: 
  "_" = Negation 
  "n" = Intersection 
  "u" = Union 
  \n')
  Logic: 
  "_" = Negation 
  "^" = AND 
  "v" = OR \n'
  
  #################################################################'''
  
  return p_notation



def distribute_skills(skills_list, ask_list):

  ask = int(input('How many questions would you like?: '))

  total_skills = len(skills_list)

  ask_list = []
  for i in range(total_skills):
    ask_list.append(0)

  counter = ask
  while counter > 0:
    for i in range(total_skills):
      if counter > 0:
          ask_list[i] += 1
          counter -= 1

  # check if asking less questions than skills selected
  if ask < len(skills_list):
    skills_list = skills_list[:ask]
    ask_list = ask_list[:ask]

  # remove later
  question_dict = dict(zip(skills_list,ask_list))

  return skills_list, ask_list

################################################################################

# Global Skill Dictionary Containing All Skills
# Working and Under Construction

# {'skill':generator_func,(num_questions,correct_questions,percent,time)}
# pass skill values(num_questions,correct,etc) to gen function
# update those values
# create a check func that checks question

skill_dict = {

              'vd': {
              'function': venn3_to_dnf,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'vb': {
              'function': venn3_to_bit,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'bd': {
              'function': venn3_bit_to_dnf,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},

              'db': {
              'function': venn3_dnf_to_bit,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},

              'so': {
              'function': venn3_set_operators,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'rn': {
              'function': rn_create,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'ca': {
              'function': ca_create,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'ps': {
              'function': ps_create,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'dm': {
              'function': dm_create,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'sb': {
              'function': sb_create,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},

              'v1': {
              'function': v1_create,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'v2': {
              'function': venn_2,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'v3': {
              'function': venn_3_v3,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},

              'ls': {
              'function': logic_symbols,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'pt': {
              'function': pt_to_truth,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'ct': {
              'function': circ_to_tru,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},
              'cp': {
              'function': circ_to_propositional_logic,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
},

              'pe': {
              'function': proof_by_equivalence,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
              },

              'kp': {
              'function': karnaugh_to_propositional,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
              },

              'pk': {
              'function': propositional_logic_to_karnaugh,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
              },

              'ck': {
              'function': circuit_to_kmap,
              'num_questions': 0,
              'correct_questions': 0,
              'percent': 0,
              'time': 0
              }
}

#################not_using_this############################
# function that takes ask list and updates in dictionary
# testing out generics in python
from typing import TypeVar, Generic, Callable
T = TypeVar('T')
#def user_input(ques: str, T_type: Callable[[str],]) -> T:
#  user_input = input(ques)
#
#  return T_type(user_input)
##########################################################

# working and under construction
def check(skills_list, ask_list):
  total_questions = 0
  decimal_places = 2

  # clear terminal
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')

  for i, skill in enumerate(skills_list): 
    if skill in skill_dict:
      skill_entry = skill_dict[skill] # 'vb'
      func = skill_entry['function']
      skill_entry['num_questions'] = ask_list[i] # number of times we are going to ask same skill
      total_questions += ask_list[i] 

      start_time = time.time()
      for _ in range(ask_list[i]):
        #print(ask_list[i])

        tries = 0 # number of tries
        question, answer = func() # this is calling the diagram
        # this fixed the issue with the diagram displaying over input box
        time.sleep(0.5)

        # the \n fixes the auto adjustement of the page after every input
        print(f'{question} \n')
        user_input = input(f': ')

        # edge case that crashed the program if user does ex: {1, 2, 3]
        # TODO: update this to also update num_wrong

        # i want to fix this later. it feels sloppy
        user_ans_type_str = ['vd', 'vb', 'db', 'bd', 'so', 'ca']
        user_ans_type_set = ['sb', 'ro']

        unique_questions = ('ps') # dont touch they have their own process of being assessed
        fixed_types = ('vd', 'vb', 'db', 'bd', 'so', 'ca', 'sb', 'ro', 'ps')

        if type(answer) == set and skill not in unique_questions:
          if skill not in fixed_types:
            user_ans_type_set.append(skill)
        elif type(answer) == str or type(answer) == int and skill not in unique_questions:
          if skill not in fixed_types:
            user_ans_type_str.append(skill)

        if skill in user_ans_type_str:
          user_input = str(user_input)
          answer = str(answer)

        elif skill in user_ans_type_set:
          # we know the answer should return a set
          while ('{' in user_input or '}' in user_input) and ('[' in user_input or ']' in user_input) and type(answer) == set:
            print(f"Incorrect notation. Please use curly braces.")
            user_input = input(f'{question} \n')

          while ('[' in user_input and ']' in user_input) and type(answer) == set:
            print(f"Incorrect notation. Please use curly braces.")
            user_input = input(f'{question} \n')

          if '{' in user_input:
            import re
            import string
            # this is a "set" question
            # re.findall = finds which '\d' = ints(0-9) and '+' = matches one or more consecutive digits
            # \d+ → Match a full number (not just one digit at a time)
            # checks if there is any occurence of a character
            if_abc = any(x in string.ascii_lowercase for x in list(user_input))
            if not if_abc:
              # this regular expression only fixes ints
              using_findall = re.findall('\d+', user_input)
              #print(f"using_findall: {using_findall}")
              for i in range(len(using_findall)):
                using_findall[i] = f'{using_findall[i]}'

              user_input = set(using_findall)
            else:
              # we are dealing with chars/strings
              user_input = set(re.findall('[a-zA-Z]+', user_input))

        elif skill == 'ps':
          # we know the answer should return a string
          # subsets = [[], [17], [6], [1], [17, 6], [17, 1], [6, 1], [17, 6, 1]]
          # we are getting {{}, {17}, {6}, {1}, {17, 6}, {17, 1}, {1, 6}, {1, 6, 17}}

          if '{' in user_input:
            # we are dealing with powersets
            #Your answer: ['{{}', ' {3}', ' {3', ' 4}', ' {4}}']

            #list: ['{', '{', '}', ',', ' ', '{', '3', '}', ',', ' ', '{', '4', '}', ',', ' ', '{', '3', ',', ' ', '4', '}', '}']
            while '{' != user_input[0] or '{' != user_input[1]:
              print(f'Did you forget a curly brace at the start? ')
              user_input = input(f'{question} \n')

            while '}' != user_input[len(user_input) - 1] or '}' != user_input[len(user_input) - 2]:
              print(f'Did you forget a curly brace at the end? ')
              user_input = input(f'{question} \n')

            user_input = list(user_input)
            for i in range(len(user_input)):
              if user_input[i] == '{':
                user_input[i] = '['
              elif user_input[i] == '}':
                user_input[i] = ']'

            import ast
            try:
              #ast.literal_eval replaces "[1, 2]" into [1, 2]
              # converts strings that look like a ds into actual python ds
              user_input = ast.literal_eval(''.join(user_input))#godspeed
            except SyntaxError as e:
              # update num_wrong here ???
              print(f"  {e.text.strip()}\n  {' ' * (e.offset - 1)}^\nSyntaxError: {e.msg}")
              print(f'Maybe you included a "." or "/" in your response?\n')
              user_input = input(f'{question} \n')

            print(f'after join: user_input {user_input}')
            print(f'user_input type: {type(user_input)}')

            #ewwwwwwwwwwwwwwwwww
            # TODO: refactor later
            for i in range(len(user_input)):
              curr = user_input[i]
              for _ in range(len(curr) - 1):
                for j in range(len(curr) - 1):
                  if curr[j] > curr[j + 1]:
                    curr[j], curr[j + 1] = curr[j + 1], curr[j]

            user_input = sorted(user_input)
          else:
            user_input, answer = str(user_input), str(answer)
        
        # checking if answer is correct
        while True:
          if user_input == answer:
            if tries == 0:
              print('Correct')
              skill_entry['correct_questions'] += 1
            elif tries == 1:
              print('Correct')
            break
          else:
            tries += 1
            print('Try Again. \n') 
            user_input = input(': ')
            if tries == 1:
              print(f'Incorrect. Correct answer is {answer} \n')
              break

        print('\n')

    end_time = time.time()
    total_time = round((end_time - start_time)/60,decimal_places)

    # under construction
    skill_entry['percent'] = round((100*skill_entry['correct_questions']/skill_entry['num_questions']), decimal_places)
    skill_entry['time'] = total_time

    # for each individual skill
    print(f'Total Questions: {total_questions}')

  return None

################################################################################

# redirect to a score page after program is finished

# Ex:
# ##### Skill Grades ######  Date: .. Time: ..
# ...
# ...

# checking for spaces

all_skills = {
  'ALL': [x for x in choice_list if x not in ('AS', 'AL')],
  'AS':  ['vb','vd','bd','db','so','rn','ca','ps','dm','sb','ss','v2','v3'],
  'AL':  ['ls','pt','kp','pk','cp','pe']
}

def distribute_skills(skills_list, num_of_ques):

  total_skills = len(skills_list)

  ask_list = []
  for i in range(total_skills):
    ask_list.append(0)

  counter = num_of_ques
  while counter > 0:
    for i in range(total_skills):
      if counter > 0:
          ask_list[i] += 1
          counter -= 1

  # check if asking less questions than skills selected
  if num_of_ques < len(skills_list):
    skills_list = skills_list[:num_of_ques]
    ask_list = ask_list[:num_of_ques]

  return ask_list

def parse_selection(raw: str):
  raw = (raw or "").strip()
  parts = re.split(r"[,\s]+", raw)          
  return [p for p in parts if p]

@app.route("/", methods=["GET", "POST"])
def index():

  # I need to return all prints into HTML strings
  
#  data = {
#      "verify_print": f'<h1>\n\nVerify you are running the update from: {updated_on}.\n\n</h1>',
#      "skill_grade_print": f'<h1>\n##########skill grades###############</h1>'
#  }
#  
  verify_print = f'\n\nVerify you are running the update from: {updated_on}.\n\n'

#v1  - Venn Diagram with 1 Set
  
  skills_menu = dedent('''
############# CSC230 Discrete Math #############
ALL - ALL Skills and Exit Selection
################# Set Theory ###################
AS  - All Set Theory Sklls and Exit Selection
vd  - Identify the Venn Disjunctive Normal Form
vb  - Identify the Venn Bit Stream
bd  - Bit Stream to Disjunctive Normal Form
db  - Disjunctive Normal Form to Bit Stream
so  - Set Operators (union(u), intersection(n), compliment(_))
rn  - Roster Notation
ca  - Cardinality
ps  - Power Sets
dm  - DeMorgan's Law
sb  - Set Builder Notation
ss  - Subsets & Proper Subsets
#### SKILLS BELOW ARE UNDER CONSTRUCTION #####
v2  - Venn Diagram with 2 Sets
v3  - Venn Diagram with 3 Sets
################## Logic #####################
AL  - All Logic Skills and Exit Selection
ls  - Logic Symbols
pt  - Propositional Logic to Truth Table
kp  - Karnaugh Map to Propositional Logic
pk  - Propositional Logic to Karnaugh Map
cp  - Circuit to Propositional Logic
ck  - Circuit to Karnaugh Map
ct  - Circuit to Truth Table
##############################################''').strip()

#  check(skills_list, ask_list)

#  skill_grade_print = f'\n##########skill grades###############'
#  for i in range(len(skills_list)):
#    skill_entry = skill_dict[skills_list[i]]
#    percent = skill_entry['percent']
#    time_ = skill_entry['time']
#
#    print(f"{skills_list[i]}: {percent}% in {time_} minutes.")
#
#  print('##################################### \n')
  
  # I need to display:
  # menu
  # questions
  # results
  
  index_dic = {
    "verify_print": verify_print,
    "menu": skills_menu
  }

  # we are going post our selection
  if request.method == "POST":
    answer = request.form["ans"]
    if answer in choice_list:
      # we are making a selection
      session["answer"] = answer
  else:
    return render_template("index.html", dic=index_dic)


@app.route("/rubric")
def rubric():
  return render_template("rubric.html")

@app.get("/selection/current")
def selection_current():
    current = session.get("current", [])
    return render_template("partials/current.html", current=current)

@app.post("/clear")
def clear():
  session.clear()
  return render_template("partials/current.html", current=[])

@app.post("/run")
def run():

  tokens = parse_selection(request.form.get("ans"))
  prev = session.get("current", []) 

  if isinstance(prev, str):         
      prev = [prev]

  allowed = set(choice_list) 
  current = [c for c in prev if c in allowed] 

  for code in tokens:
      if code in allowed and code not in current:
          current.append(code)

  session["current"] = current

  return render_template("partials/current.html", current=current)

"""

state lives in session. session is the duration of the users interaction with the application.
if a user logs in, session starts, and when the user logs out, session is ended.

fragments/partials: small HTML chunks that dont extend base.html(not a real page, just html logic)
using HTMX im able to swap this fragment into #question-box 


"""


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    skills = session.get("current", [])

    # Start/Update: rebuild everything when n is posted
    if request.method == "POST" and ("n" in request.form):
      n_raw = (request.form.get("n") or "").strip()
      try:
        n = int(n_raw)
      except ValueError:
        n = session.get("n", 10)
      if n < 1:
        n = 1
      session["n"] = n
      ask_list = reset_quiz_state(skills, n)
    else:
      n = session.get("n", 10)
      ask_list = session.get("ask_list")
      if ask_list is None:
        ask_list = reset_quiz_state(skills, n)

    # Return the full page. The question box is loaded via /quiz/current (HTMX).
    return render_template(
      "quiz.html",
      skills=skills,
      num_of_ques=n,
      ask_list=ask_list,
    )

def clear_quiz_state(hard: bool = False):
    """remove all quiz related session keys 
    if we set hard=True flag then we will remove current skill list and # of questions asked.
    """
    for k in (
      "ask_list", "queue", "qi", "tries", "score",
      "current_q", "started_at", "progress", "decimal_places"
    ):
      session.pop(k, None)
    if hard:
      session.pop("current", None) # selected skills
      session.pop("n", None) # question count

def reset_quiz_state(skills, n, shuffle=False):
    ask_list = distribute_skills(skills, n) if skills else []
    session["ask_list"] = ask_list

    queue = []

    for s, c in zip(skills, ask_list):
      queue.extend([s] * int(c))
    if shuffle:
      random.shuffle(queue)

    session["queue"] = queue
    session["qi"] = 0
    session["tries"] = 2
    session["score"] = 0
    session["current_q"] = None
    session["started_at"] = time.time()

    # consistent keys with the scoreboard
    session["progress"] = {
        s: {"planned": int(c), "asked": 0, "correct": 0}
        for s, c in zip(skills, ask_list) if c > 0
    }

    session["decimal_places"] = 2
    return ask_list

DEFAULT_N = 0

@app.post("/quiz/restart")
def quiz_restart():
    hard = request.args.get("hard") == "1"
    reset = request.args.get("reset") == "1"

    # clear all quiz variables
    clear_quiz_state(hard=hard)
    
    # soft restart = keep skills and # of questions asked
    if not hard:
      skills = session.get("current", [])
      n = session.get("n", DEFAULT_N)
      session["n"] = n
      reset_quiz_state(skills, n)
      if reset:
        return quiz_current()  
      else:
        return redirect(url_for("quiz"))

    # i dont think we'll need this tbh
    if request.headers.get("HX-Request"):
      return quiz_current()  # will create the first question and table of prev/curr quiz
    # Fallback: reload the full page
    return redirect(url_for("quiz"))


# TODO: combine these normalize functions into one since they have same functionality
def normalize_answer(a):

  if type(a) == set:
    a_list = []
    
    for x in a:
      a_list.append(x)
    
    if a_list[0] in list(string.ascii_lowercase):
      # we are dealing with a list of characters
      region_list = {'a': 1,'b': 2,'c': 3,'d': 4,'e': 5,'f': 6,'g': 7,'h': 8}

      for i in range(len(a_list)):
        for j in range(0, len(a_list) - i - 1):
          if region_list[a_list[j]] > region_list[a_list[j + 1]]:
            a_list[j], a_list[j + 1] = a_list[j + 1], a_list[j]

    else:

      for i in range(len(a_list)):
        a_list[i] = int(a_list[i])

      for i in range(len(a_list)):
        for j in range(0, len(a_list) - i - 1):
          if a_list[j] > a_list[j + 1]:
            a_list[j], a_list[j + 1] = a_list[j + 1], a_list[j]

    a_list = str(a_list)
    #print(f'a_list {a_list}')

    return a_list

  else:
    a = str(a)

    return (a or "").strip().replace(" ", "").lower()

def normalize_user_input(user_input, skill):

  user_ans_type_str = ['vd', 'vb', 'db', 'bd', 'so', 'ca', 'ps']

  if skill not in user_ans_type_str:

    char_set = any(c.islower() for c in user_input)

    if not char_set:
      # nums
      u_list = [int(x) for x in re.findall(r'-?\d+', user_input)]
      for i in range(len(u_list)):
        for j in range(len(u_list) - i - 1):
          if u_list[j] > u_list[j + 1]:
            u_list[j], u_list[j + 1] = u_list[j + 1], u_list[j]
    else:
    
      u_list = [x for x in user_input if x in set(string.ascii_lowercase)]
      
      #print(f'u_list str: {u_list}')
      region_list = {'a': 1,'b': 2,'c': 3,'d': 4,'e': 5,'f': 6,'g': 7,'h': 8}

      for i in range(len(u_list)):
        for j in range(0, len(u_list) - i - 1):
          if region_list[u_list[j]] > region_list[u_list[j + 1]]:
            u_list[j], u_list[j + 1] = u_list[j + 1], u_list[j]
  
    if u_list:
      u_list = str(u_list)
      return (u_list or "").strip().replace(" ", "").lower()

  else:
    return (user_input or "").strip().replace(" ", "").lower()

@app.get("/quiz/current")
def quiz_current():

  queue = session.get("queue", [])
  qi = session.get("qi", 0)
  tries = session.get("tries", 2)
  score = session.get("score", 0)

  finished = (qi >= len(queue))
  state = session.get("current_q")

  if not finished and state is None:
    state = _create_next_question()

  return render_template(
    "partials/question.html",
    finished=finished,
    state=state,
    tries=tries,
    idx=qi,
    total=len(queue),
    message=None,
    score=score,
    per_skill=_build_per_skill_rows(), # always pass
  )

@app.post("/quiz/check")
def quiz_check():

  queue = session.get("queue", [])
  qi = session.get("qi", 0)
  tries = session.get("tries", 2)
  score = session.get("score", 0)
  state = session.get("current_q") or _create_next_question()

  if state is None:
    return render_template(
      "partials/question.html",
      finished=True,
      score=score,
      total=len(queue),
      idx=qi,
      message="No questions queued.",
      per_skill=_build_per_skill_rows(),
    )

  vals = request.form.getlist("ans") # user input
  user_ans = normalize_user_input(vals[-1], queue[qi]) if vals else ""

  # we are getting the expected answer
  expected = state.get("expected", "").replace(" ", "")
  print(f"expected: {expected}")
  message = None
  
  print(f'user_answer: {user_ans}')

  if user_ans == expected:

    # per skill correct
    skill = state.get("skill")
    prog = session.get("progress", {})

    if skill in prog:
      prog[skill]["correct"] = prog[skill].get("correct", 0) + (1 if tries == 2 else 0)
      session["progress"] = prog

    # advance to next question
    qi += 1
    tries = 2
    message = "Correct!"

    session["qi"] = qi
    session["tries"] = tries
    session["current_q"] = None

    # overall score
    score += 1
    session["score"] = score

  else:
    tries = max(0, tries - 1)

    session["tries"] = tries
    if tries > 0:
      # stay on same question
      return render_template(
        "partials/question.html",
        finished=False,
        state=state,
        tries=tries,
        idx=qi,
        total=len(queue),
        message=f"Try again. {tries} attempt left.",
        score=score,
        per_skill=_build_per_skill_rows(),   # <<< pass it here, too
      )
    else:
      # out of tries 
      qi += 1
      session["qi"] = qi
      tries = 2
      session["tries"] = tries
      session["current_q"] = None
      message = ""

  # finished?
  if qi >= len(queue):
    return render_template(
      "partials/question.html",
      finished=True,
      score=score,
      total=len(queue),
      idx=qi,
      message=message,
      per_skill=_build_per_skill_rows(),
    )

  # next question
  next_state = _create_next_question()
  return render_template(
    "partials/question.html",
    finished=False,
    state=next_state,
    tries=session.get("tries", 2),
    idx=session.get("qi", 0),
    total=len(session.get("queue", [])),
    message=message,
    score=session.get("score", 0),
    per_skill=_build_per_skill_rows(),
  )


def _build_per_skill_rows():

    prog = session.get("progress") or {}
    dp = session.get("decimal_places", 2)
    rows = []

    for s, info in prog.items():
      planned = info.get("planned", 0)
      asked = info.get("asked", 0)
      correct = info.get("correct", 0)

      pct_asked = round(100 * correct / asked, dp) if asked else 0.0
      pct_planned = round(100 * correct / planned, dp) if planned else 0.0

      rows.append({
        "skill": s,
        "correct": correct,
        "asked": asked,
        "planned": planned,
        "percent": pct_asked, 
        "percent_of_planned": pct_planned # eh not gna use
      })

    rows.sort(key=lambda r: (-r["asked"], r["skill"]))

    return rows

def _create_next_question():

    """create and store the next question in session['current_q'], or None if finished"""

    queue = session.get("queue", [])
    qi = session.get("qi", 0)
    
    # we finished
    if qi >= len(queue):
      session["current_q"] = None
      return None
      
    skill = queue[qi]
    entry = skill_dict.get(skill)
    if not entry or not callable(entry.get("function")):
      # skip unknown
      session["qi"] = qi + 1
      return _create_next_question()

    q, a, img_url = entry["function"]()  # must return (q, a, img_url)
    print(f'answer: {a}')

    # Mark this question as asked for that skill
    prog = session.get("progress", {})
    if skill in prog:
      prog[skill]["asked"] = prog[skill].get("asked", 0) + 1
      session["progress"] = prog

    state = {
      "skill": skill,
      "question": q,
      "img_url": img_url,
      "expected": normalize_answer(a),
    }
    session["current_q"] = state
    return state

#@app.route("/quiz", methods=["GET", "POST"])
#def quiz():
#
#    skills = session.get("current", [])
#
#    if request.method == "POST": 
#        n_raw = (request.form.get("n") or "").strip() # n number of questions
#        try:
#            n = int(n_raw)
#        except ValueError:
#            n = session.get("n", 10)
#        if n < 1:
#            n = 1
#        session["n"] = n
#    else:
#        n = session.get("n", 10)
#
#    ask_list = distribute_skills(skills, n) if skills else [] 
#    # keep in session if other routes need it ( not rlly needed )
#    session["ask_list"] = ask_list
#
#    ques_items = []
#    total_questions = 0
#
#    # ['vb', 'vd']
#    # [2, 2]
#    # ((vb, 2), (vd, 2))
#
#    for skill, count in zip(skills, ask_list):
#        if count <= 0:
#            continue
#        if skill not in skill_dict:
#            continue
#
#        entry = dict(skill_dict[skill])
#        entry["num_questions"] = count # assigning the num_questions for given skill
#
#        func = entry.get("function") 
#        func_name = getattr(func, "__name__", None)
#
#        question, answer, img_url = func()
#
#        ques_items.append({
#            "skill": skill,
#            "skill_entry": entry,      
#            "func_name": func_name, 
#            "num_ques": count,         
#            "question": question,
#            "answer": answer,
#            "img_url": img_url,
#        })
#
#        total_questions += count
#
#    ques_info = {
#        "items": ques_items,            
#        "total_ques": total_questions, 
#        "n_requested": n,
#    }
#
#    return render_template(
#        "quiz.html",
#        skills=skills,
#        num_of_ques=n,
#        ask_list=ask_list,
#        ques_info=ques_info,
#    )
#
#          for _ in range(ask_list[i]):
#
#            tries = 0 # number of tries
#            question, answer = func() # this is calling the diagram
#
#
#
#            # this fixed the issue with the diagram displaying over input box
#            time.sleep(0.5)
#
#            # the \n fixes the auto adjustement of the page after every input
#            print(f'{question} \n')
#            user_input = input(f': ')
#
#            # edge case that crashed the program if user does ex: {1, 2, 3]
#            # TODO: update this to also update num_wrong
#
#            # i want to fix this later. it feels sloppy
#            user_ans_type_str = ['vd', 'vb', 'db', 'bd', 'so', 'ca']
#            user_ans_type_set = ['sb', 'ro']
#
#            unique_questions = ('ps') # dont touch they have their own process of being assessed
#            fixed_types = ('vd', 'vb', 'db', 'bd', 'so', 'ca', 'sb', 'ro', 'ps')
#
#            if type(answer) == set and skill not in unique_questions:
#              if skill not in fixed_types:
#                user_ans_type_set.append(skill)
#            elif type(answer) == str or type(answer) == int and skill not in unique_questions:
#              if skill not in fixed_types:
#                user_ans_type_str.append(skill)
#
#            if skill in user_ans_type_str:
#              user_input = str(user_input)
#              answer = str(answer)
#
#            elif skill in user_ans_type_set:
#              # we know the answer should return a set
#              while ('{' in user_input or '}' in user_input) and ('[' in user_input or ']' in user_input) and type(answer) == set:
#                print(f"Incorrect notation. Please use curly braces.")
#                user_input = input(f'{question} \n')
#
#              while ('[' in user_input and ']' in user_input) and type(answer) == set:
#                print(f"Incorrect notation. Please use curly braces.")
#                user_input = input(f'{question} \n')
#
#              if '{' in user_input:
#                import re
#                import string
#                # this is a "set" question
#                # re.findall = finds which '\d' = ints(0-9) and '+' = matches one or more consecutive digits
#                # \d+ → Match a full number (not just one digit at a time)
#                # checks if there is any occurence of a character
#                if_abc = any(x in string.ascii_lowercase for x in list(user_input))
#                if not if_abc:
#                  # this regular expression only fixes ints
#                  using_findall = re.findall('\d+', user_input)
#                  #print(f"using_findall: {using_findall}")
#                  for i in range(len(using_findall)):
#                    using_findall[i] = f'{using_findall[i]}'
#
#                  user_input = set(using_findall)
#                else:
#                  # we are dealing with chars/strings
#                  user_input = set(re.findall('[a-zA-Z]+', user_input))
#
#            elif skill == 'ps':
#              # we know the answer should return a string
#              # subsets = [[], [17], [6], [1], [17, 6], [17, 1], [6, 1], [17, 6, 1]]
#              # we are getting {{}, {17}, {6}, {1}, {17, 6}, {17, 1}, {1, 6}, {1, 6, 17}}
#
#              if '{' in user_input:
#                # we are dealing with powersets
#                #Your answer: ['{{}', ' {3}', ' {3', ' 4}', ' {4}}']
#
#                #list: ['{', '{', '}', ',', ' ', '{', '3', '}', ',', ' ', '{', '4', '}', ',', ' ', '{', '3', ',', ' ', '4', '}', '}']
#                while '{' != user_input[0] or '{' != user_input[1]:
#                  print(f'Did you forget a curly brace at the start? ')
#                  user_input = input(f'{question} \n')
#
#                while '}' != user_input[len(user_input) - 1] or '}' != user_input[len(user_input) - 2]:
#                  print(f'Did you forget a curly brace at the end? ')
#                  user_input = input(f'{question} \n')
#
#                user_input = list(user_input)
#                for i in range(len(user_input)):
#                  if user_input[i] == '{':
#                    user_input[i] = '['
#                  elif user_input[i] == '}':
#                    user_input[i] = ']'
#
#                import ast
#                try:
#                  #ast.literal_eval replaces "[1, 2]" into [1, 2]
#                  # converts strings that look like a ds into actual python ds
#                  user_input = ast.literal_eval(''.join(user_input))#godspeed
#                except SyntaxError as e:
#                  # update num_wrong here ???
#                  print(f"  {e.text.strip()}\n  {' ' * (e.offset - 1)}^\nSyntaxError: {e.msg}")
#                  print(f'Maybe you included a "." or "/" in your response?\n')
#                  user_input = input(f'{question} \n')
#
#                print(f'after join: user_input {user_input}')
#                print(f'user_input type: {type(user_input)}')
#
#                #ewwwwwwwwwwwwwwwwww
#                # TODO: refactor later
#                for i in range(len(user_input)):
#                  curr = user_input[i]
#                  for _ in range(len(curr) - 1):
#                    for j in range(len(curr) - 1):
#                      if curr[j] > curr[j + 1]:
#                        curr[j], curr[j + 1] = curr[j + 1], curr[j]
#
#                user_input = sorted(user_input)
#              else:
#                user_input, answer = str(user_input), str(answer)
#            
#            # checking if answer is correct
#            while True:
#              if user_input == answer:
#                if tries == 0:
#                  print('Correct')
#                  skill_entry['correct_questions'] += 1
#                elif tries == 1:
#                  print('Correct')
#                break
#              else:
#                tries += 1
#                print('Try Again. \n') 
#                user_input = input(': ')
#                if tries == 1:
#                  print(f'Incorrect. Correct answer is {answer} \n')
#                  break
#
#            print('\n')
#
#        end_time = time.time()
#        total_time = round((end_time - start_time)/60,decimal_places)
#
#        # under construction
#        skill_entry['percent'] = round((100*skill_entry['correct_questions']/skill_entry['num_questions']), decimal_places)
#        skill_entry['time'] = total_time
#
#        # for each individual skill
#        print(f'Total Questions: {total_questions}')
#
#      return None

 # print('\n##########Skill Grades###############')
 # for i in range(len(skills_list)):
 #   skill_entry = skill_dict[skills_list[i]]
 #   percent = skill_entry['percent']
 #   time_ = skill_entry['time']

 #   print(f"{skills_list[i]}: {percent}% in {time_} minutes.")
    



@app.route("/help")
def help():
  return render_template("help.html")

@app.route("/about", methods=["GET", "POST"])
def about():

  heads_tails = random.randint(0, 1)

  if heads_tails == 1:
    answer = "Heads"
  else:
    answer = "Tails"
  
  random_dic = {
      "answer": answer
  }

  return render_template("about.html", random_dic=random_dic)

def main():

  print(f'\n\nVerify you are running the update from: {updated_on}.\n\n')
  while True:

    skills_list, ask_list = select_skills()
    check(skills_list, ask_list)

    print('\n##########Skill Grades###############')
    for i in range(len(skills_list)):
      skill_entry = skill_dict[skills_list[i]]
      percent = skill_entry['percent']
      time_ = skill_entry['time']

      print(f"{skills_list[i]}: {percent}% in {time_} minutes.")

    print('##################################### \n')


  return None

################################################################################

if __name__ == "__main__":
  #main()
  app.run(debug=True)


