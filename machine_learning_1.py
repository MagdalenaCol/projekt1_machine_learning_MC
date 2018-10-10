import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def odleglosc_do_kwadratu(a, b, dim=2):
    rob = [(a[i] - b[i]) ** 2 for i in range(dim)]
    return sum(rob)

def losuj_punkty_pomiarowe(N):
    losuj = []
    for i in range(0, N):
        losuj.append(numpy.random.rand() * numpy.pi * 2)
    katy = sorted(losuj)
    x = numpy.array([numpy.sin(katy[i]) for i in range(N)])
    y = numpy.array([numpy.cos(katy[i]) for i in range(N)])
    punkty_pomiarowe = []
    for i in range(0, N):
        rob = [x[i], y[i]]
        punkty_pomiarowe.append(rob)
    return punkty_pomiarowe

def losuj_punkt_eksplozji():
    ex = 2
    ey = 2
    odleglosc_e = odleglosc_do_kwadratu([ex, ey], [0, 0])
    while (odleglosc_e > 1):
        ex = numpy.random.rand()
        ey = numpy.random.rand()
        if (numpy.random.rand() < 0.5):
            ex = -ex
        if (numpy.random.rand() < 0.5):
            ey = -ey
        odleglosc_e = odleglosc_do_kwadratu([ex, ey], [0, 0])
    e = [ex, ey]
    return e

def obserwacje(punkty, e, N, sigma2):
    d2 = [odleglosc_do_kwadratu(punkty[i], e) for i in range(N)]
    obserwacja = [1 / (d2[i] + 0.1) for i in range(N)]
    zaburzenie = [obserwacja[i] + numpy.random.normal(0, sigma2) for i in range(N)]
    return zaburzenie


def prawdopodobna_odleglosc(odczyty):
    prawd_odleglosci = []
    for i in range(0, N):
        prawd_odleglosci.append(numpy.sqrt((1 / odczyty[i]) - 0.1))
    return prawd_odleglosci

def reverse_colourmap(cmap, name = 'my_cmap_r'): #funkcja do odwrocenia kolorów na heatmapie
    reverse = []
    k = []
    for key in cmap._segmentdata:
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []
        for t in channel:
            data.append((1-t[0],t[2],t[1]))
        reverse.append(sorted(data))
    LinearL = dict(zip(k,reverse))
    my_cmap_r = matplotlib.colors.LinearSegmentedColormap(name, LinearL)
    return my_cmap_r

