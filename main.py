import pandas as pd 

df = pd.read_json('fakeUsers.json', lines=True)
print(df)