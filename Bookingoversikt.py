# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:38:27 2020

@author: tho2303
"""
import requests
import numpy as np
import pandas as pd
from decimal import*
import dataframe_image as dfi #lager tabell direkte fra en pd.dataframe

#%% Variabler
Maaned=2
Dato=22
namelength=20
timeshift=+1
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
    M[i]=list[i*3]+list[i*3+1]+list[i*3+2]
  
Ms=np.sort(M)     #sorterer M   

#%% finner antallet n som tilfredsstiller måned og dato
n=0
for i in range (0,len(M)):
    if int(Ms[i][5:7])==Maaned and int(Ms[i][8:10])==Dato:
        n+=1
#%% Deler opp sortert liste i ny array T
T=np.zeros([n,5],dtype=object)
N=0
for i in range (0,len(M)):
    getcontext().prec =4
    tekst=Ms[i]
    if int(tekst[5:7])==Maaned and int(tekst[8:10])==Dato:
        T[N,0]=int(tekst[5:7])
        T[N,1]=int(tekst[8:10])
        T[N,2]=Decimal(tekst[11:13]+'.'+tekst[14:16])+timeshift  
        T[N,3]=Decimal(tekst[35:37]+'.'+tekst[38:40])+timeshift
        T[N,4]=tekst[48:48+namelength]
        N+=1
    
#%% Oppretter panda dataframe fra T
data = pd.DataFrame(T)
data.rename(columns={0: 'Month', 1: 'Day',2: 'Start', 3: 'Stop', 4: 'Name'}, inplace=True)
print(data)
#%% eksport til png-tabell
df_styled = data.style.background_gradient() 
dfi.export(df_styled,"Bookingoversikt.png")
  
