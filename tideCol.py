# Dependency:
#   Anaconda3
#   Python3.7

import pandas
import re

df = pandas.read_csv('Phones_Refined.csv')

# Column: SIM
sim_column_list = list(df['SIM'])

# To check all individual values.
# sim_set = set(sim_column_list)
# print(sim_set)

# Count the different rows.
single_count = 0
dual_count = 0
triple_count = 0
# mini_count = 0
# micro_count = 0
# nano_count = 0
# electronic_count = 0
no_count = 0
yes_count = 0
other_count = 0

# Micro, Mini, Nano, Electronic all belongs to the Single.
for i in range(len(sim_column_list)):
    cell = str(sim_column_list[i])
    if 'Dual' in cell:
        sim_column_list[i] = 'Dual'
        dual_count += 1
    elif 'Triple' in cell:
        sim_column_list[i] = 'Triple'
        triple_count += 1
    elif 'Yes' in cell:
        sim_column_list[i] = 'Yes'
        yes_count += 1
    elif 'No' in cell:
        sim_column_list[i] = 'No'
        no_count += 1
    elif 'Single' in cell or 'Mini' in cell or \
        'Micro' in cell or 'Nano' in cell or 'Electronic' in cell:
        sim_column_list[i] = 'Single'
        single_count += 1
    else:
        sim_column_list[i] =  'other'
        other_count += 1

#print(sim_column_list)
print('Single:', single_count, 'Dual:', dual_count, \
    'Triple:', triple_count, 'No:', no_count, \
    'Yes:', yes_count, 'Other:', other_count)

# Column: desplay_resolution
display_size = []
screen_to_body_ratio = []
display_column_list = list(df['display_resolution'])
for i in range(len(display_column_list)):
    cell = str(display_column_list[i])

    inch = str(re.findall('.*inches', cell))
    inch = inch.replace(' inches', '')
    display_size.append(inch)

    ratio = str(re.findall('~.*\%', cell))
    ratio = ratio.replace('~', '')
    ratio = ratio.replace('%', '')
    screen_to_body_ratio.append(ratio)


# Column: OS
os_column_list = list(df['OS'])

android_count = 0
windows_count = 0
bada_count = 0
tizen_count = 0
blackberry_count = 0
symbian_count = 0
ios_count = 0
empty_count = 0
other_os_count = 0

# To check all individual values.
# os_set = set(os_column_list)
# print(os_set)

os_list = []
for i in range(len(os_column_list)):
    cell = str(os_column_list[i])
    if 'Android' in cell:
        os_list.append('Android')
        android_count += 1
    elif 'Windows' in cell or 'Microsoft' in cell:
        os_list.append('Windows')
        windows_count += 1
    elif 'Bada' in cell:
        os_list.append('Bada')
        bada_count += 1
    elif 'Tizen' in cell:
        os_list.append('Tizen')
        tizen_count += 1
    elif 'BlackBerry' in cell:
        os_list.append('BlackBerry')
        blackberry_count += 1
    elif 'Symbian' in cell:
        os_list.append('Symbian')
        symbian_count += 1
    elif 'iOS' in cell:
        os_list.append('iOS')
        ios_count += 1
    elif 'nan' == cell:
        os_list.append('')
        empty_count += 1
    else:
        os_list.append('Other')
        other_count += 1

print('Andorid:', android_count, 'Windows:', windows_count, 'Bada:', bada_count, \
      'Tizen:', tizen_count, 'BlackBerry:', blackberry_count, 'Symbian:', symbian_count, \
      'iOS:', ios_count, 'Empty:', empty_count, 'Other:', other_count)

output_df = pandas.DataFrame.from_items([
    ('SIM', sim_column_list),
    ('display_size', display_size),
    ('screen_to_body_ratio', screen_to_body_ratio),
    ('OS', os_list)
    ])
print(output_df)
output_df.to_csv('./col_sim_display_os.csv')
print('Data export to: ./col_sim_display_os.csv')
