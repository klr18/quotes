import random

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import QuoteForm, SourceForm
from .models import Quote, PageViews

def index(request):
    quote_list = Quote.objects.all()
    weights = Quote.objects.values_list('weight', flat=True)
    quote = random.choices(quote_list, weights=weights, k=1)[0]

    try:
        views = get_object_or_404(PageViews)
    except:
        PageViews().save()
        views = get_object_or_404(PageViews)

    views.total_views += 1
    views.save()

    context = {'quote': quote, 'views': views}
    return render(request, 'quotes/index.html', context)

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            return redirect('index')
    else:
        form = QuoteForm()

    context = {'form': form}
    return render(request, 'quotes/add_quote.html', context)

def add_source(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            source = form.save(commit=False)
            source.save()
            return redirect('add_quote')
    else:
        form = SourceForm()

    context = {'form': form}
    return render(request, 'quotes/add_source.html', context)

def like(request, pk):
    quote = get_object_or_404(Quote, pk=pk)

    voted = request.session.get('voted', {})

    prev_vote = voted.get(str(pk))

    if prev_vote == 'like':
        quote.likes -= 1
        voted.pop(str(pk))
    else:
        if prev_vote == 'dislike':
            quote.dislikes -= 1
        quote.likes += 1
        voted[str(pk)] = 'like'

    quote.save()
    request.session['voted'] = voted

    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})


def dislike(request, pk):
    quote = get_object_or_404(Quote, pk=pk)

    voted = request.session.get('voted', {})

    prev_vote = voted.get(str(pk))

    if prev_vote == 'dislike':
        quote.dislikes -= 1
        voted.pop(str(pk))
    else:
        if prev_vote == 'like':
            quote.likes -= 1
        quote.dislikes += 1
        voted[str(pk)] = 'dislike'

    quote.save()
    request.session['voted'] = voted

    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

def rating(request, sample):
    if sample == 'popular':
        quotes = Quote.objects.order_by('-likes')[:10]
        title = 'Наиболее популярные'
        data_list = quotes.values_list('likes', flat=True)
        title_graph = 'Количество лайков'
    elif sample == 'worst':
        quotes = Quote.objects.order_by('-dislikes')[:10]
        title = 'Худшие'
        data_list = quotes.values_list('dislikes', flat=True)
        title_graph = 'Количество дизлайков'
    elif sample == 'newest':
        quotes = Quote.objects.order_by('-id')[:10]
        title = 'Самые новые'
        data_list = quotes.values_list('id', flat=True)
        title_graph = 'Порядковый номер цитаты'
    elif sample == 'oldest':
        quotes = Quote.objects.order_by('id')[:10]
        title = 'Самые старые'
        data_list = quotes.values_list('id', flat=True)
        title_graph = 'Порядковый номер цитаты'
    elif sample == 'frequent':
        quotes = Quote.objects.order_by('-weight')[:10]
        title = 'Часто встречающиеся'
        data_list = quotes.values_list('weight', flat=True)
        title_graph = 'Показатель весов'
    elif sample == 'rare':
        quotes = Quote.objects.order_by('weight')[:10]
        title = 'Редкие'
        data_list = quotes.values_list('weight', flat=True)
        title_graph = 'Показатель весов'

    context = {'quotes': quotes, 'title': title, 'sample': sample,
               'quotes_text': list(range(1, 11)) if len(quotes) > 9 else list(range(1, len(quotes) + 1)),
               'data_list': data_list,
               'title_graph': title_graph,
               }
    return render(request, 'quotes/rating.html', context)