#-----------------------------------------------------------------------------
# 1. Citirea datelor din fișier și împărțirea setului de date
# în date de antrenare și testare, aleatoriu
#------------------------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

#pentru a folosi OneHotEncoder -> pip install scikit-learn !!!

# avem nevoie de date in format numeric
date = pd.read_excel("Data_cat_numerice.xlsx")

# print(date)

# elimin coloana PLUS // aici mentionase doamna sa folosim ceva special
# pentru a transforma plus in numeric
date = date.drop(date.columns[28], axis=1)

# încercăm să prezicem coloana cu rasa, restul sunt caracteristicile specifice
X = date.iloc[:, [col for col in range(date.shape[1]) if col != 4]].values
y = date.iloc[:, 4].values  

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
#15 clase diferite = 15 tipuri de rase = corect

# parametrii pentru antrenare
rata_invatare = 0.01
numar_maxim_epoci = 1000
# "epoci" = de câte ori modelul parcurge întregul set de date de antrenare

# inițializarea ponderilor și bias-urilor
np.random.seed(42)
ponderi_intrare_ascuns = np.random.rand(dimensiune_intrare, dimensiune_strat_ascuns) - 0.5 #intre 0 si 1
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

# definim functia pentru OneHotEncoding

def oneHotEncoder(y):
    # transformam y intr o matrice de 2 dimensiuni

    y = np.array(y).reshape(-1, 1)  # Transformă y în format bidimensional

    # aplicam one hot encoder pe y(matricea de 2 dimensiuni)

    enc = OneHotEncoder(sparse_output=False)  # Setează sparse=False pentru a obține array dens
    y_enc = enc.fit_transform(y)
    return y_enc

    # construim noul dataframe folosind coloanele obtinute mai sus

    enc_dataframe = pd.DataFrame(y_enc.toarray(), columns=enc.categories_[0])

    return enc_dataframe

z = oneHotEncoder(y)

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

    # calculam predictiile
    # ele reprezinta clasa cu probabilitatea maxima
    
    # vom returna iesire_strat_ascuns pentru a putea transmite informatia mai departe catre stratul de iesire
    # vom returna iesire_strat_iesire pentru a obtine predictiile retelei

    return iesire_strat_ascuns, iesire_strat_iesire

iesire_strat_ascuns, iesire_strat_iesire = propagare_inainte(X, ponderi_intrare_ascuns, ponderi_ascuns_iesire, bias_ascuns,bias_iesire)

#-------------------------------------------------------------------------------
# 5. Propagarea înapoi: actualizarea ponderilor și biasurilor
#-------------------------------------------------------------------------------

def propagare_inapoi(X, z, iesire_strat_ascuns, iesire_strat_iesire, 
                     ponderi_intrare_strat_ascuns, ponderi_iesire_strat_ascuns, 
                     bias_strat_ascuns, bias_strat_iesire, rata_invatare):
    
    # se calculeaza erorile pentru stratul de iesire
    # ele reprezinta diferenta dintre valorile reale si predictiile obtinute de retea

    eroare_strat_iesire = iesire_strat_iesire - z
    gradient_strat_iesire = eroare_strat_iesire * derivata_sigmoid(iesire_strat_iesire)
    
    # aici actualizam ponderile si bias-urile pentru stratul de iesire
    # gradientul este derivata functiei de eroare fata de ponderi sau bias-uri si ne indica 
    # directia in care vom ajusta ponderile si bias-urile pentru a obtine o eroare mai mica
    # ponderile reprezinta produsul dintre activarile stratului anterior si erorile stratului curent
    # rata de invatare are rol de a controla procesul ajustarii pentru a nu destabiliza antrenarea
    # bias-urile sunt erorile stratului curent, combinand contributiile din toate instantele

    delta_ponderi_strat_ascuns_iesire = np.dot(iesire_strat_ascuns.T, gradient_strat_iesire)
    delta_bias_strat_iesire = np.sum(gradient_strat_iesire, axis=0)
    ponderi_iesire_strat_ascuns -= rata_invatare * delta_ponderi_strat_ascuns_iesire
    bias_strat_iesire -= rata_invatare * delta_bias_strat_iesire
    
    # se calculeaza erorile pentru stratul ascuns
    # calculul se realizeaza propagand inapoi eroarea din stratul de iesire

    eroare_strat_ascuns = np.dot(gradient_strat_iesire, ponderi_iesire_strat_ascuns.T)
    gradient_strat_ascuns = eroare_strat_ascuns * derivata_sigmoid(iesire_strat_ascuns)
    
    # aici actualizam ponderile si bias-urile pentru stratul ascuns
    # idem ca la stratul de iesire

    delta_ponderi_intrare_strat_ascuns = np.dot(X.T, gradient_strat_ascuns)
    delta_bias_strat_ascuns = np.sum(gradient_strat_ascuns, axis=0)
    ponderi_intrare_strat_ascuns -= rata_invatare * delta_ponderi_intrare_strat_ascuns
    bias_strat_ascuns -= rata_invatare * delta_bias_strat_ascuns
    
    # returnam noile ponderi si noile bias-uri

    return ponderi_intrare_strat_ascuns, ponderi_iesire_strat_ascuns, bias_strat_ascuns, bias_strat_iesire

