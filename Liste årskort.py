# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:38:27 2020

@author: tho2303
"""

import numpy as np
import pandas as pd
import dataframe_image as dfi #lager tabell direkte fra en pd.dataframe




#%%  henter meldemsliste fra csv lastet ned fra triplex og legger kundenavn i array ordre 
filepath='Ordreoversikt ny.csv'

ordre_pd=pd.read_csv(filepath,delimiter=';')
kundenavn=ordre_pd[['Nummer','Kundenavn']]

#%% eksport til png-tabell
df_styled = kundenavn.style.background_gradient() 
dfi.export(df_styled,"Liste årskort.png")