if __name__ == '__main__':

    #PRZYGOTOWANIE DANYCH
    wspolrzedne_pomiarowe_x = []
    wspolrzedne_pomiarowe_y = []
    ilosc_punktow_pomiarowych = 10 #ile bedzie losowych punktow pomiarowych
    krok_siatki = 0.01 #jak bardzo 'gesto' bedzie podzielona koncowa heatmapa
    vmax = 3 #jaka roznica miedzy koncowymi wynikami jest istotna przy wyswiatlaniu koncowej heatmapy
    N = ilosc_punktow_pomiarowych
    e = losuj_punkt_eksplozji()
    punkty_pomiaru = losuj_punkty_pomiarowe(ilosc_punktow_pomiarowych)
    sigma2 = 0.1
    pomiar = obserwacje(punkty_pomiaru, e, ilosc_punktow_pomiarowych, sigma2)


    #OBLICZENIA DO METODY ODLEGLOSCIOWEJ
    obliczone_odleglosci = prawdopodobna_odleglosc(pomiar)

    #UMIESZCZENIE DANYCH W PLIKU TEKSTOWYM
    nazwa_pliku='pomiar eksplozji.txt'
    plik_z_danymi = open(nazwa_pliku, 'w')
    print('dane do interferencji zapisano w pliku tekstowym:',nazwa_pliku,'\n')
    for i in range(0, ilosc_punktow_pomiarowych):
        linia = '\tpunkt:\t' + str(punkty_pomiaru[i]) + '\t pomiar:\t ' + str(pomiar[i]) +'\n'
        #print(linia)
        plik_z_danymi.write(linia)
    plik_z_danymi.close()

    #UTWORZENIE TABLICY STANOW
    ilosc_stanow=0
    xx=-1
    yy=-1
    tablica_stanow=[]
    while(xx<=1):
        yy=-1
        while(yy<1):
            tablica_stanow.append([round(xx,2),round(yy,4)])
            yy=round(yy,2)+krok_siatki
            ilosc_stanow=ilosc_stanow+1
        tablica_stanow.append([round(xx,2),round(yy,4)])
        xx=round(xx,2)+krok_siatki
        ilosc_stanow=ilosc_stanow+1
    print('wartosc kroku na siatce:',krok_siatki)


    #OBLICZENIE WARTOSCI PRZYPUSZCZANYCH DLA KAZDEGO STANU
    pomiar_przypuszczalnych_wartosci=[]
    sigma2 = 0.1
    for i in range(ilosc_stanow):
        pomiar_przypuszczalnych_wartosci.append(obserwacje(punkty_pomiaru, tablica_stanow[i], ilosc_punktow_pomiarowych, sigma2))
    #print(pomiar_przypuszczalnych_wartosci)
    #print(pomiar)

    #POROWNYWANIE WARTOSCI RZECZYWISTYCH ODCZYTU Z WLICZONYMI DLA KAZDEGO KROKU SIATKI
    tab_score=[]
    min_score=[]
    max_score=10000
    for i in range(0,len(pomiar_przypuszczalnych_wartosci)):
        score=0
        for j in range(0,ilosc_punktow_pomiarowych):
           score=score+(numpy.fabs(pomiar[j]-pomiar_przypuszczalnych_wartosci[i][j])) #wartosc bezwzgledna dla roznicy w pomiarach
        tab_score.append(score)
        if score<max_score:
            min_score=[]
            min_score.append(score)
            min_score.append(i)
            max_score=score

    #WYSWIETLANIE INFORMACJI KONCOWYCH
    print('ilosc wszystkich stanow:',len(tablica_stanow))
    przewidziane_miejsce=tablica_stanow[min_score[1]]
    print('najlepszy wynik=', min_score[0])
    print('przewidziano że wybuch znajduje się w punkcie:',przewidziane_miejsce)
    print('faktyczne miejsce eksplozji:',e)

    # ZAMIANA KONCOWYCH WYNIKOW NA TABLICE 2 WYMIAROWA
    pierwiastek = int(numpy.sqrt(len(tab_score)))
    #print('tablica wynikow:',tab_score)
    print('ilosc stanow w osi x i y:', pierwiastek)
    b = []
    i = 0
    for j in range(0, pierwiastek):
        b.append(tab_score[i:i + pierwiastek])
        i = i + pierwiastek
    #print(b) koncowe wyniki

    #RYSOWANIE METODA ODLEGLOSCI
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, aspect='equal')
    ax2.set_xlim((-1, 1))
    ax2.set_ylim((-1, 1))
    ax2.add_patch(patches.Circle((0, 0), 1, fill=True))
    for i in range(0,N):
        ax2.add_patch(patches.Circle((punkty_pomiaru[i]),obliczone_odleglosci[i],color='white' , fill=False))
    for i in range(0, ilosc_punktow_pomiarowych):
        tmp = punkty_pomiaru[i]
        wspolrzedne_pomiarowe_x.append(tmp[0])
        wspolrzedne_pomiarowe_y.append(tmp[1])
    plt.plot(wspolrzedne_pomiarowe_x, wspolrzedne_pomiarowe_y, 'ro')
    plt.plot(e[0], e[1], 'D', color='yellow', label='punkt eksplozji')
    #plt.legend()
    plt.title('Metoda odleglosci')
    plt.savefig('figura1.png')
    plt.show()

    #RYSOWANIE HEATMAPY
    px=przewidziane_miejsce[0]
    py=przewidziane_miejsce[1]
    cmap2 = matplotlib.cm.jet
    my_cmap_r = reverse_colourmap(cmap2)
    X, Y = numpy.mgrid[-1:1:complex(0, pierwiastek), -1:1:complex(0, pierwiastek)]
    fig3 = plt.figure()
    ax2 = fig3.add_subplot(111, aspect='equal')
    ax2.add_patch(patches.Circle((0, 0), 1, fill=False))
    plt1=plt.plot(e[0], e[1], 'D', color='yellow',label='punkt eksplozji')
    plt.plot(px,py, 'bo', color='green',label='obliczone miejsce eksplozji')
    plt.plot(wspolrzedne_pomiarowe_x, wspolrzedne_pomiarowe_y, 'ro',label='punkty pomiarowe')
    matplotlib.pyplot.pcolormesh(X,Y,b,cmap=my_cmap_r,vmin=numpy.min(tab_score),vmax=(numpy.min(tab_score)+vmax))
    plt.colorbar()
    #plt.legend(loc='best') #pokazanie legendy
    title1=str(przewidziane_miejsce)
    title2=str(e)
    plt.title('\nprzewidziane wspolrzedne:'+title1+'\n'+'rzeczywiste:'+title2)
    plt.savefig('figura2.png')
    plt.show()
