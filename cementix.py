import requests
import random
from bs4 import BeautifulSoup
from timeit import default_timer as timer
from datetime import timedelta

start = timer()

bestWord = ''
maxScore = 0.0
tested_words = []

def getSingular(word):
    return word[:-1] if 's' == word[-1] else word

def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

# Test the word and get its score
def getScore(word):
    url = 'https://cemantix.certitudes.org/score'
    result = requests.post(url, data={'word': word}).json()
    if 'score' not in result:
        print('Unknow word=', word)
        return -1.0
    return result['score']

# Obtain a semantic field list of the word
def getMotsCles(word):
    url='https://www.rimessolides.com/motscles.aspx?m=' + word
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    result = requests.post(url, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup.find_all("a", class_="l-black")

# Random word from file
def randomSearch():
    score = -1.0
    global maxScore, bestWord
    # We consider that a score of 30% is sufficient to start research around the lexical field
    while score < 0.3 :
        word = getSingular(random_line('words-full.txt'))
        if word in tested_words: continue
        score = getScore(word)
        if score > maxScore: 
            maxScore = score
            bestWord = word
        tested_words.append(word)
        print('word:', word, ' score:', score, ' bestWord:', bestWord, ' maxScore:', maxScore)
    return bestWord, maxScore

# Finding words from the lexical field
def findCemantix(word):
    global maxScore, bestWord
    motsCles = getMotsCles(word)
    for mot in motsCles :
        word = getSingular(mot.text)
        if word in tested_words: continue
        score = getScore(word)
        if score > maxScore : 
            maxScore = score
            bestWord = word
            if score == 1.0 : break
        tested_words.append(word)
        print('word cemantix:', word, ' score:', score, ' bestWord:', bestWord, ' maxScore:', maxScore)
    return bestWord, maxScore

# Initial phase
bestWord, maxScore = randomSearch()
print('########################################## Found word:', bestWord)
# Iterate over semantic words, otherwise try your luck with other random words
while maxScore < 1.0 :
    bestWord, maxScore = findCemantix(bestWord)
    print('New best word:', bestWord)
    if bestWord == '' : 
        print('######################### Debug - cest reparti pour un tour...')
        bestWord, maxScore = randomSearch()

end = timer()
print('Bingo!! word:', bestWord, ' found in ', timedelta(seconds=end-start))