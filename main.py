import json
import time
from datetime import datetime


class Vocabulary:
    def __init__(self, word, meaning, added_date):
        self.word = word
        self.meaning = meaning
        self.added_date = added_date
        self.last_used_date = added_date
        self.times_used = 0
        self.times_correct = 0
        self.times_incorrect = 0
        self.waiting_for_review_days = 1

    def __eq__(self, other):
        return self.word == other.vocab

    def __hash__(self):
        return hash(self.word)

    def __str__(self):
        return '\u001b[32mword:' + self.word + "\n" + '\u001b[33mmeaning:' + self.meaning + '\u001b[0m'

    def __dict__(self):
        return {'word': self.word, 'meaning': self.meaning, 'added_date': self.added_date.__str__(),
                'last_used_date': self.last_used_date.__str__(), 'times_used': self.times_used,
                'times_correct': self.times_correct, 'times_incorrect': self.times_incorrect,
                'waiting_for_review_days': self.waiting_for_review_days}


all_vocabs = []


def add_vocabulary():
    word = input("Enter a word: ")
    meaning = input("Enter meaning of the word: ")
    added_date = datetime.now()
    new_vocabulary = Vocabulary(word, meaning, added_date)
    all_vocabs.append(new_vocabulary)
    print("Vocabulary added successfully!")
    input_any_key()


def remove_vocabulary():
    vocab = input("Enter it's word: ")
    for every_vocabulary in all_vocabs[:]:
        if every_vocabulary.word == vocab:
            all_vocabs.remove(every_vocabulary)
            break
    print("Vocabulary removed successfully!")
    input_any_key()


def add_waiting_for_review_days(vocab):
    temp = vocab.waiting_for_review_days
    if temp < 30:
        vocab.waiting_for_review_days *= 2
    elif temp >= 30:
        vocab.waiting_for_review_days = temp + temp // 2


def quiz():
    all_quiz_vocabs = []
    for every_vocabulary in all_vocabs:
        if (datetime.now() - every_vocabulary.last_used_date).days >= every_vocabulary.waiting_for_review_days:
            all_quiz_vocabs.append(every_vocabulary)
    all_quiz_vocabs.sort(key=lambda x: x.last_used_date, reverse=True)
    for every_vocabulary in all_quiz_vocabs:
        print('\u001b[34mThe word is: \u001b[31m' + every_vocabulary.word)
        answer = input("\u001b[36mEnter meaning of the word: ")
        if answer == every_vocabulary.meaning:
            every_vocabulary.times_correct += 1
            every_vocabulary.last_used_date = datetime.now()
            add_waiting_for_review_days(every_vocabulary)
            print("\u001b[35mCorrect!\u001b[0m")
            time.sleep(2)
        else:
            print('\u001b[31manswer is \u001b[32m' + every_vocabulary.meaning)
            check_answer = input(
                "\u001b[36mWas your answer correct? (\u001b[32my\u001b[36m/\u001b[31mn\u001b[36m)\u001b[0m")
            if check_answer == "y":
                every_vocabulary.times_correct += 1
                every_vocabulary.last_used_date = datetime.now()
                add_waiting_for_review_days(every_vocabulary)
                print("\u001b[35mCorrect!\u001b[0m")
                time.sleep(2)
            else:
                print('\u001b[31mOOPS!!!\u001b[0m')
                every_vocabulary.times_incorrect += 1
                every_vocabulary.last_used_date = datetime.now()
                every_vocabulary.waiting_for_review_days = 1
                print('You can see Persian meaning here:')
                print('https://translate.google.com/?sl=auto&tl=fa&text=' + every_vocabulary.word + '&op=translate')
                print('Or English meaning here:')
                print('https://dictionary.cambridge.org/dictionary/english/' + every_vocabulary.word)
                input_any_key()


def input_any_key():
    input("\n\u001b[36mPress any key to continue...\u001b[0m")


def printing_underline():
    print('\u001b[36m\n' + '-' * 50 + '\u001b[0m')


