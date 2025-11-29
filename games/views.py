from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from .models import GameTheme, GameCategory, Game

def theme_list(request):
    themes = GameTheme.objects.all()
    return render(request, 'games/theme_list.html', {'themes': themes})

def theme_detail(request, theme_slug):
    # якщо зайшли за адресою /games/<game-slug>/ — чемно редіректимо на сторінку гри
    game = Game.objects.filter(slug=theme_slug).first()
    if game:
        return redirect('games:game_detail', slug=game.slug)

    theme = get_object_or_404(GameTheme, slug=theme_slug)
    categories = theme.categories.all().order_by('title')
    return render(request, 'games/theme_detail.html', {
        'theme': theme,
        'categories': categories,
    })

def category_detail(request, theme_slug, category_slug):
    theme = get_object_or_404(GameTheme, slug=theme_slug)
    category = get_object_or_404(GameCategory, slug=category_slug, theme=theme)
    games = category.games.all()
    return render(request, 'games/category_detail.html', {
        'theme': theme,
        'category': category,
        'games': games,
    })

# ⬇️ Працює і для короткого маршруту (тільки slug), і для вкладеного
def game_detail(request, slug, theme_slug=None, category_slug=None):
    """
    Якщо прийшли з короткого URL /games/g/<slug>/ — показуємо гру за slug.
    Якщо прийшли з вкладеного /games/<theme>/<category>/<slug>/ — валідуємо шлях повністю.
    """
    if theme_slug and category_slug:
        theme = get_object_or_404(GameTheme, slug=theme_slug)
        category = get_object_or_404(GameCategory, slug=category_slug, theme=theme)
        game = get_object_or_404(Game, slug=slug, category=category)
    else:
        game = get_object_or_404(Game, slug=slug)
        category = game.category
        theme = category.theme if category else None

    return render(request, 'games/game_detail.html', {
        'theme': theme,
        'category': category,
        'game': game,
    })

def game_play(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render(request, "games/game_play.html", {"game": game})
