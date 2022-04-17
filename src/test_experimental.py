# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 08:51:04 2021

@author: User
"""

# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from urllib.request import urlopen

from sklearn.model_selection import train_test_split


import core_helper.helper_general as hg
#import src.Prj_Core.core_helper.helper_general as hg
hg.set_base_path()


#import core_helper.helper_acces_db as hadb
import src.Prj_Core.core_helper.helper_acces_db as hadb

import src.Prj_Core.core_helper.helper_feature_selection as hfs

#import core_helper.helper_transformers as ht
import src.Prj_Core.core_helper.helper_transformers as ht

import src.Prj_Core.core_helper.helper_clean as hc
import src.Prj_Core.core_helper.helper_classification_model as hcm

import src.Prj_Core.core_helper.helper_dataframe as hd
import src.Prj_Core.core_helper.helper_siagie_kpi as hsk
import src.Prj_Core.core_helper.helper_terceros_kpi as htk

from sklearn.metrics import classification_report,average_precision_score
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats 
from sklearn.preprocessing import RobustScaler

def get_df_procesado_temp(anio,col_name_y,key_grupo_grados, grupo_grados,macro_region, 
                     feature_selection=False,df_id_persona=None,anio_serv=None):
    
    
    dtypes_columns = {'COD_MOD': str,
                      'ANEXO':int,                    
                      'COD_MOD_T_MENOS_N':str,
                      'ANEXO_T_MENOS_N':int,                      
                      'UBIGEO_NACIMIENTO_RENIEC':str,
                      'N_DOC':str,
                      'ID_GRADO':int,
                      'ID_PERSONA':int,#nurvo
                      'CODIGO_ESTUDIANTE':str,
                      'NUMERO_DOCUMENTO':str,
                      'NUMERO_DOCUMENTO_APOD':str,
                      'CODOOII':str
                      }   


    
    df_servicios = hadb.get_df_servicios(macro_region=macro_region,anio=anio_serv)    

    list_pd = []
    #5,6,7,8
    for ID_GRADO in grupo_grados:
        url = hg.get_base_path()+"\\src\\Prj_Interrupcion_Estudios\\Prj_Desercion\\_02_Preparacion_Datos\\_02_Estructura_Base\\_data_\\nominal\\estructura_base_EBR_{}_{}_delta_1_temp.csv"
        url = url.format(ID_GRADO,anio)
        df =pd.read_csv(url, dtype=dtypes_columns ,encoding="utf-8")
        df['STR_ID_GRADO'] = "GRADO_" + str(ID_GRADO)      
        df = pd.merge(df,df_servicios, left_on=["COD_MOD","ANEXO"], right_on = ["COD_MOD","ANEXO"] ,how="inner")
        if df_id_persona is not None:
            df = pd.merge(df,df_id_persona[["ID_PERSONA"]], left_on="ID_PERSONA", right_on = "ID_PERSONA",how="inner")        
        list_pd.append(df)
        
    df_reg = pd.concat(list_pd)
    print("df_reg.shape", df_reg.shape)
    anio_notas = anio-1   
    
    ''' 
    cls_json = {}
    cls_json['SITUACION_FINAL']=["APROBADO","DESAPROBADO"]
    cls_json['SF_RECUPERACION']=["APROBADO","DESAPROBADO"]
    cls_json['SITUACION_MATRICULA']=["PROMOVIDO","REPITE","INGRESANTE","REENTRANTE"]
    cls_json['JUNTOS']="dummy"
    
    df_reg = hsk.generar_kpis_historicos(df_reg,anio_df=anio,anio_h=anio-2,cls_json=cls_json,t_anios=4)      
    df_reg = hsk.agregar_notas(df_reg,anio,anio_notas, cls_group=["ZSCORE"])    
    df_reg = htk.agregar_sisfoh(df_reg)       
    df_reg = hsk.generar_kpis_desercion(df_reg,anio_df=anio, anio_h=anio-2 ,t_anios=4)  
      
    df_reg =  htk.agregar_shock_economico(df_reg,anio=anio)  
    
    df_reg = hsk.generar_kpis_traslado(df_reg,anio_df=anio,anio_h=anio-1,t_anios=5)
    df_reg = hsk.generar_kpis_traslado_a_publico(df_reg,anio_df=anio,anio_h=anio-1,t_anios=5)
    '''
    if key_grupo_grados=="6 prim":
        df_reg = hsk.agregar_distancia_prim_sec(df_reg)
        df_reg = hc.fill_nan_with_nan_category_in_cls(df_reg , ["GRUPO_DISTANCIA"])
    
    
    
    df_reg = hc.fill_nan_with_nan_category_in_cls(df_reg , ["SITUACION_MATRICULA_T_MENOS_N",
                                                            "SF_RECUPERACION_T_MENOS_N",
                                                            "PARENTESCO","DSC_DISCAPACIDAD",
                                                            "SEXO_APOD", "SITUACION_FINAL_T_MENOS_N",                                                        
                                                            "SITUACION_MATRICULA_T",
                                                            "TIENE_CERTIFICADO_DISCAPACIDAD",
                                                            "PADRE_VIVE","MADRE_VIVE"])
    
    df_reg = hc.trim_category_cls(df_reg)
    
    df_reg = hsk.formatear_columnas_siaguie(df_reg)
    
   
    
    #df_reg['EDAD_EN_DIAS_T']  = df_reg['EDAD_EN_DIAS_T'].round()
   
   
    columns_too_much_nan_and_categories = ["JUSTIFICACION_RETIRO_T_MENOS_N","DSC_PAIS","DSC_LENGUA"]
    columns_to_drop  = ['ID_PERSONA','COD_MOD','ANEXO','COD_MOD_T_MENOS_N','ANEXO_T_MENOS_N','ID_GRADO_T_MENOS_N',
                        'NUMERO_DOCUMENTO_APOD','N_DOC','NIVEL_INSTRUCCION_APOD'] 
    #cat_muy_largas = ['D_REGION']
    
    columns_to_drop_all = columns_too_much_nan_and_categories+columns_to_drop 
    
    ID_P_T = df_reg['ID_PERSONA']
    
    if col_name_y is not None:
        y = df_reg[col_name_y]
        columns_to_drop_all.append(col_name_y)
    else:    
        y = None
        
        
    X = df_reg.drop(columns = columns_to_drop_all) 

    ct = ht.CatTransformer(pp = "lb",console=True) #lb le
    ct.fit(X)
    X_t = ct.transform(X)
    #print(X_t.columns)
    if feature_selection:
        X_t = hfs.drop_cls_unique_value(X_t)
        X_t = hfs.drop_corr_columns(X_t)
        X_t = hfs.drop_nan_columns(X_t)
    
    return ID_P_T, X_t , y
