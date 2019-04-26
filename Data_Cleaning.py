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


##GLOBAL VARIABLES

FILE_NAME="Original_Phone_Dataset.csv"
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

#APPROX PRICE
def clean_approx_price_EUR_data(approx_price_EUR):
    nan_items = [" ","Smoky Titanium| Smoky Blue| White","Gray"]
    approx_price_EUR=replace_dirtydata_nan(approx_price_EUR,nan_items)
    approx_price_EUR.fillna(0)
    #print(pd.Series(approx_price_EUR).unique())
    approx_price_EUR=approx_price_EUR.astype(float)
    approx_price_DOLLAR=approx_price_EUR*1.12
    return approx_price_DOLLAR

#PRIMARY CAMERA
    
def clean_primary_camera_data(primary_camera):
    primary_camera=primary_camera.str.extract(r"(\b\d+ MP)")[0]
    return primary_camera

#SECONDARY CAMERA
def clean_secondary_camera_data(secondary_camera):
    secondary_camera=secondary_camera.str.extract(r"(\b\d+ MP)")[0]
    return secondary_camera

#RAM
    
def clean_RAM_data(RAM):
    RAM=RAM.str.extract(r"(\b\d+ MB|\b\d+ GB)")
    return RAM

#LOUD SPEAKER
    
def clean_loud_speaker_data(loud_speaker):
    loud_speaker=rep_with_boolean(loud_speaker)
    return loud_speaker

#INTERNAL MEMORY
    
#def clean_internal_memory_data(internal_memory):
    
#----------------------- DARP ---------------------------
#
#BRAND
def clean_brand_data(brand):
    
    brand_types=pd.Series(brand).unique()
    brand=brand.astype("category",brand_types).cat.codes
    return brand
    

