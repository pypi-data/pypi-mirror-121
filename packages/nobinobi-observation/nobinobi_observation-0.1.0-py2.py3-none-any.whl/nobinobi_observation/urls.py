# -*- coding: utf-8 -*-
from django.urls import path, include

from nobinobi_observation import views

app_name = 'nobinobi_observation'
urlpatterns = [
    path(
        'api/observation/<uuid:child_pk>/',
        views.ObservationViewSet.as_view({'get': 'list'}),
        name='api-observation'
    ),
    path("observation/", include([
        path("observation/", include([
            path("",
                 view=views.ObservationListView.as_view(),
                 name='Observation_list',
                 ),
            path("~create/",
                 view=views.ObservationCreateView.as_view(),
                 name='Observation_create',
                 ),
            path("~choice/",
                 view=views.ObservationChoiceView.as_view(),
                 name='Observation_choice',
                 ),
            path("child/<uuid:pk>/",
                 view=views.ObservationDetailListView.as_view(),
                 name='Observation_detail_list',
                 ),
            path("<int:pk>/", include([
                path("",
                     view=views.ObservationDetailView.as_view(),
                     name='Observation_detail', ),
                path("~delete/",
                     view=views.ObservationDeleteView.as_view(),
                     name='Observation_delete', ),
                path("~update/",
                     view=views.ObservationUpdateView.as_view(),
                     name='Observation_update',
                     ),
            ])),
        ]))
    ]))
]
