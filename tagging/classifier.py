from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB


classifiers = {
    'lr': LogisticRegression,
    'svm': LinearSVC,
    'mnb': MultinomialNB
}


def feature_dict(sent, i):
    """Feature dictionary for a given sentence and position.

    sent -- the sentence.
    i -- the position.
    """
    palabra=sent[i] #suponinedo que al menos tiene una palabra
    especiales= ["á","é","í","ó","ú", "ü"] #solo chequeo minusculas porque pregunto sobre el lower del string

    #sobre la anterior
    if i==0: #primera de la oracion
        alower=""
        aistitle=False
        aisupper=False
        aisnumeric=False
        aisplural=False
        #aunder=False
        #aislower=False
        aespecial=False
    else:
        alower = sent[i-1].lower()
        aistitle = sent[i-1].istitle()
        aisupper = sent[i-1].isupper()
        aisnumeric = sent[i-1].isnumeric()
        aisplural= (sent[i-1][-1:].lower() == 's')
        #aunder= (sent[i-1].find('_') >= 0)
        aislower = sent[i-1].islower()
        aespecial = (1 in [c in sent[i-1].lower() for c in especiales]),

    #sobre la proxima
    if i==len(sent)-1: #si es la ultima
        plower = ""
        pistitle = False
        pisupper = False
        pisnumeric = False
        pisplural= False
        #punder=False
        pislower = False
        pespecial = False
    else:
        plower = sent[i + 1].lower()
        pistitle = sent[i + 1].istitle()
        pisupper = sent[i + 1].isupper()
        pisnumeric = sent[i + 1].isnumeric()
        pisplural= (sent[i + 1][-1:].lower() == 's')
        #punder = (sent[i + 1].find('_') >= 0)
        pislower = sent[i + 1].islower()
        pespecial = (1 in [c in sent[i+1].lower() for c in especiales]),

    return {
        'lower': palabra.lower(),
        'istitle': palabra.istitle(),
        'isupper': palabra.isupper(),
        'isnumeric': palabra.isnumeric(),
        'isplural': (palabra[-1:].lower() == 's'),
        #'under': (palabra.find('_') >= 0),
        #'islower': palabra.islower(),
        'especial': (1 in [c in palabra.lower() for c in especiales]),
        'alower': alower,
        'aistitle': aistitle,
        'aisupper': aisupper,
        'aisnumeric': aisnumeric,
        'aisplural': aisplural,
        #'aunder': aunder,
        'aespecial': aespecial,
        'aislower': aislower,
        'plower': plower,
        'pistitle': pistitle,
        'pisupper': pisupper,
        'pisnumeric': pisnumeric,
        'pisplural': pisplural,
        #'punder': punder,
        'pislower': pislower,
        'pespecial': pespecial,
    }


class ClassifierTagger:
    """Simple and fast classifier based tagger.
    """

    def __init__(self, tagged_sents, clf='lr'):
        """
        clf -- classifying model, one of 'svm', 'lr' (default: 'lr').
        """
        self.pipeline = Pipeline([
            ('vect', DictVectorizer()),
            ('clf', classifiers[clf]())
        ])
        self.tagged_sents = list(tagged_sents)
        self._palabrasvistas = set()
        self.fit(self.tagged_sents)

    def fit(self, tagged_sents):
        """
        Train.

        tagged_sents -- list of sentences, each one being a list of pairs.
        """

        X = []
        y_true = []
        for sent in tagged_sents:
            #frase=list
            frase = [word[0] for word in sent]
            #print(sent)
            #for w in sent:
            #    frase.append(w[0])
            for i in range(0,len(sent)):
                self._palabrasvistas.add(sent[i][0])  # como es set, si ya esta va a obviarla
                x = feature_dict(frase, i)
                X.append(x)
                y_true.append(sent[i][1])

        #print(X)
        #print(y_true)
        self.pipeline.fit(X, y_true)

    def tag_sents(self, sents):
        """Tag sentences.

        sent -- the sentences.
        """

        return [self.tag(sent) for sent in sents]

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        X_test = [feature_dict(sent, i) for i in range(0,len(sent))]
        y_pred = self.pipeline.predict(X_test)
        return y_pred


    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """

        return w not in self._palabrasvistas
