from django.test import TestCase


class PersonalCabinetTests(TestCase):
    def test_profile_saves_name_and_theme_and_shows_greeting(self):
        response = self.client.post(
            '/cabinet/',
            {'name': '  Олена  ', 'theme': 'dark'},
        )

        self.assertRedirects(response, '/cabinet/')
        self.assertEqual(self.client.session['cabinet_name'], 'Олена')
        self.assertEqual(response.cookies['cabinet_theme'].value, 'dark')
        self.assertContains(self.client.get('/cabinet/'), 'Вітаємо, Олена!')

    def test_profile_shows_previous_visit_time(self):
        first_response = self.client.get('/cabinet/')

        self.assertContains(first_response, 'перший візит')
        self.assertIn('cabinet_last_visit', self.client.session)

        second_response = self.client.get('/cabinet/')

        self.assertContains(second_response, 'Останнє відвідування:')

    def test_tasks_can_be_added_listed_deleted_and_counted(self):
        self.client.post('/cabinet/tasks/', {'action': 'add', 'task': '  Купити хліб  '})
        response = self.client.get('/cabinet/tasks/')

        self.assertContains(response, 'Купити хліб')
        self.assertContains(response, 'Усього справ: <strong>1</strong>')

        self.client.post('/cabinet/tasks/', {'action': 'delete', 'index': '0'})

        self.assertNotContains(self.client.get('/cabinet/tasks/'), 'Купити хліб')

    def test_blank_task_is_not_added(self):
        response = self.client.post(
            '/cabinet/tasks/',
            {'action': 'add', 'task': '   '},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введіть назву справи.')
        self.assertEqual(self.client.session.get('cabinet_tasks', []), [])

    def test_settings_can_clear_name_tasks_and_theme_cookie(self):
        self.client.post('/cabinet/', {'name': 'Олена', 'theme': 'dark'})
        self.client.post('/cabinet/tasks/', {'action': 'add', 'task': 'Завдання'})

        self.client.post('/cabinet/settings/', {'action': 'clear_name'})
        self.client.post('/cabinet/settings/', {'action': 'clear_tasks'})
        response = self.client.post('/cabinet/settings/', {'action': 'clear_theme'})

        self.assertNotIn('cabinet_name', self.client.session)
        self.assertNotIn('cabinet_tasks', self.client.session)
        self.assertEqual(response.cookies['cabinet_theme'].value, '')
