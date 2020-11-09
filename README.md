# Using Markov Chains to Generate Chord Progressions in the Style of The Beatles

This repository contains a personal project that generates chord progressions in the style of The Beatles. It originated as a project for my undergraduate Linear Algebra course at Colorado College in 2013. 

There are two main parts of this project, each of which are separated into their own python file. 

The first file, called Chord_Scraping.py, uses dynamic web scraping to collect data about The Beatles chord progressions from HookTheory.com's Theory Tab. Theory Tab contains over 13,000 chord progressions in an interactive, difficult to web-scrape interface. The program writes a 'csv' file with the name, key, and chord progressions in each song from the given artist.   
<br>

<center><img src="https://www.hooktheory.com/images/controllers/press/TT-1.jpg"></center>
<br>


The second file, called Chord_Analysis.py, reads in a csv file of chord progression data (like the one from Chord_Scraping.py) and analyzes it so it can generate chord progressions that are in a similar style. In a general sense, this program analyzes the chord movements of chord progression from The Beatles, keeping track of what types of chord movements they typically make. 

For example, if they're writing in the key of C major, and they just played a E minor chord, what chord would The Beatles tend to choose next? The data shows they'll likely move to A minor, D minor seventh, or G major. 
<p align="center">
  <img src='https://raw.githubusercontent.com/connorobrien/BeatlesStyleChordProgressions/main/Em_in_C_probabilities.png' width="700">
</p>
<br>
This file keeps track of all of the typical chord movements of The Beatles a 'transition state matrix', which in layperson's terms is a table of numbers that can be used to find the probability of a next chord given a current chord. This method allows for 'chaining' of chord predictions (i.e. Markov Chains), which allows it to generate full chord progressions. As its set up right now, Chord_Scraping.py will produce ten chord progressions in the style of The Beatles in both a major and minor key. I've included an existing csv with the web-scraped chord progression data for The Beatles, named 'the_beatles_chordprogressiondata.csv'.   

<h3>Running This Program</h3>

To run this program, you'll need to download Chord_Analysis.py and Chord_Scraping.py, and potentially 'the_beatles_chordprogressiondata.csv' if you'd like to save yourself the trouble of web-scraping.

The modules necessary to run these two files are common, many of which are default libraries. You'll need:

<ul>
<li>Beautiful Soup (bs4)</li>
<li>collections</li>
<li>csv</li>
<li>numpy</li>
<li>pandas</li>
<li>random</li>
<li>requests</li>
<li>regex</li>
<li>selenium with Chrome Driver</li>
<li>time</li>
</ul>

To run Chord_Scraping.py, the only adjust you'll need to make it to set the path of your Selenium Chrome Driver as the PATH in line 12. You can also change the artist in line 10 to scrape chord progressions from other artists present in Hook Theory's Theory Tab. 

To run Chord_Analysis.py, you'll need to specify the path of the csv file with chord progression data, such as the one included in this repository. 

<h3>Some Examples</h3>

As the program is set up currently, it outputs ten chord progressions in both a major and minor key in the style of The Beatles. Below is an example of this output.

<p align="center">
  <img src='https://raw.githubusercontent.com/connorobrien/BeatlesStyleChordProgressions/main/Output_Example.png' width="500">
</p>

There's a lot that goes into a Beatles-style sound, and the chord progression is just one part of it. Many of their top songs (such as Hey Jude or Paperback Writer) feature simply traditional pop chord progressions, while others (such as Martha My Dear) feature more 'interesting' and 'colorful' chords. Generally, I'll find 2-3 chord progressions for every ten generated that work well and carry a stylistic influence of the beatles.

From the output above, I personally found the fourth major key chord progression and the third minor key chord progression sounded the best. 

[Click here to take a listen to these chord progressions, each of which I added a "Beatles" style rhythmic movement.](soundcloud.com)
