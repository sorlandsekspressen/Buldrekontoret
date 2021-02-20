# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:01:41 2021

@author: tho2303
"""
import requests
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
# import dataframe_image as dfi #Ikke i bruk her

plotwish='month'  #day, month eller dayplot 
glatting=True       #glatting hvis plotwish==dayplot

#%% henter csv-fil fra BK-app
body = {
    'email':'',
    'password':''
}

response = requests.post('https://app.buldrekontoret.com/api/login', json=body)
requestCookies = {'connect.sid': response.cookies['connect.sid']}
data = requests.get('https://app.buldrekontoret.com/api/admin/reservations.csv', cookies=requestCookies)
#%% ordner opp i datastrengen og samler den i array M klar for sortering
string=data.text.replace('\r\n',',') 
list= string.split(",")

M=np.zeros(int((len(list)/3)),dtype=object)

for i in range(0,len(M)):        
    M[i]=list[i*3][2:10]  # Henter kun ut hvert 3. element(YMD bokstav 2-10) fra list og legger i M
  
M_s=np.sort(M)     #sorterer M 
#%% Lager arrayer med dato, dag , uke og år fra M ved å bruke datetime

dagtall=np.zeros((len(M)), dtype=int)     #utkommenterte arrayer trengs ikke foreløpig
ukedag=np.zeros((len(M)),dtype=object)
# maanedtall=np.zeros((len(M)), dtype=int)
maanednavn=np.zeros((len(M)), dtype=object)
aar=np.zeros((len(M)), dtype=int)

for i in range (0,len(M)):    
    t=datetime.strptime(M_s[i], '%y-%m-%d')   #oppretter et datetimeobjekt fra streng i M_s[i]
    
    dagtall[i]=t.strftime("%j") #dag i året (001-366)
    ukedag[i]=t.strftime("%A") #ukedag
    # maanedtall[i]=t.strftime("%m") #måned tall
    maanednavn[i]=t.strftime("%B") #måned navn
    aar[i]=t.strftime("%Y") #årstall
   
#%% plotfunk dager

if plotwish=='day':
    
    mandag=np.count_nonzero(ukedag=='Monday') #tell hvor mange ganger 'monday' finnes i ukedag
    tirsdag=np.count_nonzero(ukedag=='Tuesday')
    onsdag=np.count_nonzero(ukedag=='Wednesday')
    torsdag=np.count_nonzero(ukedag=='Thursday')
    fredag=np.count_nonzero(ukedag=='Friday')
    lørdag=np.count_nonzero(ukedag=='Saturday')
    søndag=np.count_nonzero(ukedag=='Sunday')

    sizes= [mandag, tirsdag, onsdag, torsdag, fredag, lørdag, søndag]
    tag=['Man', 'Tir', 'Ons', 'Tor', 'Fre', 'Lør', 'Søn']

    plt.figure(1)
    plt.bar(tag,sizes, width=0.6) 
    plt.title('Bookinger fordelt på ukedag')
    plt.savefig('Aktivitet ukedag.jpg')
#%% plotfunk månedsoversikt    
elif plotwish=='month':
    
    jan=np.count_nonzero(maanednavn=='January') #tell hvor mange ganger 'monday' finnes i ukedag
    feb=np.count_nonzero(maanednavn=='February')
    mar=np.count_nonzero(maanednavn=='March')
    apr=np.count_nonzero(maanednavn=='April')
    mai=np.count_nonzero(maanednavn=='Mai')
    jun=np.count_nonzero(maanednavn=='June')
    jul=np.count_nonzero(maanednavn=='july')
    aug=np.count_nonzero(maanednavn=='August')
    sept=np.count_nonzero(maanednavn=='September')
    okt=np.count_nonzero(maanednavn=='October')
    nov=np.count_nonzero(maanednavn=='November')
    dec=np.count_nonzero(maanednavn=='December')

    sizes= [dec,jan,feb,mar,apr,mai,jun,jul, aug, sept, okt, nov]
    tag=['Des', 'Jan', 'Feb', 'Mar', 'Apr','mai', 'Jun', 'Jul', 'Aug','Sep','Okt','Nov']

    plt.figure(1)
    plt.bar(tag,sizes, width=0.6)  
    plt.title('Bookinger fordelt på måned')
    plt.savefig('Aktivitet månedlig.jpg')
#%% plotfunk dager i året
elif plotwish=='dayplot':
    n=np.linspace(1,366,366)
    # N=np.zeros(len(uni))
    N= np.empty(len(n),)  #Oppretter tom array
    N[:] = np.nan  #fyller N med NaN
    
    
    i=0
    for x in n:
        N[i]=np.count_nonzero(dagtall==x) #teller opp frekvensen i array dagtall til hver av dagtallene i uni
        i+=1                              
    
    if glatting:
        for i in range (1,len(N)-2):   #   Glatting av N
            if N[i]!='nan':
                N[i]=(N[i-1]+N[i]+N[i+1]+N[i+2])/4
    
    plt.figure(1)
    plt.plot(n,N,'r-')  #plotter uni mot frekvensen av hver av dem.
    plt.ylabel('Besøk')
    plt.xlabel('Dag i året')
    if glatting:
        plt.title('Glattet kurve over antall besøkende per dag i året')
    else:
        plt.title('Antall besøk per dag i året')
    plt.savefig('Aktivitet per dag i året.jpg')
    
