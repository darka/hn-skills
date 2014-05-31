from collections import defaultdict

import HTMLParser
import urllib2
import json
import operator
import re

alias = { 'js' : 'javascript', 'angular' : 'angularjs' }

def parse_text(text, words, common_words):
  # Remove HTML tags
  text = re.sub(r'<[^>]*?>', ' ', text) # Do this properly next time
  text = text.replace('\\n', ' ')
  words_new = set() 

  h = HTMLParser.HTMLParser()

  for word in text.split():
    word = word.lower().strip()
    word = word.strip('(){},.\"!?[]:')

    word = h.unescape(word)

    if len(word) == 1 and not word.isalpha():
      continue

    if word in common_words:
      continue

    if word in alias:
      word = alias[word]

    if word:
      words_new.add(word)
  for word in words_new:
    words[word] += 1

def parse_json_recursively(contents, words, common_words):
  if 'text' in contents:
    parse_text(contents['text'], words, common_words)
  if 'children' in contents and len(contents['children']) > 0:
    for child in contents['children']:
      parse_json_recursively(child, words, common_words)
  
def top(words):
  words = words.items()
  words = sorted(words, key=operator.itemgetter(1), reverse=True)
  return words

def read_common_words(filename):
  f = open(filename, 'r')
  ret = set()
  for line in f.readlines():
    line = line.strip()
    if line and line[0] != '#':
      ret.add(line)
  return ret

def retrieve_json(url):
  contents = urllib2.urlopen(url).read()
  contents = json.loads(contents)
  return contents

def parse(contents, limit=20):
  words = defaultdict(int)
  parse_json_recursively(contents, words, read_common_words('english.txt'))
  popular = top(words)
  return popular[:limit]

def get_stats(id):
  ret = {}
  url = "https://hn.algolia.com/api/v1/items/{}".format(id)
  contents = retrieve_json(url)
  ret['title'] = contents['title']

  popular = parse(contents)
  ret['scores'] = popular
  return ret

def print_stats(stats):
  print(stats['title'])
  for word, score in stats['scores']:
    print(score, word)

def main():
  ids = [5803767]
  for id in ids:
    print_stats(get_stats(id))

if __name__ == '__main__':
  main()
