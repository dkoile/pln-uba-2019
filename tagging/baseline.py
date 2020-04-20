from collections import defaultdict


class BadBaselineTagger:

    def __init__(self, tagged_sents, default_tag='nc0s000'):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        default_tag -- tag for all words.
        """
        self._default_tag = default_tag

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        return self._default_tag

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return True


class BaselineTagger:

    def __init__(self, tagged_sents, default_tag='nc0s000'):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        default_tag -- tag for unknown words.
        """

        self._default_tag = default_tag
        self._tcount = defaultdict(dict)

        for sent in tagged_sents:
            for word in sent:
                # Contando para cada palabra, cuantas veces aparece con cada etiqueta. Si los diccionarios no estan, los creo
                if (word[0]) in self._tcount:
                    if (word[1]) in self._tcount[word[0]]:
                        self._tcount[word[0]][word[1]] += 1
                    else:
                        self._tcount[word[0]][word[1]] = 1
                else:
                    self._tcount[word[0]][word[1]] = 1

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        print("tageando")
        print(w)
        if w in self._tcount:
            itemMaxValue = max(self._tcount[w].items(), key=lambda x: x[1])
            print('Max value in Dict: ', itemMaxValue[1])
            print('Key With Max value in Dict: ', itemMaxValue[0])

            return itemMaxValue[0]
        else:
            return self._default_tag

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return (w not in self._tcount)
