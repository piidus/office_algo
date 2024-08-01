file_name = "apr-jun23-allotment.csv"
import pandas as pd

df = pd.read_csv(filepath_or_buffer=f'data/{file_name}', index_col='SL')
df = df[[ 'Name of the Institution','PP', 'I-IV', 'V', 'VI-VIII']]
convert_dict = {'PP': 'float', 'I-IV': 'float', 'V': 'float', 'VI-VIII': 'float'}
df = df.astype(convert_dict)
df = df.fillna(0)
# print(df)
def call_the_data(no):
    start = no-1
    db_process = df.iloc[start:, :]
    return db_process


if __name__ == '__main__':
    data = call_the_data(12)
    print(data)
    