from django import forms
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Prefetch
import json
from django.contrib.auth.forms import AuthenticationForm

from videos.models import Video
from django.urls import reverse, NoReverseMatch

from .models import Post, PostImage, WinxCard, Quiz, QuizQuestion, QuizResult, Horoscope
from games.models import Game
from django.db.models.functions import Random   # ⬅ додай

from django.db.models import F
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from .models import Poll, PollOption  # + ваші інші імпорти


# core/views.py (фрагменти)
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Comment
# ...

from django import forms
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
# core/views.py
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from .models import Post, Comment
from .forms import CommentForm




@login_required(login_url='authbox:login')
def post_comment(request, slug):
    # Пропускаємо лише POST від авторизованих
    if request.method != 'POST':
        return redirect('core:post_detail', slug=slug)

    article = get_object_or_404(Post, type='post', slug=slug)

    # Форму все одно валідовуємо (напр., на наявність body)
    form = CommentForm(request.POST)
    if form.is_valid():
        c = Comment(
            post=article,
            user=request.user,
            # якщо у вашій моделі є display_name — можна зберегти його як нікнейм
            display_name=form.cleaned_data.get('display_name') or request.user.get_username(),
            body=form.cleaned_data['body'],
        )
        c.save()

    return redirect('core:post_detail', slug=slug)


def core(request):
    news = Post.objects.filter(type='news')[:6]
    articles = Post.objects.filter(type='post')[:6]
    quiz_exists = Quiz.objects.filter(is_active=True).exists()
    horoscope = Horoscope.objects.first()
    cards = WinxCard.objects.filter(is_active=True).order_by('order', 'id')

    latest_videos = Video.objects.order_by('-created_at')[:4]  # <— нове
     # === Гра дня (остання додана) ===
    featured_game = Game.objects.order_by(Random()).first()   # ⬅ випадкова гра
    featured_game_url = None
    if featured_game:
        try:
            featured_game_url = reverse('games:play', args=[featured_game.slug])
        except Exception:
            try:
                featured_game_url = reverse('games:detail', args=[featured_game.slug])
            except Exception:
                featured_game_url = f"/games/{featured_game.slug}/"
    
    active_poll = Poll.objects.filter(is_active=True).prefetch_related('options').first()
    return render(request, 'core/index.html', {
        'news': news,
        'articles': articles,
        'quiz_exists': quiz_exists,
        'horoscope': horoscope,
        'cards': cards,
        'latest_videos': latest_videos,
        "login_form" : AuthenticationForm(request=request),
        'featured_game': featured_game,
        'featured_game_url': featured_game_url,
        'poll': active_poll,  # <— ДОДАНО
    })


def _poll_payload(poll):
    total = poll.total_votes or 0
    data = []
    for o in poll.options.all():
        pct = int(round((o.votes * 100.0 / total), 0)) if total else 0
        data.append({'id': o.id, 'text': o.text, 'votes': o.votes, 'pct': pct})
    return {'question': poll.question, 'total': total, 'options': data}

@require_POST
def poll_vote(request, slug):
    poll = get_object_or_404(Poll, slug=slug, is_active=True)
    # анти-повтор: по кукі
    cookie_name = f'voted_poll_{poll.pk}'
    if request.COOKIES.get(cookie_name):
        resp = JsonResponse({'ok': False, 'reason': 'already', 'results': _poll_payload(poll)})
        resp.status_code = 409
        return resp

    option_id = request.POST.get('option')
    try:
        opt = poll.options.get(pk=option_id)
    except PollOption.DoesNotExist:
        return JsonResponse({'ok': False, 'reason': 'bad-option'}, status=400)

    # інкремент атомарно
    PollOption.objects.filter(pk=opt.pk).update(votes=F('votes') + 1)
    poll.refresh_from_db()

    resp = JsonResponse({'ok': True, 'results': _poll_payload(poll)})
    # зберігаємо кукі на рік
    resp.set_cookie(cookie_name, '1', max_age=60 * 60 * 24 * 365, samesite='Lax')
    return resp

@require_GET
def poll_results(request, slug):
    poll = get_object_or_404(Poll, slug=slug)
    return JsonResponse({'ok': True, 'results': _poll_payload(poll)})




from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from .models import Post

# опціонально: якщо BeautifulSoup не встановлено, постав:
# pip install beautifulsoup4
try:
    from bs4 import BeautifulSoup  # для fallback-розбору <img> всередині body
except Exception:
    BeautifulSoup = None


def post_detail(request, slug):
    # УВАГА: тип саме 'post' (а не 'article')
    print(2)
    article = get_object_or_404(Post, type='post', slug=slug)


    comments = (Comment.objects
                .filter(post=article)
                .select_related('user__profile')
                .order_by('created_at'))

    # єдина форма, яку й передаємо в шаблон
    comment_form = CommentForm()
    if request.user.is_authenticated and 'display_name' in comment_form.fields:
        comment_form.fields['display_name'].widget = forms.HiddenInput()


    # Галерея з пов’язаних зображень (аналог ігор): пропускаємо обкладинку
    related = list(article.images.all())
    gallery = related[1:] if related else []

    # За замовчуванням показуємо оригінальне тіло
    body_html = article.body
    inline_gallery = []

    # Якщо пов’язаних зображень немає — дістаємо <img> із body
    if not gallery and BeautifulSoup is not None and body_html:
        try:
            soup = BeautifulSoup(body_html, "html.parser")
            imgs = soup.find_all("img")
            for im in imgs:
                src = im.get("src")
                alt = im.get("alt", "")
                if src:
                    inline_gallery.append({"src": src, "alt": alt})
                im.decompose()  # прибираємо <img> з тіла, щоб не дублювати
            body_html = str(soup)
        except Exception:
            pass

    prev_item = Post.objects.filter(type='post', id__lt=article.id).order_by('-id').first()
    next_item = Post.objects.filter(type='post', id__gt=article.id).order_by('id').first()

    return render(request, 'core/post_detail.html', {
        "article": article,
        "prev_item": prev_item,
        "next_item": next_item,
        "gallery": gallery,                 # пов’язані зображення (після обкладинки)
        "inline_gallery": inline_gallery,   # fallback із <img> у body
        "article_body": mark_safe(body_html),
        "comments": comments,
        "comment_form": comment_form,
    })

# core/views.py (доповнення)
from django.views.decorators.http import require_GET
from .models import Quiz  # вже імпортовано у тебе; просто переконайся

def _quiz_to_dict(q: Quiz):
    qs = q.questions.order_by('order', 'id').prefetch_related('answers')
    questions = []
    for qu in qs:
        answers = []
        for a in qu.answers.order_by('order', 'id'):
            answers.append({
                'id': a.id, 'text': a.text,
                'image': a.image.url if a.image else '',
                'code': a.code, 'is_correct': a.is_correct,
            })
        questions.append({
            'id': qu.id, 'text': qu.text,
            'image': qu.image.url if qu.image else '',
            'answers': answers,
        })
    results = [{
        'code': r.code, 'title': r.title,
        'image': r.image.url if r.image else '',
    } for r in q.results.order_by('order', 'id')]
    return {'title': q.title, 'subtitle': q.subtitle, 'questions': questions, 'results': results}

def quiz_list(request):
    quizzes = Quiz.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'core/quiz_list.html', {'quizzes': quizzes})

@require_GET
def quiz_get(request, slug):
    q = get_object_or_404(Quiz, slug=slug, is_active=True)
    return JsonResponse({'ok': True, 'quiz': _quiz_to_dict(q)})
