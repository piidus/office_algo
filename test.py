from data import call_the_data

def test(data):
    # print(data['SCH NAME'])
    for index, row in data.iterrows():
        try:
            print(row['SCH NAME'])
        except Exception as e:
            print(e)
d = call_the_data(3)
print(len(d))
test(d)