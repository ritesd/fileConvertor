from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .xmlToCsv import XML2DataFrame
from django.core.files.storage import FileSystemStorage
import os


# Create your views here.
def index(request):
    return render(request,'online/index.html')

def contact(request):
    return render(request,'online/contact.html')

def convert(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        xmldata = request.FILES['myfile'].read()
        
        xml2df = XML2DataFrame(xmldata)
        xml_dataframe = xml2df.process_data()
        fs = FileSystemStorage()
        xml_dataframe.to_csv('temp/'+ (myfile.name).replace('xml','csv'))
        file = open('temp/'+ (myfile.name).replace('xml','csv'))
        filename = fs.save((myfile.name).replace('xml','csv'), file)
        os.remove('temp/'+ (myfile.name).replace('xml','csv'))
        uploaded_file_url = fs.url(filename)
        return render(request, 'online/convert.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'online/convert.html')


def about(request):
    return render(request,'online/about.html')	
