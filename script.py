import uuid
import requests
from bs4 import BeautifulSoup

import pandas as pd

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.co.uk/ssc-napoli/kader/verein/6195/plus/1/galerie/0?saison_id=2019"
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

Numbers = pageSoup.find_all("div", {"class": "rn_nummer"})
Images = pageSoup.find_all("img", {"class": "bilderrahmen-fixed"})
Players = pageSoup.find_all("a", {"class": "spielprofil_tooltip"})
Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})


ImageList = []
NumberList = []
PlayersList = []
ValuesList = []


with open('players.txt', 'w') as players:
    for i in range(len(Players)):
        if Players[i].find_parent("span", {"class": "hide-for-small"}) is not None:
            PlayersList.append(Players[i].text)
    for i in range(len(Numbers)):
        NumberList.append(Numbers[i].text)
        ImageList.append(Images[i].attrs['src'])
        ValuesList.append(Values[i].text)

df = pd.DataFrame({"Numbers": NumberList, "Images": ImageList,
                   "Names": PlayersList, "Values": ValuesList})

df.head()

df.to_csv('napoli.csv')


df = pd.read_csv('napoli.csv', sep='\s*,\s*', encoding='UTF-8')
print(df.columns.tolist())
with open('inserts.sql', 'w') as inserts:
    for index, row in df.iterrows():
        number = row['Numbers']
        image = row['Images'].replace('/small/', '/medium/')
        name = row['Names']
        value = row['Values']
        print(
            f'insert into football_player(id,name,transfer_value,player_number,player_image_url) values({uuid.uuid4()}, \'{name}\', \'{value}\', \'{number}\', \'{image}\');\n')
        inserts.write(
            f'insert into football_player(id,name,transfer_value,player_number,player_image_url) values({uuid.uuid4()}, \'{name}\', \'{value}\', \'{number}\', \'{image}\');\n')
