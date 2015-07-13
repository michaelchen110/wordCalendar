import datetime
import numpy
import re
import sys, traceback

header = '\documentclass[landscape,a4paper]{article}\n' + '\usepackage{calendar}\n' + '\usepackage[landscape,margin=0.5in]{geometry}\n' + '\usepackage{color}\n' + '%\usepackage{fontspec}\n' + '%\setmainfont{BiauKai}\n' + '\\begin{document}\n'+'\pagestyle{empty}\n'+'\\noindent\n'+'\StartingDayNumber=1\n'
calendar = []
Month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
forgettingCurve = [0, 1, 2, 4, 7, 15]

# today = time.strftime('%m/%d/%A/%Y').split('/')
# print today
# ----------------------------------------------------------------------------------------
# 	GENERATE MEMORIZING ORDER
# ----------------------------------------------------------------------------------------
start = 0
for line in open('wordList.txt').readlines():
	tmp = line.split('\n')[0].split('*')
	if '#' in tmp[0]: #comment
		continue
	elif len(tmp) == 1: #start point
		start = int(tmp[0])
	else:
		for chapter in range(1, int(tmp[1])+1):
			while len(calendar) < int(tmp[1])+int(forgettingCurve[-1])+start:
				calendar.append([])
			times = 1
			for repeat in forgettingCurve:
				if len(tmp) == 3:
					for unit in range(1, int(tmp[2])+1):
						calendar[int(repeat)+start+chapter-1+unit-1].append(tmp[0]+str(chapter)+'.'+str(unit)+'_{'+str(times)+'}')
				else:
					calendar[int(repeat)+start+chapter-1].append(tmp[0]+str(chapter)+'_{'+str(times)+'}')
				times = times + 1
# print numpy.matrix(calendar)
# ----------------------------------------------------------------------------------------
# 	Make a Latex Calendar
# ----------------------------------------------------------------------------------------

today = datetime.date.today()
endDate = today + datetime.timedelta(days=len(calendar))
startMonth = Month.index(str(today.strftime('%B')))
endMonth = Month.index(str(endDate.strftime('%B')))
monthSpan = 1 + endMonth - startMonth + 12*(int(endDate.strftime('%Y')) - int(today.strftime('%Y')))

file = open("./calendar.tex", "w")
file.write(header);

calIndex = 0
for month in range(startMonth, startMonth+monthSpan):
	file.write('\\begin{center}\n')
	file.write('\\textsc{\LARGE ' + Month[month%12] + '}\\\\\n')
	file.write('\\textsc{\large ' + str((today + datetime.timedelta(days=calIndex)).strftime('%Y')) + '}\n')
	file.write('\end{center}\n')
	file.write('\\begin{calendar}{\hsize}\n')

	for i in range(int((today + datetime.timedelta(days=calIndex)).strftime('%w'))):
		file.write('\BlankDay\n')
	
	file.write('\setcounter{calendardate}{1}\n')

	while Month.index((today + datetime.timedelta(days=calIndex)).strftime('%B')) == month%12:
		print today + datetime.timedelta(days=calIndex)
		file.write('\day{}{')
		if calIndex < len(calendar):
			for i in range(len(calendar[calIndex])):
				file.write('$'+calendar[calIndex][i]+'$' + '\\\\')
		file.write('}\n')
		calIndex += 1

	file.write('\\finishCalendar\n')
	# if the the line over the box
	if calIndex < len(calendar):
		file.write('\\BlankDay\n')  
	file.write('\end{calendar} \clearpage \n')
file.write('\end{document}\n')
file.close()