 pln-uba-2019
Introducción al Procesamiento de Lenguaje Natural - UBA 2019


------------------------------------------------------------------------------------------------------------------------
TP1.1

Estadisticas generadas a partir de los datos del argumento, en este caso, del corpus Ancora

Basic Statistics
================
sents: 17378
tokens: 517194
words: 46501
tags: 85

Most Frequent POS Tags
======================
tag     freq    %       top                                         significado
sp000   79884   15.45   (de, en, a, del, con)                       Preposicion
nc0s000 63452   12.27   (presidente, equipo, partido, país, año)    Sustantivo común (en singular)
da0000  54549   10.55   (la, el, los, las, El)                      Articulo definido
aq0000  33906   6.56    (pasado, gran, mayor, nuevo, próximo)       Adjetivo
fc      30147   5.83    (,)                                         Coma
np00000 29111   5.63    (Gobierno, España, PP, Barcelona, Madrid)   Nombre propio
nc0p000 27736   5.36    (años, millones, personas, países, días)    Sustantivo comun (en plural)
fp      17512   3.39    (.)                                         Punto
rg      15336   2.97    (más, hoy, también, ayer, ya)               Adverbio (generico, no incluyendo la negacion)
cc      15023   2.90    (y, pero, o, Pero, e)                       Conjunción coordinante

