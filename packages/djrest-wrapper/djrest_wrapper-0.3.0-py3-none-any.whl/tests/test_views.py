from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from djrest_wrapper.exceptions.apis.errors import *
from tests.models import ExampleModel
from djrest_wrapper.exceptions.apis import errors


class ExampleAPITestCase(APITestCase):
    def setUp(self):
        pass

    def test_create_example(self):
        url = reverse('example-list')
        data = {
            'text': 'some text'
        }
        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIsNotNone(response.json().get(
            'data').get('examplemodel', None))

        id = response.json().get('data').get('examplemodel').get('id')
        self.assertIsNotNone(ExampleModel.objects.get(id=id))

    def test_create_example_failure(self):
        url = reverse('example-list')
        data = {
        }
        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json().get('err'), True)

        self.assertEqual(response.json().get('err_code'),
                         errors.ERR_INPUT_VALIDATION)

    def test_list_example(self):
        for i in range(20):
            ExampleModel.objects.create(text=f'model number {i}')

        url = reverse('example-list')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        total_pages = response.json().get('data').get('page').get('total_pages')
        for i in range(1, total_pages+1):
            models = response.json().get('data').get('examples')
            self.assertIsInstance(models, list)
            next_page = response.json().get('data').get('page').get('next')
            if next_page != None:
                response = self.client.get(path=next_page)
            else:
                break