# Copyright (C) 2026 xis.ai
#
# SPDX-License-Identifier: MIT

from django.db.models import Count
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from cvat.apps.engine.models import LabeledShape, Task
from cvat.apps.engine.permissions import TaskPermission


class TaskAnnotationAnalyticsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Return drawn-shape counts for every label configured on a task."""

    queryset = Task.objects
    iam_permission_class = TaskPermission

    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()
        counts_by_label_id = {
            row["label_id"]: row["count"]
            for row in (
                LabeledShape.objects.filter(job__segment__task=task)
                .values("label_id")
                .annotate(count=Count("id"))
            )
        }
        classes = [
            {
                "label": label.name,
                "count": counts_by_label_id.get(label.id, 0),
            }
            for label in task.get_labels().order_by("name")
        ]

        return Response({"task_id": task.id, "classes": classes})
