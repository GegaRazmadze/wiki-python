from django.shortcuts import render, redirect
from django.http import HttpResponse

import random

import markdown2

from re import search

from . import util

def index(request):
    if request.method == "POST":
        # get query and Uppercase it:
        query = request.POST.get('q')

        entries = util.list_entries()
        for entry in entries:
            if query.casefold() == entry.casefold():
                # get file with name
                get_entry = util.get_entry(query)
                #check
                if get_entry is None:
                    return render(request, "encyclopedia/index.html")
                return render(request, "encyclopedia/content.html", {
                    "content":  markdown2.markdown(get_entry),
                })
            
        # if there is any query like entries:
        # for entry in entries:
        filtered = []
        for entry in entries:
            # for same char case (caseFold) and startswith:
            if entry.casefold().startswith(query.casefold()):
                filtered.append(entry)
            
        return render(request, "encyclopedia/index.html", {
        "entries": filtered,
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
        })

def entry(request, name):
   #check if enry exist :
    name = name
    # if Get reqves has made
    entries = util.list_entries()
    if name not in entries:
        return render(request, "encyclopedia/index.html")
    #if exisit
    else:
        # Give me file
        get_entry = util.get_entry(name)
        #check
        if get_entry is None:
            return render(request, "encyclopedia/index.html")
        return render(request, "encyclopedia/content.html", {
            "title":name,
            "content":  markdown2.markdown(get_entry),
        })

def createNew(request):
    if request.method == "POST":
        # get query:
        title = request.POST.get('title')
        content = request.POST.get('textarea')
        # check title and content
        if title is None or content is None:
            return render(request, "encyclopedia/createNew.html", {
                'alert': True
            })
        # check if there is same entry:
        entries = util.list_entries()
        for entry in entries:
            if title.casefold() == entry.casefold():
                return render(request, "encyclopedia/createNew.html", {
                'same': True
            })

        # save Page
        util.save_entry(title,content)
            # Give me file
        get_entry = util.get_entry(title)
        #check
        if get_entry is None:
            return render(request, "encyclopedia/index.html")

        return render(request, "encyclopedia/content.html", {
            "title": title,
            "content":  markdown2.markdown(get_entry),
        })

    else:
        return render(request, "encyclopedia/createNew.html")


def editPage(request):
    if request.method == "POST":
        # get query:
        title = request.POST.get('title')
        content = request.POST.get('edit_textarea')
        # if request is Edit Post
        if content is None and title is not None:
            # check title and content
            if title is None:
                return render(request, "encyclopedia/editPage.html", {
                    'alert': True
                })
            # get Page content
            content = util.get_entry(title)
            return render(request, "encyclopedia/editPage.html", {
                    'title':title,
                    'content': content
                })
        # if request is to save post
        if content is not None and title is not None:
                # save Page
            util.save_entry(title,content)
                # Give me file
            get_entry = util.get_entry(title)
            #check
            if get_entry is None:
                return render(request, "encyclopedia/index.html")

            return render(request, "encyclopedia/content.html", {
                "title": title,
                "content":  markdown2.markdown(get_entry),
            })

    else:
        return render(request, "encyclopedia/editPage.html")

def rendomPage(request):
    entries = util.list_entries()
    # give me rendom number
    rendom_number = random.randint(0,(len(entries)-1))
    name = entries[rendom_number]
    # Give me file
    get_entry = util.get_entry(name)
    #check
    if get_entry is None:
        return render(request, "encyclopedia/index.html")
    return render(request, "encyclopedia/content.html", {
        "title":name,
        "content":  markdown2.markdown(get_entry),
    })
    
