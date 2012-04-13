import os, subprocess

files = os.listdir(".")
for f in files:
	if '.ps' in f:
		subprocess.call(['sh', 'convert.sh', f.split('.ps')[0]])
