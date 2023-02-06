import requests
import pandas as pd
import numpy as np

number_of_pages = 100
#number_of_ads = number_of_pages * per_page

job_title = ["'Python' and 'Django' and 'Flask'"]
data=[]
df1 = pd.DataFrame()

for job in job_title:
	for i in range(number_of_pages):
		url = 'https://api.hh.ru/vacancies'
		par1 = {'text':job, 'area':'1','per_page':'10', 'page':i}
		r = requests.get(url, params=par1)
		e = r.json()
		data.append(e)
		par2 = {'text':job, 'area':'2', 'per_page':'10', 'page':i}
		r = requests.get(url, params=par2)
		e = r.json()
		data.append(e)
		vacancy_details = data[0]['items'][0].keys()
		df = pd.DataFrame(columns= list(vacancy_details))
		ind = 0
		for i in range(len(data)):
			for j in range(len(data[i]['items'])):
				df.loc[ind] = data[i]['items'][j]
				ind+=1
# расщепление колонок для получения информации, требуемой в задании
df1["company"] =(df['employer'].apply(lambda x: x.get("name") if isinstance(x,dict) else np.nan))
df1["href"] =(df['employer'].apply(lambda x: x.get("url") if isinstance(x,dict) else np.nan))
df1["salary_from"] =(df['salary'].apply(lambda x: x.get("from") if isinstance(x,dict) else np.nan))
df1["salary_to"] =(df['salary'].apply(lambda x: x.get("to") if isinstance(x,dict) else np.nan))
df1["salary_currency"] =(df['salary'].apply(lambda x: x.get("currency") if isinstance(x,dict) else np.nan))
df1["town"] =(df['area'].apply(lambda x: x.get("name") if isinstance(x,dict) else np.nan))
#print(df1[['href', 'salary_from', 'salary_to', 'salary_currency', 'company', 'town']])
csv1_name = job+"all"+".csv"
df1.to_csv(csv1_name)
df2 = df1[df1['salary_currency'] == 'USD']
csv2_name = job+"usd"+".csv"
df2.to_csv(csv2_name)
