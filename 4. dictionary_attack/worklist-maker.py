import string
import random
import itertools
'''
ahsan 1950 2050
khalid 
awfa
tuntun
'''

f = open('custom-wordlist.txt', 'w')
word = input('Enter word(s):')
p_list = list(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in word))))
for i in range(1950, 2050):
	for j in range(len(p_list)):
		for k in string.punctuation:
			word = p_list[j] + k + str(i) + '\n'
			f.write(word)
f.close()

