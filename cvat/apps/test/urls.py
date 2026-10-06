# Copyright (C) 2026 xis.ai
#
# SPDX-License-Identifier: MIT

from django.urls import path

from .views import TaskAnnotationAnalyticsViewSet

urlpatterns = [
    path(
        "tasks/<int:pk>/annotation-analytics",
        TaskAnnotationAnalyticsViewSet.as_view({"get": "retrieve"}, detail=True),
        name="task-annotation-analytics",
    ),
]
