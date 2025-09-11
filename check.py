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

