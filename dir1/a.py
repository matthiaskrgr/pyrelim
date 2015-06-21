#/usr/bin/python

# pyrelim - a stupid implementation of relative import paths for python
# Copyright (C) 2015 Matthias Krüger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



# problem:
# we have
#
#	 root_dir
#	 ├──dir1
#	 │  └── a.py
#	 └──dir2
#	    └── b.py
# and we want to "import b" (b.py) inside a.py while keeping root_dir untouched 


import os
import sys


if (sys.argv[0][0] == "/") or (sys.argv[0][0] == "~") : # assume absolute paths
	fullScriptPath = sys.argv[0]  # full script path from FS root
else:
	fullScriptPath = os.getcwd() + "/" + sys.argv[0]


fullScriptPath = fullScriptPath.replace("/./","/")  # fix path if we launch script via "./script.."

DIRS_WE_HAVE_TO_GO_DOWN = 2 # basically, the dir "./dir2" is in  (needs to be adjusted for other trees)

repoRoot = fullScriptPath.split("/")[:-DIRS_WE_HAVE_TO_GO_DOWN] # the root dir of the repo, since script is root_dir/dir2/script.py

if (sys.argv[0].split("/", 1)[0] == ".."): # ../{,../}whatever.py
	dirsWeGoDown = sys.argv[0].rsplit("/", 1)[0] + "/"

	path=[] # awful way to get rid of ".."
	for i in repoRoot:
		if (i != ".."):
			path.append(i)

	number_of_dotslashes = int((len(dirsWeGoDown)/3)) # how many "../"s do we have?; divide by 3 bc "../" == 3 chars

	import_path = "/".join(path) + "/../"*number_of_dotslashes +  "../dir2" # the final path 
else:
	import_path = "/".join(repoRoot)  + "/dir2/"

sys.path.append(import_path)


import b

b.Foo.test("Carrots") # expected output: "It works!"


"""
tested:

python3.4 a.py
python3.4 ./a.py
python3.4 /absolute/path/dir1/a.py
python3.4 ~/some/dir/dir1/a.py
python3.4 some/folder/dir1/a.py
python3.4 ../../a.py
python3.4 ../../../../a.py
"""
