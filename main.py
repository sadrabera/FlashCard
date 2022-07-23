import json
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
        return 'word:' + self.word + "\n" + 'meaning:' + self.meaning

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


def remove_vocabulary():
    vocab = input("Enter a word: ")
    for every_vocabulary in all_vocabs[:]:
        if every_vocabulary.word == vocab:
            all_vocabs.remove(every_vocabulary)
            break


def add_waiting_for_review_days(vocab):
    temp = all_vocabs[vocab].waiting_for_review_days
    if temp < 30:
        all_vocabs[vocab].waiting_for_review_days *= 2
    elif temp >= 30:
        all_vocabs[vocab].waiting_for_review_days = temp + temp // 2


def quiz():
    all_quiz_vocabs = []
    for every_vocabulary in all_vocabs:
        if (datetime.now() - every_vocabulary.last_used_date).days >= every_vocabulary.waiting_for_review_days:
            all_quiz_vocabs.append(every_vocabulary)
    all_quiz_vocabs.sort(key=lambda x: x.last_used_date, reverse=True)
    for every_vocabulary in all_quiz_vocabs:
        print('The word is: ' + every_vocabulary.word)
        answer = input("Enter meaning of the word: ")
        if answer == every_vocabulary.meaning:
            every_vocabulary.times_correct += 1
            every_vocabulary.last_used_date = datetime.now()
            add_waiting_for_review_days(every_vocabulary)
            print("Correct!")
        else:
            print('answer is ' + every_vocabulary.meaning)
            check_answer = input("Was your answer correct? (y/n)")
            if check_answer == "y":
                every_vocabulary.times_correct += 1
                every_vocabulary.last_used_date = datetime.now()
                add_waiting_for_review_days(every_vocabulary)
            else:
                every_vocabulary.times_incorrect += 1
                every_vocabulary.last_used_date = datetime.now()
                every_vocabulary.waiting_for_review_days = 1
                print('You can see Persian meaning here:')
                print('https://translate.google.com/?sl=auto&tl=fa&text=' + every_vocabulary.word + '&op=translate')
                print('You can see English meaning here:')
                print('https://dictionary.cambridge.org/dictionary/english/' + every_vocabulary.word)
                input("\nPress any key to continue...")


if __name__ == '__main__':

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

        print('\n' + '-' * 50)
        print('Please select an option:')
        if counter != 0:
            print('0. Take a quiz\t%d vocabs should be reviewed' % counter)

        else:
            print('Hooray!! you have no vocab to review')
        print('1. Add a new vocabulary')
        print('2. Remove a vocabulary')
        print('3. View all vocabularies')
        print('4. View all vocabularies added in a specific month')
        print('5. View all vocabularies added in a specific year')
        selected = input('6. Exit\n')

        match selected:
            case '0':
                quiz()

            case '1':
                add_vocabulary()

            case '2':
                remove_vocabulary()

            case '3':
                for i in all_vocabs:
                    print('\n' + '-' * 50)
                    print(i)
                input("\nPress any key to continue...")

            case '4':
                print('Enter a date with year and month:')
                date = input('Example: 2019-01\n')
                for i in all_vocabs:
                    if i.added_date.strftime('%Y-%m') == date:
                        print('\n' + '-' * 50)
                        print(i)
                input("\nPress any key to continue...")
            case '5':
                print('Enter a year :')
                year = input('Example: 2019\n')
                for i in all_vocabs:
                    if i.added_date.strftime('%Y') == year:
                        print('\n' + '-' * 50)
                        print(i)
                input("\nPress any key to continue...")
            case '6':
                flag = True
                print('Exiting...')
                break
            case default:
                print('Invalid input')
                break
        if flag:
            break
        print('\n' + '-' * 50)
    with open('vocab_file.json', 'w') as f:
        json.dump(all_vocabs, f, default=lambda o: o.__dict__(), sort_keys=True, indent=4)
