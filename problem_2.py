import requests
import re
import pandas as pd
import os
# import lxml
# if "requests" gives error as -ModuleNotFoundError: No module named 'requests'
# then install it as- pip install requests
# ModuleNotFoundError: No module named 'pandas'
# pip install pandas


url = "https://www.worldometers.info/coronavirus/"


header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

data = requests.get(url, headers=header)

data = data.text

data = re.sub(r'<.*?>', lambda g: g.group(0).upper(), data)

dfs = pd.read_html(data)

def get_csv():
    for i in range(len(dfs)):
        columns = dfs[i].columns

        dfs[i].to_csv(f"{i+1}.csv", index=False, header=False)
        df = pd.read_csv(f"{i+1}.csv", skiprows=7)

        df.columns = columns
        df1 = df[['Country,Other', 'TotalCases', 'ActiveCases', 'TotalDeaths']]
        df1['Recovery Rate'] = df['TotalRecovered']/df['TotalCases']
        df1['Percentage of Population Infected'] = (df['TotalCases']/df['Population'])*100
        df1.columns = ['CountryName',
                       'TotalCases',
                       'ActiveCases',
                       'TotalDeaths',
                       'RecoveryRate',
                       'PercentageOfPopulationInfected']
        df1.to_csv(f"{i+10}.csv", index=False)
    return os.getcwd()