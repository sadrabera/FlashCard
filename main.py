import json
from datetime import datetime


class Vocabulary:
    def __init__(self, vocab, meaning, added_date):
        self.vocab = vocab
        self.meaning = meaning
        self.added_date = added_date
        self.last_used_date = added_date
        self.times_used = 0
        self.times_correct = 0
        self.times_incorrect = 0

    def __eq__(self, other):
        return self.vocab == other.vocab

    def __hash__(self):
        return hash(self.vocab)

    def __str__(self):
        return self.vocab + ": " + self.meaning


all_vocabs = []


def add_vocabulary():
    vocab = input("Enter a word: ")
    meaning = input("Enter  meaning of the word: ")
    added_date = datetime.now()
    vocabulary = Vocabulary(vocab, meaning, added_date)
    all_vocabs.append(vocabulary)


def remove_vocabulary():
    vocab = input("Enter a word: ")
    for vocabulary in all_vocabs[:]:
        if vocabulary.vocab == vocab:
            all_vocabs.remove(vocabulary)
            break


if __name__ == '__main__':
    try:
        with open('vocab_file.json', 'r') as f:
            all_vocabs = json.load(f)
    except FileNotFoundError:
        open('vocab_file.json', 'w').close()
    except json.decoder.JSONDecodeError:
        open('vocab_file.json', 'w').close()

    while True:
        print('\n' + '-' * 50)
        print('Please select an option:')
        print('1. Add a new vocabulary')
        print('2. Remove a vocabulary')
        print('3. View all vocabularies')
        print('4. View all vocabularies added in a specific month')
        print('5. View all vocabularies added in a specific year')
        selected = input('6. Exit\n')

        match selected:
            case '1':
                add_vocabulary()
                break
            case '2':
                remove_vocabulary()
                break
            case '3':
                break
