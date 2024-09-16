import streamlit as st
import pandas as pd
#from openpyxl import load_workbook, Workbook
import os
import time

import gspread
from google.oauth2.service_account import Credentials

from io import BytesIO
#from PIL import Image
#import base64
import xlsxwriter

#from openpyxl import Workbook
#from openpyxl.drawing.image import Image

### funcion descarga de excel
def descargar_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
        #workbook =  writer.book
        #worksheet = writer.sheets['Sheet1']
        #worksheet.insert_image('N2', 'picture.png', {'foto': dataframe})
        #writer.save()  # No es necesario, pero se puede usar para asegurarse de que se escribe
        #wb = Workbook()
        #ws = wb.active
        #for index, row in dataframe.iterrows():
            #imagen = Image(BytesIO(row['miImage']))
            #ws.add_image(imagen,f'B{index + 2}')
    processed_data = output.getvalue()
    return processed_data

### función para convertir imagen a base64
#def convertir_imagen_a_base64(img):
    #buffered = BytesIO()
    #img.save(buffered, format="PNG")
    #buffered.seek(0)
    #base64.b64encode(buffered.getvalue()).decode()
    #return base64.b64encode(buffered.getvalue()).decode()


##### contrucción de la APP

def CargaDosis():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["Fecha de Receta","Campo",
                                                    "Lote","Hectáreas totales Lote/s",
                                                    "Tipo de Insumo","Insumo",
                                                    "Insumo para agregar a la lista",
                                                    "Unidad de Medida","Cantidad por Lote",
                                                    "Dosis por Hectárea",
                                                    "Persona Recetó","Observaciones", "Foto"])
    
        
    st.title(f"ANIBAL BARBERO")
    #st.checkbox(f"A")

    
    Campos = ["Gobbi", "San Miguel (Pascuet)", "Miloch","Pontel","Dandrea-Mores-Rossi-Capellari","Defassi","Ferrero"]  # Este será el input que determine la cantidad de tablas
    Lote = [1,2,3,4,5,6]

    Tipo_Insumos = ["Herbicida", "Insecticida","Fungicida_Inoculante","Fertilizante","Semilla"]
        
    Herbicida =["2,4 D 100xciento","2,4 D enlist colexx-d x20lts","2,4 D Advance ethex-ester hf ac 68xciento x20lts","ACEITE agricola",
                "ACETOCLOR harness (bidon x20lts)","ACETOCLOR guardian","ACEITE AGRÍCOLA (Nimbus)(bidon x20lts)","ACEITE METILADO (0,5)(soly-oil) x 20lts",
                "ADENGO","ALTEZA imazetapir 10xciento initios x 20lts","ATRAZINA LIQUIDA 50xciento","ATRAZINA 90xciento g90 (bolsa x 10kg)",
                "AUTORITHY sulfentrtazone x 5/10lts","BASAGRAN 60xciento","BENAZOLIN dasen (benazolini 50xciento) x 10lts","BREAK THRU MSO MAX dash msox 5lts",
                "BREAK THRU (trisiliconado) x 1 lts","BRODAL x 5lts","CADRE (imazapic 70xciento x 360grs)","CERILLO/DESECANTE x 5lts","COADYUVANTE rizospray extremos (bidon x 10lts)",
                "CLETODIM 24xciento select (bidon x10lts)","CLETODIM latium super 36xciento x 10lts","CLEAR SOL (imazapir 80xciento sobre 500gramos) x kg","DIFLUFENICAM","DICAMBA ypf x 5lts",
                "DUAL GOLD","ECORIZOSPRAY/SILICONADO adherente eco (bidon x 1lts)","EDDUS x 20lts","LACTOFEN huck 24xciento x 5 lts","LAUDIS (tembotrione 42xciento) x 5lts","FLEX (fomesafen 25xciento) x 5lts",
                "GALANT haloxifop 81xciento","ACURON uno x lts. (bidon x 5lts)","FIERCE","HEAT (saflufenazil 70xciento) 350 gramos","HALOXIFOP 54xciento ypf x 5 lts","S METOLACLOR (DUAL)","METRIBUZIN 48xciento x 5lts",
                "METSULFURON 60xciento (Bolsa x 100gramos)","ONDUTY (PACK 5 HAS) (imazapic52.5/imazaoir17.5) x 570","PLATINUM glifosato ypf 66xciento (bidon 20lts)","R.UP ULTRA MAX control max x 15kg",
                "SUPER ESTRELLA GR e.granulado (caja 15kg)","SELECT","SUPERNOVA rizopray integrum (coadyu. X 10lts)","SPEED WET aceite vegetal siliconado ypf x 20lts","SPIDER diclosulam 84xciento spider x 500 gramos","STARANE EXTRA (bidon x 5lts)",
                "SULFATO DE AMONIO (bidon x 20lts)","SULFOSATO touchdown (bidon x 20lts)","TROP CS","SUMISOYA (atanor) flumioxazin 48xciento fluminens aca x 5lts","PICLORAN PEYTE","TEXARO",
                "TORDÓN 24 K/picloran (bidon x 5lts)","OTRO"]
    Insecticida = ["AMPILGO ( clorantra10 + lambdas) x 1lts","ABAMECTINA 3,6% ((bidon x5lts)/20lts)","BELT (flubendiamide 48%) x 1lts","CIPERMETRINA","CLAP","CLORPIRIFOS","CONNECT","CORAGEN","CURYON","DECIS FLOW (super nock: deltametrina 3.5%) x 20lts","DIMETOATO (rogor plus) x 20lts",
                    "ENGEO /chinche/medidora/anticarsia (tiametoxam14xciento lambd10%) x 5lts","LAMBDA KARATE zeon lambda 25% CS x 1lts","SOLOMON (bidon x 5lts)","SUMITHION EXTRA (matsuri (esfen.12.5+bif.10+abam.2.4)","FURY","VIRANTA (bidon x 5 lts)","OTRO"]
    Fungicida_Inoculante = ["AMISTAR EXTRA (bidon x 5lts)","BIAGRO + TC (FUNG + INOC) x50- Risopac 101","CLOROTALONIL 72xciento x 20lts","FOLICUR 25 EW","MIRAVIS DUO x 5lts","ORQUESTA","OPERA","OPTIMIZER (bidon x 10lts)","FUNGICIDA (triazol+estrobirulina) orquesta ultra x 5lts",
                              "TEBUCONAZOLE 43xciento","SIGMUN PACK 312 hc p/3000 kg (2022)","SPHERE MAX (bidonx 5lts)","STINGER (bidon x 5lts)","OTRO"]
    Fertilizante = ["DAP - monoamonico (fosfato monoamonico granel x tonelada)","SZ","UREA granel x tons","SPS granel x tons","SPT granel x tons","UAN 32","NUTRITION GROW microstar cmb bio x 20kg","Agroquimicos Varios (preguntar a COTAGRO cuales son)", "OTRO"]
    
    Semilla = ["Don Mario 46e21","Semilla Girasol CL ACA 203 CLDM B1","Dekalb 173 US$ + silo","Nidera AX 7784 VT3PRO","La Tijereta","Algarrobo","Syngenta SYN840 vip3","Syngenta 907TGplus","natal seed","Semilla Sorgo Talero","Semilla P/1 hectarea MANI Cotagro"]
    proveedor = ["Cotagro","Depetris","Dreyfus"]
    
    
    unidad_de_medida = ["Litros","Kilos","Gramos"]
    
    lotesConHectareas = {
            "Gobbi": {
                "1 picadas": 53,
                "2 entrando derecha": 64,
                "3 atrás": 43
            },
            "San Miguel (Pascuet)": {
                "1": 88,
                "2": 92,
                "3": 71,
                "4": 66,
                "5": 63,
                "6": 87
            },
            "Miloch": {
                "1 atrás del lote 2": 31,
                "2 lado ruta (chico)": 28,
                "3 lado ruta (grande)": 29,
                "4 casa": 35
                
            },
            "Pontel": {
                "1 tapera": 50,
                "2 G/pollos": 34.2,
                "3 casa": 43.6,
                "4 atras del 5": 50.4,
                "5 lado ruta casa": 49.4
                
            },
            "Dandrea-Mores-Rossi-Capellari": {
                "1": 37,
                "2 G/pollos": 37
                
            },
            "Defassi": {
                "1 entrada": 24,
                "2 atrás": 25
                
            },
            "Ferrero": {
                "1": 30,
                "2": 17,
                "3": 34,
                "4": 48,
                "5": 30
                
            }
        }

    # Defino las columnas que se utilizarán en la tabla
    columnas = ["Fecha de Retiro", "Campo", "Lote", "Proveedor", "Tipo de Insumo","Insumo",
                "Insumo para agregar a la lista", "Tipo del insumo a agregar a la lista",
                "Unidad de Medida", "Cantidad","Persona Retiró", "Persona Recibio",
                "Persona Aplicó", "Persona Recetó" ,
                "Persona que Pagará" ]

   

    
    st.header(f"Receta ")
    
    camp1 = st.selectbox(f"Campo ", options=list(lotesConHectareas.keys()), key=f"Camp_1")
    FechaActual = st.date_input(f"Fecha", format="DD/MM/YYYY")

    #dfcheck = pd.DataFrame(lotesConHectareas[camp1])
    #st.dataframe(dfcheck)
    #check = st.checkbox(f'{list(dfcheck.keys())}')

    lote = st.multiselect(f"Lote", options=lotesConHectareas[camp1].keys(), key=f"Lote_1")
    
    Total_hectareas_por_lotes_seleccionados = 0
    for camp, lot in lotesConHectareas.items():
        for lo in lote:
            if lo in lot:
                Total_hectareas_por_lotes_seleccionados = Total_hectareas_por_lotes_seleccionados +lot[lo]

    #hectateras_lote = st.selectbox(f"Hectáreas lote {lote}", options=lotesConHectareas[camp1][lote], key=f"Hectáreas_1", disabled= True)
    hectateras_lote = st.selectbox(f"Hectáreas lote/s {lote}", options=[str(Total_hectareas_por_lotes_seleccionados)], key=f"Hectáreas_1", disabled= True)

    Tinsumo = st.selectbox(f"Tipo de Insumo", options= Tipo_Insumos, key=f"Tipo_Insumos_1")

    # Genero inputs en Streamlit anidados 
    Insumo = st.selectbox(f"{Tinsumo} para {camp1}. *SI no lo encontrás elige la opción OTRO* ",
                        Herbicida if Tinsumo == "Herbicida" else 
                        Insecticida if Tinsumo == "Insecticida" else
                        Fungicida_Inoculante if Tinsumo == "Fungicida_Inoculante" else
                        Fertilizante if Tinsumo == "Fertilizante" else
                        Semilla if Tinsumo == "Semilla" else "")
    agregar_este_insumo = None
    #input_3 = None
    if Insumo == "OTRO":
        #input_3 = st.selectbox(f" Selecciona el tipo de insumo que es", Tipo_Insumos, key=f"Tipo_Insumo_{i}")
        agregar_este_insumo = st.text_input(f"Escribe el nombre del Insumo que no encuentras", None)
    else:
        pass

    # Inputs sin anidar
    Unidad_de_Medida = st.selectbox(f"Unidad de medida", options=unidad_de_medida, key=f"unidad_de_medida_1")

    #Cantidad = st.number_input(f"Cantidad TOTAL de {Unidad_de_Medida} para lote {lote}", min_value=1)#, min_value=0
    Dosis_por_hectarea = st.number_input(f"Dosis Por Hectárea de {Insumo}", min_value=0.0000)
    cantidad_total = Dosis_por_hectarea*Total_hectareas_por_lotes_seleccionados
    Cantidad = st.text_input(f"Cantidad TOTAL de {Unidad_de_Medida} para lote/s {lote}", value=str(cantidad_total), disabled= True)
    #Precio = st.number_input(f"Precio Unitario en USD (*Sin IVA*) del insumo para {camp1}") #, min_value=0
    Persona_Recetó = st.text_input(f"Persona que Recetó ", None, key=f"Persona_{camp1}_3")
    Observaciones = st.text_input(f"Observación", None, key=f"Persona_{camp1}_31")


    
    fileName = None
    
    if 'miImage' not in st.session_state.keys():
        st.session_state['miImage'] = None
    picture = st.camera_input("foto")

    if picture is not None:
        st.session_state['miImage'] = picture

    if st.session_state['miImage']:
        #abrirr_imagen = Image.open(st.session_state['miImage'])
        st.image(st.session_state['miImage'], caption="Imagen capturada", use_column_width=True)
        
        fileName = f'Imagen_Para_{camp1}_Fecha_{FechaActual}_lotes:{lote}{st.session_state["miImage"].name}'
        #saveButton = st.button('guardar imagen')
        
        
        #if saveButton:
            #with open(fileName, "wb") as imageFile:
                #imageFile.write(st.session_state['miImage'].getbuffer())
                #st.success('Imagen guardada correctamente')
            
        bytes_data = fileName
        #img = open(bytes_data)
        #st.image(img, caption="imagen capturada")
        #convertir_imagen_a_base64(abrirr_imagen)
        #picture.getvalue()
     


    # Creo el DataFrame a partir de los inputs

    if agregar_este_insumo == "":
        data = {
            "Fecha de Receta": FechaActual,
            "Campo": camp1,
            "Lote": lote,
            "Hectáreas totales Lote/s": hectateras_lote,
            "Tipo de Insumo": Tinsumo,
            "Insumo": Insumo,
            "Insumo para agregar a la lista": None,
            "Unidad de Medida":Unidad_de_Medida,
            "Cantidad por Lote": Cantidad,
            #"Cantidad por Hectárea": [Cantidadhc],
            "Dosis por Hectárea": Dosis_por_hectarea,
            "Persona Recetó" :Persona_Recetó,
            "Observaciones":Observaciones,
            "Foto": fileName
            }
    else:
        data = {
            "Fecha de Receta": FechaActual,
            "Campo": camp1,
            "Lote": lote,
            "Hectáreas totales Lote/s": hectateras_lote,
            "Tipo de Insumo": Tinsumo,
            "Insumo": Insumo,
            "Insumo para agregar a la lista": agregar_este_insumo,
            "Unidad de Medida":Unidad_de_Medida,
            "Cantidad por Lote": Cantidad,
            #"Cantidad por Hectárea": [Cantidadhc],
            "Dosis por Hectárea": Dosis_por_hectarea,
            "Persona Recetó" :Persona_Recetó,
            "Observaciones": Observaciones,
            "Foto": fileName
            }
    
    #df = pd.DataFrame(data)
    
    if st.button("Agregar Insumo"):
    # Creo una nueva fila con los valores capturados
        if agregar_este_insumo == "":
            nueva_fila = {
                "Fecha de Receta": FechaActual,
                "Campo": camp1,
                "Lote": lote,
                "Hectáreas totales Lote/s": hectateras_lote,
                "Tipo de Insumo": Tinsumo,
                "Insumo": Insumo,
                "Insumo para agregar a la lista": None,
                "Unidad de Medida":Unidad_de_Medida,
                "Cantidad por Lote": Cantidad,
                #"Cantidad por Hectárea": [Cantidadhc],
                "Dosis por Hectárea": Dosis_por_hectarea,
                "Persona Recetó" :Persona_Recetó,
                "Observaciones":Observaciones,
                "Foto": fileName
                }
        else:
            nueva_fila = {
                "Fecha de Receta": FechaActual,
                "Campo": camp1,
                "Lote": lote,
                "Hectáreas totales Lote/s": hectateras_lote,
                "Tipo de Insumo": Tinsumo,
                "Insumo": Insumo,
                "Insumo para agregar a la lista": agregar_este_insumo,
                "Unidad de Medida":Unidad_de_Medida,
                "Cantidad por Lote": Cantidad,
                #"Cantidad por Hectárea": [Cantidadhc],
                "Dosis por Hectárea": Dosis_por_hectarea,
                "Persona Recetó" :Persona_Recetó,
                "Observaciones":Observaciones,
                "Foto": fileName
                }
        
        # Agrego nueva fila al DataFrame con append
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nueva_fila])], ignore_index=True)
        st.success("Fila agregada correctamente.")
        #agregar_fila()
    SDF = st.session_state.df
    st.write(f"Controlar Datos Cargados!!")
    st.write(SDF)


        ## boton para descargar datos ya guardados en un xlsl

    st.download_button(
        label="Descargar Receta en Excel",
        data=descargar_excel(pd.DataFrame(SDF)),
        file_name=f'Receta_Para_{camp1}_Fecha_{FechaActual}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    if st.session_state['miImage']:
        st.download_button('Descacargar foto',  data=st.session_state['miImage'], file_name=f'Imagen_Para_{camp1}_Fecha_{FechaActual}.jpg')
    
        

if __name__ == "__main__":
    CargaDosis()
    
    
