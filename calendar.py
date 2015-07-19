import datetime
import numpy
import re
import sys, traceback

header = '\documentclass[landscape,a4paper]{article}\n' + '\usepackage{calendar}\n' + '\usepackage[landscape,margin=0.5in]{geometry}\n' + '\usepackage{color}\n' + '%\usepackage{fontspec}\n' + '%\setmainfont{BiauKai}\n' + '\\begin{document}\n'+'\pagestyle{empty}\n'+'\\noindent\n'+'\StartingDayNumber=1\n'
calendar = []
Month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
forgettingCurve = [0, 1, 3, 7, 15, 30]

# ----------------------------------------------------------------------------------------
# 	17 DAYS KO VOCABULARIES
# ----------------------------------------------------------------------------------------
# 5min 10words --> 0.5min re 10words
# .
# .
# .
# .
# 30min 60words --> 3min re 60words
# .
# .
# .
# 60min 120words --> 5min re 120words
#
#
# night --> re 120 words
#
#
#
# 3 cannot remember --> quizlet



# ----------------------------------------------------------------------------------------
# 	GENERATE MEMORIZING ORDER
# ----------------------------------------------------------------------------------------
start = 0
offset = 0
for line in open('wordList.txt').readlines():
	tmp = line.split('\n')[0].split('*')
	if '#' in tmp[0]: #comment
		continue
	elif len(tmp) == 1: #start point
		if len(calendar) == 0:
			offset = int(tmp[0])
		else:
			start = int(tmp[0]) - offset
	else:
		divide = 1
		if '/' in tmp[1]:
			divide = int(tmp[1].split('/')[1])
			tmp[1] = tmp[1].split('/')[0]
		remain = 1-((divide-int(tmp[1])%divide)/divide)
		for chapter in range(1, int(tmp[1])/divide+remain+1):
			units = 1
			if len(tmp) > 2:
				units = int(tmp[2])
			while len(calendar) < int(tmp[1])*units/divide+int(forgettingCurve[-1])+start:
				calendar.append([])

			times = 1
			for repeat in forgettingCurve:
				if len(tmp) == 3:
					for unit in range(1, int(tmp[2])+1):
						# if times == 1:
							# calendar[int(repeat)+start+(chapter-1)*units+unit-1].append(tmp[0]+str(chapter)+'.'+str(unit))
						calendar[int(repeat)+start+(chapter-1)*units+unit-1].append(tmp[0]+str(chapter)+'.'+str(unit)+'$'+'_{'+str(times)+'}$')
				elif divide > 1:
					# if times == 1:
						# calendar[int(repeat)+start+chapter-1].append(tmp[0]+str((chapter-1)*divide+1)+'-'+str(chapter*divide))
					if chapter == int(tmp[1])/divide + 1:
						if int(tmp[1])%divide == 1:
							calendar[int(repeat)+start+chapter-1].append(tmp[0]+tmp[1]+'$_{'+str(times)+'}$')
						else:
							calendar[int(repeat)+start+chapter-1].append(tmp[0]+str(int(tmp[1])-int(tmp[1])%divide+1)+'-'+tmp[1]+'$_{'+str(times)+'}$')
					else:
						calendar[int(repeat)+start+chapter-1].append(tmp[0]+str((chapter-1)*divide+1)+'-'+str(chapter*divide)+'$_{'+str(times)+'}$')
				else:
					# if times == 1:
						# calendar[int(repeat)+start+chapter-1].append(tmp[0]+str(chapter))
					calendar[int(repeat)+start+chapter-1].append(tmp[0]+str(chapter)+'$'+'_{'+str(times)+'}$')
				times = times + 1

for i in range(len(calendar)):
	calendar[i] = list(reversed(calendar[i]))

# print numpy.matrix(calendar)
# ----------------------------------------------------------------------------------------
# 	Make a Latex Calendar
# ----------------------------------------------------------------------------------------

initDate = datetime.date.today() + datetime.timedelta(days=offset)
endDate = initDate + datetime.timedelta(days=len(calendar)-1)
startMonth = Month.index(str(initDate.strftime('%B')))
endMonth = Month.index(str(endDate.strftime('%B')))
monthSpan = 1 + endMonth - startMonth + 12*(int(endDate.strftime('%Y')) - int(initDate.strftime('%Y')))

# print len(calendar)
# print endDate

file = open("./calendar.tex", "w")
file.write(header);
calIndex = 0
for month in range(startMonth, startMonth+monthSpan):
	file.write('\\begin{center}\n')
	file.write('\\textsc{\LARGE ' + Month[month%12] + '}\\\\\n')
	file.write('\\textsc{\large ' + str((initDate + datetime.timedelta(days=calIndex)).strftime('%Y')) + '}\n')
	file.write('\end{center}\n')
	file.write('\\begin{calendar}{\hsize}\n')

	for i in range(int((initDate + datetime.timedelta(days=1-int(initDate.strftime('%d')))).strftime('%w'))):
		file.write('\BlankDay\n')
	
	file.write('\setcounter{calendardate}{1}\n')

	if calIndex == 0:
		for i in range(int(initDate.strftime('%d'))-1):
			file.write('\day{}{}\n')
	while Month.index((initDate + datetime.timedelta(days=calIndex)).strftime('%B')) == month%12:
		file.write('\day{}{')
		if calIndex < len(calendar):
			for i in range(len(calendar[calIndex])):
				file.write(calendar[calIndex][i] + '\\\\')
		file.write('}\n')
		calIndex += 1

	file.write('\\finishCalendar\n')
	# if the the line over the box
	if calIndex < len(calendar):
		file.write('\\BlankDay\n')  
	file.write('\end{calendar} \clearpage \n')
file.write('\end{document}\n')
file.close()
