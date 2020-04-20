"""Print corpus statistics.

Usage:
  stats.py -c <path>
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict
0
from tagging.ancora import SimpleAncoraCorpusReader
import collections


class POSStats:
    """Several statistics for a POS tagged corpus.
    """

    def __init__(self, tagged_sents):
        """
        tagged_sents -- corpus (list/iterable/generator of tagged sentences)
        """
        # WORK HERE!!
        # COLLECT REQUIRED STATISTICS INTO DICTIONARIES.

        self._estadisticas = dict()
        self._count = defaultdict(int)
        self._countTag = defaultdict(int)
        self._tcount = defaultdict(dict)
        self._wcount = defaultdict(set)

        sentences = 0
        palabras = 0
        for sent in tagged_sents:
            sentences += 1 #Cantidad de oraciones
            for word in sent:
                palabras += 1 #Cantidad de ocurrencias de palabras
                self._count[word[0]] += 1 #contando cuantas veces cada palabra aparece
                self._countTag[word[1]] += 1 #contado de etiquetas (vocabulario de tags)
                #print(word)

                # Contando para cada etiqueta, cuantas veces aparece la palabra con esa etiqueta. Si los diccionarios no estan, los creo
                if (word[1]) in self._tcount:
                    if (word[0]) in self._tcount[word[1]]:
                        self._tcount[word[1]][word[0]] += 1
                    else:
                        self._tcount[word[1]][word[0]] = 1
                else:
                    self._tcount[word[1]][word[0]] = 1

                # Contando para cada palabra, los tags diferentes con que aparece. Si los diccionarios no estan, los creo
                if (word[0]) in self._wcount:
                    self._wcount[word[0]].add(word[1]) #agrega el tag al set de la palabra. si esta, el add ignora
                else:
                    self._wcount[word[0]] = {word[1]}

        self._estadisticas["sentences"] = sentences
        self._estadisticas["palabras"] = palabras
        self._estadisticas["vocabulario"] = len(self._count) #Cantidad de palabras (vocabulario).
        self._estadisticas["vocabularioDeTags"] = len(self._countTag)  # Cantidad de palabras (vocabulario).
        self._estadisticas["tokens"] = sum(self._count.values())

    def sent_count(self):
        """Total number of sentences."""
        return self._estadisticas["sentences"]


    def token_count(self):
        """Total number of tokens."""
        return self._estadisticas["tokens"]


    def words(self):
        """Vocabulary (set of word types)."""
        return self._estadisticas["palabras"]

    def word_count(self):
        """Vocabulary size."""
        return self._estadisticas["vocabulario"]


    def word_freq(self, w):
        """Frequency of word w."""
        return self._count[w]

    def unambiguous_words(self):
        """List of words with only one observed POS tag."""
        return (ambiguous_words(self, 1))

    def ambiguous_words(self, n):
        """List of words with n different observed POS tags.

        n -- number of tags.
        """
        ntag = []

        for word in self._wcount:
            if len(self._wcount[word]) == n:
                ntag.append(word)

        return ntag

    def tags(self):
        """POS Tagset."""
        return(self._countTag.keys()) #(necesario que sea de tipo set?)

    def tag_count(self):
        """POS tagset size."""
        return self._estadisticas["vocabularioDeTags"]

    def tag_freq(self, t):
        """Frequency of tag t."""
        return(self._countTag[t])

    def tag_word_dict(self, t):
        """Dictionary of words and their counts for tag t."""
        return dict(self._tcount[t])


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data

    #corpus = SimpleAncoraCorpusReader(opts['-c'])  #No se porque no me esta cargando asi
    corpus = SimpleAncoraCorpusReader(opts['<path>']) #por la documentacion que encontre, lo cambie a '<path>' para no hardcodearlo
    # corpus = SimpleAncoraCorpusReader("ancora-3.0.1es")
    sents = corpus.tagged_sents()

    count = defaultdict(int)




    # compute the statistics
    stats = POSStats(sents)

    print('Basic Statistics')
    print('================')
    print('sents: {}'.format(stats.sent_count()))
    token_count = stats.token_count()
    print('tokens: {}'.format(token_count))
    word_count = stats.word_count()
    print('words: {}'.format(word_count))
    print('tags: {}'.format(stats.tag_count()))
    print('')

    print('Most Frequent POS Tags')
    print('======================')
    tags = [(t, stats.tag_freq(t)) for t in stats.tags()]
    sorted_tags = sorted(tags, key=lambda t_f: -t_f[1])
    print('tag\tfreq\t%\ttop')
    for t, f in sorted_tags[:10]:
        words = stats.tag_word_dict(t).items()
        sorted_words = sorted(words, key=lambda w_f: -w_f[1])
        top = [w for w, _ in sorted_words[:5]]
        print('{0}\t{1}\t{2:2.2f}\t({3})'.format(t, f, f * 100 / token_count, ', '.join(top)))
    print('')

    print('Word Ambiguity Levels')
    print('=====================')
    print('n\twords\t%\ttop')
    for n in range(1, 10):
        words = list(stats.ambiguous_words(n))
        m = len(words)

        # most frequent words:
        sorted_words = sorted(words, key=lambda w: -stats.word_freq(w))
        top = sorted_words[:5]
        print('{0}\t{1}\t{2:2.2f}\t({3})'.format(n, m, m * 100 / word_count, ', '.join(top)))
