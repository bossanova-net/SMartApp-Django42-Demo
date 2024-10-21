

import unittest

from django.test import TestCase
from django.urls import reverse

from app.models import Project
from app.views import manage_project


class ManageProjectTestCase(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            description='This is a test project.',
        )

    def test_get_manage_project(self):
        url = reverse('manage_project')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('app/project_manage.html')

    def test_post_manage_project(self):
        url = reverse('manage_project')
        data = {
            'name': 'Test Project 2',
            'description': 'This is a test project 2.',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

        project = Project.objects.get(id=2)
        self.assertEqual(project.name, 'Test Project 2')
        self.assertEqual(project.description, 'This is a test project 2.')