if __name__ == '__main__':
    print()
    print(""" \u001b[36m  
                                                                                    
I8,        8        ,8I            88                                               
`8b       d8b       d8'            88                                               
 "8,     ,8"8,     ,8"             88                                               
  Y8     8P Y8     8P   ,adPPYba,  88   ,adPPYba,   ,adPPYba,   88,dPYba,,adPYba,   
  `8b   d8' `8b   d8'  a8P_____88  88  a8"     ""  a8"     "8a  88P'   "88"    "8a  
   `8a a8'   `8a a8'   8PP"""""""  88  8b          8b       d8  88      88      88  
    `8a8'     `8a8'    "8b,   ,aa  88  "8a,   ,aa  "8a,   ,a8"  88      88      88  
     `8'       `8'      `"Ybbd8"'  88   `"Ybbd8"'   `"YbbdP"'   88      88      88  
                                                                                    
                                                                                    
""")
    try:
        with open('vocab_file.json', 'r') as f:
            temp_load = json.load(f)
            for i in temp_load:
                new_vocabulary = Vocabulary(i['word'], i['meaning'],
                                            datetime.strptime(i['added_date'], '%Y-%m-%d %H:%M:%S.%f'))
                new_vocabulary.last_used_date = datetime.strptime(i['last_used_date'], '%Y-%m-%d %H:%M:%S.%f')
                new_vocabulary.times_used = i['times_used']
                new_vocabulary.times_correct = i['times_correct']
                new_vocabulary.times_incorrect = i['times_incorrect']
                new_vocabulary.waiting_for_review_days = i['waiting_for_review_days']
                all_vocabs.append(new_vocabulary)

    except FileNotFoundError:
        open('vocab_file.json', 'w').close()
    except json.decoder.JSONDecodeError:
        open('vocab_file.json', 'w').close()

    while True:
        flag = False
        counter = 0
        for vocabulary in all_vocabs:
            if (datetime.now() - vocabulary.last_used_date).days >= vocabulary.waiting_for_review_days:
                counter += 1
        printing_underline()
        if counter != 0:
            print(
                '\u001b[32m0. Take a quiz,\t\u001b[31m%d \u001b[32mvocabs \u001b[31mshould\u001b[32m be reviewed' % counter)

        else:
            print('\u001b[35mHooray!! you have no vocab to review. \u001b[0m')
        print('\u001b[34m1. Add a \u001b[31mnew\u001b[34m vocabulary')
        print('\u001b[34m2. \u001b[31mRemove \u001b[34ma vocabulary')
        print('\u001b[34m3. View all \u001b[33mvocabularies')
        print('\u001b[34m4. View all \u001b[33mvocabularies \u001b[34madded in a specific month')
        print('\u001b[34m5. View all \u001b[33mvocabularies \u001b[34madded in a specific year')
        print('\u001b[31m6. Exit\n')

        selected = input('\u001b[36mPlease select an option:\u001b[0m')

        match selected:
            case '0':
                quiz()

            case '1':
                add_vocabulary()

            case '2':
                remove_vocabulary()

            case '3':
                for i in all_vocabs:
                    printing_underline()

                    print(i)
                input_any_key()

            case '4':
                print('Enter a date with year and month:')
                date = input('Example: 2019-01\n')
                for i in all_vocabs:
                    if i.added_date.strftime('%Y-%m') == date:
                        printing_underline()
                        print(i)
                input_any_key()
            case '5':
                print('Enter a year :')
                year = input('Example: 2019\n')
                for i in all_vocabs:
                    if i.added_date.strftime('%Y') == year:
                        printing_underline()

                        print(i)
                input_any_key()
            case '6':
                flag = True
                print('Exiting...')
                break
            case default:
                print('Invalid input')
                break
        if flag:
            break
        printing_underline()

    with open('vocab_file.json', 'w') as f:
        json.dump(all_vocabs, f, default=lambda o: o.__dict__(), sort_keys=True, indent=4)
