import math
import Levenshtein as Lev # see https://pypi.python.org/pypi/python-Levenshtein

#see https://stackoverflow.com/q/29233888/2583476
keyboard_cartesian = {'q': {'x':0, 'y':0}, 'w': {'x':1, 'y':0}, 'e': {'x':2, 'y':0}, 'r': {'x':3, 'y':0}, 't': {'x':4, 'y':0}, 'y': {'x':5, 'y':0}, 'u': {'x':6, 'y':0}, 'i': {'x':7, 'y':0}, 'o': {'x':8, 'y':0}, 'p': {'x':9, 'y':0}, 'a': {'x':0, 'y':1},'z': {'x':0, 'y':2},'s': {'x':1, 'y':1},'x': {'x':1, 'y':2},'d': {'x':2, 'y':1},'c': {'x':2, 'y':2}, 'f': {'x':3, 'y':1}, 'b': {'x':4, 'y':2}, 'm': {'x':5, 'y':2}, 'j': {'x':6, 'y':1}, 'g': {'x':4, 'y':1}, 'h': {'x':5, 'y':1}, 'j': {'x':6, 'y':1}, 'k': {'x':7, 'y':1}, 'l': {'x':8, 'y':1}, 'v': {'x':3, 'y':2}, 'n': {'x':5, 'y':2}, }
def euclidean_distance(a,b):
    X = (keyboard_cartesian[a]['x'] - keyboard_cartesian[b]['x'])**2
    Y = (keyboard_cartesian[a]['y'] - keyboard_cartesian[b]['y'])**2
    return math.sqrt(X+Y)
     
# words.txt is any list of words at one word per line.  I used SCOWL: http://app.aspell.net/create 

lines = [line.strip().lower() for line in open('words.txt')]
outfile=open("covfefe_list.txt",'w')
covfefe="covfefe"						# This is your trumpism
threshold=0.5							# Jaro-Winkler metric threshold: 0=completely different, 1=identical
alphabet="abcdefghijklmnopqrstuvwyz"
header="From\tTo\tEdits\tJaro-Winkler\tTotal Distance\tEdit list\n"
outfile.write(header)
for line in lines:
	total_dist=0
	editout=''
	d= Lev.distance(line,covfefe)
	j=Lev.jaro_winkler(line,covfefe)
	edits=Lev.editops(line,covfefe)
	if j>threshold:	
		print 'From \''+line+'\' to \''+covfefe+ '\' takes %d'%d+ ' edits. The J-W metric is %.3g'%j+' and the edits are:'
		outstring=line+'\t'+covfefe+'\t%d\t%.3g'%(d,j)
		for edit in edits:
			e=edit[0]
			if e=='delete':
				edittext='delete \''+ line[edit[1]] +'\' at %d'%(edit[1]+1)
			elif e=='insert':
				edittext='insert \''+covfefe[edit[2]]+ '\' at %d'%(edit[2]+1)
			else:#replace
				if line[edit[1]] in alphabet and covfefe[edit[2]] in alphabet: 
					dist=euclidean_distance(line[edit[1]],covfefe[edit[2]])
					total_dist+=dist
					edittext=edit[0]+' \''+line[edit[1]]+'\' at %d'%(edit[1]+1)+' with \''+covfefe[edit[2]]+'\' (distance %.3g)'%dist
				else:
					edittext=edit[0]+' \''+line[edit[1]]+'\' at %d'%(edit[1]+1)+' with \''+covfefe[edit[2]]+'\' (non-letter, distance ignored)'
			print '  '+edittext
			editout+=edittext+', '
		outstring+='\t%.3g\t'%total_dist+editout+'\n'	
		print '  total replacement distance: %.3g'%total_dist
		outfile.write(outstring)
outfile.close()

# The output format is tab-delimited and ready to import into a spreadsheet.
# Unless you want the list of edits to be split into multiple cells, make sure commas is not sleected as a delimiter