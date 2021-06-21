from flask import Flask
import pandas as pd
import requests
import re
import os

app = Flask(__name__)

url = "https://www.worldometers.info/coronavirus/"    # given data Source url


header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

data = requests.get(url, headers=header)

data = data.text                       # get data in text format

data = re.sub(r'<.*?>', lambda g: g.group(0).upper(), data)

dfs = pd.read_html(data)               # set of all the available dataframes


@app.route('/')
def get_csv_path():
    """ get latest coronavirus cases summary for one or more countries and it will give path where csv will get store"""
    for i in range(len(dfs)):
        columns = dfs[i].columns

        # saving a Pandas Dataframe as a CSV
        dfs[i].to_csv(f"{i+1}.csv", index=False, header=False)

        # skipping first 7 rows which is irrelevant
        df = pd.read_csv(f"{i+1}.csv", skiprows=7)

        # getting required no of columns from dataframe
        df.columns = columns
        df1 = df[['Country,Other', 'TotalCases', 'ActiveCases', 'TotalDeaths']]

        # Recovery Rate(Total Recovered/Total Cases)
        df1['Recovery Rate'] = df['TotalRecovered']/df['TotalCases']

        # Percentage of Population Infected(TotalCases / Population)
        df1['Percentage of Population Infected'] = (df['TotalCases']/df['Population'])*100
        df1.columns = ['CountryName',
                       'TotalCases',
                       'ActiveCases',
                       'TotalDeaths',
                       'RecoveryRate',
                       'PercentageOfPopulationInfected']
        df1.to_csv(f"{i+10}.csv", index=False)
    return os.getcwd()


if __name__ == '__main__':
    app.run(debug=True)
