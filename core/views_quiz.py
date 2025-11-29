# core/views_quiz.py
import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .models import Quiz, QuizQuestion, QuizAnswer, QuizResult

# core/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from .models import Quiz
import random



@require_GET
def quiz_random(request):
    quiz = Quiz.objects.filter(is_active=True).order_by('?').first()
    if not quiz:
        return JsonResponse({'ok': False, 'error': 'no_quiz'}, status=404)

    # Питання (з урахуванням міксу)
    qs = list(quiz.questions.all().order_by('order', 'id'))
    if quiz.shuffle_questions:
        random.shuffle(qs)

    questions_payload = []
    for q in qs:
        answers = list(q.answers.all().order_by('order', 'id'))
        if quiz.shuffle_answers:
            random.shuffle(answers)
        questions_payload.append({
            'id': q.id,
            'text': q.text,
            'image': (q.image.url if q.image else ''),
            'answers': [
                {
                    'id': a.id,
                    'text': a.text,
                    'image': (a.image.url if a.image else ''),
                    'code': a.code,
                    'is_correct': a.is_correct,
                } for a in answers
            ]
        })

    results_payload = [
        {
            'code': r.code,
            'title': r.title,
            'image': (r.image.url if r.image else '')
        } for r in quiz.results.all().order_by('order', 'id')
    ]

    payload = {
        'ok': True,
        'quiz': {
            'id': quiz.id,
            'title': quiz.title,
            'subtitle': quiz.subtitle,
            'image_url': quiz.image_url,
            'questions': questions_payload,
            'results': results_payload,
        }
    }
    return JsonResponse(payload, status=200)


def _q_to_dict(q, shuffle_answers=False):
    answers = list(q.answers.order_by('order', 'id'))
    if not answers:
        return None
    if shuffle_answers:
        random.shuffle(answers)
    return {
        'id': q.id,
        'text': q.text,
        'image': q.image.url if q.image else None,
        'answers': [
            {
                'id': a.id,
                'text': a.text,
                'image': a.image.url if a.image else None,
                'code': a.code or '',
            } for a in answers
        ]
    }


@require_POST
def quiz_submit(request):
    import json
    payload = json.loads(request.body.decode('utf-8'))
    quiz_id = payload.get('quiz_id')
    answers = payload.get('answers', [])  # [{question: id, answer: id}, ...]

    try:
        quiz = Quiz.objects.get(pk=quiz_id, is_active=True)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'bad_quiz'}, status=404)

    answer_ids = {a['answer'] for a in answers if 'answer' in a}

    # Визначаємо режим: “правильні відповіді” чи “за кодами”
    has_correct = QuizAnswer.objects.filter(
        question__quiz=quiz, is_correct=True
    ).exists()

    if has_correct:
        correct_ids = set(
            QuizAnswer.objects.filter(question__quiz=quiz, is_correct=True)
            .values_list('id', flat=True)
        )
        score = sum(1 for aid in answer_ids if aid in correct_ids)
        total = quiz.questions.count()
        return JsonResponse({'mode': 'correct', 'score': score, 'total': total})
    else:
        # підсумовуємо коди
        from collections import Counter
        codes = QuizAnswer.objects.filter(id__in=answer_ids)\
                .values_list('code', flat=True)
        cnt = Counter([c or '' for c in codes])
        top = cnt.most_common(1)[0][0] if cnt else ''
        result = QuizResult.objects.filter(quiz=quiz, code=top).first()
        if not result:
            return JsonResponse({'mode': 'codes', 'code': top, 'result': None})
        return JsonResponse({
            'mode': 'codes',
            'code': result.code,
            'result': {'title': result.title,
                       'image': result.image.url if result.image else None}
        })