# propagare_inapoi(X, z, iesire_strat_ascuns, iesire_strat_iesire, ponderi_intrare_ascuns, ponderi_ascuns_iesire, bias_ascuns, bias_iesire, rata_invatare)


#-------------------------------------------------------------------------------
# 6. Antrenarea rețelei neuronale pentru un număr de epoci 
# execută propagare înainte pentru întregul set de antrenare.
# Calculează eroarea și reține-o pentru vizualizare.
# Execută propagare înapoi pentru a actualiza ponderile.
# Repetă pentru numărul maxim de epoci.
#-------------------------------------------------------------------------------

# Separarea datelor în antrenare și testare
from sklearn.model_selection import train_test_split

X_antrenare, X_testare, y_antrenare, y_testare = train_test_split(X, y, test_size=0.2, random_state=42)

# Aplică One-Hot Encoding pentru y_antrenare și y_testare
y_antrenare = oneHotEncoder(y_antrenare)
y_testare = oneHotEncoder(y_testare)


eroare_pe_epoca = []  # pentru a înregistra eroarea pe fiecare epocă

for epoca in range(numar_maxim_epoci):
    # Propagare înainte
    iesire_ascuns, iesire_finala = propagare_inainte(
        X_antrenare, ponderi_intrare_ascuns, ponderi_ascuns_iesire, bias_ascuns, bias_iesire
    )
    
    # Calculul erorii pentru setul de antrenare
    eroare = functie_eroare(y_antrenare, iesire_finala)
    eroare_pe_epoca.append(eroare)
    
    # Propagare înapoi și actualizarea parametrilor
    ponderi_intrare_ascuns, ponderi_ascuns_iesire, bias_ascuns, bias_iesire = propagare_inapoi(
        X_antrenare, y_antrenare, iesire_ascuns, iesire_finala, 
        ponderi_intrare_ascuns, ponderi_ascuns_iesire, bias_ascuns, bias_iesire, rata_invatare
    )
    
    # Afișare progres
    if epoca % 100 == 0 or epoca == numar_maxim_epoci - 1:
        print(f"Epoca {epoca + 1}/{numar_maxim_epoci}, Eroare: {eroare:.4f}")

#-------------------------------------------------------------------------------
# 7. Predicția pe setul de date de testare și afișarea metricilor de performanță
# Folosești modelul antrenat pentru a face predicții pe setul de testare:
# Aplici propagarea înainte pe setul de testare.
# Compari predicțiile cu etichetele reale.
# Calculezi acuratețea (sau alte metrici, ex.: precizie, recall, F1).
# Opțional, afișezi exemple clasificate greșit.
#-------------------------------------------------------------------------------
# Calculul acurateței pe setul de antrenare
_, iesire_train = propagare_inainte(
    X_antrenare, ponderi_intrare_ascuns, ponderi_ascuns_iesire, bias_ascuns, bias_iesire
)

# Conversie ieșire în predicții (alegem clasa cu probabilitatea cea mai mare)
predictii_train = np.argmax(iesire_train, axis=1)  # indexul clasei prezise pentru antrenare
etichete_reale_train = np.argmax(y_antrenare, axis=1)  # indexul clasei reale pentru antrenare

# Calcularea acurateței pentru antrenare
acuratete_train = np.mean(predictii_train == etichete_reale_train) * 100
print(f"Acuratețea pe setul de antrenare: {acuratete_train:.2f}%")

# Calculul acurateței pe setul de testare
_, iesire_test = propagare_inainte(
    X_testare, ponderi_intrare_ascuns, ponderi_ascuns_iesire, bias_ascuns, bias_iesire
)

# Conversie ieșire în predicții (alegem clasa cu probabilitatea cea mai mare)
predictii_test = np.argmax(iesire_test, axis=1)  # indexul clasei prezise pentru testare
etichete_reale_test = np.argmax(y_testare, axis=1)  # indexul clasei reale pentru testare

# Calcularea acurateței pentru testare
acuratete_test = np.mean(predictii_test == etichete_reale_test) * 100
print(f"Acuratețea pe setul de testare: {acuratete_test:.2f}%")



print("Dimensiuni y_antrenare:", y_antrenare.shape)  # Trebuie să fie (număr_sample, număr_clase)
print("Dimensiuni iesire_finala:", iesire_finala.shape)  # Trebuie să fie la fel cu y_antrenare




#-------------------------------------------------------------------------------
# Opțional: Graficul erorii pe epoci pentru a vizualiza progresul antrenării
#-------------------------------------------------------------------------------
import matplotlib.pyplot as plt

plt.plot(range(numar_maxim_epoci), eroare_pe_epoca, label='Eroare')
plt.xlabel('Epoci')
plt.ylabel('Eroare')
plt.title('Progresul antrenării')
plt.legend()
plt.show()