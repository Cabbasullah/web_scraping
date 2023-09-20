import requests
from bs4 import BeautifulSoup
import pandas as pd

class Song_Details():
    def fetching_songs(self):
        url = 'https://genius.com/'

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            song_details = soup.find_all('a', class_='PageGriddesktop-hg04e9-0 ChartItemdesktop__Row-sc-3bmioe-0 qsIlk')

            song_data = []
            for song in song_details:
                song_name = song.find('div', class_='ChartSongdesktop__Title-sc-18658hh-3 fODYHn').text.strip()
                singer_name = song.find('h4', class_='ChartSongdesktop__Artist-sc-18658hh-5 kiggdb').text.strip()
                link = song['href']

                song_data.append([song_name, singer_name, link])

            framed_data = pd.DataFrame(song_data, columns=['Song', 'Singer', 'Link'])

            data_file = 'songs_and_singers.csv'
            framed_data.to_csv(data_file, index=False)

            print(f"Data has been stored in {data_file}")
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
song_details = Song_Details()
song_details.fetching_songs()
