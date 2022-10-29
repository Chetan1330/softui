# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.conf import settings

from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Folder,File
@login_required(login_url="/login/")
def index(request):
    print("User id:",request.user.id)
    folder = Folder.objects.filter(folderuser=request.user)
    # media_root = getattr(settings, 'MEDIA_ROOT', None)
    # if image:
    #     image.delete()
    # print(media_root)
    context = {'folder':folder,'segment':'index'}
    #return render(request,'home/index.html',context)
    #context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

# Folder with files in it
def folder(request,folderid):
    
    folder_user = Folder.objects.get(id=folderid)
    files = File.objects.filter(folder=folder_user)
    
    ext = []
    for i in range(len(files)):
        # print(files[i].filetitle.split('.')[1])
        ext.append([files[i],files[i].filetitle.split('.')[1]])

    print(ext)
    context = {'folderid':folderid,'files':files,'ext':ext}
    # file_user = request.FILES.get('file')
    # for f in file_user:
    #     print("Files:",f)

    if request.method == 'POST':
        file_user = request.FILES.get('file')
        file_title = request.POST.get('filetitle')
        fileadd = File.objects.create(filetitle=file_user.name,file=file_user,folder=folder_user)
        
    return render(request,'home/folder.html',context)

# Delete Folder with files in it
def delete(request,deleteid):
    
    folder_user = Folder.objects.get(id=deleteid)
    folder_user.delete()
    context = {'folder':folder,'segment':'index'}

    return redirect("index")


# Add Folder View
def addfolder(request):
    # folder_user = Folder.objects.get(id=folderid)
    # files = File.objects.filter(folder=folder_user)
    # context = {'folderid':folderid,'files':files}
    if request.method == 'POST':
        folder_name = request.POST['foldername']
        folder_desc = request.POST['desc']
        print("Folder Desc:",folder_desc)
        folder = Folder.objects.create(foldername=folder_name,folderdesc=folder_desc,folderuser=request.user)
        folder.save()
        #file_title = request.FILES['file']
        file_user = request.FILES.getlist('file')
        for f in file_user:
            print("f",f)
            file = request.FILES.get('file')
            # file_title = request.POST.get('filetitle')
            fileadd = File.objects.create(filetitle=f.name,file=file,folder=folder)
            fileadd.save()
        if folder:
            return redirect("index")
        else:
            messages.error(request,"Folder Not Created")
            return redirect("index")

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
            
        segment, active_menu = get_segment( request )
        
        context['segment']     = segment
        context['active_menu'] = active_menu
        
        
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment     = request.path.split('/')[-1]
        active_menu = None

        if segment == '' or segment == 'index.html':
            segment     = 'index'
            active_menu = 'dashboard'

        if segment.startswith('dashboards-'):
            active_menu = 'dashboard'

        if segment.startswith('account-') or segment.startswith('users-') or segment.startswith('profile-') or segment.startswith('projects-'):
            active_menu = 'pages'

        if  segment.startswith('notifications') or segment.startswith('sweet-alerts') or segment.startswith('charts.html') or segment.startswith('widgets') or segment.startswith('pricing'):
            active_menu = 'pages'            

        return segment, active_menu     

    except:
        return 'index', 'dashboard'  
