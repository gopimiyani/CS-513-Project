#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:40:23 2019
@author: gopi
## ABOUT DATASET
Name: Origina_Phone_Dataset
No_Cols: 40
No_Rows: 8631
Column Header: ['brand', 'model', 'network_technology', '2G_bands', '2G_bands', '4G_bands', 'network_speed', 'GPRS', 
                'EDGE', 'announced', 'status', 'dimentions', 'weight_g', 'weight_oz', 'SIM', 'display_type', 'display_resolution', 
                'display_size', 'OS', 'CPU', 'Chipset', 'GPU', 'memory_card', 'internal_memory', 'RAM', 'primary_camera', 
                'secondary_camera', 'loud_speaker', 'audio_jack', 'WLAN', 'bluetooth', 'GPS', 'NFC', 'radio', 'USB', 'sensors', 
                'battery', 'colors', 'approx_price_EUR', 'img_url']
>> Cleaning Data <<
    
Brand:Splitting the brands into columns and just putting the 1's and 0's,  ---DARP                      
model:
Network Technology: Splitting into 3 Columns 2G, 3G, 4G and putting 1's and 0's,  ---DARP
2G_bands, 2G_bands, 4G_bands : REMOVE ---DARP
network_speed: 
GPRS : NO CHANGE ---DARP
EDGE : NO CHANGE ---DARP
announced : REMOVE
status: REMOVE
Dimension:  Just keeping the Thickness ---DARP
weigth_g: NO CHANGE ---DARP
weight_oz: REMOVE
SIM: Just keep 3 values (Single, Dual and No) ---CHENGZHI
display_type: REMOVE
display_resolution: Split into 2 columns (Screen Size & Screen to body Ratio) Just keep the float values nothing else) ---CHENGZHI
display_size: REMOVE
OS: Just keep the name of OS and Version (remove everything else like Android 4.2.2/) ---CHENGZHI
CPU: NO CHANGE  ---CHENGZHI
Chipset: NO CHANGE ---CHENGZHI
GPU: NO CHANGE  ---CHENGZHI
memory_card:  ---DARP
internal_memory:  ---GOPI
RAM:  ---GOPI
primary_camera:  ---GOPI
secondary_camera:  ---GOPI
loud_speaker: REMOVE
audio_jack:  ---ALISHA
WLAN: REMOVE
bluetooth: REMOVE
GPS: ---ALISHA
NFC:  ---ALISHA
radio:  ---ALISHA
USB: REMOVE
sensors: REMOVE
battery:  ---ALISHA
colors: ------------------------------NEED TO DO
approx_price_EUR:  ---GOPI
img_url: REMOVE
"""

## IMPORT LIBRARIES

import pandas as pd
import numpy as np
import re
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


##GLOBAL VARIABLES

FILE_NAME="Phones_Refined.csv"
FILE_PATH="DATASET/" + FILE_NAME


#----------------------- ALISHA ---------------------------
#Replace dirty values in the column with nan
def replace_dirtydata_nan(data_col, nan_items):
    replacements = dict.fromkeys(nan_items, np.nan)
    data_col = data_col.replace(replacements)
    return data_col

#make the column values boolean (yes/no)
def rep_with_boolean(data_col):
    conditions = ((data_col == "No") | data_col.isna())
    data_col = pd.Series(np.where(conditions, data_col, "Yes"))
    return data_col

#extract first occurrence of numbers in the string
def extract_mAh(data):
    res = data.str.extract(r"(\b\d+)")[0]
    return res.astype(float)

#convert battery data in Wh to mAh to make the data consistent
def convert_Wh_to_mAh(data):
    Wh = extract_mAh(data)
    return round(Wh*1000/3.7)

#MAIN DATA CLEANING FUNCTIONS

#AUDIO
def clean_audiojack_data(audio_jack):
    audio_jack = pd.Series(audio_jack.str.split(r'[\s"|"]').str[0])
    audio_jack = audio_jack.replace("TBD", np.nan)
    return audio_jack

#GPS
def clean_GPS_data(GPS):
    nan_items = ["To be confirmed", "TBD"]
    GPS = replace_dirtydata_nan(GPS, nan_items)
    GPS = rep_with_boolean(GPS)
    return GPS

#NFC
def clean_NFC_data(NFC):
    nan_items = ["TBC", "TBD", "To be confirmed"]
    NFC = replace_dirtydata_nan(NFC, nan_items)
    NFC = rep_with_boolean(NFC)
    return NFC

#RADIO
def clean_radio_data(radio):
    nan_items = ["TBC", "TBD", "To be confirmed", "N&#1086"]
    radio = replace_dirtydata_nan(radio, nan_items)
    radio = rep_with_boolean(radio)
    return radio

#BATTERY
def clean_battery_data(battery):
    battery = pd.Series(np.where(battery.str.contains("mAh"), extract_mAh(battery), convert_Wh_to_mAh(battery)))
    return battery


#----------------------- GOPI ---------------------------
#extract MP as numbers from the string
def extract_MP(data):
   
    res = data.str.extract(r"(\b\d+ MP)")[0]
    return res

def replace_with_nan(data):
    res = data.replace('-',np.nan)
    return res

def get_GB(data_col):
    val = data_col.str.split(" ").str[0]
    return val.astype(float)

def convert_MB_to_GB(data_col):
    MB_val = get_GB(data_col)
    return MB_val/1024


#APPROX PRICE
def clean_approx_price_EUR_data(approx_price_EUR):
    nan_items = [" ","Smoky Titanium| Smoky Blue| White","Gray"]
    approx_price_EUR=replace_dirtydata_nan(approx_price_EUR,nan_items)
    approx_price_EUR.fillna(0)
    approx_price_EUR=approx_price_EUR.astype(float)
    approx_price_DOLLAR=approx_price_EUR*1.12
    return approx_price_DOLLAR

#PRIMARY CAMERA
    
def clean_primary_camera_data(primary_camera):
    primary_camera=primary_camera.str.extract(r"(\b\d+)")[0]
    return primary_camera

#SECONDARY CAMERA
def clean_secondary_camera_data(secondary_camera):
    secondary_camera=secondary_camera.str.extract(r"(\b\d+)")[0]
    return secondary_camera

#RAM   
def clean_RAM_data(RAM):
    RAM=RAM.str.extract(r"(\b\d+ MB|\b\d+ GB)", expand = False)
    RAM = pd.Series(np.where(RAM.str.contains("GB"), get_GB(RAM), convert_MB_to_GB(RAM)))
    return RAM

#LOUD SPEAKER
def clean_loud_speaker_data(loud_speaker):
    loud_speaker=rep_with_boolean(loud_speaker)
    return loud_speaker

#INTERNAL MEMORY   
def clean_internal_memory_data(internal_memory):
    internal_memory=internal_memory.str.extract(r"(\b\d+ MB|\b\d+ GB)", expand = False)
    internal_memory = pd.Series(np.where(internal_memory.str.contains("MB"), convert_MB_to_GB(internal_memory), get_GB(internal_memory)))
    return internal_memory
    
#----------------------- DARP ---------------------------

def data_clean_darp(Phones1):
    
    Phones1['2G'] = Phones1['network_technology']
    Phones1['3G'] = Phones1['network_technology']
    Phones1['4G'] = Phones1['network_technology']
    
    Phones2 = Phones1.replace({'memory_card': {'microSD (dedicated slot)': 'Yes', 'microSD  up to 128 GB (dedicated slot)': 'Yes', 'microSD  up to 512 GB (dedicated slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - single-SIM model': 'Yes', 'miniSD': 'No', 'miniSD  miniSDHC': 'No', 'miniSD  128 MB included': 'No', 'miniSD  up to 8 GB': 'No', 'microSD  up to 128 GB (dedicated slot)': 'Yes', 'Memory Stick Micro (M2)  up to 16 GB': 'No', 'microSD  up to 64 GB (dedicated slot)': 'Yes', 'Memory Stick Micro (M2)  up to 16 GB  1 GB included': 'No', 'microSD (dedicated slot)  128 MB included': 'Yes', 'microSD  up to 64 GB (dedicated slot)/ 32 GB (SGP351)': 'Yes', 'Memory Stick Micro (M2)  up to 2 GB  64 MB included': 'No', 'microSD  up to 2 GB (dedicated slot)  1 GB included': 'Yes', 'RS-DV-MMC  64 MB included': 'Yes', 'microSD  up to 32 GB (uses SIM 2 slot)': 'Yes', 'MMC  up to 2 GB': 'Yes', 'miniSD up to 8 GB': 'Yes', 'microSD  up to 2 GB (dedicated slot)  256 MB included': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  8 GB included': 'No', 'SD  up to 1 GB': 'Yes', 'SDIO/MMC': 'Yes', 'microSD  up to 64 GB (uses SIM 2 slot)': 'Yes', 'To be confirmed': 'No', 'miniSD  up to 2 GB': 'No', 'microSD  up to 4 GB (dedicated slot)  1 GB included': 'Yes', 'microSD  up to 32 GB (dedicated slot) - optional': 'Yes', 'SDIO/MMC  up to 2 GB': 'Yes', 'microSD (dedicated slot)': 'Yes', 'microSD  up to 16 GB (dedicated slot)  1 GB included': 'Yes', 'miniSD  64 MB included': 'No', 'miniSD  1 GB included': 'Yes', 'microSD  up to 8 GB': 'Yes', 'microSD  up to 32 GB (dedicated slot)  1 GB included': 'Yes', 'microSD  up to 32/256 GB (dedicated slot)': 'Yes', 'RS-DV-MMC': 'Yes', 'miniSD  up to 32 GB': 'Yes', 'microSD  up to 64 GB (dedicated slot) - single-SIM model': 'Yes', 'Memory Stick Micro (M2)  up to 2 GB  512 MB included': 'No', 'Memory Stick Micro (M2)  up to 4 GB  64 MB included': 'No', 'microSD  up to 2 GB (dedicated slot)  128 MB included': 'Yes', 'SD/microSD  up to 32 GB (dedicated slot)': 'Yes', 'microSD  up to 32 GB (dedicated slot)  8 GB included': 'Yes', 'microSD (dedicated slot)  1 GB included': 'Yes', 'Memory Stick Micro (M2)  up to 16 GB  8 GB included': 'No', 'microSD  up to 32 GB (dedicated slot) - single-SIM model': 'Yes', 'Memory Stick Micro (M2)  up to 2 GB  128 MB included': 'No', 'microSD  up to 32 GB (dedicated slot)  4 GB included': 'Yes', '2 x SDIO': 'No', 'microSD  up to 64 GB': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB  2 GB included': 'No', 'SD/MMC  SDIO': 'No', 'microSD  up to 32 GB (dedicated slot) - not user accessible': 'No', 'Memory Stick Micro (M2)': 'No', 'SD': 'Yes', 'microSD  up to 16 GB (dedicated slot)  512 MB/ 1 GB included': 'Yes', 'microSD  up to 128 GB (uses SIM 2 slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - single-SIM model (G930F  G930W8)': 'Yes', 'SD/MMC': 'Yes', 'SDIO/MMC + miniSD': 'No', 'miniSD  512 MB included': 'Yes', 'microSD  up to 2 GB (dedicated slot)  512 MB/ 2 GB included': 'Yes', 'Adreno 320': 'No', 'SD  up to 2 GB': 'Yes', 'microSD  up to 2 GB (dedicated slot)  512 MB included': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB  1 GB included': 'No', 'microSD  up to 8 GB (dedicated slot)  128 MB included': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB  256 MB included': 'No', 'Memory Stick Duo Pro  up to 2 GB  64 MB included': 'No', 'microSD  up to 16 GB': 'Yes', 'microSD  up to 512 MB (dedicated slot)': 'No', 'microSD  up to 64 GB (dedicated slot)  2 GB included': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  1 GB included': 'No', 'microSD  up to 256 GB': 'Yes', 'microSD  up to 1 GB (dedicated slot)': 'Yes', 'microSD  up to 8 GB (dedicated slot)  8 GB included': 'Yes', 'SD/MMC  up to 4 GB': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB. 512 MB included': 'No', 'Memory Stick Micro (M2)  up to 2 GB': 'No', 'microSD  up to 32 GB (dedicated slot)  512 MB  included': 'Yes', 'microSD  up to 32 GB (dedicated slot)  4 GB card included': 'Yes', 'Memory Stick Micro (M2)/microSD  up to 4 GB (dedicated slot)  512 MB included': 'No', 'microSD  up to 16 GB (dedicated slot)  2 GB included': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB  512 MB included': 'No', 'microSD  up to 8 GB (dedicated slot)  4 GB included': 'Yes', 'microSD  up to 8 GB (dedicated slot)': 'Yes', 'microSD  up to 4 GB (dedicated slot)  2 GB included': 'Yes', 'Memory Stick Micro (M2)  256 MB included': 'No', 'microSD  up to 8 GB (dedicated slot)  512 MB included': 'Yes', 'microSD  up to 256 GB (dedicated slot) - F5121': 'Yes', 'microSD  up to 4 GB (dedicated slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - single SIM': 'Yes', 'MMC': 'Yes', 'Memory Stick Micro (M2)  up to  2 GB  256 MB included': 'No', 'Memory Stick Duo Pro  up to 2 GB  512 MB included': 'No', 'microSD  up to 128 GB': 'Yes', 'microSD (dedicated slot)  512 MB included': 'Yes', 'SD  up to 32 GB': 'Yes', 'Memory Stick Duo Pro  64 MB included': 'No', 'microSD  up to 16 GB (dedicated slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - single & dual SIM models': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  2 GB included': 'No', 'microSD  up to 32 GB (dedicated slot)': 'Yes', 'microSD  up to 32 GB (dedicated slot)  2 GB included': 'Yes', 'microSD (dedicated slot)  up to 256 GB (LTE model)  32 GB (3G model)': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB': 'No', 'miniSD  up to 16 GB': 'Yes', 'microSD  up to 256 GB (uses SIM 2 slot)': 'Yes', 'Memory Stick Duo Pro  up to 4 GB': 'No', 'microSD (dedicated slot)  16 GB included': 'Yes', 'microSD  up to 256 GB (uses SIM 1 slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - F620S': 'Yes', 'microSD  up to 2 GB (dedicated slot)': 'Yes', 'microSD  up to 16 GB (dedicated slot)  8 GB included': 'Yes', 'SDIO': 'No', 'microSD  up to 8 GB (dedicated slot)  1 GB included': 'Yes', 'microSD (dedicated slot)  SD 2.0 compatible': 'Yes', 'microSD  up to 8 GB (dedicated slot)  2 GB included': 'Yes', 'microSD  up to 32 GB (dedicated slot)  2/4 GB included': 'Yes', 'MiniSD': 'No', 'microSD  up to 256 GB (dedicated slot)': 'Yes', 'microSD  up to 256GB (uses SIM2 slot)': 'Yes', 'microSD (dedicated slot)  2 GB included': 'Yes', 'microSD  up to 32 GB (dedicated slot) - Chinese version only': 'Yes', 'SD/MMC  up to 2 GB': 'Yes', 'microSD  up to 64 GB (dedicated slot)  16 GB included': 'Yes', 'microSD  up to 32 GB (dedicated slot) - market dependent': 'Yes', 'miniSD  up to 2 GB  128 MB included': 'No', 'microSD  up to 32 GB': 'Yes', 'RS-DV-MMC  128 MB included': 'Yes', 'microSD  up to 256 GB (dedicated slot) - G8231': 'Yes', 'microSD  up to 32 GB (dedicated slot)  32 GB included': 'Yes', 'Memory Stick Duo Pro  up to 4 GB  512 MB included': 'No', 'microSD': 'Yes', 'SD/SDIO': 'No', 'Memory Stick Micro (M2)  up to 8 GB': 'No', 'Memory Stick Duo Pro  up to 4 GB  256 MB included': 'No', 'microSD  up to 32 GB (dedicated slot)  16 GB included': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  4 GB included': 'No', 'Yes  up to 64 GB (dedicated slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - non microSDXC compliant': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  2 GB/ 8 GB included': 'No', 'microSD  up to 32 GB (dedicated slot); SD cards': 'Yes', 'microSD   up to 512 MB (dedicated slot)': 'Yes', 'microSD  up to 16 GB (dedicated slot)  4 GB included': 'Yes', 'microSD  up to 200 GB (dedicated slot)': 'Yes', 'Memory Stick Micro (M2)   up to 8 GB  512 MB included': 'No', 'RS-MMC  32 MB included': 'Yes', 'Memory Stick Micro (M2)  up to 2 GB  256 MB included': 'No', 'microSD  up to 32 GB (uses SIM 2 slot) - mediatek model': 'Yes', 'Memory Stick Duo Pro  1 GB included': 'No', 'miniSDIO  128 MB included': 'No', 'microSD  up to 256 GB (dedicated slot) - single-SIM model - G935F  G935W8': 'Yes', 'microSD  up to 2 GB (dedicated slot)  64 MB included': 'Yes'}})
    Phones3 = Phones2.replace({'2G': {'GSM / CDMA': 'Yes', 'GSM / UMTS / HSPA': 'Yes', 'GSM / HSPA / CDMA2000': 'Yes', 'LTE': 'No', 'CDMA / LTE': 'No', 'CDMA / CDMA2000': 'No', 'GSM / UMTS': 'Yes', 'HSPA / LTE': 'No', 'GSM / HSPA / EVDO / LTE': 'Yes', 'GSM / LTE': 'Yes', 'CDMA / EVDO': 'No', 'GSM / CDMA / EVDO / LTE': 'Yes', 'CDMA / EVDO / LTE': 'No', 'GSM / CDMA / HSPA / EVDO / LTE': 'Yes', 'GSM / HSPA / CDMA2000 / LTE': 'Yes', 'No cellular connectivity': 'No', 'HSPA / EVDO': 'No', 'GSM / CDMA / HSPA': 'Yes', 'CDMA / HSPA': 'No', 'GSM / CDMA2000': 'Yes', 'GSM / CDMA / HSPA / EVDO': 'Yes', 'GSM':'Yes', 'GSM / CDMA / HSPA / CDMA2000 / LTE': 'Yes', 'CDMA / HSPA / EVDO': 'No', 'CDMA': 'No', 'GSM / CDMA / EVDO': 'Yes', 'GSM / HSPA / EVDO': 'Yes', 'GSM / HSPA': 'Yes', 'CDMA / HSPA / EVDO / LTE': 'No', 'GSM / CDMA / UMTS / EVDO': 'Yes', 'GSM / CDMA / HSPA / LTE': 'Yes', 'GSM / UMTS / HSPA / LTE': 'Yes', 'CDMA / HSPA / LTE': 'No', 'HSPA': 'No', 'GSM / HSPA / LTE': 'Yes'}})
    Phones4 = Phones3.replace({'3G': {'GSM / CDMA': 'Yes', 'GSM / UMTS / HSPA': 'Yes', 'GSM / HSPA / CDMA2000': 'Yes', 'LTE': 'No', 'CDMA / LTE': 'Yes', 'CDMA / CDMA2000': 'Yes', 'GSM / UMTS': 'Yes', 'HSPA / LTE': 'Yes', 'GSM / HSPA / EVDO / LTE': 'Yes', 'GSM / LTE': 'No', 'CDMA / EVDO': 'Yes', 'GSM / CDMA / EVDO / LTE': 'Yes', 'CDMA / EVDO / LTE': 'Yes', 'GSM / CDMA / HSPA / EVDO / LTE': 'Yes', 'GSM / HSPA / CDMA2000 / LTE': 'Yes', 'No cellular connectivity': 'No', 'HSPA / EVDO': 'Yes', 'GSM / CDMA / HSPA': 'Yes', 'CDMA / HSPA': 'Yes', 'GSM / CDMA2000': 'Yes', 'GSM / CDMA / HSPA / EVDO': 'Yes', 'GSM':'No', 'GSM / CDMA / HSPA / CDMA2000 / LTE': 'Yes', 'CDMA / HSPA / EVDO': 'Yes', 'CDMA': 'Yes', 'GSM / CDMA / EVDO': 'Yes', 'GSM / HSPA / EVDO': 'Yes', 'GSM / HSPA': 'Yes', 'CDMA / HSPA / EVDO / LTE': 'No', 'GSM / CDMA / UMTS / EVDO': 'Yes', 'GSM / CDMA / HSPA / LTE': 'Yes', 'GSM / UMTS / HSPA / LTE': 'Yes', 'CDMA / HSPA / LTE': 'Yes', 'HSPA': 'Yes', 'GSM / HSPA / LTE': 'Yes'}})
    Phones5 = Phones4.replace({'4G': {'GSM / CDMA': 'No', 'GSM / UMTS / HSPA': 'No', 'GSM / HSPA / CDMA2000': 'No', 'LTE': 'Yes', 'CDMA / LTE': 'Yes', 'CDMA / CDMA2000': 'No', 'GSM / UMTS': 'No', 'HSPA / LTE': 'Yes', 'GSM / HSPA / EVDO / LTE': 'Yes', 'GSM / LTE': 'Yes', 'CDMA / EVDO': 'No', 'GSM / CDMA / EVDO / LTE': 'Yes', 'CDMA / EVDO / LTE':'Yes','GSM / CDMA / HSPA / EVDO / LTE': 'Yes', 'GSM / HSPA / CDMA2000 / LTE': 'Yes', 'No cellular connectivity': 'No', 'HSPA / EVDO': 'No', 'GSM / CDMA / HSPA': 'No', 'CDMA / HSPA': 'No', 'GSM / CDMA2000': 'No', 'GSM / CDMA / HSPA / EVDO': 'No', 'GSM':'No', 'GSM / CDMA / HSPA / CDMA2000 / LTE': 'Yes', 'CDMA / HSPA / EVDO': 'No', 'CDMA': 'No', 'GSM / CDMA / EVDO': 'No', 'GSM / HSPA / EVDO': 'No', 'GSM / HSPA': 'No', 'CDMA / HSPA / EVDO / LTE': 'Yes', 'GSM / CDMA / UMTS / EVDO': 'No', 'GSM / CDMA / HSPA / LTE': 'Yes', 'GSM / UMTS / HSPA / LTE': 'Yes', 'CDMA / HSPA / LTE': 'Yes', 'HSPA': 'No', 'GSM / HSPA / LTE': 'Yes'}})
    
    b = {}
    b = set(Phones5['brand'])
    
    c = list(b)
    Phones6 = Phones5
    for i in range(0, len(c)):
        Phones6[c[i]] = Phones5['brand']
        Phones6[c[i]] = np.where(Phones5[c[i]] == c[i], 1, 0)
    
    E = Phones6['dimentions']
    
    for i in range (0, len(E)):
        if (len(re.findall('\d+\.\d+', E[i]))>0):
            E[i] = (re.findall('\d+\.\d+', E[i]))[-1]
        elif (E[i] == '-'):
            E[i] = np.nan
        
    E = pd.to_numeric(E, errors='ignore')
    Phones6['Thickness'] = E
    Phones7 = Phones6.replace({'GPRS': {'Class 32' : 'Yes', 'Up to 70.4 kbps' : 'Yes', 'Up to 70.4 kbps' : 'Yes','Class 32| 53.6 kbps' : 'Yes','Class 10' : 'Yes', 'Class 32| 107 / 64.2 kbps' : 'Yes', 'Class 32| 100 kbps' : 'Yes', 'Yes - SCH-I605| SPH-L900' : 'Yes', 'Class 8' : 'Yes', 'Class 11| 118.4 kbits' : 'Yes', 'Up to 85.6 kbps' : 'Yes', 'Class 11|  53.6 kbps' : 'Yes', 'Up to 85 kbps' : 'Yes', 'Up to 80 kbps' : 'Yes', 'Up to 114 kbps' : 'Yes', 'Class 32|  53.6 kbps' : 'Yes', 'Up to 107 kbps' : 'Yes', 'Up to 59.2 kbps': 'Yes', 'Class 6' : 'Yes', 'Class 33' : 'Yes', 'Class 12 (T-Mobile)' : 'Yes', 'Up to 115 kbps' : 'Yes', 'Class 4' : 'Yes', 'Class B' : 'Yes', 'Up to 48 kbps' : 'Yes', 'Yes - 3G model' : 'Yes', 'Class 32|  123 kbps' : 'Yes', 'Class 11' : 'Yes', 'Class 32| 52.6 kbps' : 'Yes', 'Class 12' : 'Yes', 'Class 32| 107.2/64.2 kbps' : 'Yes', 'Up to 60 kbps' : 'Yes', 'Class 32| 107 kbps' : 'Yes', 'Up to 42.8 kbps' : 'Yes', 'Class 32|  88 kbps' : 'Yes', 'Up to 100 kbps' : 'Yes', 'Up to 86 kbps' : 'Yes', 'Up to 42 kbps' : 'Yes', 'Class 12 (SIM 1)| Class 10 (SIM 2)' : 'Yes', 'No  (Planned GPRS version for Q4 2012)' : 'No'}})
    Phones8 = Phones7.replace({'EDGE': {'Class 32' : 'Yes', 'Up to 296 kbps': 'Yes', 'Class 10': 'Yes', 'Class 32| 296 / 177.6 kbits': 'Yes', 'Yes - SCH-I605| SPH-L900': 'Yes', 'Class 32| 296 / 178.8 kbits' : 'Yes', 'Class 8' : 'Yes', 'Yes| DL only' : 'Yes', 'W958c only' : 'Yes', 'Up to 560 kbps' : 'Yes', 'Up to 236.8 kbps' : 'Yes', 'Yes| 118.4 kbps' : 'Yes', 'Class 6 (Up to 177.6 kbps)' : 'Yes', 'Class 32| 296 kbps; DTM Class 11| 178.8 kbps' : 'Yes', 'Class 32|  up to 177 kbits' : 'Yes', 'Up to 177 kbps' : 'Yes', 'Class 11| 236.8 kbps' : 'Yes', 'Class 12 (SIM 1)' : 'Yes', 'Class 6' : 'Yes', 'Class 12| 296 / 177.6 kbits' : 'Yes', 'Up to 236 kbps' : 'Yes', 'Class 32| 296 kbps; DTM Class 11| 236.8 kbps' : 'Yes', 'Class 32| 296 kbps; DTM Class 11| 177 kbps' : 'Yes', 'Class 33' : 'Yes', 'Class 12 (T-Mobile)' : 'Yes', 'Class 6 (downlink only)' : 'Yes', 'Up to 247 kbps' : 'Yes', 'Class 32| 296 kbps' : 'Yes', 'Class B' : 'Yes', 'Up to 200 kbps' : 'Yes', 'Yes - 3G model' : 'Yes', 'Class 10 (SIM 1| download only)' : 'Yes', 'Yes (SIM 1 only)' : 'Yes', 'Up to 384 kbps' : 'Yes', 'Class 11' : 'Yes', 'Up to 225 kbps' : 'Yes', 'Class 12' : 'Yes', 'Class 32| 296 kbits' : 'Yes', 'Up to 60 kbps' : 'Yes', 'Class 32| 236.8 kbits' : 'Yes', 'Up to 237 kbps' : 'Yes'}})
    z = np.multiply(Phones8['approx_price_EUR'],1.11)
    Phones8['Price'] = z
    Phones9 = Phones8.drop(['brand', 'network_technology', 'dimentions', 'approx_price_EUR'], axis = 1)
    
    return Phones9
    
#-------------------------- CHENGZHI -----------------------------
    
def clean_SIM(SIM):
    sim_column_list = SIM
    # Micro, Mini, Nano, Electronic all belongs to the Single.
    for i in range(len(sim_column_list)):
        cell = str(sim_column_list[i])
        if 'Dual' in cell:
            sim_column_list[i] = 'Dual'
        elif 'Triple' in cell:
            sim_column_list[i] = 'Triple'
        elif 'No' in cell:
            sim_column_list[i] = 'No'
        elif 'Yes' in cell or 'Single' in cell or 'Mini' in cell or             'Micro' in cell or 'Nano' in cell or 'Electronic' in cell:
            sim_column_list[i] = 'Single'
        else:
            sim_column_list[i] = np.nan
    return sim_column_list

def clean_display_resolution(display_resolution):
    display_size = []
    screen_to_body_ratio = []
    display_column_list = display_resolution
    for i in range(len(display_column_list)):
        cell = str(display_column_list[i])

        l = re.findall('.*inches', cell)
        if len(l) == 0:
            inch = ''
        else:
            inch = str(l[0])
        inch = inch.replace(' inches', '')
        display_size.append(inch)

        l = re.findall('~.*\%', cell)
        if len(l) == 0:
            ratio = ''
        else:
            ratio = str(l[0])
        # ratio = str(re.findall('~.*\%', cell))
        ratio = ratio.replace('~', '')
        ratio = ratio.replace('%', '')
        screen_to_body_ratio.append(ratio)

    return [pd.Series(display_size), pd.Series(screen_to_body_ratio)]

def clean_OS(os_column_list):
    os_list = []
    for i in range(len(os_column_list)):
        cell = str(os_column_list[i])
        if 'Android' in cell:
            l = re.match(r'^Android ((\d\.\d\.\d)|(\d\.\d))', cell)
            g = None
            if l:
                g = l.group()
            if g is None or len(g) == 0:
                android_version = 'Android'
            else:
                android_version = str(g)
            os_list.append(android_version)
        elif 'Windows' in cell or 'Microsoft' in cell:
            os_list.append('Windows')
        elif 'Bada' in cell:
            os_list.append('Bada')
        elif 'Tizen' in cell:
            os_list.append('Tizen')
        elif 'BlackBerry' in cell:
            os_list.append('BlackBerry')
        elif 'Symbian' in cell:
            os_list.append('Symbian')
        elif 'iOS' in cell:
            os_list.append('iOS')
        else:
            os_list.append(np.nan)
    return pd.Series(os_list)

## ------------------------------- MAIN METHOD -------------------------------
if __name__ == "__main__":  
    
    data = pd.read_csv(FILE_PATH)

    print('Cleaning Data...')
    
    # DATA --ALISHA
    audio_jack = clean_audiojack_data(data["audio_jack"])
    GPS = clean_GPS_data(data["GPS"])
    NFC = clean_NFC_data(data["NFC"])
    radio = clean_radio_data(data["radio"])
    battery = clean_battery_data(data["battery"])
    
    #  DATA --GOPI
    RAM=clean_RAM_data(data["RAM"])
    primary_camera=clean_primary_camera_data(data["primary_camera"])
    secondary_camera=clean_secondary_camera_data(data["secondary_camera"])
    loud_speaker=clean_loud_speaker_data(data["loud_speaker"])
    #approx_price_DOLLAR=clean_approx_price_EUR_data(data["approx_price_EUR"])
    internal_memory=clean_internal_memory_data(data["internal_memory"]) 
    
    print("Halfway there...")
    
    #DATA --CHENGZHI
    SIM=clean_SIM(data["SIM"])
    display_size, screen_to_body_ratio = clean_display_resolution(data["display_resolution"])
    OS=clean_OS(data["OS"])
    
    #DATA --DARP
    darp = data_clean_darp(data)
    
    print('Finished data cleaning!')
    
    _2G = darp["2G"]
    _3G = darp["3G"]
    _4G = darp["4G"]
    GPRS = darp["GPRS"]
    EDGE = darp["EDGE"]
    weight_g = darp["weight_g"]
    memory_card = darp["memory_card"]
    CPU = darp["CPU"]
    chipset = darp["Chipset"]
    GPU = darp["GPU"]
    thickness = darp["Thickness"]
    price = darp["Price"]
    
    print("Combining brands and feature columns...")

    all_features = pd.concat({"SIM": SIM, "display_size":display_size, "screen_to_body_ratio":screen_to_body_ratio,"OS":OS,
               "internal_memory":internal_memory,"RAM":RAM,"primary_camera":primary_camera,"secondary_camera":secondary_camera,
               "loud_speaker":loud_speaker,"audio_jack": audio_jack, "GPS": GPS, "NFC":  NFC, "radio": radio, "battery": battery, 
               "2G": _2G, "3G": _3G, "4G": _4G, "GPRS": GPRS, "EDGE": EDGE, "weight_g": weight_g, "memory_card": memory_card, 
               "CPU": CPU, "Chipset": chipset, "GPU": GPU, "Thickness": thickness, "Price": price},axis = 1)
    
    brands = darp.iloc[:, 24:-2]
    
    print("Creating CSV file of the complete dataset...")
    pd.concat([brands, all_features], axis = 1).to_csv("DATASET/Refined_Phone_Dataset.csv")
   
    print("CSV file created. Go to './dataset/Refined_Phone_Dataset.csv'")


# In[ ]:




