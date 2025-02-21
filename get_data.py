import requests
from bs4 import BeautifulSoup
import os
import re

with open('keys.txt','r') as f:
    keys = f.readlines()

API_TOKEN = keys[5]

def requestArtistInfo(artist, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist}
    response = requests.get(search_url, data=data, headers=headers)
    return response

def requestSongURL(artist):
    page = 1
    songs = []
    max_songs = 1000
    
    while True:
        try:
            response = requestArtistInfo(artist, page)
            response.raise_for_status()
            json = response.json()
            
            if 'response' not in json or 'hits' not in json['response']:
                break
            
            song_info = [
                hit for hit in json['response']['hits']
                if artist.lower() in hit['result']['primary_artist']['name'].lower()
            ]
            
            if not song_info:
                break
            
            new_songs = 0
            for song in song_info:
                url = song['result']['url']
                if url not in songs:
                    songs.append(url)
                    new_songs += 1
                    if len(songs) >= max_songs:  # Check if we've reached the limit
                        print(f"Reached {max_songs} songs limit.")
                        return songs[:max_songs]  # Return only first 100 songs
            
            if new_songs == 0:
                break
            
            page += 1
            print(f"Found {len(songs)} songs by {artist} so far...")
            
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            break
        except KeyError as e:
            print(f"Unexpected response format: {e}")
            break
    
    print(f"Completed fetching songs for {artist}. Total: {min(len(songs), max_songs)}")
    return songs  

def getLyrics(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
        html = BeautifulSoup(page.text, 'html.parser')
        
        lyrics_div = html.find('div', class_='Lyrics-sc-1bcc94c6-1 bzTABU')
        if not lyrics_div:
            print(f"Lyrics not found for URL: {url}")
            return ""
        
        lyrics = lyrics_div.get_text()
        
        lyrics = os.linesep.join([s.strip() for s in lyrics.splitlines() if s.strip()])
        
        return lyrics
    
    except requests.RequestException as e:
        print(f"Error fetching page: {url}. Error: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error while processing URL: {url}. Error: {e}")
        return ""

def writeToFile(artist):
    # Create lyrics directory if it doesn't exist
    os.makedirs('lyrics', exist_ok=True)
    
    with open('lyrics/' + artist + '.txt', 'wb') as f:
        urls = requestSongURL(artist)
        print(f"Processing {len(urls)} songs...")
        for url in urls:
            lyrics = getLyrics(url)
            if lyrics:  # Only write if lyrics were found
                f.write(lyrics.encode("utf8"))
                f.write(b'\n\n')  # Add spacing between songs

artist = input("Name The Artist: ")
writeToFile(artist)