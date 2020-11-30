import csv
import numpy as np
import matplotlib.pyplot as plt

#Instalacja modulow w systemie
# pip install numpy
# pip install matplotlib

przeplyw = []
temp_zas = []
temp_pow = []
rozn_temp = []
moc = []

plik = open('dane.csv', 'rt')
dane = csv.reader(plik, delimiter=',')

next(dane)

for obserwacja in dane:
    przeplyw.append(float(obserwacja[6]))
    temp_zas.append(float(obserwacja[7]))
    temp_pow.append(float(obserwacja[8]))
    rozn_temp.append(float(obserwacja[9]))
    moc.append(float(obserwacja[12]))

plik.close()

zmienne = {"Temperatura zasilania":temp_zas,
            "Temperatura powrotu":temp_pow,
            "Roznica tamperatur":rozn_temp,
            "Przeplyw":przeplyw,
            "Moc":moc
            }

for nazwa, zmienna in zmienne.items():
    print("Zmienna:", nazwa)
    print("MIN:", min(zmienna))
    print("MAX:", max(zmienna))
    print("Srednia:", np.mean(zmienna))
    print("Mediana:", np.median(zmienna))
    print("Zakres:", np.ptp(zmienna))
    print("ODCH. STD.:", np.std(zmienna))
    print("Wariacja:", np.var(zmienna))
    print("Histogram:", np.histogram(zmienna))
    print()
    '''
    plt.hist(zmienna, 100)
    plt.show()
    '''


zmienne_do_naprawienia = {"Roznica tamperatur":rozn_temp,
                            "Przeplyw":przeplyw,
                            "Moc":moc
                            }

for nazwa, zminena in zmienne_do_naprawienia.items():
    for i,wartosc in enumerate(zmienna):
        if wartosc>10000:
            zmienna[i] = np.median(zmienna)
            print("Wykryto anomalie dla zmiennej {} pod indeksem {}".format(nazwa, i))



def korel_unorm(a,b):
    #Funkcja zwraca unormowano korelacje liszt a i b
    a = (a - np.mean(a)) / (np.std(a)*len(a))
    b = (b - np.mean(b)) / np.std(b)
    return np.correlate(a,b)


'''
a = [0, 1, 3, 1, 4, 0, 50, 0]
b = [1, 3, 10, 9, 8, 6, 20, 100]

print(np.correlate(a,b))
print(korel_unorm(a,b))
'''

for nazwa1, zmienna1 in zmienne.items():
    for nazwa2, zmienna2 in zmienne.items():
        print("Korelacja miedzy {}, a {} wynosi {}".format(nazwa1, nazwa2, korel_unorm(zmienna1, zmienna2)))

plt.plot(range(len(moc)), moc, "x")
plt.plot(range(len(przeplyw)), przeplyw, "+")
plt.ylim(top = 1600)
plt.ylim(bottom = -77)
plt.show()


plt.plot(range(len(moc[1000:1100])), [i*10 for i in moc[1000:1100]])
plt.plot(range(len(przeplyw[1000:1100])), przeplyw[1000:1100])
plt.show()

plt.plot(rozn_temp, temp_pow, ".")
plt.xlabel("Roznica temperatur")
plt.ylabel("Temperatura powrotu")
plt.show()

plt.plot(moc, przeplyw, ".")
plt.xlabel("Moc")
plt.ylabel("przeplyw")
plt.show()

a,b = np.polyfit(moc, przeplyw, 1)
yreg = [a*i + b for i in moc]
plt.plot(moc, przeplyw, '.')
plt.plot(moc, yreg)
plt.show()


a,b = np.polyfit(range(len(temp_zas)), temp_zas, 1)
print("Wzro prostej: y =",a,"* x +",b)
yreg=[a*i + b for i in range(len(temp_zas))]
plt.plot(range(len(temp_zas)), temp_zas)
plt.plot(range(len(temp_zas)), yreg)
plt.show()
