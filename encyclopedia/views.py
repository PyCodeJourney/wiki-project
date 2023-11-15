from django import forms
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice
import markdown2

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title:")
    content = forms.CharField(label="Page Content:", widget=forms.Textarea)


class EditEntryForm(forms.Form):
    content = forms.CharField(label="Page Content:", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    entry = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if entry is None:
        raise Http404
    entry = markdowner.convert(entry)
    return render(request, "encyclopedia/entry.html", {"title": title, "entry": entry})


def search(request):
    if request.method == "GET":
        query = request.GET.get("q")
        entry = util.get_entry(query)
        if entry is not None:
            return HttpResponseRedirect(
                reverse(
                    "encyclopedia:entry",
                    kwargs={"title": query},
                )
            )
        else:
            entries = util.list_entries()
            results = []
            for result in entries:
                if query.lower() in result.lower():
                    results.append(result)
            return render(
                request,
                "encyclopedia/search_results.html",
                {"title": query, "entries": results},
            )


def choose_random(request):
    title = choice(util.list_entries())
    return HttpResponseRedirect(
        reverse(
            "encyclopedia:entry",
            kwargs={"title": title},
        )
    )


def create_entry(request):
    if request.method == "POST":
        all_entries = util.list_entries()
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in all_entries:
                return HttpResponseForbidden("Such Entry already exists")
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(
                    reverse(
                        "encyclopedia:entry",
                        kwargs={"title": title},
                    )
                )
    return render(
        request,
        "encyclopedia/new_page.html",
        {"form": NewEntryForm()},
    )


def edit_entry(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(
                reverse(
                    "encyclopedia:entry",
                    kwargs={"title": title},
                )
            )
    return render(
        request,
        "encyclopedia/edit_page.html",
        {
            "title": title,
            "form": EditEntryForm(initial={"content": util.get_entry(title)}),
        },
    )
