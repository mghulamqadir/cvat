# Copyright (C) 2026 xis.ai
#
# SPDX-License-Identifier: MIT

from types import SimpleNamespace
from unittest import TestCase, mock

from cvat.apps.engine.permissions import TaskPermission
from cvat.apps.test.views import TaskAnnotationAnalyticsViewSet


class TestTaskAnnotationAnalyticsViewSet(TestCase):
    def test_returns_counts_and_zero_count_labels(self):
        task = mock.Mock(id=12)
        labels = [
            SimpleNamespace(id=1, name="car"),
            SimpleNamespace(id=2, name="person"),
        ]
        task.get_labels.return_value.order_by.return_value = labels
        view = TaskAnnotationAnalyticsViewSet()
        view.get_object = mock.Mock(return_value=task)

        with mock.patch("cvat.apps.test.views.LabeledShape.objects") as objects:
            objects.filter.return_value.values.return_value.annotate.return_value = [
                {"label_id": 2, "count": 3},
            ]

            response = view.retrieve(mock.Mock())

        objects.filter.assert_called_once_with(job__segment__task=task)
        self.assertEqual(
            response.data,
            {
                "task_id": 12,
                "classes": [
                    {"label": "car", "count": 0},
                    {"label": "person", "count": 3},
                ],
            },
        )

    def test_uses_cvat_task_permission(self):
        self.assertIs(TaskAnnotationAnalyticsViewSet.iam_permission_class, TaskPermission)
