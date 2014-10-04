import time
import numpy
import re

header = '\documentclass[landscape,a4paper]{article}\n' + '\usepackage{calendar}\n' + '\usepackage[landscape,margin=0.5in]{geometry}\n' + '\usepackage{color}\n' + '\\begin{document}\n'+'\pagestyle{empty}\n'+'\\noindent\n'+'\StartingDayNumber=1\n'

year = 0
Month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

m31 = [1, 3, 5, 7, 8, 10, 12]
m30 = [4, 6, 9, 11]		
def monthDays(month):
	if int(month) in m31:
		return 31
	elif int(month) in m30:
		return 30
	else:
		return 28
def dateFromToday(days):
	global year
	weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'] 
	today = time.strftime('%m/%d/%A/%Y').split('/')
	m = int(today[0])
	d = int(today[1]) + int(days)
	weekday = (weekdays.index(today[2])+days-1)%7
	# m = 9
	# d = 25 + int(days)
	while True:
		if m > 12:
			m = 1
		if d > monthDays(m):
			m += 1
			d -= monthDays(m)
		else:
			break
	if m == 1 and d == 1:
		year += 1
	return str(m)+'/'+str(d)+'/'+str(weekday)+'/'+str(int(today[3])+year/4)

wordList = []
calendar = []
forgettingCurve = [0, 1, 2, 4, 7, 15]

# ----------------------------------------------------------------------------------------
# 	PARSING MEMORY FILE
# ----------------------------------------------------------------------------------------
for line in open('wordList.txt').readlines():
	tmp = line.split('\n')[0].split('*')
	for i in range(int(tmp[1])):
		calendar.append([])
		wordList.append(tmp[0]+'_{'+str(i+1)+'}')
for i in range(29):
	calendar.append([])

# ----------------------------------------------------------------------------------------
# 	Arrange Task By Ebbinghaus Forgetting Curve
# ----------------------------------------------------------------------------------------
for i in range(len(wordList)):
	calendar[i].insert(0, '$' + wordList[i] + '$')
	for j in range(len(forgettingCurve)):
		calendar[i+sum(forgettingCurve[:j+1])].append('$-'+wordList[i] + '$')

for i in range(len(calendar)):
	for j in range(4):
		calendar[i].insert(j, dateFromToday(i+1).split('/')[j])	
	# print calendar[i]

while int(calendar[0][1]) != 1:
	calendar.insert(0, [calendar[0][0], str(int(calendar[0][1])-1), str((int(calendar[0][2])+6)%7), int(calendar[0][3])])
while int(calendar[-1][1]) < monthDays(int(calendar[-1][0])):
	calendar.append([calendar[-1][0], str(int(calendar[-1][1])+1), calendar[-1][2], calendar[-1][3]])

# print len(calendar)

# print numpy.matrix(calendar)

# ----------------------------------------------------------------------------------------
# 	Make a Latex Calendar
# ----------------------------------------------------------------------------------------


file = open("./calendar.tex", "w")
file.write(header);

count = 0
monthSpan = int(calendar[-1][0]) - int(calendar[0][0]) + 1 + year*3
for month in range(monthSpan):
	file.write('\\begin{center}\n')
	file.write('\\textsc{\LARGE ' + Month[(int(calendar[0][0])+month-1)%12] + '}\\\\\n')
	file.write('\\textsc{\large ' + str(calendar[count][3]) + '}\n')
	file.write('\end{center}\n')
	file.write('\\begin{calendar}{\hsize}\n')

	for i in range(int(calendar[count][2])):
		file.write('\BlankDay\n')
	
	file.write('\setcounter{calendardate}{1}\n')

	for i in range(monthDays(calendar[count][0])):
		if len(calendar[count]) > 4 and not re.search('-', calendar[count][4]):
			file.write('\day{\color{blue}' + calendar[count][4] + '}{')
			for chapter in calendar[count][5:]:
				file.write(chapter + '\\\\')
		else:
			file.write('\day{}{')
			for j in range(len(calendar[count])-4):
				file.write(calendar[count][j+4] + '\\\\')
		file.write('}\n')
		count += 1

	file.write('\\finishCalendar\n')
	file.write('\end{calendar} \clearpage \n')
file.write('\end{document}\n')
file.close()