# 1. Napisać funkcję, która zlicza wystąpienia wszystkich słów w pliku tekstowym.
# Umożliwić wyświetlenie n najczęściej występujących słów _z remisami_ (tzn. jeśli słowa
# na pozycji n+1 i n+2 wystąpiły tyle samo razy co to na pozycji n, to także mają zostać wyświetlone).
# Przetestować na załączonym pliku potop.txt.
def words_counter(filename, n):  # nazwa
    with open(filename, 'r', encoding='utf-8') as file:  # przesłonięcie symbolu wbudowanego
        text = file.read().lower()  # cały plik do pamięci?

        # Tokenizowanie
        words = []
        for word in text.split():
            words.append(word.strip('.,!?()[]{}"\''))
        # text.split() dzieli mi na pojedyncze slowa a word.strip usunie znaki specjalne

        # Zliczanie
        word_counts = {}  # collections.Counter?
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        max_count = sorted_words[n][1]

        tied_words = [word for word, count in sorted_words if count >= max_count]

        return tied_words

#
# def top_words(words_counter, top_n):
#     sorted_words = sorted(words_counter.items(), key=lambda x: x[1], reverse=True)[:top_n]
#     current_count = None
#     current_rank = 0
#         # for ngram, count in sorted_ngrams:
#     for rank, (words, count) in enumerate(sorted_ngrams, start=1):
#          if count != current_count:
#               current_count = count
#               current_rank = rank
#          print(f'{current_rank}.{words}: appears {count} times')
#
#          if rank == top_n:
#              break

# 2. Napisać funkcje, które zliczają wystąpienia wszystkich n-gramów słownych w pliku tekstowym.
# Również umożliwić wyświetlenie czołówki z remisami.
# N-gram to KAŻDE n występujących po sobie słów (albo innych jednostek, w zależności od kontekstu).
# Np. zdanie "Ala ma kota" ma 2 digramy: "Ala ma" i "ma kota".

def ngrams_counter(filename, n):
    with open(filename, 'r', encoding='utf-8') as file:  # DRY
        text = file.read()

        words = text.lower().split()
        ngrams = []
        for i in range(len(words) - n + 1):
            ngrams.append(tuple(words[i:i + n]))

        ngram_counter = {}
        for ngram in ngrams:
            ngram_counter[ngram] = ngram_counter.get(ngram, 0) + 1

        return ngram_counter

def top_ngrams(ngram_counter, top_ng):
    sorted_ngrams = sorted(ngram_counter.items(), key=lambda x: x[1], reverse=True)[:top_ng]
    current_count = None
    current_rank = 0
    # for ngram, count in sorted_ngrams:
    for rank, (ngram, count) in enumerate(sorted_ngrams, start=1):
        if count != current_count:
            current_count = count
            current_rank = rank
        print(f'{current_rank}.{ngram}: appears {count} times')

        if rank == top_ng:
            break  # a remisy?

# 3. Napisać context manager do obsługi pliku .conll.
# Iteracja po pliku powinna zwracać kolejne linie w postaci krotki bądź listy.
# Przykładowe użycie:
#
# 	with open_conll('ala_ma_kota.conll') as infile:
# 		for token in infile:
# 			print(token)
#
# Przykładowe wyjście:
# ('Ala', 'Ala', 'noun')
# ('ma', 'mieć', 'verb')
# ('kota', 'kot', 'noun')
# ('.', '.', 'punct')

class using_conll:  # proszę przemyśleć tę nazwę
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'r', encoding='utf-8')
        return self

    def __exit__(self, type, value, traceback):
        if self.file:
            self.file.close()

    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()
        if not line:
            raise StopIteration

        # Tokenizacja linii w formie listy
        tokens = line.replace("\"", "").split()

        return tokens

if __name__ == "__main__":
    filename = 'potop.txt'

    n = 3
    top_words = words_counter(filename, n)
    print(f"Najczesciej wystepujace slowa: {top_words}")

    ng = 3  # st n gramu
    top_ng = 5  # Liczba topowych n-gramów
    ngram_counts = ngrams_counter(filename, ng)
    top_ngrams(ngram_counts, top_ng)

    with using_conll('nkjp.conll') as file:
        for token in file:
            print(token)


