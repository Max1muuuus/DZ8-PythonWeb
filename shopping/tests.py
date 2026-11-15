from django.test import TestCase


class ShoppingListTests(TestCase):
    def test_empty_or_whitespace_item_is_not_added(self):
        for item in ('', '   '):
            with self.subTest(item=item):
                response = self.client.post(
                    '/shopping/',
                    {'action': 'add', 'item': item},
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Введіть назву товару')
                self.assertEqual(self.client.session.get('shopping_list', []), [])

    def test_profile_name_is_saved_and_visible_on_other_pages(self):
        response = self.client.post(
            '/shopping/profile/',
            {'action': 'save', 'name': '  Олена  '},
        )

        self.assertRedirects(response, '/shopping/profile/')
        self.assertEqual(self.client.session['profile_name'], 'Олена')
        self.assertContains(self.client.get('/shopping/'), 'Вітаємо, Олена!')
        self.assertContains(self.client.get('/shopping/about/'), 'Вітаємо, Олена!')

    def test_profile_name_can_be_cleared(self):
        self.client.post('/shopping/profile/', {'action': 'save', 'name': 'Олена'})

        response = self.client.post('/shopping/profile/', {'action': 'clear'})

        self.assertRedirects(response, '/shopping/profile/')
        self.assertNotIn('profile_name', self.client.session)
        self.assertNotContains(self.client.get('/shopping/'), 'Вітаємо, Олена!')
