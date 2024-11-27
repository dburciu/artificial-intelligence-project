#-----------------------------------------------------------------------------
# 1. Citirea datelor din fișier și împărțirea setului de date
# în date de antrenare și testare, aleatoriu
#------------------------------------------------------------------------
import pandas as pd
import numpy as np

# avem nevoie de date in format numeric
date = pd.read_excel("Data_cat_numerice.xlsx")

# elimin coloana PLUS // aici mentionase doamna sa folosim ceva special
# pentru a transforma plus in numeric
date = date.drop(date.columns[28], axis=1)

# încercăm să prezicem coloana 4 (rasa), restul sunt caracteristicile specifice
X = date.iloc[:, [col for col in range(date.shape[1]) if col != 4]].values
y = date.iloc[:, 4].values  # coloana 5 (indice 4)

# normalizăm caracteristicile pentru convergență mai rapidă
X = (X - X.mean(axis=0)) / X.std(axis=0)

# împărțirea în seturi de antrenare și testare
np.random.seed(42)
indici = np.random.permutation(len(X))  # amestecăm indicii
indice_impartire = int(0.8 * len(X))  # 80% pentru antrenare, 20% pentru testare

X_antrenare, X_testare = X[indici[:indice_impartire]], X[indici[indice_impartire:]]
y_antrenare, y_testare = y[indici[:indice_impartire]], y[indici[indice_impartire:]]

#-----------------------------------------------------------------------------
# 2. Inițializarea parametrilor: dimensiunea stratului de intrare,
# a straturilor ascunse și de ieșire, rata de învățare,
# numărul maxim de epoci, etc) și a ponderilor
#------------------------------------------------------------------------

dimensiune_intrare = X_antrenare.shape[1]  # numărul de caracteristici
dimensiune_strat_ascuns = 10  # numărul de neuroni din stratul ascuns
dimensiune_iesire = len(np.unique(y))  # numărul de clase distincte

# parametrii pentru antrenare
rata_invatare = 0.01
numar_maxim_epoci = 1000
# "epoci" = de câte ori modelul parcurge întregul set de date de antrenare

# inițializarea ponderilor și bias-urilor
np.random.seed(42)
ponderi_intrare_ascuns = np.random.rand(dimensiune_intrare, dimensiune_strat_ascuns) - 0.5
ponderi_ascuns_iesire = np.random.rand(dimensiune_strat_ascuns, dimensiune_iesire) - 0.5
bias_ascuns = np.zeros(dimensiune_strat_ascuns)
bias_iesire = np.zeros(dimensiune_iesire)


# Ponderile (weights) sunt coeficienți asociați fiecărei conexiuni
# dintre neuronii din straturi diferite.
# Ele controlează importanța fiecărei intrări asupra rezultatului unui neuron.
#
# Biasurile (biases) sunt valori adăugate la suma ponderată
# z înainte de aplicarea funcției de activare.
# Biasul permite modelului să deplaseze funcția de activare,
# astfel încât să poată modela relații mai complexe,
# inclusiv situațiile în care ieșirea nu este 0 când toate intrările sunt 0.

# z = x1*w1 + x2*w2 + ... + xn*wn + b

#-----------------------------------------------------------------------------
# 3. Funcțiile de activare și derivatele acestora, funcția de eroare
#------------------------------------------------------------------------

# funcția sigmoidă - de activare
# transformă o valoare de intrare într-un interval între 0 și 1
# convertește scorurile brute z în probabilități, astfel încât acestea să poată fi interpretate.
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# pentru a calcula gradientul, care ajustează ponderile și biasurile.
# permite actualizarea ponderilor proporțional cu eroarea și contribuția fiecărei intrări.
def derivata_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


# funcția de eroare (entropie încrucișată)
# Funcția de eroare măsoară cât de bine se potrivesc predicțiile rețelei neuronale cu valorile reale
# (etichetele). Scopul antrenării este să minimizăm funcția de eroare
def functie_eroare(y_real, y_pred):
    return -np.sum(y_real * np.log(y_pred) + (1 - y_real) * np.log(1 - y_pred)) / len(y_real)

#-------------------------------------------------------------------------------
# 4. Propagarea înainte: calculează ieșirea neuronilor
#-------------------------------------------------------------------------------

def propagare_inainte(X, ponderi_intrare_strat_ascuns, ponderi_iesire_strat_ascuns, bias_strat_ascuns, bias_strat_iesire):

    # Calculul pentru stratul ascuns
    # np.dot realizeaza suma ponderata a intrarilor 
    # poate efectua produs scalar(daca ambele intrari sunt vectori unidimensionali)
    # produs matricial(daca ambele intrari sunt matrici bidimensionale)
    # produs dintre o matrice si un vector(una dintre intrari este o matrice si cealalta un vector)
    # se efectueaza calculul activarilor in stratul ascuns(pentru fiecare neuron din stratul ascuns, se calculeaza suma ponderata
    # a intrarilor din stratul anterior(stratul de intrare) si se adauga bias-ul asociat

    intrare_strat_ascuns = np.dot(X, ponderi_intrare_strat_ascuns) + bias_strat_ascuns

    # aici se aplica functia de activare a fiecarui neuron din stratul ascuns 

    iesire_strat_ascuns = sigmoid(intrare_strat_ascuns)
    
    # se efectueaza calculul activarilor din stratul de iesire
    # se utilizeaza activarile din stratul ascuns pentru a calcula intrarea ponderata a stratului de iesire

    intrare_strat_iesire = np.dot(iesire_strat_ascuns, ponderi_iesire_strat_ascuns) + bias_strat_iesire

    # se aplica functia de activare pentru a afla predictiile retelei pentru fiecare clasa a setului de date
    iesire_strat_iesire = sigmoid(intrare_strat_iesire)
    
    # vom returna iesire_strat_ascuns pentru a putea transmite informatia mai departe catre stratul de iesire
    # vom returna iesire_strat_iesire pentru a obtine predictiile retelei
    return iesire_strat_ascuns, iesire_strat_iesire
