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

    c = 0
    a = 1
    b = 2

    true=1
    false=0
    print('----DANE----')
    pot = [potential() for i in range(3)]

    pot[a].variables = numpy.array([a])
    table = numpy.zeros((2))
    table[true]=0.65
    table[false]=0.35
    pot[a].table=table

    for n in [true,false]:
        print('p(A =',n,')=',pot[a].table[n])

    pot[b].variables = numpy.array([b])
    table = numpy.zeros((2))
    table[true]=0.77
    table[false]=0.23
    pot[b].table=table

    for m in [true,false]:
        print('p(B =',m,')=',pot[b].table[m])

    pot[c].variables = numpy.array([a, b, c])
    table = numpy.zeros((2, 2, 2))
    table[true, false, false] = 0.1
    table[true, false, true] = 0.99
    table[true, true, false] = 0.8
    table[true, true, true] = 0.25
    pot[c].table = table
    pot[c].table[false][:][:] = 1 - pot[c].table[true][:][:]

    for x in[true,false]:
        for y in [true,false]:
            for z in [true,false]:
                print('p(C =',x,'| A =',y,',B =',x,')=',pot[c].table[x,y,z])



    #mnożenie prawdopodobnieństw w celu otrzymania prawdopodobieństwa łącznego
    #((a,b,c) = p(c|a,b) * p(a) * p(b))
    print('----OBLICZENIA----')
    multipot = potential()
    multipot.variables = numpy.array([a, b, c])
    table = numpy.zeros((2, 2, 2))
    table[true, false, false] = pot[c].table[true, false, false] * pot[a].table[false] * pot[b].table[false]
    table[true, false, true] = pot[c].table[true, false, true] * pot[a].table[false] * pot[b].table[true]
    table[true, true, false] = pot[c].table[true, true, false] * pot[a].table[true] * pot[b].table[false]
    table[true, true, true] = pot[c].table[true, true, true] * pot[a].table[true] *pot[b].table[true]
    table[false, false, false] = pot[c].table[false, false, false] * pot[a].table[false] * pot[b].table[false]
    table[false, false, true] = pot[c].table[false, false, true] * pot[a].table[false] * pot[b].table[true]
    table[false, true, false] = pot[c].table[false, true, false] * pot[a].table[true] * pot[b].table[false]
    table[false, true, true] = pot[c].table[false, true, true] * pot[a].table[true] * pot[b].table[true]
    multipot.table = table
    #print(multipot.table)

    suma_kontrolna_1=0
    for x in [true, false]:
        for y in [true, false]:
            for z in [true, false]:
                print('p(C =', x, ',A =', y, ',B =', x, ')=', multipot.table[x, y, z])
                suma_kontrolna_1=suma_kontrolna_1+multipot.table[x, y, z]

    #print('suma (kontrolna) prawdopodobienstwa łącznego=',suma_kontrolna_1)

    #p(A=1,C=0)
    suma1=0
    for i in [true,false]:
        suma1=suma1+(pot[c].table[false,true,i]*pot[a].table[true]*pot[b].table[i])
    print('p(A=1,C=0)=',suma1)

    #p(A=0,C=0)
    suma2=0
    for j in [true,false]:
        suma2=suma2+(pot[c].table[false,false,j]*pot[a].table[false]*pot[b].table[j])
    print('p(A=0,C=0)=',suma2)

    #p(A=1|C=0)
    licznik=suma1
    mianownik=suma1+suma2
    print('p(A=1|C=0)=',licznik/mianownik)