Word Ambiguity Levels
=====================
n       words   %       top
1       43972   94.56   (,, con, por, su, El)
2       2318    4.98    (el, en, y, ", los)
3       180     0.39    (de, la, ., un, no)
4       23      0.05    (que, a, dos, este, fue)
5       5       0.01    (mismo, cinco, medio, ocho, vista)
6       3       0.01    (una, como, uno)
7       0       0.00    ()
8       0       0.00    ()
9       0       0.00    ()


Tuve problemas en la recepcion de parametros del docopt de este ejercicio, y siguiendo la documentacion termine cambiando '-c' por '<path>'. No ocurrio lo mismo en el resto de los ejercicios


------------------------------------------------------------------------------------------------------------------------
TP1.2

Se implemento un etiquetador basico que etiqueta cada palabra con la etiqueta con que mas frecuentemente aparecio en el entrenamiento. Para las palabras desconocidas, se le asignaba nombre comun singular (nc0s000)
Se lo comparo tambien con BadBaselineTagger, uno que etiqueta todo con una etiqueta default (nc0s000)

Con BadBaselineTagger los resultados fueron de

Accuracy: 12.65% / 0.00% / 12.65% (total / known / unk)

Y la matriz de confucion (sabiamos que todo terminaria en esa etiqueta)

g \ m   sp000   nc0s000 da0000  aq0000  fc      nc0p000 rg      np00000 fp      cc
sp000   -       14.39   -       -       -       -       -       -       -       -
nc0s000 -       12.65   -       -       -       -       -       -       -       -
da0000  -       9.70    -       -       -       -       -       -       -       -
aq0000  -       7.28    -       -       -       -       -       -       -       -
fc      -       5.85    -       -       -       -       -       -       -       -
nc0p000 -       5.53    -       -       -       -       -       -       -       -
rg      -       3.73    -       -       -       -       -       -       -       -
np00000 -       3.58    -       -       -       -       -       -       -       -
fp      -       3.55    -       -       -       -       -       -       -       -
cc      -       3.41    -       -       -       -       -       -       -       -

Con el tagger basico que programamos, la eficacia fue

Accuracy: 87.57% / 95.25% / 18.01% (total / known / unk)

y la matriz de confucion

g \ m   sp000   nc0s000 da0000  aq0000  fc      nc0p000 rg      np00000 fp      cc
sp000   14.28   0.05    -       -       -       -       0.01    -       -       -
nc0s000 0.00    12.20   -       0.27    -       0.00    0.03    0.00    -       0.00
da0000  -       0.15    9.54    -       -       -       -       -       -       -
aq0000  0.01    2.04    -       4.88    -       0.12    0.00    -       -       -
fc      -       -       -       -       5.85    -       -       -       -       -
nc0p000 -       1.24    -       0.22    -       4.06    -       -       -       -
rg      0.02    0.31    -       0.04    -       -       3.27    -       -       0.02
np00000 0.00    2.04    -       0.00    -       0.00    -       1.52    -       0.00
fp      -       -       -       -       -       -       -       -       3.55    -
cc      0.00    0.01    -       -       -       -       0.05    0.00    -       3.34


los tiempos de la primera fueron de entrenamiento:
real    0m0,797s
user    0m1,088s
sys     0m0,728s
y de evaluacion
real    0m2,528s
user    0m2,776s
sys     0m0,712s

de la segunda en entrenamiento
real    0m9,283s
user    0m9,276s
sys     0m0,880s
y evaluacion
real    0m3,056s
user    0m3,224s
sys     0m0,836s


------------------------------------------------------------------------------------------------------------------------
TP1.3

Se implemento el clasificador "three words" requerido. Para esto se vectorirzaron los datos pedidos para la palabra actual, anterior y proxima, ademas de las funciones necesarias.
Tambien el archivo de entrenamiento fue adaptado para ser compatible con los clasificadores pedidos. La nueva forma de usarlo es la siguiente:

"""Train a sequence tagger.

Usage:
  train.py [options] -c <path> -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: badbase]:
                  badbase: Bad baseline
                  base: Baseline
                  class: Classifier
  -k <Classifier> Classifier [default: lr]
                  lr: Logistic Regression
                  svm: Linerar SVM
                  mnb: Multinomial NB
  -c <path>     Ancora corpus path.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""

Logistic Regression

time python tagging/scripts/train.py -c ancora-3.0.1es -m class -k lr -o baselinelr
time python tagging/scripts/eval.py -c ancora-3.0.1es -i baselinelr -m

Resultados:
Accuracy: 91.69% / 95.01% / 61.66% (total / known / unk)

g \ m   sp000   nc0s000 da0000  aq0000  fc      nc0p000 rg      np00000 fp      cc
sp000   14.26   0.01    -       0.05    -       -       0.01    0.00    -       -
nc0s000 0.00    11.89   0.01    0.52    -       0.02    0.02    0.09    -       -
da0000  -       0.11    9.50    0.01    -       0.01    -       0.01    -       -
aq0000  0.00    0.51    -       6.43    -       0.17    0.01    0.06    -       -
fc      -       -       -       -       5.85    -       -       -       -       -
nc0p000 -       0.35    -       0.47    -       4.61    -       0.04    -       -
rg      0.02    0.04    0.00    0.39    -       0.00    3.11    0.03    -       0.02
np00000 -       0.22    -       0.08    -       0.01    -       3.24    -       0.00
fp      -       -       -       -       -       -       -       -       3.55    -
cc      0.00    0.00    -       0.01    -       0.00    0.05    0.00    -       3.34


Tiempo de entrenamiento:
real    11m36,838s
user    35m2,484s
sys     45m21,908s

Tiempo de evaluacion:
real    0m6,050s
user    0m5,700s
sys     0m0,936s

Linerar SVM

time python tagging/scripts/train.py -c ancora-3.0.1es -m class -k svm -o baseline
time python tagging/scripts/eval.py -c ancora-3.0.1es -i baseline -m

Resultados:

Accuracy: 94.11% / 97.57% / 62.76% (total / known / unk)

g \ m   sp000   nc0s000 da0000  aq0000  fc      nc0p000 rg      np00000 fp      cc
sp000   14.30   0.00    -       0.03    -       -       0.00    -       -       -
nc0s000 0.00    12.09   0.01    0.33    -       0.02    0.02    0.08    -       0.00
da0000  -       0.08    9.53    -       -       0.00    -       0.00    -       -
aq0000  0.00    0.34    -       6.61    -       0.15    0.01    0.05    -       -
fc      -       -       -       -       5.85    -       -       -       -       -
nc0p000 -       0.25    -       0.31    -       4.90    -       0.04    -       -
rg      0.02    0.02    0.00    0.21    -       0.01    3.35    0.01    -       0.02
np00000 0.00    0.21    -       0.08    -       0.01    -       3.26    -       0.00
fp      -       -       -       -       -       -       -       -       3.55    -
cc      0.00    -       -       0.01    -       -       0.05    0.00    -       3.34

Tiempo de entrenamiento:
real    5m31,784s
user    5m28,760s
sys     0m2,460s

Tiempo de evaluacion:
real    0m7,547s
user    0m6,332s
sys     0m1,020s

Multinomial NB

time python tagging/scripts/train.py -c ancora-3.0.1es -m class -k mnb -o baselinemnb
time python tagging/scripts/eval.py -c ancora-3.0.1es -i baselinemnb -m
Resultados:
Accuracy: 84.28% / 88.07% / 49.99% (total / known / unk)

g \ m   sp000   nc0s000 da0000  aq0000  fc      nc0p000 rg      np00000 fp      cc
sp000   14.31   -       0.01    0.00    0.00    0.00    0.00    0.00    -       -
nc0s000 0.05    12.05   0.07    0.09    0.02    0.01    0.00    0.29    -       0.00
da0000  0.00    0.14    9.52    0.00    0.00    0.00    -       0.01    -       -
aq0000  0.22    0.88    0.19    5.11    0.14    0.23    0.01    0.40    0.00    0.01
fc      0.00    -       -       -       5.85    -       -       0.00    -       -
nc0p000 0.06    0.28    0.17    0.07    0.02    4.64    0.00    0.26    -       0.00
rg      0.20    0.17    0.08    0.14    0.04    0.01    2.77    0.23    -       0.02
np00000 0.03    0.27    0.05    0.00    0.00    0.01    0.00    3.21    -       -
fp      0.00    -       -       -       -       -       -       -       3.55    -
cc      0.01    0.00    0.00    -       -       0.00    0.05    0.05    -       3.29

Tiempo de entrenamiento:
real    0m21,138s
user    0m18,440s
sys     0m2,892s

Tiempo de evaluacion:
real    2m29,013s
user    1m57,748s
sys     0m31,972s


------------------------------------------------------------------------------------------------------------------------
TP1.4

------------------------------------------------------------------------------------------------------------------------
TP1.5

