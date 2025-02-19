import os, time, sys, pandas as pd

## Clear screen
def clear(seconds: int = 0):
    time.sleep(seconds)
    os.system('cls' if os.name == 'nt' else 'clear')

## Exit Program
def exit_program():
    print("\nGoodbye!")
    clear(1)
    sys.exit()

def find_file(filename, search_path='.'):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.abspath(os.path.join(root, filename))
    
def csv_retriver(category: int = -1,sample: int = -1, filename: str = 'quests.csv') -> pd.DataFrame:

    try:

        questions = pd.read_csv(\
                find_file(filename),\
                quotechar='"',\
                delimiter=',',\
                skipinitialspace=True,\
                encoding='utf-8',\
        )
        
        if sample == -1 and category == -1:
                questions.index = questions['index']   
                q_num = questions.groupby('question_category').count()['question'].to_list()
                return q_num
        else:

            try:
                questions.index = questions['index']   
                questions = questions.query(f'question_category == {category}').copy()
                questions.drop('question_category', axis=1, inplace=True)
                questions.columns = ['0', '1', '2', '3', '4']
                questions = questions.sample(sample)
            except Exception as e:
                print("Error", e)
    
    except Exception as e:
        print(e)
        exit()
    
    return questions

def choice(msg: str = "",max_sel: int = 3):
    while True:
        print(msg)
        value = input("").strip()
        if value.isnumeric() and len(value) < 4:
            try:
                if int(value) in range(1,max_sel+1):
                    return int(value)
            except ValueError:
                print("Invalid input type")
                continue
        elif value == 'q':
            exit_program()
        else:
            print("Invalid input")
            continue

def score(data):

    questions = data['1'].to_list()
    answers = [i.strip() for i in data['2'].to_list()]
    correct_answers = data['3'].to_list()
    score = 0

    for question, answer, correct_answer in zip(questions,answers,correct_answers):
        clear(2)
        print(question,'\n')
        
        answs = answer.split(",")
        max_answs = len(answs)
        for index, ans in enumerate(answs,start=1):
            print(f"{index}. {ans}")
        
        correct_answer = correct_answer.split(',')
        users = []
        print()

        for i in range(len(correct_answer)):
            user = choice("Select the answer:",max_answs)
            users.append(answs[user-1])
        
        if sorted(users) == sorted(correct_answer):
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect answer! the correct answer is {', '.join(correct_answer)}")
    
    print(f"Your score is {(score/len(questions))*100}%")
    print("\n")
    clear(3)