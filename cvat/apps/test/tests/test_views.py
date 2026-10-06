# Copyright (C) 2026 xis.ai
#
# SPDX-License-Identifier: MIT

from types import SimpleNamespace
from unittest import TestCase, mock

from cvat.apps.engine.models import SourceType
from cvat.apps.engine.permissions import TaskPermission
from cvat.apps.test.views import TaskAnnotationAnalyticsViewSet


class TestTaskAnnotationAnalyticsViewSet(TestCase):
    def test_returns_counts_and_zero_count_labels(self):
        task = mock.Mock(id=12, project_id=None)
        labels = [
            SimpleNamespace(id=1, name="car"),
            SimpleNamespace(id=2, name="person"),
        ]
        view = TaskAnnotationAnalyticsViewSet()
        view.get_object = mock.Mock(return_value=task)

        with (
            mock.patch("cvat.apps.test.views.LabeledShape.objects") as objects,
            mock.patch("cvat.apps.test.views.Label.objects") as labels_objects,
        ):
            objects.filter.return_value.values.return_value.annotate.return_value = [
                {"label_id": 2, "count": 3},
            ]
            labels_objects.filter.return_value.order_by.return_value = labels

            response = view.retrieve(mock.Mock(query_params={}))

        objects.filter.assert_called_once_with(job__segment__task=task)
        self.assertEqual(
            response.data,
            {
                "task_id": 12,
                "source": None,
                "classes": [
                    {"label": "car", "count": 0},
                    {"label": "person", "count": 3},
                ],
            },
        )

    def test_filters_shapes_by_source(self):
        task = mock.Mock(id=12, project_id=None)
        view = TaskAnnotationAnalyticsViewSet()
        view.get_object = mock.Mock(return_value=task)

        with (
            mock.patch("cvat.apps.test.views.LabeledShape.objects") as objects,
            mock.patch("cvat.apps.test.views.Label.objects") as labels_objects,
        ):
            objects.filter.return_value.filter.return_value.values.return_value.annotate.return_value = []
            labels_objects.filter.return_value.order_by.return_value = []

            response = view.retrieve(mock.Mock(query_params={"source": SourceType.MANUAL}))

        objects.filter.assert_called_once_with(job__segment__task=task)
        objects.filter.return_value.filter.assert_called_once_with(source=SourceType.MANUAL)
        self.assertEqual(response.data["source"], SourceType.MANUAL)

    def test_uses_cvat_task_permission(self):
        self.assertIs(TaskAnnotationAnalyticsViewSet.iam_permission_class, TaskPermission)
