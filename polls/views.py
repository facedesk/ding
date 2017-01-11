from django.shortcuts import render
from config import Config
from django.http import HttpResponse
import gspread
from datetime import date
from django.views.decorators.csrf import csrf_exempt

from oauth2client.service_account import ServiceAccountCredentials


def _wrapWithPost(value,route,CSVExtraValues=""):
    if CSVExtraValues!="":
       CSVExtraValues= "," + CSVExtraValues
    html = '''
    <form id={0} action="{1}" method="post">
    
     <input type="submit" name ="{0}{2}"value="{0}">
    </form>
    '''.format(value,route,CSVExtraValues)
    return html

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
    currentyear = date.today().year

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
    return HttpResponse(html)

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
    return HttpResponse(html)


@csrf_exempt   
def listStudents(request):
    requestCSV = list(request.POST)[0]
    requestValues = unicode.split(requestCSV,",")
    #requestValues = str.split(list(request.POST)[0],",")
    term = requestValues[1]
    period = requestValues[0]
    gc = authenticate()
    wks = gc.open(term).worksheet(period)
    students = wks.row_values(1)
    html = "<div id='students'>"
    html +=list(request.POST)[0]

    students = students[2:]#clip header
    for student in students:
    	if student == "":
    	    continue
    	html += _wrapWithPost(student,"/dingStudent",term+","+period)
    html += "</div>"
    return HttpResponse(html)

def CreateNewDay(request):

	pass
@csrf_exempt    
def dingStudent(request):
    requestCSV = list(request.POST)[0]
    requestValues = unicode.split(requestCSV,",")
    #requestValues = str.split(list(request.POST)[0],",")

    term = requestValues[2]
    period = requestValues[1]
    student = requestValues[0]
    return HttpResponse(term+period+student)