# -*- coding: utf-8 -*-
from django.urls import path, include, register_converter
from nobinobi_core.functions import FourDigitConverter, TwoDigitConverter
from nobinobi_daily_follow_up.utils import IsoDateConverter

from nobinobi_stats import views

app_name = 'nobinobi_stats'

register_converter(FourDigitConverter, 'yyyy')
register_converter(TwoDigitConverter, 'mmdd')
register_converter(IsoDateConverter, 'isodate')

urlpatterns = [
    path("stats/", include([
        path("attendance/", include([
            path("period/", include([
                path("~choice/", view=views.ChoiceAttendancePeriod.as_view(), name='choice_attendance_period'),
                path("<isodate:from_date>/<isodate:end_date>/", view=views.AttendancePeriod.as_view(),
                     name='attendance_period'),
            ])),
            path("calendar/", include([
                path("~choice/", view=views.ChoiceAttendanceCalendar.as_view(), name='choice_attendance_calendar'),
                path("<isodate:date>/", view=views.AttendanceCalendar.as_view(), name='attendance_calendar'),
            ])),
            path("child/", include([
                path("~choice/", view=views.ChoiceAttendanceChild.as_view(), name='choice_attendance_child'),
                path(
                    "<isodate:from_date>/<isodate:end_date>/<uuid:child>/",
                    view=views.AttendanceChild.as_view(),
                    name='attendance_child'
                ),
            ])),
        ])),
        path("occupancy/", include([
            path("period/", include([
                path("~choice/", view=views.ChoiceOccupancyPeriod.as_view(), name='choice_occupancy_period'),
                path("<isodate:from_date>/<isodate:end_date>/", view=views.OccupancyPeriod.as_view(),
                     name='occupancy_period'),
            ])),
        ])),
    ])),
]
