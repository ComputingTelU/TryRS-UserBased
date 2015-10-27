__author__ = 'Febrian Imanda Effendy'

import xlrd
import numpy as np
import math

# sh = data.sheet_by_index(0)
# print sh.name, sh.nrows, sh.ncols
# for rx in range(sh.nrows):
#   print sh.row(rx)
def getData(filename):
  data = xlrd.open_workbook(filename)
  sheet = data.sheet_by_index(0)
  return sheet

DATA = getData("jester-data-1500.xls")
SHEET_ROWS = DATA.nrows
SHEET_COLUMN = DATA.ncols

# Fungsi untuk mendapatkan rating dari 1 item berdasarkan user
def getRating(user, item):
	val = DATA.row(user)[item].value
	return 0 if val >= 99 else val

# Fungsi untuk mendapatkan rating dari seluruh item berdasarkan user
def getItemRating(user):
	rating = []
	for item in range(1, SHEET_COLUMN):
		rating += [getRating(user, item)]
	# return rating
	listRating = np.array(rating)
	return listRating

# Fungsi untuk menghitung rata-rata dari list rating yang diberikan (numpy format)
def getAverageRating(rates):
	total = []
	for i in rates:
		if i < 99 :
			total.append(i)
	listTotal = np.array(total)
	return np.mean(listTotal)

# Fungsi untuk mendapatkan semua neighbour dari user
def getNeighbours(user):
	neighbour = []
	for i in range(1,SHEET_ROWS):
		if i != user :
			for j in range(SHEET_COLUMN):
				yUser = getRating(user, j)
				yNeighbour = getRating(i, j)
				if (yUser < 99) and (yNeighbour < 99) :
					neighbour += [i]
					break
	# return neighbour
	listNeighbours = np.array(neighbour)
	return listNeighbours

# Fungsi untuk mendapatkan similiaritas dari 2 user yang dibandingkan
def getSimiliarity(user1, user2):
	yAvgUser1 = getAverageRating(getItemRating(user1))
	yAvgUser2 = getAverageRating(getItemRating(user2))
	atas = 0
	bawah = 0
	for i in range(1,SHEET_COLUMN) :
		yUser1  = getRating(user1, i)
		yUser2 = getRating(user2, i)
		# print "yuser1 : ", yUser1
		# print "yuser2 : ", yUser2
		if yUser1 != 0 and yUser2 != 0 :
			atas += (yUser1 - yAvgUser1) * (yUser2 - yAvgUser2)
	yUser1a = 0
	yUser2a = 0
	for i in range(1,SHEET_COLUMN) :
		yUser1  = getRating(user1, i)
		yUser2 = getRating(user2, i)
		if yUser1 != 0 and yUser2 != 0 :
			yUser1a += (yUser1 - yAvgUser1) ** 2
			yUser2a += (yUser2 - yAvgUser2) ** 2
	bawah = math.sqrt(yUser1a * yUser2a)
	sim = atas / bawah
	return sim

# Fungsi untuk mendapatkan 20 similiaritas terbesar menggunakan metode mergesort dengan O(nlog(n))
def getTopSimiliarity(listSim):
	listSim = np.sort(listSim, kind='mergesort')
	listSim = listSim[::-1]
	return listSim[1:21:1]

# Fungsi untuk mendapatkan prediksi rating
def getPredictedRating(user, item):
	yAvgUser = getAverageRating(getItemRating(user))
	neighbours = getNeighbours(user)
	atas = 0
	bawah = 0
	# for i in range(SHEET_COLUMN):
 	for j in range(len(neighbours)):
 		similiarities = getSimiliarity(neighbours[j], user)
 		tempRating = getRating(neighbours[j], item)
 		rating = 0 if tempRating >= 99 else tempRating
 		yAvgNeighbour = getAverageRating(getItemRating(neighbours[j]))
 		print "User",user, " | User",neighbours[j], " - Similiarities :", similiarities, " - rating :", rating, " - avg :", yAvgNeighbour 
 		atas += similiarities * (rating - yAvgNeighbour)
 		bawah += abs(similiarities)
	predicted = yAvgUser + (atas / bawah)
	return predicted

# print getNeighbours(5)
# print getSimiliarity(0,410)
# print getAverageRating(getItemRating(0))
predicted = getPredictedRating(0, 100)
print "Predicted :", predicted