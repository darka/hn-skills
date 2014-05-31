import skills
import os
import sys

results_dir = 'results'

filename = sys.argv[1]

f_in = open(filename, 'r')
for i, line in enumerate(f_in.readlines()):
  line = line.strip()
  if not line: 
    continue

  year, month, id = line.split()
  print year, month
  filename = '{}-{}-{}.txt'.format(i, year, month)
  f_out = open(os.path.join(results_dir, filename), 'w')
  #f_out.write('{} {}\n'.format(year, month))

  stats = skills.get_stats(id, 60)
  for word, score in stats['scores']:
    f_out.write('{} {}\n'.format(score, word))

  f_out.close()
