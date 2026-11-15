from django.shortcuts import redirect, render
from django.utils import timezone


THEME_COOKIE = 'cabinet_theme'
THEMES = {'light', 'dark'}
THEME_COOKIE_MAX_AGE = 60 * 60 * 24 * 365


def _render(request, template_name, context=None, status=200):
    page_context = {
        'profile_name': request.session.get('cabinet_name', ''),
        'theme': request.COOKIES.get(THEME_COOKIE, 'light'),
    }
    if page_context['theme'] not in THEMES:
        page_context['theme'] = 'light'
    if context:
        page_context.update(context)
    return render(request, template_name, page_context, status=status)


def _save_theme(response, theme):
    if theme in THEMES:
        response.set_cookie(
            THEME_COOKIE,
            theme,
            max_age=THEME_COOKIE_MAX_AGE,
            samesite='Lax',
        )
    return response


def profile(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        theme = request.POST.get('theme', 'light')
        if not name:
            return _render(
                request,
                'personal_cabinet/profile.html',
                {'error': "Введіть ім'я, щоб зберегти профіль."},
                status=400,
            )
        if theme not in THEMES:
            return _render(
                request,
                'personal_cabinet/profile.html',
                {
                    'error': 'Оберіть одну з доступних тем.',
                    'selected_theme': 'light',
                },
                status=400,
            )
        request.session['cabinet_name'] = name
        response = redirect('personal_cabinet:profile')
        return _save_theme(response, theme)

    previous_visit = request.session.get('cabinet_last_visit')
    request.session['cabinet_last_visit'] = timezone.localtime().strftime(
        '%d.%m.%Y о %H:%M:%S'
    )
    return _render(
        request,
        'personal_cabinet/profile.html',
        {'last_visit': previous_visit},
    )


def tasks(request):
    task_list = request.session.get('cabinet_tasks', [])
    error = ''

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            task_name = request.POST.get('task', '').strip()
            if task_name:
                task_list.append(task_name)
                request.session['cabinet_tasks'] = task_list
                return redirect('personal_cabinet:tasks')
            error = 'Введіть назву справи.'
        elif action == 'delete':
            try:
                index = int(request.POST.get('index', '-1'))
            except ValueError:
                index = -1
            if 0 <= index < len(task_list):
                task_list.pop(index)
                request.session['cabinet_tasks'] = task_list
                return redirect('personal_cabinet:tasks')

    return _render(
        request,
        'personal_cabinet/tasks.html',
        {'tasks': task_list, 'error': error},
    )


def settings(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save_theme':
            theme = request.POST.get('theme', '')
            if theme not in THEMES:
                return _render(
                    request,
                    'personal_cabinet/settings.html',
                    {'error': 'Оберіть одну з доступних тем.'},
                    status=400,
                )
            response = redirect('personal_cabinet:settings')
            return _save_theme(response, theme)
        if action == 'clear_name':
            request.session.pop('cabinet_name', None)
            return redirect('personal_cabinet:settings')
        if action == 'clear_tasks':
            request.session.pop('cabinet_tasks', None)
            return redirect('personal_cabinet:settings')
        if action == 'clear_theme':
            response = redirect('personal_cabinet:settings')
            response.delete_cookie(THEME_COOKIE, samesite='Lax')
            return response

    return _render(
        request,
        'personal_cabinet/settings.html',
        {'selected_theme': request.COOKIES.get(THEME_COOKIE, 'light')},
    )
