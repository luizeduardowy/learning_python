import copy
import os
quiz_completed = False
questions_answered = 0
questions_correct = 0
questions_incorrect = 0
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

while quiz_completed != True:
    try:
        questions = [
            {
                'question': 'What is 10/2?',
                'options': ['2', '10', '5', '0'],
                'answer': '5'
            },
            {
                'question': 'What is 5*5(5x5)?',
                'options': ['25', '5', '55', '0'],
                'answer': '25'
            },
            {
                'question': 'What programming language was used to make this test?',
                'options': ['Python', 'Javascript', 'C++', 'TypeScript', 'HTML'],
                'tip': "The language´s name is also the name of an animal",
                'answer': 'Python'
            }
        ]

        while questions_answered < 3:
            print(f'Question: {str(questions_answered + 1)}: {questions[questions_answered]['question']}')
            print(f'Options: {questions[questions_answered]['options']}')
            if questions[questions_answered].get('tip', False):
                print(f'Tip: {questions[questions_answered]['tip']}')
            answer = input('Write your answer: ')
            if answer == questions[questions_answered]['answer']:
                questions_correct += 1
            elif answer in questions[questions_answered]['options']:
                questions_incorrect += 1
            else:
                clear()
                print('Please pick an valid answer')
                continue
            questions_answered += 1
        correct_percentage = (((questions_correct/questions_answered) * 1000).__round__())/10
        incorrect_percentage = (((questions_incorrect/questions_answered) * 1000).__round__())/10
        print(f'Of the {str(questions_answered)} questions in this quiz, you answered {str(correct_percentage)}% of them correctly and you answered {str(incorrect_percentage)}% of them incorectly')
        quiz_completed = True

    except ValueError:
        ...