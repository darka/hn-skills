import skills
import os

results_dir = 'results'

f_in = open('threads-lite.txt', 'r')
for line in f_in.readlines():
  line = line.strip()
  if not line: 
    continue

  year, month, id = line.split()
  filename = '{}-{}.txt'.format(year, month)
  f_out = open(os.path.join(results_dir, filename), 'w')
  #f_out.write('{} {}\n'.format(year, month))

  stats = skills.get_stats(id, 60)
  for word, score in stats['scores']:
    f_out.write('{} {}\n'.format(score, word))

  f_out.close()
