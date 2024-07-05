import pandas as pd
file_name = 'MONTHLY RECEIVE FORMAT-24-25 - JUNE-24.csv'
df = pd.read_csv(filepath_or_buffer=f'data/{file_name}', index_col='khata no')
# df['status']='pending'
# df.to_csv(path_or_buf=file_name)
# Filtering the column
# print(df.columns)
df = df[['SCHOOL NAME','CATEGORY NAME', 'DAYS',  'PP MEAL', 'PRI MEAL','V MEAL', 'UPPRI MEAL','PP_ALLOT', 'I_IV ALLOT','V ALLOT','EXPEN PP', 'EXPEN PRI','EXPEN V',
         'PP_R_ALLOT', 'I-IV_R_ALLOT', 'V_R_ALLOT',  'PP-RICE-EXPEN','PRI-RICE-EXPEN','V -RICE-EXPEN', 'CCH', 'TAB BOYS']]

convert_dict = {'DAYS': 'Int64', 'PP MEAL': 'Int64', 'PRI MEAL':'Int64', 'V MEAL': 'Int64', 'UPPRI MEAL': 'Int64','PP_ALLOT': 'Int64', 'I_IV ALLOT': 'Int64',
                'V ALLOT':'Int64','PP_R_ALLOT':'float','I-IV_R_ALLOT':'float', 'V_R_ALLOT':'float', 'PP-RICE-EXPEN':'float','PRI-RICE-EXPEN':'float','V -RICE-EXPEN': 'float',  'CCH': 'Int64'}
df = df.astype(convert_dict)
# df['MME']=df['MME'].fillna(0)
df_filtered = df[(df['CATEGORY NAME']=='PRIMARY ONLY')] # & (df['TAB BOYS']=='DONE')]

df_filtered  = df_filtered.fillna(0)

# print(df_filtered.head(30))
# print(df)
def call_the_data(no):
    start = no-1
    db_process = df_filtered.iloc[45:46, :]
    # db_process = df_filtered[df_filtered['NAME TRGMDM'].isin(['SSK. GARAGARI', 'NABIN CHANDRA F P SCHOOL', 'MAHISGOTE F P SCHOOL',
                                                            #   'BANAMALIPUR F P SCHOOL', 'CHAKPANCHURIA F P SCHOOL', 'RAIGACHI FP SCHOOL'])]
    print(db_process)
    sch = (db_process)
    # print(type(sch))
    return sch
call_the_data(1)
# d= call_the_data(1)
# print(d['SCH NAME'])
# for i in range(1):
#     df.loc[1, 'status'] = 'com'
#     print(df.head())
#     df.to_csv(path_or_buf='MONTHLY DATA 23-24 - MAR-23.csv')