def clean_data(Phones1):
    Phones1['2G'] = Phones1['network_technology']
    Phones1['3G'] = Phones1['network_technology']
    Phones1['4G'] = Phones1['network_technology']
    d = {}
    d = set(Phones1['network_technology'])
    print(d)
    Phones2 = Phones1.replace({'memory_card': {'microSD (dedicated slot)': 'Yes', 'microSD  up to 128 GB (dedicated slot)': 'Yes', 'microSD  up to 512 GB (dedicated slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - single-SIM model': 'Yes', 'miniSD': 'No', 'miniSD  miniSDHC': 'No', 'miniSD  128 MB included': 'No', 'miniSD  up to 8 GB': 'No', 'microSD  up to 128 GB (dedicated slot)': 'Yes', 'Memory Stick Micro (M2)  up to 16 GB': 'No', 'microSD  up to 64 GB (dedicated slot)': 'Yes', 'Memory Stick Micro (M2)  up to 16 GB  1 GB included': 'No', 'microSD (dedicated slot)  128 MB included': 'Yes', 'microSD  up to 64 GB (dedicated slot)/ 32 GB (SGP351)': 'Yes', 'Memory Stick Micro (M2)  up to 2 GB  64 MB included': 'No', 'microSD  up to 2 GB (dedicated slot)  1 GB included': 'Yes', 'RS-DV-MMC  64 MB included': 'Yes', 'microSD  up to 32 GB (uses SIM 2 slot)': 'Yes', 'MMC  up to 2 GB': 'Yes', 'miniSD up to 8 GB': 'Yes', 'microSD  up to 2 GB (dedicated slot)  256 MB included': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  8 GB included': 'No', 'SD  up to 1 GB': 'Yes', 'SDIO/MMC': 'Yes', 'microSD  up to 64 GB (uses SIM 2 slot)': 'Yes', 'To be confirmed': 'No', 'miniSD  up to 2 GB': 'No', 'microSD  up to 4 GB (dedicated slot)  1 GB included': 'Yes', 'microSD  up to 32 GB (dedicated slot) - optional': 'Yes', 'SDIO/MMC  up to 2 GB': 'Yes', 'microSD (dedicated slot)': 'Yes', 'microSD  up to 16 GB (dedicated slot)  1 GB included': 'Yes', 'miniSD  64 MB included': 'No', 'miniSD  1 GB included': 'Yes', 'microSD  up to 8 GB': 'Yes', 'microSD  up to 32 GB (dedicated slot)  1 GB included': 'Yes', 'microSD  up to 32/256 GB (dedicated slot)': 'Yes', 'RS-DV-MMC': 'Yes', 'miniSD  up to 32 GB': 'Yes', 'microSD  up to 64 GB (dedicated slot) - single-SIM model': 'Yes', 'Memory Stick Micro (M2)  up to 2 GB  512 MB included': 'No', 'Memory Stick Micro (M2)  up to 4 GB  64 MB included': 'No', 'microSD  up to 2 GB (dedicated slot)  128 MB included': 'Yes', 'SD/microSD  up to 32 GB (dedicated slot)': 'Yes', 'microSD  up to 32 GB (dedicated slot)  8 GB included': 'Yes', 'microSD (dedicated slot)  1 GB included': 'Yes', 'Memory Stick Micro (M2)  up to 16 GB  8 GB included': 'No', 'microSD  up to 32 GB (dedicated slot) - single-SIM model': 'Yes', 'Memory Stick Micro (M2)  up to 2 GB  128 MB included': 'No', 'microSD  up to 32 GB (dedicated slot)  4 GB included': 'Yes', '2 x SDIO': 'No', 'microSD  up to 64 GB': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB  2 GB included': 'No', 'SD/MMC  SDIO': 'No', 'microSD  up to 32 GB (dedicated slot) - not user accessible': 'No', 'Memory Stick Micro (M2)': 'No', 'SD': 'Yes', 'microSD  up to 16 GB (dedicated slot)  512 MB/ 1 GB included': 'Yes', 'microSD  up to 128 GB (uses SIM 2 slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - single-SIM model (G930F  G930W8)': 'Yes', 'SD/MMC': 'Yes', 'SDIO/MMC + miniSD': 'No', 'miniSD  512 MB included': 'Yes', 'microSD  up to 2 GB (dedicated slot)  512 MB/ 2 GB included': 'Yes', 'Adreno 320': 'No', 'SD  up to 2 GB': 'Yes', 'microSD  up to 2 GB (dedicated slot)  512 MB included': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB  1 GB included': 'No', 'microSD  up to 8 GB (dedicated slot)  128 MB included': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB  256 MB included': 'No', 'Memory Stick Duo Pro  up to 2 GB  64 MB included': 'No', 'microSD  up to 16 GB': 'Yes', 'microSD  up to 512 MB (dedicated slot)': 'No', 'microSD  up to 64 GB (dedicated slot)  2 GB included': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  1 GB included': 'No', 'microSD  up to 256 GB': 'Yes', 'microSD  up to 1 GB (dedicated slot)': 'Yes', 'microSD  up to 8 GB (dedicated slot)  8 GB included': 'Yes', 'SD/MMC  up to 4 GB': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB. 512 MB included': 'No', 'Memory Stick Micro (M2)  up to 2 GB': 'No', 'microSD  up to 32 GB (dedicated slot)  512 MB  included': 'Yes', 'microSD  up to 32 GB (dedicated slot)  4 GB card included': 'Yes', 'Memory Stick Micro (M2)/microSD  up to 4 GB (dedicated slot)  512 MB included': 'No', 'microSD  up to 16 GB (dedicated slot)  2 GB included': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB  512 MB included': 'No', 'microSD  up to 8 GB (dedicated slot)  4 GB included': 'Yes', 'microSD  up to 8 GB (dedicated slot)': 'Yes', 'microSD  up to 4 GB (dedicated slot)  2 GB included': 'Yes', 'Memory Stick Micro (M2)  256 MB included': 'No', 'microSD  up to 8 GB (dedicated slot)  512 MB included': 'Yes', 'microSD  up to 256 GB (dedicated slot) - F5121': 'Yes', 'microSD  up to 4 GB (dedicated slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - single SIM': 'Yes', 'MMC': 'Yes', 'Memory Stick Micro (M2)  up to  2 GB  256 MB included': 'No', 'Memory Stick Duo Pro  up to 2 GB  512 MB included': 'No', 'microSD  up to 128 GB': 'Yes', 'microSD (dedicated slot)  512 MB included': 'Yes', 'SD  up to 32 GB': 'Yes', 'Memory Stick Duo Pro  64 MB included': 'No', 'microSD  up to 16 GB (dedicated slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - single & dual SIM models': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  2 GB included': 'No', 'microSD  up to 32 GB (dedicated slot)': 'Yes', 'microSD  up to 32 GB (dedicated slot)  2 GB included': 'Yes', 'microSD (dedicated slot)  up to 256 GB (LTE model)  32 GB (3G model)': 'Yes', 'Memory Stick Micro (M2)  up to 4 GB': 'No', 'miniSD  up to 16 GB': 'Yes', 'microSD  up to 256 GB (uses SIM 2 slot)': 'Yes', 'Memory Stick Duo Pro  up to 4 GB': 'No', 'microSD (dedicated slot)  16 GB included': 'Yes', 'microSD  up to 256 GB (uses SIM 1 slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - F620S': 'Yes', 'microSD  up to 2 GB (dedicated slot)': 'Yes', 'microSD  up to 16 GB (dedicated slot)  8 GB included': 'Yes', 'SDIO': 'No', 'microSD  up to 8 GB (dedicated slot)  1 GB included': 'Yes', 'microSD (dedicated slot)  SD 2.0 compatible': 'Yes', 'microSD  up to 8 GB (dedicated slot)  2 GB included': 'Yes', 'microSD  up to 32 GB (dedicated slot)  2/4 GB included': 'Yes', 'MiniSD': 'No', 'microSD  up to 256 GB (dedicated slot)': 'Yes', 'microSD  up to 256GB (uses SIM2 slot)': 'Yes', 'microSD (dedicated slot)  2 GB included': 'Yes', 'microSD  up to 32 GB (dedicated slot) - Chinese version only': 'Yes', 'SD/MMC  up to 2 GB': 'Yes', 'microSD  up to 64 GB (dedicated slot)  16 GB included': 'Yes', 'microSD  up to 32 GB (dedicated slot) - market dependent': 'Yes', 'miniSD  up to 2 GB  128 MB included': 'No', 'microSD  up to 32 GB': 'Yes', 'RS-DV-MMC  128 MB included': 'Yes', 'microSD  up to 256 GB (dedicated slot) - G8231': 'Yes', 'microSD  up to 32 GB (dedicated slot)  32 GB included': 'Yes', 'Memory Stick Duo Pro  up to 4 GB  512 MB included': 'No', 'microSD': 'Yes', 'SD/SDIO': 'No', 'Memory Stick Micro (M2)  up to 8 GB': 'No', 'Memory Stick Duo Pro  up to 4 GB  256 MB included': 'No', 'microSD  up to 32 GB (dedicated slot)  16 GB included': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  4 GB included': 'No', 'Yes  up to 64 GB (dedicated slot)': 'Yes', 'microSD  up to 256 GB (dedicated slot) - non microSDXC compliant': 'Yes', 'Memory Stick Micro (M2)  up to 8 GB  2 GB/ 8 GB included': 'No', 'microSD  up to 32 GB (dedicated slot); SD cards': 'Yes', 'microSD   up to 512 MB (dedicated slot)': 'Yes', 'microSD  up to 16 GB (dedicated slot)  4 GB included': 'Yes', 'microSD  up to 200 GB (dedicated slot)': 'Yes', 'Memory Stick Micro (M2)   up to 8 GB  512 MB included': 'No', 'RS-MMC  32 MB included': 'Yes', 'Memory Stick Micro (M2)  up to 2 GB  256 MB included': 'No', 'microSD  up to 32 GB (uses SIM 2 slot) - mediatek model': 'Yes', 'Memory Stick Duo Pro  1 GB included': 'No', 'miniSDIO  128 MB included': 'No', 'microSD  up to 256 GB (dedicated slot) - single-SIM model - G935F  G935W8': 'Yes', 'microSD  up to 2 GB (dedicated slot)  64 MB included': 'Yes'}})
    Phones3 = Phones2.replace({'2G': {'GSM / CDMA': 'Yes', 'GSM / UMTS / HSPA': 'Yes', 'GSM / HSPA / CDMA2000': 'Yes', 'LTE': 'No', 'CDMA / LTE': 'No', 'CDMA / CDMA2000': 'No', 'GSM / UMTS': 'Yes', 'HSPA / LTE': 'No', 'GSM / HSPA / EVDO / LTE': 'Yes', 'GSM / LTE': 'Yes', 'CDMA / EVDO': 'No', 'GSM / CDMA / EVDO / LTE': 'Yes', 'CDMA / EVDO / LTE': 'No', 'GSM / CDMA / HSPA / EVDO / LTE': 'Yes', 'GSM / HSPA / CDMA2000 / LTE': 'Yes', 'No cellular connectivity': 'No', 'HSPA / EVDO': 'No', 'GSM / CDMA / HSPA': 'Yes', 'CDMA / HSPA': 'No', 'GSM / CDMA2000': 'Yes', 'GSM / CDMA / HSPA / EVDO': 'Yes', 'GSM':'Yes', 'GSM / CDMA / HSPA / CDMA2000 / LTE': 'Yes', 'CDMA / HSPA / EVDO': 'No', 'CDMA': 'No', 'GSM / CDMA / EVDO': 'Yes', 'GSM / HSPA / EVDO': 'Yes', 'GSM / HSPA': 'Yes', 'CDMA / HSPA / EVDO / LTE': 'No', 'GSM / CDMA / UMTS / EVDO': 'Yes', 'GSM / CDMA / HSPA / LTE': 'Yes', 'GSM / UMTS / HSPA / LTE': 'Yes', 'CDMA / HSPA / LTE': 'No', 'HSPA': 'No', 'GSM / HSPA / LTE': 'Yes'}})
    Phones4 = Phones3.replace({'3G': {'GSM / CDMA': 'Yes', 'GSM / UMTS / HSPA': 'Yes', 'GSM / HSPA / CDMA2000': 'Yes', 'LTE': 'No', 'CDMA / LTE': 'Yes', 'CDMA / CDMA2000': 'Yes', 'GSM / UMTS': 'Yes', 'HSPA / LTE': 'Yes', 'GSM / HSPA / EVDO / LTE': 'Yes', 'GSM / LTE': 'No', 'CDMA / EVDO': 'Yes', 'GSM / CDMA / EVDO / LTE': 'Yes', 'CDMA / EVDO / LTE': 'Yes', 'GSM / CDMA / HSPA / EVDO / LTE': 'Yes', 'GSM / HSPA / CDMA2000 / LTE': 'Yes', 'No cellular connectivity': 'No', 'HSPA / EVDO': 'Yes', 'GSM / CDMA / HSPA': 'Yes', 'CDMA / HSPA': 'Yes', 'GSM / CDMA2000': 'Yes', 'GSM / CDMA / HSPA / EVDO': 'Yes', 'GSM':'No', 'GSM / CDMA / HSPA / CDMA2000 / LTE': 'Yes', 'CDMA / HSPA / EVDO': 'Yes', 'CDMA': 'Yes', 'GSM / CDMA / EVDO': 'Yes', 'GSM / HSPA / EVDO': 'Yes', 'GSM / HSPA': 'Yes', 'CDMA / HSPA / EVDO / LTE': 'No', 'GSM / CDMA / UMTS / EVDO': 'Yes', 'GSM / CDMA / HSPA / LTE': 'Yes', 'GSM / UMTS / HSPA / LTE': 'Yes', 'CDMA / HSPA / LTE': 'Yes', 'HSPA': 'Yes', 'GSM / HSPA / LTE': 'Yes'}})
    Phones5 = Phones4.replace({'4G': {'GSM / CDMA': 'No', 'GSM / UMTS / HSPA': 'No', 'GSM / HSPA / CDMA2000': 'No', 'LTE': 'Yes', 'CDMA / LTE': 'Yes', 'CDMA / CDMA2000': 'No', 'GSM / UMTS': 'No', 'HSPA / LTE': 'Yes', 'GSM / HSPA / EVDO / LTE': 'Yes', 'GSM / LTE': 'Yes', 'CDMA / EVDO': 'No', 'GSM / CDMA / EVDO / LTE': 'Yes', 'CDMA / EVDO / LTE':'Yes','GSM / CDMA / HSPA / EVDO / LTE': 'Yes', 'GSM / HSPA / CDMA2000 / LTE': 'Yes', 'No cellular connectivity': 'No', 'HSPA / EVDO': 'No', 'GSM / CDMA / HSPA': 'No', 'CDMA / HSPA': 'No', 'GSM / CDMA2000': 'No', 'GSM / CDMA / HSPA / EVDO': 'No', 'GSM':'No', 'GSM / CDMA / HSPA / CDMA2000 / LTE': 'Yes', 'CDMA / HSPA / EVDO': 'No', 'CDMA': 'No', 'GSM / CDMA / EVDO': 'No', 'GSM / HSPA / EVDO': 'No', 'GSM / HSPA': 'No', 'CDMA / HSPA / EVDO / LTE': 'Yes', 'GSM / CDMA / UMTS / EVDO': 'No', 'GSM / CDMA / HSPA / LTE': 'Yes', 'GSM / UMTS / HSPA / LTE': 'Yes', 'CDMA / HSPA / LTE': 'Yes', 'HSPA': 'No', 'GSM / HSPA / LTE': 'Yes'}})
    E = Phones5['dimentions']
    print(E)
    for i in range (0, len(E)):
        if (len(re.findall('\d+\.\d+', E[i]))>0):
            E[i] = (re.findall('\d+\.\d+', E[i]))[-1]
    Phones5['Thickness'] = E
    Phones6 = Phones5.drop(['brand', 'network_technology', 'dimentions'], axis = 1)
    return Phones6
#GPRS

#EDGE

    

#----------------------- CHENGZHI ---------------------------
    


    
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
    approx_price_DOLLAR=clean_approx_price_EUR_data(data["approx_price_EUR"])
  
    #DATA --DARP
    #brand=clean_brand_data(data["brand"])
    #clean_data=clean_data(data)
    
    #network_technology=clean_network_technology_data(data["network_technology"])
    
    #DATA --CHENGZHI
    
    
    print('Data Cleaning is done.')
    pd.concat({"RAM":RAM,"primary_camera":primary_camera,"secondary_camera":secondary_camera,"loud_speaker":loud_speaker,"audio_jack": audio_jack, "GPS": GPS, "NFC":  NFC, "radio": radio, "battery": battery,"approx_price_DOLLAR":approx_price_DOLLAR}, axis = 1).to_csv("DATASET/Refined_Phone_Dataset.csv")
    #pd.concat(clean_data_darp, axis = 1).to_csv("DATASET/alisha_refined_phonedata.csv")
