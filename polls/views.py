from django.shortcuts import render
from config import Config
from django.http import HttpResponse
from django.shortcuts import redirect

import gspread
import datetime,calendar
from django.views.decorators.csrf import csrf_exempt
from oauth2client.service_account import ServiceAccountCredentials


def _wrapWithPost(value,route,PSVExtraValues=""):
    if PSVExtraValues!="":
       PSVExtraValues= "|" + PSVExtraValues
    html = '''
   
    <form class=".col-md-4" id={0} action="{1}" method="post">
     <input  class="btn btn-primary btn-lg" type="submit" name ="{0}{2}"value="{0}">
    </form>
    
    '''.format(value,route,PSVExtraValues)
    return html

def _wrapWithTemplate(innerHTML):
	html ='''
<html>
	<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script></head>
<body>

	{0}

	<hr>
	<hr>
</body>
</html>
	'''
	return html.format(innerHTML)

@csrf_exempt
def index(request):
	#HttpResponse("<h1>Hello</h1>")
	#listStudents("test","1")
	#listPeriods("test")
	return listTerms("")
def authenticate():
    scope = Config["scope"]
    credentials = Config["credentials"]
    gc = gspread.authorize(credentials)
    return gc

def listTerms(request):
    gc = authenticate()
    currentyear = datetime.date.today().year

    html = "<div id='terms'>"
    #html += str(request.POST)
    route="/listPeriods"
    html += _wrapWithPost(str(currentyear-1)+"Fall",route)
    html += _wrapWithPost(str(currentyear-1)+"Spring",route)
    html += _wrapWithPost(str(currentyear)+"Fall",route)
    html += _wrapWithPost(str(currentyear)+"Spring",route)
    html += _wrapWithPost(str(currentyear+1)+"Fall",route)
    html += _wrapWithPost(str(currentyear+1)+"Spring",route)
    html += "</div>"
    return HttpResponse(_wrapWithTemplate(html))

@csrf_exempt
def listPeriods(request):
    term=list(request.POST)[0]

    gc = authenticate()
    sheets = gc.open(term)
    periods = sheets.worksheets()
    html ="<h1>"+str(term)+"</h1>"
    html += "<div id = 'periods'>"
    
    for period in periods:
        html += _wrapWithPost(period.title,"/listStudents",term)
    html += "</div>"
    return HttpResponse(_wrapWithTemplate(html))


@csrf_exempt   
def listStudents(request):
    term = 0
    period = ""
    if(len(list(request.POST))==0):
        print request.session.get('_old_post')
        request.POST = request.session.get('_old_post')
        requestCSV = list(request.POST)[0]
        requestValues = unicode.split(requestCSV,"|")
        term = requestValues[1]
        period = requestValues[2]
    else:
        requestCSV = list(request.POST)[0]
        requestValues = unicode.split(requestCSV,"|")
        term = requestValues[1]
        period = requestValues[0]
    CreateNewDay(term,period)
    gc = authenticate()
    wks = gc.open(term).worksheet(period)
    students = wks.row_values(1)
    html = "<div id='students'>"
    html +=list(request.POST)[0]
    students = students[2:]#clip header
    for student in students:
    	if student == "":
    	    continue
    	html += _wrapWithPost(student,"/dingStudent",term+"|"+period)
    html += "</div>"
    return HttpResponse(_wrapWithTemplate(html))

def CreateNewDay(term,period):
    gc = authenticate()
    wks = gc.open(term).worksheet(period)
    if(str(datetime.date.today()) in wks.col_values(1)):#don't duplicate data
    	return
    dates = wks.col_values(1)
    #remove empty with slice
    dates =  list(filter(None, dates))
    dateCount=len(dates)+1

    students=wks.row_values(1)
    students =  list(filter(None, students)) 
    num_students = len(students)

    letter = 'A'
    for st in students:
    	letter = chr(ord(letter) + 1)
    newGrades = wks.range('A'+str(dateCount)+':'+letter+str(dateCount))
    #cell_list = worksheet.range('A1:C7')
    print('A'+str(dateCount)+':'+letter+str(dateCount))

    for i, val in enumerate(students):  #gives us a tuple of an index and value
    	if(students[i]==""):
    		break
    	if(i==0):
    		newGrades[i].value = datetime.date.today()
    	elif(i==1):
    		newGrades[i].value = calendar.day_name[datetime.date.today().weekday()]
        else:
            newGrades[i].value = 20    #use the index on cell_list and the val from cell_values
    
    print(newGrades)
    print('A'+str(dateCount)+':'+letter+str(dateCount))
    wks.update_cells(newGrades)

@csrf_exempt    
def dingStudent(request):
    requestPSV = list(request.POST)[0]
    requestValues = unicode.split(requestPSV,"|")
    #requestValues = str.split(list(request.POST)[0],",")
    gc= authenticate()
    period = requestValues[2]
    term = requestValues[1]
    student = requestValues[0]
    print requestPSV
    wks = gc.open(term).worksheet(period)
    
    studentCell = wks.find(student)
    dayCell = wks.find(str(datetime.date.today()))


    studentsGrade = wks.cell(dayCell.row,studentCell.col)
    
    if(studentsGrade.value >0):
        studentsGrade.value = int(studentsGrade.value) - 4
    
    wks.update_cell(studentsGrade.row,studentsGrade.col,studentsGrade.value)
	#update_cell(row, col, val)
	#print("Found something at R%sC%s" % (cell.row, cell.col))
    request.session['_old_post'] = request.POST
    return redirect('/listStudents/')