import json
from multiprocessing import context
import requests
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template import loader
from datetime import datetime
from django.shortcuts import render
from django.apps import apps
from django.views.generic import DeleteView
import pandas as pd
from django.http import FileResponse
import pathlib
import xlsxwriter
from django.conf import settings
from .forms import ResForm, DetailForm, FilterForm, ExcelForm
from django.core.paginator import Paginator, EmptyPage
Resume = apps.get_model('api', 'Resume')



def home(request):
    resumes = Resume.objects.all()
    if "Search" in request.POST:
        search = request.POST.get('Search')
        resumes = resumes.filter(text__icontains = search) 
    form = FilterForm(request.POST)
    form_type = 'all'
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == "filter" :
            date_from= request.POST.get('date_from')
            date_to= request.POST.get('date_to')
            start_date = datetime.strptime(date_from, '%Y-%m-%d')
            end_date = datetime.strptime(date_to, '%Y-%m-%d')
            resumes = Resume.objects.filter(timestamp__date__lte=date_to,timestamp__date__gte=date_from)
        elif form_type == "report" :
            date_from= request.POST.get('date_from')
            date_to= request.POST.get('date_to')
            request.session["date_from"] = date_from
            request.session["date_to"] = date_to
            return redirect('to-excel')
        elif form_type == "all" :
            resumes = Resume.objects.all()
        elif form_type == "Search_name" :
            sr_type = "name"
            search = request.POST.get('Search')
            return redirect('web-search',sr_type,search)
        elif form_type == "Search_designation" :
            sr_type = "designation"
            search = request.POST.get('Search')
            return redirect('web-search',sr_type,search)
        elif form_type == "Search_skill" :
            sr_type = "skill" 
            search = request.POST.get('Search')
            return redirect('web-search',sr_type,search)   
        elif form_type == "parsed" :
            resumes = Resume.objects.filter(is_parsed=True)
        elif form_type == "not_parsed" :
            resumes = Resume.objects.filter(is_parsed=False)
        elif form_type == "download":
            date_from= request.POST.get('date_from')
            date_to= request.POST.get('date_to')
            start_date = datetime.strptime(date_from, '%Y-%m-%d')
            end_date = datetime.strptime(date_to, '%Y-%m-%d')
            fields = [f.name for f in Resume._meta.get_fields()]
            fields.remove('is_parsed')
            fields.remove('timestamp')
            fields.remove('text')
            resumes = Resume.objects.filter(is_parsed=True,timestamp__date__lte=date_to,timestamp__date__gte=date_from).values(*fields)
            df = pd.DataFrame(resumes)
            base_dir =settings.MEDIA_ROOT
            file_name = str(date_from) +"-"+ str(date_to ) + '.xlsx'
            path = base_dir + '/excels/'+file_name
            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet()
            workbook.close()
            df.to_excel(base_dir + '/excels/'+file_name)
            file_server = pathlib.Path(path)
            if file_server.exists(): 
                file_to_download = open(str(file_server), 'rb')
                response = FileResponse(file_to_download, content_type='application/force-download')
                response['Content-Disposition'] = 'inline; filename="{}"'.format(file_name)
            return response
        elif form_type == "file" :
            files = request.FILES.getlist('resume')
            for file in files:
                response = requests.post('http://127.0.0.1:8000/api/resume-create/', files={'resume': file})
            resumes = Resume.objects.filter(is_parsed=False)
            for resume in resumes:
                response = requests.put(f'http://127.0.0.1:8000/api/resume-parse/{resume.id}/')
            return redirect('web-home')       
    p = Paginator(resumes, 40)
    page_num = request.GET.get('page', 1)
    try:
        resumes = p.page(page_num)
    except EmptyPage:
        resumes = p.page(1)
    context = {
        "resumes":resumes,
        "form":form,
        "class": form_type,
    }
    return render(request, 'home.html', context)





def ResumeWebDetail(request, pk):

    api = "http://127.0.0.1:8000/api/resume-detail/"+str(pk)+"/"
    instance = Resume.objects.get(id=pk)
    form = DetailForm(request.POST, request.FILES,instance=instance, use_required_attribute=False)
    data = requests.get(api).json()
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.path_info)
    else:
        form = DetailForm(initial=data)
    return render(request, 'ResumeDetail.html', {'data': data, 'form':form})

def ResumeParse(request,pk):
    api = "http://127.0.0.1:8000/api/resume-parse/"+str(pk)+"/"
    print(api)
    data = requests.put(api)
    print(data)
    return redirect('web-detail',pk)
# upload resume

def ResumeWebDelete(request, pk):

    api = "http://127.0.0.1:8000/api/resume-delete/"+str(pk)+"/"

    requests.delete(api)

    return redirect('web-home')


class DeleteView(DeleteView):
    model = Resume
    template_name = 'ResumeDelete.html'
    success_url = '/'
    
def ResumeSearch(request,sr_type,qr):
    query = qr
    if sr_type == "name":
        best = Resume.objects.filter(name__icontains=query) 
    elif sr_type == "designation":
        best = Resume.objects.filter(designation__icontains=query)
    elif sr_type == "skill":
        best = Resume.objects.filter(skills__icontains=query)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == "Search_name" :
            sr_type = "name"
            search = request.POST.get('Search')
            return redirect('web-search',sr_type,search)
        elif form_type == "Search_designation" :
            sr_type = "designation"
            search = request.POST.get('Search')
            return redirect('web-search',sr_type,search)
        elif form_type == "Search_skill" :
            sr_type = "skill" 
            search = request.POST.get('Search')
            return redirect('web-search',sr_type,search) 
    other = Resume.objects.filter(text__icontains=query)
    other = other.difference(best)
    print(other)
    context = {
        "best" : best,
        "other" : other
    }
    return render(request, "search.html", context)

def ResumeExcel(request):
    date_from= request.session['date_from']
    date_to= request.session['date_to']
    start_date = datetime.strptime(date_from, '%Y-%m-%d')
    end_date = datetime.strptime(date_to, '%Y-%m-%d')
    fields = [f.name for f in Resume._meta.get_fields()]
    fields.remove('is_parsed')
    fields.remove('timestamp')
    fields.remove('text')
    fields.remove('id')
    fields.remove('resume')
    resumes = Resume.objects.filter(is_parsed=True,timestamp__date__lte=date_to,timestamp__date__gte=date_from).values(*fields)
    df = pd.DataFrame(resumes)
    base_dir =settings.MEDIA_ROOT
    file_name = str(date_from) +"-"+ str(date_to ) + '.xlsx'
    path = base_dir + '/excels/'+file_name
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    workbook.close()
    df.to_excel(base_dir + '/excels/'+file_name)
    file_server = pathlib.Path(path)
    if file_server.exists(): 
        file_to_download = open(str(file_server), 'rb')
        response = FileResponse(file_to_download, content_type='application/force-download')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(file_name)
    context={
        'df':df.to_html(),
        'path':path,
    }
    return render(request,'excel.html',context)