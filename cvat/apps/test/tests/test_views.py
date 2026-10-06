# Copyright (C) 2026 xis.ai
#
# SPDX-License-Identifier: MIT

from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from cvat.apps.engine.models import Job, Label, LabeledShape, Segment, SourceType, Task
from cvat.apps.iam.models import User
from cvat.apps.iam.permissions import PolicyEnforcer


class TaskAnnotationAnalyticsAPITestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="analytics-owner", password="password")
        self.outsider = User.objects.create_user(username="analytics-outsider", password="password")
        self.task = Task.objects.create(name="analytics task", owner=self.owner)
        self.other_task = Task.objects.create(name="other analytics task", owner=self.owner)
        self.car = Label.objects.create(task=self.task, name="car")
        self.person = Label.objects.create(task=self.task, name="person")
        Label.objects.create(task=self.task, name="empty")
        other_label = Label.objects.create(task=self.other_task, name="other")
        job = Job.objects.create(segment=Segment.objects.create(task=self.task, start_frame=0, stop_frame=0))
        other_job = Job.objects.create(segment=Segment.objects.create(task=self.other_task, start_frame=0, stop_frame=0))
        for job_, label, source in (
            (job, self.car, SourceType.FILE),
            (job, self.person, SourceType.MANUAL),
            (other_job, other_label, SourceType.FILE),
        ):
            LabeledShape.objects.create(
                job=job_, label=label, frame=0, type="rectangle", points=[0, 0, 1, 1], source=source,
            )

    @staticmethod
    def _allow_task_owner(_, request, __, task):
        return request.user == task.owner

    def _get_as_owner(self, **query):
        self.client.force_login(self.owner)
        with mock.patch.object(PolicyEnforcer, "has_object_permission", self._allow_task_owner):
            return self.client.get(f"/api/test/tasks/{self.task.id}/annotation-analytics", query)

    def test_returns_database_counts_zeroes_and_excludes_other_tasks(self):
        response = self._get_as_owner()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data, {
            "task_id": self.task.id,
            "source": None,
            "classes": [
                {"label": "car", "count": 1},
                {"label": "empty", "count": 0},
                {"label": "person", "count": 1},
            ],
        })

    def test_filters_counts_by_source(self):
        response = self._get_as_owner(source=SourceType.FILE)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data["source"], SourceType.FILE)
        self.assertEqual(response.data["classes"], [
            {"label": "car", "count": 1},
            {"label": "empty", "count": 0},
            {"label": "person", "count": 0},
        ])

    def test_rejects_anonymous_request(self):
        response = self.client.get(f"/api/test/tasks/{self.task.id}/annotation-analytics")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_user_without_task_access(self):
        self.client.force_login(self.outsider)
        with mock.patch.object(PolicyEnforcer, "has_object_permission", self._allow_task_owner):
            response = self.client.get(f"/api/test/tasks/{self.task.id}/annotation-analytics")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
