from bs4 import BeautifulSoup
import csv
from itertools import groupby
import requests
import regex as re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

artist = 'the+beatles'

PATH = "/Users/connorobrien/Documents/Coding/Resources/chromedriver" 
URL = 'https://www.hooktheory.com/theorytab/results?path=' + artist
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
lst = []
for a in soup.find_all('a', href=True):
    lst.append(a['href'])

lst_pages = []
for i in lst:
    if artist in i:
        lst_pages.append(i)
lst_pages = sorted(set(lst_pages))

lst_songs = []
for i in lst:
    if artist.replace('+','-') in i:
        lst_songs.append(i)

lst_songs = list(set(lst_songs))

for i in lst_pages[1:]:
    URL = 'https://www.hooktheory.com' + str(i)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    lst = []
    for a in soup.find_all('a', href=True):
        lst.append(a['href'])
    for i in lst:
        if "the-beatles" in i:
            lst_songs.append(i)

# Final list of artist's songs to be scrapped 
setlist = set(lst_songs)

# Empty lists for scrapped chord progressions and 
chord_list_final = []
key_list = []

# Scrapping chord progression data for each song
for song in setlist:
    
    chord_list_full = []
    title = song.replace('/theorytab/view/the-beatles/','').replace('-',' ')
    title = title.replace('%28','(').replace('%29',')').title()
    chord_list_full.append(title)
    
    print("Analyzing:",title)

    # Scrapping html data for a page with Selenium
    URL = 'https://www.hooktheory.com' + song
    PATH = '/Users/connorobrien/Documents/Coding/Resources/chromedriver'
    driver = webdriver.Chrome(PATH)
    driver.get(URL)
    element = driver.find_element_by_class_name('ng-isolate-scope')
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(10)
    src = driver.page_source
    driver.quit()

    # Getting the key
    keys = re.findall(r'(<tspan class="gotham">)([\w])(<\/tspan><\/div><div class="secondary">)(\w\w\w)(<\/div>)',src)
    sharp = re.findall(r'<div class="primary"><tspan class="gotham">([\w])<\/tspan><tspan class="scale-degrees" dx="0\.05ex">(.)<\/tspan><\/div><div class="secondary">(\w\w\w)<\/div>',src)
    if len(sharp) == 0:
        key = keys[0][1] + keys[0][3]
    else:    
        key = sharp[0][0] + sharp[0][1] + sharp[0][2]
    key_list.append(key)
    chord_list_full.append(key)

    ## Getting the main chords
    chords = re.findall(r'(<tspan class="times">([\w])<\/tspan>)?(<tspan class="times">)(\w)(<\/tspan>)(((<tspan class="times">)(\w)(<\/tspan>)(<\/text>))|(<\/text>))',src)
    chords_pos = re.finditer(r'(<tspan class="times">([\w])<\/tspan>)?(<tspan class="times">)(\w)(<\/tspan>)(((<tspan class="times">)(\w)(<\/tspan>)(<\/text>))|(<\/text>))',src)
    indices0 = [m.start(0) for m in chords_pos]

    chord_list = []
    for cl in chords:
        c = cl[1]+cl[3]+cl[8]
        chord_list.append(c.strip())

    ## Getting inversions/dominant/etc. (7, 64,54, etc.)
    mod1 = re.findall(r'<tspan class="gotham" xml:space="preserve">([\w])<\/tspan>', src)
    mod1_pos = re.finditer(r'<tspan class="gotham" xml:space="preserve">([\w])<\/tspan>', src)
    indices1 = [m.start(0) for m in mod1_pos]

    for i in indices1:
        idx = -1
        for j in indices0:
            if i < j:
                chord_list[idx] = chord_list[idx] + mod1[0]
                break
            else:
                idx +=1
        mod1.pop(0)      

    ## Sharp/Flat Chords
    mod2 = re.findall(r'<tspan class="scale-degrees">(b|#)<\/tspan><tspan class="times"', src)
    mod2_pos = re.finditer(r'<tspan class="scale-degrees">(b|#)<\/tspan><tspan class="times"', src)
    indices2 = [m.start(0) for m in mod2_pos]
    for i in indices2:
        idx = 0
        for j in indices0:
            if i - j < 0:
                chord_list[idx] = mod2[0]+ chord_list[idx]
                break
            else:
                idx +=1
        mod2.pop(0)

    ## Sus2/4, etc
    mod3 = re.findall(r'<tspan class="gotham">(...|....)<\/tspan>', src)
    mod3_pos = re.finditer(r'<tspan class="gotham">(...|....)<\/tspan>', src)
    indices3 = [m.start(0) for m in mod3_pos]

    for i in indices3:
        idx = -1
        for j in indices0:
            if i < j:
                chord_list[idx] = chord_list[idx] + mod3[0]
                break
            else:
                idx +=1
        mod3.pop(0)

    # Added tone chords
    mod4 = re.findall(r'<tspan class="gotham">(add)<\/tspan><tspan class="gotham">(\d)<\/tspan>', src)
    mod4_pos = re.finditer(r'<tspan class="gotham">(add)<\/tspan><tspan class="gotham">(\d)<\/tspan>', src)
    indices4 = [m.start(0) for m in mod4_pos]

    for i in indices4:
        idx = -1
        for j in indices0:
            if i < j:
                chord_list[idx] = chord_list[idx] + mod4[0][1]
                break
            else:
                idx +=1
        mod4.pop(0)

    # Remove consecutive chords
    chord_list_clean = [i[0] for i in groupby(chord_list)]
    
    # Chord scrapping completed
    chord_list_full = chord_list_full + chord_list_clean 
    chord_list_final.append(chord_list_full)

    
print('')
print(chord_list_final)

# Writing chord progression data to a csv file
name = artist.replace('+','_') + '_chordprogressiondata.csv'
with open(name,'w',newline = '') as fp:
    a = csv.writer(fp, delimiter = ',')
    a.writerows(chord_list_final)
