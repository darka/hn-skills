from collections import defaultdict

import HTMLParser
import urllib2
import json
import operator
import re

alias = { 'js' : 'javascript' }

def parse_text(text, words, english_words):
  # Remove HTML tags
  text = re.sub(r'<[^>]*?>', '', text) # Do this properly next time
  words_new = set() 

  h = HTMLParser.HTMLParser()

  for word in text.split():
    word = word.lower().strip()
    word = word.strip('(){},.\"!?[]')

    word = h.unescape(word)

    if len(word) == 1 and not word.isalpha():
      continue

    if word in english_words:
      continue

    if word in alias:
      word = alias[word]

    if word:
      words_new.add(word)
  for word in words_new:
    words[word] += 1

def parse(contents, words, english_words):
  if 'text' in contents:
    parse_text(contents['text'], words, english_words)
  if 'children' in contents and len(contents['children']) > 0:
    for child in contents['children']:
      parse(child, words, english_words)
  
def top(words):
  words = words.items()
  words = sorted(words, key=operator.itemgetter(1), reverse=True)
  return words

def english_words(filename):
  f = open(filename, 'r')
  ret = set()
  for line in f.readlines():
    line = line.strip()
    if line:
      ret.add(line)
  return ret

def main():
  id = 7679422

  url = "https://hn.algolia.com/api/v1/items/{}".format(id)
  contents = urllib2.urlopen(url).read()
  contents = json.loads(contents)

  words = defaultdict(int)
  parse(contents, words, english_words('english.txt'))
  popular = top(words)

  for word, score in popular[:20]:
    print score, word

if __name__ == '__main__':
  main()
