import numpy


class variable:
    def __init__(self, name=[],domain=[]):
        self.name=name
        self.domain=domain

class potential:
    def __init__(self,variables=numpy.array([]),table=numpy.array([])):
        self.variables=variables
        self.table=table

if __name__=='__main__':

    rzeznik=2
    sprzataczka=1
    noz=0
    morderca=0
    niemorderca=1
    uzyty=0
    nieuzyty=1

    pot=[potential() for i in range(3)]

    pot[rzeznik].variables=numpy.array([rzeznik])
    table=numpy.zeros((2))
    table[morderca]=0.6
    table[niemorderca]=0.4
    pot[rzeznik].table=table


    pot[sprzataczka].variables=numpy.array([sprzataczka])
    table=numpy.zeros((2))
    table[morderca]=0.2
    table[niemorderca]=0.8
    pot[sprzataczka].table=table

    pot[noz].variables=numpy.array([noz,rzeznik,sprzataczka])
    table=numpy.zeros((2,2,2))
    table[uzyty,niemorderca,niemorderca]=0.3
    table[uzyty,niemorderca,morderca]=0.2
    table[uzyty,morderca,niemorderca]=0.6
    table[uzyty,morderca,morderca]=0.1
    pot[noz].table=table
    pot[noz].table[nieuzyty][:][:]=1-pot[noz].table[uzyty][:][:]

    #print("mnozymy utworzone potencjały,by dostać prawdopodobienstwo łączne")
    #print("\tp(rzeznik,sprzataczka, noz) = p(noz|rzeznik,sprzataczka) * p(rzeznik) * p(sprzataczka)")

    multipot=potential()
    multipot.variables=numpy.array([noz,rzeznik,sprzataczka])
    table=numpy.zeros((2,2,2))
    table[uzyty,niemorderca,niemorderca]=pot[noz].table[uzyty,niemorderca,niemorderca]*pot[rzeznik].table[niemorderca]*pot[sprzataczka].table[niemorderca]
    table[uzyty,niemorderca,morderca]=pot[noz].table[uzyty,niemorderca,morderca]*pot[rzeznik].table[niemorderca]*pot[sprzataczka].table[morderca]
    table[uzyty, morderca, niemorderca] = pot[noz].table[uzyty, morderca, niemorderca] * pot[rzeznik].table[morderca] * pot[sprzataczka].table[niemorderca]
    table[uzyty, morderca, morderca] = pot[noz].table[uzyty, morderca, morderca] * pot[rzeznik].table[morderca] * pot[sprzataczka].table[morderca]
    table[nieuzyty,niemorderca,niemorderca]=pot[noz].table[nieuzyty,niemorderca,niemorderca]*pot[rzeznik].table[niemorderca]*pot[sprzataczka].table[niemorderca]
    table[nieuzyty,niemorderca,morderca]=pot[noz].table[nieuzyty,niemorderca,morderca]*pot[rzeznik].table[niemorderca]*pot[sprzataczka].table[morderca]
    table[nieuzyty, morderca, niemorderca] = pot[noz].table[nieuzyty, morderca, niemorderca] * pot[rzeznik].table[morderca] * pot[sprzataczka].table[niemorderca]
    table[nieuzyty, morderca, morderca] = pot[noz].table[nieuzyty, morderca, morderca] * pot[rzeznik].table[morderca] * pot[sprzataczka].table[morderca]
    multipot.table=table

    """
    rzeznik=2 sprzataczka=1 
    noz=0
    morderca=0 niemorderca=1
    uzyty=0 nieuzyty=1
    """
    print('rzeznik nie morderca= ',pot[rzeznik].table[niemorderca])
    print('rzeznik morderca= ', pot[rzeznik].table[morderca])

    print('sprzataczka nie morderca= ',pot[sprzataczka].table[niemorderca])
    print('sprzataczka morderca= ', pot[sprzataczka].table[morderca])

    print('\t\t\tnóż \t\tsprzataczka\t\trzeznik')
    print('[0,0,0]=[\tużyty,\t\tmorderca,\t\tmorderca]=\t\t',multipot.table[0,0,0])
    print('[0,0,1]=[\tużyty,\t\tmorderca,\t\tnie morderca]=\t', multipot.table[0, 0, 1])
    print('[0,1,0]=[\tużyty,\t\tnie morderca,\tmorderca]=\t\t', multipot.table[0, 1, 0])
    print('[0,1,1]=[\tużyty,\t\tnie morderca,\tnie morderca]=\t', multipot.table[0, 1, 1])

    print('[1,0,0]=[\tnie użyty,\tmorderca,\t\tmorderca]=\t\t',multipot.table[1,0,0])
    print('[1,0,1]=[\tnie użyty,\tmorderca,\t\tnie morderca]=\t', multipot.table[1, 0, 1])
    print('[1,1,0]=[\tnie użyty,\tnie morderca,\tmorderca]=\t\t', multipot.table[1, 1, 0])
    print('[1,1,1]=[\tnie użyty,\tnie morderca,\tnie morderca]=\t', multipot.table[1, 1, 1])

    licznik=0
    for s in [morderca, niemorderca]:
        licznik=licznik+(pot[rzeznik].table[morderca]*(pot[noz].table[uzyty,morderca,s]* pot[sprzataczka].table[s]))
    #print(licznik)

    mianownik=0
    for s in [morderca,niemorderca]:
        for rz in [morderca,niemorderca]:
            mianownik=mianownik+(pot[noz].table[uzyty,rz,s]* pot[sprzataczka].table[s]*pot[rzeznik].table[rz])

    #print(mianownik)
    wynik=licznik/mianownik
    print('p(Rzeżnik=moderca|nóż=użyty)=',wynik)


