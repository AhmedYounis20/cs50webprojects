from django.shortcuts import render,redirect
from markdown2 import markdown_path
from django.http import HttpResponse,Http404
import html
from . import util
import random
from django import forms
class edited_one(forms.Form):

    current=forms.CharField(label='page content md :',widget=forms.Textarea)
class new_one(forms.Form):
    title=forms.CharField(label='your title please  ',max_length=1000)
    markcontent=forms.CharField(label='\npage content as md  :',widget=forms.Textarea)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def view_entry(request,ent_name):
    try:
        a=markdown_path('entries/'+ent_name+'.md')
        a+="<p style='margin-top:50px;margin-left:4px;'><a href='/edit/{}' > Edit</a></p>".format(ent_name)
        return HttpResponse(a)
    except :
        return HttpResponse('sorry requested page not found')
def new_page(request):
    if request.method=='POST':
        a=util.list_entries()
        for i in range(len(a)):
            a[i]=a[i].lower()
        print(a)
        try:
            if request.POST.get('title').lower()  not in a:
                title=request.POST.get('title')
                content=request.POST.get('markcontent')
                file=open('entries/'+title+'.md','w')
                file.write(content)
                file.close()
                return redirect('wiki/'+title)
            else :
                return HttpResponse("""<h1>sorry it's already existed</h1><br>
                                    <br>
                                    <form action='wiki'>
                                    <input type='submit' value='back to main' style='margin-left:10%;'>
                                    </form>""")
        except:
            return HttpResponse('sorry try agian later')

    else :
        return render(request,'encyclopedia/create_entry.html',{'form':new_one})
def random_paging(request):
    pages=util.list_entries()
    hitted=random.choice(pages).lower()
    return redirect('wiki/'+hitted)
def search_section(request):
    entry=request.GET.get('q')
    print(entry.lower())
    entries=[i.lower() for i in util.list_entries()]
    print(entries)
    if entry.lower() in entries :
        return redirect('wiki/'+entry)
    else :
        result=[]
        for i in range(len(entries)):
            if entry.lower() in entries[i] :
                result.append(util.list_entries()[i])
        if len(result) != 0:
            return render(request,'encyclopedia/SearchReslut.html',{'suggestions':result})
        else :
            return HttpResponse("""<h1>sorry we didn't find existed results for your search</h1>
                                    <br>
                                    <br>
                                    <form action='wiki'>
                                    <input type='submit' value='back to main' style='margin-left:20%;'>
                                    </form>
                                    """)
def edited(request,entry):
    if request.method=='POST':
        new_entry=open('entries/'+entry+'.md','w')
        new_entry.write(request.POST.get("new_content"))
        new_entry.close()
        return redirect('/wiki/'+entry)
    else:
        old=open('entries/'+entry+'.md','r')
        current=old.read()
        old.close()
        print(current)
        return render(request,'encyclopedia/edit.html',{'content':current.strip(),'entry':entry})
