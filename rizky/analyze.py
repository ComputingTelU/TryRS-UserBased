import xlrd #import library pembaca excel
import math
import os

# def getData():
# 	book = xlrd.open_workbook("jester-data-1.xls") #open file jester
# 	sh = book.sheet_by_index(0) #masukkan isi file jester matrix sh
# 	return sh

Data = [[0 for x in range(6)] for x in range(6)]
Data[0][0] = 2
Data[0][3] = 4
Data[0][4] = 5
Data[1][0] = 5
Data[1][2] = 4
Data[1][5] = 1
Data[2][2] = 5
Data[2][4] = 2
Data[3][1] = 1
Data[3][3] = 5
Data[3][5] = 4
Data[4][2] = 4
Data[4][5] = 2
Data[5][0] = 4
Data[5][1] = 5
Data[5][3] = 1

if os.path.isfile("jester-data-1.xls"):
	print "ganteng"
else:
	print "fail"

def getRating (user,item): 
	return Data[user][item]


# def getRating (user,item): 
# 	return data.row(user)[item].value #return value dari matrix sh

# data = getData()

print getRating(4,0)

def getItem(n): #get item yang pernah dirating user n
	A = []
	for i in range (0,6):
		if(getRating(n,i) != 0):
			A.append(i)
	return A

print getItem(1)
print len(getItem(1))

def getItemBersama(u,v):
	A = []
	for i in range(0,6):
		if(getRating(u,i) != 0 and getRating(v,i) != 0):
			A.append(i)
	return A

def getHole(n):
	A = []
	for i in range(0,6):
		if(getRating(n,i) == 0):
			A.append(i)
	return A

def getNeighbors(n): #get neighbors user n berdasarkan kesamaan item dari fungsi getitem(n)
	A = getItem(n)
	B = []
	found = 0
	for i in range(0,6):
		found = 0
		if(i != n):
			for j in A:
				if(getRating(i,j) != 0): #jika kesamaan item sudah != 0, maka user i menjadi neighbor user n
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
	for i in y: #rumus gan
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
	return rTop/rBot #rumus gan

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

def getPredictedRating(n,i):
	avgN = getAverageRating(n)
	neighbors = getNeighbors(n)
	top = 0.0
	totalTop = 0.0
	bot = 0.0
	totalBot = 0.0
	for m in neighbors:
		sim = getSim(n,m)
		bot = sim
		if(getRating(m,i) != 0 ):
			top = sim * (getRating(m,i) - getAverageRating(m))
			totalTop = totalTop + top
		if(sim < 0):
			bot = sim * -1
		totalBot = totalBot + bot
	return avgN + totalTop/totalBot 

n = 4
holeItems = getHole(n)
for i in holeItems:
	print "User " ,n,", Item ", i, " : ", getPredictedRating(n,i)
# print Data
# print getNeighbors(4)
# print getPredictedRating(4,1)
#print "Target: User 2"

#m = sortSims(sims)
#n = len(m)
#topSims = []
#for i in range(0,20):
#	topSims.append(m[n-1-i])
#print len(topSims)
#print topSims