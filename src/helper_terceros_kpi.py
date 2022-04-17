# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 00:36:06 2021

@author: User
"""
import pandas as pd
import numpy as np
#import core_helper.helper_acces_db as hadb
import  core_helper.helper_acces_db as hadb

import core_helper.helper_clean as hc
import core_helper.helper_general as hg
import core_helper.helper_output as ho




def agregar_Censo_Educativo(df,df_ce=None,anio=2019, cache=False ):    
    
    ho.print_message('agregar_Censo_Educativo')
    if df_ce is None:
        df_ce = hadb.get_Censo_Educativo(anio=anio,cache=cache) 
    
    if 'COD_MOD' not in df.columns:
        msg = "ERROR: No existe la columnna COD_MOD en el DF proporcionado"
        raise Exception(msg)
        
    if 'ANEXO' not in df.columns:
        msg = "ERROR: No existe la columnna ANEXO en el DF proporcionado"
        raise Exception(msg)
        
    ho.print_items(df_ce.columns,excepto=['COD_MOD',"ANEXO"])
    
    if df is None:
        return 
    else:   
        df = pd.merge(df, df_ce, left_on=['COD_MOD',"ANEXO"], right_on=['COD_MOD',"ANEXO"],  how='left')    
        return df


def agregar_ECE(df,df_ece=None,anio=2019, cache=False ):    
    
    ho.print_message('agregar_ECE')
    if df_ece is None:
        df_ece = hadb.get_ECE(anio=anio,cache=cache) 
    
    if 'COD_MOD' not in df.columns:
        msg = "ERROR: No existe la columnna COD_MOD en el DF proporcionado"
        raise Exception(msg)
        
    ho.print_items(df_ece.columns,excepto=['COD_MOD',"ANEXO"])   
    
    if df is None:
        return 
    else:   
        df = pd.merge(df, df_ece, left_on=['COD_MOD',"ANEXO"], right_on=['COD_MOD',"ANEXO"],  how='left')
        return df


def agregar_nexus(df,df_nexus=None,anio=2020, cache=False ):    
    
    ho.print_message('agregar_nexus')
    if df_nexus is None:
        df_nexus = hadb.get_nexus(anio=anio,cache=cache) 
    
    if 'COD_MOD' not in df.columns:
        msg = "ERROR: No existe la columnna COD_MOD en el DF proporcionado"
        raise Exception(msg)
        
    ho.print_items(df_nexus.columns,excepto=["COD_MOD"])
        
    if df is None:
        return 
    else:   
        df = pd.merge(df, df_nexus, left_on=["COD_MOD"], right_on=["COD_MOD"],  how='left')    
        return df

def agregar_sisfoh(df,df_sisfoh=None, cache=False ):    
    
    ho.print_message('agregar_sisfoh')
    if cache:
        print("la cache para agregar_sisfoh no es necesario")
    if df_sisfoh is None:
        df_sisfoh = hadb.get_sisfoh()  
    
    if 'NUMERO_DOCUMENTO_APOD' not in df.columns:
        msg = "ERROR: No existe la columnna NUMERO_DOCUMENTO_APOD en el DF proporcionado"
        raise Exception(msg)
        
    df['NUMERO_DOCUMENTO_APOD'] = df['NUMERO_DOCUMENTO_APOD'].str.replace('.0', '')
    df['NUMERO_DOCUMENTO_APOD'] = df['NUMERO_DOCUMENTO_APOD'].apply(lambda x: '{0:0>8}'.format(x))
    df['NUMERO_DOCUMENTO_APOD'] = df['NUMERO_DOCUMENTO_APOD'].str.replace('00000nan', '00000000')     
    
    ho.print_items(df_sisfoh.columns,excepto=["PERSONA_NRO_DOC"])
    
    if df is None:
        return 
    else:  
        df = pd.merge(df, df_sisfoh, left_on=["NUMERO_DOCUMENTO_APOD"], right_on=["PERSONA_NRO_DOC"],  how='left')   
        df = hc.fill_nan_with_nan_category_in_cls(df , ["SISFOH_CSE"])
        del df["PERSONA_NRO_DOC"]        
        return df

# solo disponible 2019 y 2021 , B0 y F0
def agregar_shock_economico(df,df_se=None,anio=None,modalidad="EBR", cache=False ):
    
    ho.print_message('agregar_shock_economico')
    if cache:
        print("la cache para agregar_shock_economico no es necesario")
    if df_se is None:
        df_se = hadb.get_shock_economico(anio,modalidad)
    
    #print("hola")
    ho.print_items(df_se.columns)

    if df is None:
        return 
    else:  
        df = pd.merge(df, df_se, left_on="ID_PERSONA", right_on="ID_PERSONA",  how='inner')
        return df

