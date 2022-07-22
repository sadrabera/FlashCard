class Vocabulary:
    def __init__(self, vocab, added_date):
        self.vocab = vocab
        self.added_date = added_date
        self.last_used_date = added_date
        self.times_used = 0
