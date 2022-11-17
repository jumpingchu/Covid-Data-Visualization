from datetime import datetime
from pathlib import Path
import pandas as pd
import datefinder

def get_data_list(path):
    data_dir = Path(path)
    data_list = [f for f in data_dir.glob('*.csv')]
    return data_list

def parse_date(data_path) -> str:
    date_time = [t for t in datefinder.find_dates(str(data_path))]
    date_str = datetime.strftime(date_time[0], '%Y.%m.%d')
    return date_str

def load_and_process_data_from_path(data_path):
    df = pd.read_csv(data_path)
    if 'Country_Region' not in df.columns:
        df.rename(columns={'Country/Region': 'Country_Region'}, inplace=True)
    df.loc[df['Country_Region'] == 'Mainland China', 'Country_Region'] = 'China'
    df.loc[df['Country_Region'] == 'Korea, South', 'Country_Region'] = 'South Korea'
    df.loc[df['Country_Region'] == 'Taiwan*', 'Country_Region'] = 'Taiwan'
    return df

def extract_confirmed(data_path):
    date_str = parse_date(data_path)
    df = load_and_process_data_from_path(data_path)
    df = (df
        .loc[:, ['Country_Region', 'Confirmed']]
        .rename(columns={'Confirmed': date_str})
        .groupby('Country_Region', as_index=False).sum(date_str)
    )
    return df

def extract_lat_long(data_path):
    df = load_and_process_data_from_path(data_path)
    df = df.loc[:, ['Country_Region', 'Lat', 'Long_']]
    return df

def make_flag_url(country_name):
    base_url = 'https://cdn.countryflags.com/thumbs/{}/flag-800.png'
    country_name = country_name.lower().replace(' ', '-')
    if country_name == "us":
        country_name = 'united-states-of-america'
    if country_name == "czechia":
        country_name = 'czech-republic'
    if country_name == "cote-d'ivoire":
        country_name = 'cote-d-ivoire'
    flag_url = base_url.format(country_name)
    return flag_url