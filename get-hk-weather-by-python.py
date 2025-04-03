#import io
import json, pandas as pd, requests

"""
api_url = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType={}&rformat=csv&station={}"
response = requests.get(api_url)

if response.status_code == 200:
    file_like_object = io.BytesIO(response.content)
    #print(response.content)
    df = pd.read_csv(file_like_object, skiprows=3, header=None, names=["year","month","day","value","data_completeness"])
    df.dropna(inplace=True)
    print(df.info())
"""

dict_data_type = {
    "CLMTEMP": "Daily Mean Temperature",
    "CLMMAXT": "Daily Maximum Temperature",
    "CLMMINT": "Daily Minimum Temperature"
}
dict_station = {
    "CCH": "Cheung Chau",
    "CWB": "Clear Water Bay",
    "HKA": "Hong Kong International Airport",
    "HKO": "Hong Kong Observatory",
    "HKP": "Hong Kong Park",
    "HKS": "Wong Chuk Hang",
    "HPV": "Happy Valley",
    "JKB": "Tseung Kwan O",
    "KLT": "Kowloon City",
    "KP": "King's Park",
    "KSC": "Kau Sai Chau",
    "KTG": "Kwun Tong",
    "LFS": "Lau Fau Shan",
    "NGP": "Ngong Ping",
    "PEN": "Peng Chau",
    "PLC": "Tai Mei Tuk",
    "SE1": "Kai Tak Runway Park",
    "SEK": "Shek Kong",
    "SHA": "Sha Tin",
    "SKG": "Sai Kung",
    "SKW": "Shau Kei Wan",
    "SSH": "Sheung Shui",
    "SSP": "Sham Shui Po",
    "STY": "Stanley",
    "TC": "Tate's Cairn",
    "TKL": "Ta Kwu Ling",
    "TMS": "Tai Mo Shan",
    "TPO": "Tai Po (Conservation Studies Centre)",
    "TU1": "Tuen Mun Children and Juvenile Home",
    "TW": "Tsuen Wan Shing Mun Valley",
    "TWN": "Tsuen Wan",
    "TY1": "New Tsing Yi Station",
    "TYW": "Pak Tam Chung (Tsak Yue Wu)",
    "VP1": "The Peak",
    "WGL": "Waglan Island",
    "WLP": "Wetland Park",
    "WTS": "Wong Tai Sin",
    "YCT": "Tai Po (Yuan Chau Tsai Park)",
    "YLP": "Yuen Long Park"
}

list_data_type = dict_data_type.keys()
list_station = dict_station.keys()
list_data = []

for data_type in list_data_type:

    for station in list_station:

        api_url = f"https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType={data_type}&rformat=json&station={station}"
        response = requests.get(api_url)

        if response.status_code == 200:
            result = response.json()
            result_data = result["data"]
            print(f"processing now: {dict_station[station]} - {dict_data_type[data_type]}")
            #print(result_data)
            for subset in result_data:
                subset.extend([dict_station[station],dict_data_type[data_type]])
                #print(subset)
            list_data.extend(result_data)
            #print(list_data)
            #print(header)
            #data_values = response.json().values()
#    df = pd.read_csv(file_like_object, skiprows=3, header=None, names=["year","month","day","value","data_completeness"])
#    df.dropna(inplace=True)
#    print(df.info())

df = pd.DataFrame(list_data,columns=["year","month","day","value","data_completeness","station","data_type"])
#df.dropna(inplace=True)
print(df.info())
df = df.loc[df["data_completeness"]!=""]
print(df.info())
df.to_csv("hk-weather-mean-max-min-temp.csv", index=False)

#df = pd.read_json("https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=CLMMAXT&rformat=csv&station=CCH")
#df.info()