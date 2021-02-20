# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:38:27 2020

@author: tho2303
"""
import requests
import numpy as np
import pandas as pd
import dataframe_image as dfi #lager tabell direkte fra en pd.dataframe

#%% henter csv-fil fra BK-app
body = {
    'email':'',
    'password':''
}

response = requests.post('https://app.buldrekontoret.com/api/login', json=body)
requestCookies = {'connect.sid': response.cookies['connect.sid']}
data = requests.get('https://app.buldrekontoret.com/api/admin/reservations.csv', cookies=requestCookies)
#%% ordner opp i datastrengen og samler den i array M
string=data.text.replace('\r\n',',') 
list= string.split(",")

M=np.zeros(int((len(list)/3)),dtype=object)

for i in range(0,len(M)):        
    M[i]=list[i*3]+list[i*3+1]+list[i*3+2]

 #M Inneholder like mange elementer som i csv-fil  
#%% Deler opp sortert liste i ny array T
T=[None]*(len(M))

for i in range (0,len(T)):
    tekst=M[i]
    T[i]=tekst[48:48+20]

T.sort()  
uni=np.unique(T) 

T=T+['tom']  
#%%
K=[None]*int(len(uni)) #Oppretter tom liste

for i in range(0,len(K)):
    it=0  
    test=True
    while test:
        if T[it]==T[it+1]:
            it+=1
        else:
            test=False
        K[i]=str("%02d" % (it+1))+';'+T[0] 
    for i in range(0,it+1):
        T.pop(0)      

K.sort(reverse=True)  
#%% Finner ut hvor mange i k som har mindre enn halvparten av maksøkt. 
maks=int(K[0][0:2])  
grense=int(np.floor(maks/3))
antall=0
for i in range (0,len(K)):
    if int(K[i][0:2])>=grense:
        antall+=1
print(antall)
#%%
arr=np.zeros([antall,2],dtype=object)

for i in range (0,antall):
    tekst=K[i]
    arr[i,0]=tekst[0:2]
    arr[i,1]=tekst[3:20]
      
#%% Oppretter panda dataframe fra T
data = pd.DataFrame(arr)
data.rename(columns={0: 'Antall økter', 1: 'Navn'}, inplace=True)
print(data)
#%% eksport til png-tabell
df_styled = data.style.background_gradient() 
dfi.export(df_styled,"Ivrigste klatrer.png")