from django.shortcuts import render
from config import Config
from django.http import HttpResponse
import gspread
from datetime import date



from oauth2client.service_account import ServiceAccountCredentials


def _wrapWithPost(value,route):
    html = '''
    <form action="{1}" method="post">
     <input type="submit" value="{0}">
    </form>
    '''.format(value,route)
    return html

def index(request):
	#HttpResponse("<h1>Hello</h1>")
	#listStudents("test","1")
	#listPeriods("test")
	return listTerms()
def authenticate():
    scope = Config["scope"]
    credentials = Config["credentials"]
    gc = gspread.authorize(credentials)
    return gc
def listTerms(request):
    gc = authenticate()
    currentyear = date.today().year

    html = "<div id='terms'>"
    html += str(request.POST)
    route="/index"
    html += _wrapWithPost(str(currentyear-1)+"Fall",route)
    html += _wrapWithPost(str(currentyear-1)+"Spring",route)
    html += _wrapWithPost(str(currentyear)+"Fall",route)
    html += _wrapWithPost(str(currentyear)+"Spring",route)
    html += _wrapWithPost(str(currentyear+1)+"Fall",route)
    html += _wrapWithPost(str(currentyear+1)+"Spring",route)


    html += "</div>"
    return HttpResponse(html)
def listPeriods(term):
    gc = authenticate()
    sheets = gc.open(term)
    periods = sheets.worksheets()
    html = "<div id = 'periods'>"
    for period in periods:
        html += "<h2>"+period.title+"</h2>"
    html += "</div>"
    return HttpResponse(html)
def listStudents(term,period):
    gc = authenticate()
    wks = gc.open(term).worksheet(period)
    students = wks.row_values(1)
    html = "<div id='students'>"
    students = students[2:]#clip header
    for student in students:
    	html += "<h2>"+student+"</h2>"
    html += "</div>"
    return HttpResponse(html)
    