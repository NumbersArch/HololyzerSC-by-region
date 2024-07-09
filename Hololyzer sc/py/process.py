#!/usr/bin/env python
import html2text
import sys
import os
from os import listdir
from os.path import isfile, join
import pandas as pd

# Inputs
name = str(sys.argv[1]).strip()
if (name == ""): print("Empty list"); sys.exit(0)
names = name.split("~")
folder = sys.argv[2]
outputname = folder
if(folder == "Misc" and len(names) == 1): outputname = name

# Filenames
dname = "Currencies.txt"
vname = join("data", outputname + ".txt")
xname = join("data", outputname + ".csv")
pname = join("raw","html", folder)

# Paths
workingdirectory = os.path.dirname(os.path.realpath(__file__))
up1directory = os.path.dirname(workingdirectory)
datapath = join(up1directory, "data")
if not os.path.exists(datapath):
    os.makedirs(datapath)

# Reading and interpreting HTML files
fullarray = []; currencylist= []
print("Interpreting files....")
for n in names: 
	path = join(up1directory, pname, n + ".html")
	h = html2text.HTML2Text(); h.ignore_links = True
	htmlfile = open(path, 'r')
	html_string = htmlfile.read()    
	string = h.handle(html_string)
	string = string.split("Membership")[0].strip()
	string = string.split("円換算合計")[1].strip()
	string = string.replace("-\n","-\n\n")
	s_array = string.split("\n\n")
	b = ""
	count = 0
	sign = ""
	fstring = ""
	for s in s_array:
		count = count+1
		if count == 1:
			sign = s
		if count == 2:
			if(s.strip() == "-"):
				s = sign
			if(s.isnumeric()):
				s = sign
		
		if( "\\" in s):
			s = s.replace("\\", "")
			s = s.replace(",", "")
			b = b+"\t" + s
			fstring = fstring + b.strip() + "\n"
			b = ""
			count = 0
		else:
			b = b+"\t" + s
	fstring = fstring.split("----")[0].strip()
	fullstrings = fstring.split("\n")
	for f in fullstrings:
		a, curr, vala, valb, valc = f.split("\t")
		if(curr in currencylist):
			idex = currencylist.index(curr)
			a2, curr2, vala2, valb2, valc2 = fullarray[idex].split("\t")
			vala3 = int(vala2)+ int(vala); 
			valb3=float(valb2)+ float(valb); 
			valc3=float(valc2)+float(valc)
			fullarray[idex] = a2+"\t"+curr2+"\t"+str(vala3)+"\t"+str(valb3)+"\t"+str(valc3)
		else:
			currencylist.append(curr)
			fullarray.append(f)

# Getting a full list of currencies and their regions from Currencies.txt
currencypath = join(up1directory, dname)
cfile = open(currencypath, 'r')
currencytext = cfile.read()
cclist = currencytext.split("~ ")
countries = []; currencies = []
countrylist = [];
for c in cclist:
	c = c.strip()
	clist = c.split("\n")
	if len(clist) == 0:
		continue
	country = clist[0]
	clist.pop(0)
	if len(clist) == 0:
		continue
	countries.extend([country]*len(clist))
	countrylist.append(country)
	currencies.extend(clist)

# Matching currencies to region
regionlist = []
for f in fullstrings:
	#cdesignation, cname, cnumber, ctotal, cytotal = f.split("\t")
	cname = f.split("\t")[1]
	if cname in currencies:
		idex = currencies.index(cname)
		region = countries[idex]
	else:
		print("Unknown currency: " +currencyname)
		region = "Unknown"
	regionlist.append([region, f])
regionlist = sorted(regionlist,key=lambda x: (x[0],x[1]))

# Assembling the final string
summarystring = ""
finalstring = ""
totals = []
grandtotal = 0
for w in countrylist:
	regionstring = "~ "+w + " ~"
	total = 0
	for r in regionlist:
		if(r[0] == w):
			regionstring = regionstring+"\n"+r[1]
			total += float(r[1].split("\t")[4])
			
	if total != 0:
		finalstring = finalstring + "\n\n"+regionstring.strip()
		finalstring = finalstring + "\nTOTAL: " + str(total) 
	summarystring = summarystring + "\n"+w + "\t" + str(total)
	grandtotal += total; totals.append(total)	
summarystring = summarystring.strip()
summarystringarr = summarystring.split("\n")
totals = [round(100*x / grandtotal,2) for x in totals]
totalnet = sum(totals)
summarystringarrlvl2 = list(zip(summarystringarr,totals))
summarystring = ""
for sv in summarystringarrlvl2:
	summarystring = summarystring + "\n"+sv[0] +"\t" +str(sv[1])
summarystring2 = summarystring.strip() +"\n" + "Total: " + str(grandtotal)
headerstring = "Region\ttotal\tpercent"
summarystring2  = headerstring + "\n"+ summarystring2
finalstring = finalstring.strip()
finalstring = "~ "+folder+"\n"+summarystring2 + "\n\n------------------\n\n" + finalstring

# Printing final result
finalpath = join(up1directory,vname)
finalfile = open(finalpath, "w")
finalfile.write(finalstring)
finalfile.close()

# Printing as csv
df = pd.DataFrame()
summarystring = summarystring + "\n"+"Total" + "\t" + str(grandtotal) + "\t" + str(totalnet)
df["r1"] = summarystring.strip().split("\n")
headers = headerstring.split("\t")
df[headers] = df["r1"].str.split("\t", expand = True)
df.drop('r1', axis=1, inplace=True)
dfpath = join(up1directory, xname)
df.to_csv(dfpath, index=False)  




