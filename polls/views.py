from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import gspread

def index(request):
	return HttpResponse("<h1>Hello</h1>")
    #return HttpResponse("Hello, world. You're at the polls index.")


def listStudents():
	gc = gspread.authorize(credentials)

	# Open a worksheet from spreadsheet with one shot
	wks = gc.open("Where is the money Lebowski?").sheet1

	wks.update_acell('B2', "it's down there somewhere, let me take another look.")

	# Fetch a cell range
	cell_list = wks.range('A1:B7')