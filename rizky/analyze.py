__author__ = 'Rizky Solechudin'

import xlrd #import library pembaca excel
import math
import os
filename = "../jester-data-100.xls"

def checkFile(filename):
	if os.path.isfile(filename):
		print "File: ",filename
	else:
		print "Failed to open file"

def getData(filename):
	book = xlrd.open_workbook(filename) #open file jester
	sh = book.sheet_by_index(0) #masukkan isi file jester matrix sh
	return sh

dataTemp = getData(filename)
COLS_COUNT = dataTemp.ncols
ROWS_COUNT = dataTemp.nrows
COLS_COUNT = COLS_COUNT
ROWS_COUNT = ROWS_COUNT - 2 #perbaikan perhitungan total baris pada file jester

def getRatingTemp (user,item): 
	return dataTemp.row(user)[item].value #return value dari matrix sh

data = [[0 for x in range(COLS_COUNT)] for x in range(ROWS_COUNT)]

for x in range(ROWS_COUNT): #masukkan data jester kedalam array
	for y in range(COLS_COUNT):
		data[x][y] = getRatingTemp(x,y)

def getRating (user,item): 
	return data[user][item]

def getItem(n): #get item yang pernah dirating user n
	A = []
	for i in range (1,COLS_COUNT):
		if(getRating(n,i) != 99):
			A.append(i)
	return A

def getItemBersama(u,v): #get item yang sama-sama pernah dirating user u dan user v
	A = []
	for i in range(1,COLS_COUNT):
		if(getRating(u,i) != 99 and getRating(v,i) != 99):
			A.append(i)
	return A

def getHole(n):
	A = []
	for i in range(1,COLS_COUNT):
		if(getRating(n,i) == 99):
			A.append(i)
	return A

def getNeighbors(n): #get neighbors user n berdasarkan kesamaan item dari fungsi getitem(n)
	A = getItem(n)
	B = []
	found = 0
	for i in range(ROWS_COUNT):
		found = 0
		if(i != n):
			for j in A:
				if(getRating(i,j) != 99): #jika kesamaan item sudah != 0, maka user i menjadi neighbor user n
					found = 1
					break
			if(found == 1):
				B.append(i)
	return B

def getAverageRating(n): #get rata-rata rating dari user n
	A = getItem(n)
	u = len(A)
	p = 0.0
	for i in A:
		p = p + getRating(n,i)
	p = p / u
	return p

def getSim(n,o): #get similaritas antara user n dan user o
	rBot1 = 0.0
	rBot2 = 0.0
	rTop = 0.0
	rBot = 0.0
	rAvg1 = getAverageRating(n)
	rAvg2 = getAverageRating(o)
	y = getItemBersama(n,o)
	for i in y:
		r1 = getRating(n,i)
		r1 = r1 - rAvg1
		r2 = getRating(o,i)
		r2 = r2 - rAvg2
		r3 = r1 * r2
		r4 = r1 ** 2
		r5 = r2 ** 2
		rTop = rTop + r3
		rBot1 = rBot1 + r4
		rBot2 = rBot2 + r5
	rBot = math.sqrt(rBot1 * rBot2)
	return rTop/rBot 

def sortSims(sims): #fungsi quicksort untuk mendapatkan top similarity
	if(len(sims) > 1):
		pivotIndex = len(sims) / 2
		smallerItems = []
		largerItems = []
		for i, val in enumerate(sims):
			if i != pivotIndex:
				if val < sims[pivotIndex]:
					smallerItems.append(val)
				else:
					largerItems.append(val)
		sortSims(smallerItems)
		sortSims(largerItems)
		sims[:] = smallerItems + [sims[pivotIndex]] + largerItems
	return sims

def getPredictedRating(n,i): #get prediksi rating antara user n dengan item i
	avgN = getAverageRating(n)
	neighbors = getNeighbors(n)
	top = 0.0
	totalTop = 0.0
	bot = 0.0
	totalBot = 0.0
	for m in neighbors:
		sim = getSim(n,m)
		if(getRating(m,i) != 99 ):
			top = sim * (getRating(m,i) - getAverageRating(m))
			totalTop = totalTop + top
		bot = sim
		if(sim < 0):
			bot = bot * -1
		totalBot = totalBot + bot
	return avgN + totalTop/totalBot 

def main():
	print checkFile(filename)
	print "Total kolom: ",COLS_COUNT
	print "Total baris: ",ROWS_COUNT
	for i in range(ROWS_COUNT): 
		for j in range(1,COLS_COUNT):
	 		print "User " ,i,", Item ", j, " : ", getPredictedRating(i,j) #get semua predicted rating yang ada
 
main()