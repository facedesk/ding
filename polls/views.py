from django.shortcuts import render
from config import Config
# Create your views here.
from django.http import HttpResponse
import gspread


from oauth2client.service_account import ServiceAccountCredentials


def index(request):
	#HttpResponse("<h1>Hello</h1>")
	return listStudents()
def Authenticate():
	scope = ['https://spreadsheets.google.com/feeds']
    credentials = Config["credentials"]
    gc = gspread.authorize(credentials)
    return gc

def listPeriods():

def listStudents(period):
 
    

    wks = gc.open("test").sheet1
    
    students = wks.row_values(1)
    html = "<div id='students'>"

    students = students[2:]#clip header
    for student in students:
    	html += "<h2>"+student+"</h2>"
    html += "</div>"

    return HttpResponse(html)
     
    #gc = gspread.authorize(Config["credentials"])
	# You can open a spreadsheet by its title as it appears in Google Doc
    #sh = gc.open('test') # <-- Look ma, no keys!
    #sh.worksheets()
    #sht1 = gc.open_by_key('1incg6CDgZOyzwynSSvtG3v8oswgteG6wW3vmD6FwO6w')
    #1incg6CDgZOyzwynSSvtG3v8oswgteG6wW3vmD6FwO6w/
    