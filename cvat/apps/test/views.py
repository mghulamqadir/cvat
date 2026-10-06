# Copyright (C) 2026 xis.ai
#
# SPDX-License-Identifier: MIT

from django.db.models import Count
from rest_framework import mixins, serializers, viewsets
from rest_framework.response import Response

from cvat.apps.engine.models import Label, LabeledShape, SourceType, Task
from cvat.apps.engine.permissions import TaskPermission


class TaskAnnotationAnalyticsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Return drawn-shape counts for every label configured on a task."""

    queryset = Task.objects
    iam_permission_class = TaskPermission
    filter_backends = []

    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()
        source = request.query_params.get("source")
        source_values = tuple(item.value for item in SourceType)
        if source and source not in source_values:
            raise serializers.ValidationError(
                {"source": f"Unsupported source. Choose one of: {', '.join(source_values)}."}
            )

        shapes = LabeledShape.objects.filter(job__segment__task=task)
        if source:
            shapes = shapes.filter(source=source)

        counts_by_label_id = {
            row["label_id"]: row["count"]
            for row in shapes.values("label_id").annotate(count=Count("id"))
        }

        labels = (
            Label.objects.filter(project_id=task.project_id)
            if task.project_id
            else Label.objects.filter(task_id=task.id)
        )
        classes = [
            {
                "label": label.name,
                "count": counts_by_label_id.get(label.id, 0),
            }
            for label in labels.order_by("name")
        ]

        return Response({"task_id": task.id, "source": source, "classes": classes})
