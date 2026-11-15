import datetime

from django.shortcuts import redirect, render

# Create your views here.
def shopping_list(request):
    items = request.session.get('shopping_list', [])
    last_visit = request.COOKIES.get('last_visit')
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            item_name = request.POST.get('item', '').strip()
            if not item_name:
                return render(
                    request,
                    'shopping/index.html',
                    {
                        'items': items,
                        'profile_name': request.session.get('profile_name', ''),
                        'error': 'Введіть назву товару, щоб додати його до списку.',
                    },
                )
            items.append(item_name)
            request.session['shopping_list'] = items
            return redirect('shopping_list')
        elif action == 'remove':
            try:
                index = int(request.POST.get('index', -1))
            except ValueError:
                return redirect('shopping_list')
            if 0 <= index < len(items):
                items.pop(index)
                request.session['shopping_list'] = items
            return redirect('shopping_list')
        elif action == 'clear':
            request.session['shopping_list'] = []
            return redirect('shopping_list')
    response = render(
        request,
        'shopping/index.html',
        {
            'items': items,
            'profile_name': request.session.get('profile_name', ''),
        },
    )
    response.set_cookie('last_visit', current_time)

    return response


def about(request):
    return render(
        request,
        'shopping/about.html',
        {'profile_name': request.session.get('profile_name', '')},
    )


def profile(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save':
            name = request.POST.get('name', '').strip()
            if name:
                request.session['profile_name'] = name
                return redirect('profile')
            return render(
                request,
                'shopping/profile.html',
                {
                    'profile_name': request.session.get('profile_name', ''),
                    'error': "Введіть ім'я перед збереженням.",
                },
            )
        if action == 'clear':
            request.session.pop('profile_name', None)
            return redirect('profile')

    return render(
        request,
        'shopping/profile.html',
        {'profile_name': request.session.get('profile_name', '')},
    )