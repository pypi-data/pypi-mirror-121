#  Copyright (c) 2021 <Florian Alu - alu@prolibre.com - https://www.prolibre.com>
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import datetime  # import the logging library
import logging
import sys

import arrow
from datetimerange import DateTimeRange
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_naive
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView
from nobinobi_child.models import Classroom, Child, AgeGroup, ChildToPeriod, FoodRestriction, Absence, \
    TYPE_PERIOD_CHOICES
from nobinobi_core.functions import week_span_from_date
from nobinobi_daily_follow_up.models import Presence

from nobinobi_kitchen.forms import KitchenSelectForm

# Get an instance of a logger
logger = logging.getLogger(__name__)


class KitchenSelectView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    """ View for select day for kitchen"""
    permission_required = ("nobinobi_daily_follow_up.can_view_kitchen",)
    template_name = "nobinobi_kitchen/kitchen_select.html"
    form_class = KitchenSelectForm

    def get_context_data(self, **kwargs):
        context = super(KitchenSelectView, self).get_context_data()
        context['title'] = _("Choosing a date for the kitchen view")
        return context

    def form_valid(self, form):
        date = form.cleaned_data['date']
        display_view = form.cleaned_data['display_view']
        if display_view == "0":
            return HttpResponseRedirect(reverse("nobinobi_kitchen:kitchen_view", kwargs={"date": date}))
        elif display_view == "1":
            return HttpResponseRedirect(reverse("nobinobi_kitchen:kitchen_view2", kwargs={"date": date}))
        else:
            return HttpResponseRedirect(reverse("nobinobi_kitchen:kitchen_view", kwargs={"date": date}))


class KitchenView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """ View for select day for kitchen"""
    permission_required = ("nobinobi_daily_follow_up.can_view_kitchen",)
    template_name = "nobinobi_kitchen/kitchen_view.html"

    def __init__(self):
        super().__init__()
        self.date = None
        self.dates_range = None
        self.classrooms = None
        self.classrooms_kindergarten = None
        self.age_groups = None
        self.day_list = None
        self.total_dict = None
        self.total_dict_kindergarten = None
        self.children_dict = None
        self.children_dict_kindergarten = None
        self.food_restrictions = None
        self.food_restrictions_dict = None
        self.PERIOD_ACCEPTED = [TYPE_PERIOD_CHOICES.morning, TYPE_PERIOD_CHOICES.day]

    def get_context_data(self, **kwargs):
        context = super(KitchenView, self).get_context_data()
        context['title'] = _("Kitchen View")
        self.date = self.kwargs.get("date")
        context['now'] = timezone.localtime()
        context['date'] = self.date
        self.dates_range = week_span_from_date(self.date)
        context['week_before'] = arrow.get(self.dates_range[0]).shift(weeks=-1)
        context['week_after'] = arrow.get(self.dates_range[-1]).shift(weeks=+1)
        # self.classrooms = Classroom.objects.all().values("id", "name", "capacity", 'mode')
        self.classrooms = list(Classroom.objects.filter(mode=Classroom.OPERATION_MODE.creche))
        self.classrooms_kindergarten = list(Classroom.objects.filter(mode=Classroom.OPERATION_MODE.kindergarten))
        self.age_groups = get_list_or_404(AgeGroup)
        context['age_groups'] = self.age_groups
        self.food_restrictions = list(FoodRestriction.objects.all())
        context['food_restrictions'] = self.food_restrictions
        self.day_list = self.create_day_list(self.dates_range)
        context["day_list"] = self.day_list
        self.total_dict = self.create_total_dict()
        self.total_dict_kindergarten = self.create_total_dict_kindergarten()
        self.children_dict = self.create_children_dict()
        self.children_dict_kindergarten = self.create_children_dict_kindergarten()
        self.food_restrictions_dict = self.create_food_restrictions_dict()
        context["children_dict"] = self.children_dict
        context["total_dict"] = self.total_dict
        context["children_dict_kindergarten"] = self.children_dict_kindergarten
        context["total_dict_kindergarten"] = self.total_dict_kindergarten
        return context

    @staticmethod
    def create_day_list(dates_range):
        day_list = []
        for date in dates_range:
            day_list.append(date)

        return day_list

    def create_children_dict(self):
        children = Child.objects.filter(status=Child.STATUS.in_progress,
                                        classroom__mode=Classroom.OPERATION_MODE.creche,
                                        age_group__isnull=False).prefetch_related(
            "food_restrictions")

        children_dict = {}
        for classroom in self.classrooms:
            children_dict[classroom] = {}
            for age_group in self.age_groups:
                children_dict[classroom][age_group] = {}

                for day in self.day_list:
                    children_dict[classroom][age_group][day.isoweekday()] = {
                        "normal": {"list": [], "total": 0}, "restrict": {"list": [], "total": 0},
                    }
        ctps = ChildToPeriod.objects.filter(start_date__lte=self.dates_range[-1],
                                            end_date__gte=self.dates_range[0], ).values_list("period__start_time",
                                                                                             "period__end_time",
                                                                                             "period__weekday",
                                                                                             "child__id",
                                                                                             "period__type")
        for child in children:
            frs = child.food_restrictions.all()
            for day in self.day_list:
                ctp_list = [ctp for ctp in ctps if
                            ctp[2] == day.isoweekday() and ctp[3] == child.id and ctp[4] in self.PERIOD_ACCEPTED]
                for period in ctp_list:
                    time_range_day = DateTimeRange(day, day)
                    # get period from day child
                    time_eat_start = datetime.datetime.combine(day, datetime.time(hour=12, minute=0))
                    time_eat_end = datetime.datetime.combine(day, datetime.time(hour=13, minute=0))
                    time_eat_range = DateTimeRange(time_eat_start, time_eat_end)

                    for date in time_range_day.range(datetime.timedelta(days=1)):
                        # create time range of period
                        start_date = datetime.datetime.combine(date, period[0])
                        end_date = datetime.datetime.combine(date, period[1])
                        time_range_period = DateTimeRange(start_date, end_date)
                        # if time range period is in time range absence
                        if time_eat_range.is_intersection(time_range_period):
                            if child and child.classroom:
                                try:
                                    child.age_group
                                except KeyError:
                                    exc_type, value, traceback = sys.exc_info()
                                    messages.warning("[Kitchen][Warning] Age group for [%s] is not set - [%s]" % child)

                                    logger.warning("[Kitchen][Warning] Age group for [%s] is not set - [%s]" % (
                                        child, exc_type.__name__))
                                else:
                                    if frs.count() > 0:
                                        if child not in \
                                            children_dict[child.classroom][child.age_group][date.isoweekday()][
                                                "restrict"][
                                                "list"]:
                                            children_dict[child.classroom][child.age_group][date.isoweekday()][
                                                "restrict"][
                                                "list"].append(child)
                                            children_dict[child.classroom][child.age_group][date.isoweekday()][
                                                "restrict"][
                                                "total"] += 1
                                            # on ajoute au total
                                            self.total_dict['age_group'][child.age_group.id]["days"][
                                                date.isoweekday()]["restrict_dict"][child] = {}

                                            for food_restriction in self.food_restrictions:
                                                self.total_dict['age_group'][child.age_group.id]["days"][
                                                    date.isoweekday()][
                                                    "restrict_dict"][child][food_restriction.id] = None
                                            for fr in frs:
                                                self.total_dict['age_group'][child.age_group.id]["days"][
                                                    date.isoweekday()][
                                                    "restrict_dict"][child][fr.id] = fr
                                            self.total_dict['age_group'][child.age_group.id]["days"][
                                                date.isoweekday()]["restrict"] += 1

                                    else:
                                        children_dict[child.classroom][child.age_group][date.isoweekday()]["normal"][
                                            "list"].append(child)
                                        children_dict[child.classroom][child.age_group][date.isoweekday()]["normal"][
                                            "total"] += 1
                                        #  on ajoute au total
                                        self.total_dict['age_group'][child.age_group.id]["days"][date.isoweekday()][
                                            "normal_list"].append(child)
                                        self.total_dict['age_group'][child.age_group.id]["days"][date.isoweekday()][
                                            "normal"] += 1

        presences_children = Presence.objects.select_related("child", "classroom").filter(
            child__in=list(children), date__range=[self.dates_range[0], self.dates_range[-1]]).order_by('date')

        for presence in presences_children:
            if presence.child not in \
                children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                    "normal"]["list"] and presence.child not in \
                children_dict[presence.classroom][presence.child.age_group][presence.date.isoweekday()][
                    "restrict"]["list"]:
                frs = presence.child.food_restrictions.all()
                if frs.count() > 0:
                    self.total_dict['age_group'][presence.child.age_group.id]["days"][presence.date.isoweekday()][
                        "restrict_dict"][presence.child] = {}
                    for food_restriction in self.food_restrictions:
                        self.total_dict['age_group'][presence.child.age_group.id]["days"][presence.date.isoweekday()][
                            "restrict_dict"][presence.child][food_restriction.id] = None
                    for fr in frs:
                        self.total_dict['age_group'][presence.child.age_group.id]["days"][presence.date.isoweekday()][
                            "restrict_dict"][presence.child][fr.id] = fr
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "restrict"]["total"] += 1
                    self.total_dict['age_group'][presence.child.age_group.id]["days"][presence.date.isoweekday()][
                        "restrict"] += 1
                else:
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "normal"]["list"].append(
                        presence.child)
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "normal"]["total"] += 1
                    self.total_dict['age_group'][presence.child.age_group.id]["days"][presence.date.isoweekday()][
                        "normal"] += 1

        #     absences
        date_list = [day.date() for day in self.day_list]

        absences = Absence.objects.filter(child__in=list(children), start_date__lte=self.dates_range[-1],
                                          end_date__gte=self.dates_range[0])
        for absence in absences:
            if make_naive(absence.start_date) > make_naive(absence.end_date):
                messages.error(self.request,
                               _("The absence {} has a start date after the end date.").format(absence))
            else:
                time_range_absence = DateTimeRange(make_naive(absence.start_date), make_naive(absence.end_date))
                # get period from day child
                # time_eat_start = datetime.datetime.combine(day, datetime.time(hour=12, minute=0))
                # time_eat_end = datetime.datetime.combine(day, datetime.time(hour=13, minute=0))
                # time_eat_range = DateTimeRange(time_eat_start, time_eat_end)

                for date in time_range_absence.range(datetime.timedelta(days=1)):
                    # create time range of period
                    if date.date() in date_list:
                        if absence.child in \
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "normal"][
                                "list"]:
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "normal"][
                                "list"].remove(absence.child)
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "normal"][
                                "total"] -= 1
                            self.total_dict['age_group'][absence.child.age_group.id]["days"][date.isoweekday()][
                                "normal"] -= 1
                            self.total_dict['age_group'][absence.child.age_group.id]["days"][date.isoweekday()][
                                "normal_list"].remove(absence.child)
                        elif absence.child in \
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "restrict"][
                                "list"]:
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "restrict"][
                                "list"].remove(absence.child)
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "restrict"][
                                "total"] -= 1
                            self.total_dict['age_group'][absence.child.age_group.id]["days"][date.isoweekday()][
                                "restrict"] -= 1
                            del (self.total_dict['age_group'][absence.child.age_group.id]["days"][date.isoweekday()][
                                "restrict_dict"][absence.child])

        return children_dict

    def create_children_dict_kindergarten(self):
        children = Child.objects.filter(status=Child.STATUS.in_progress,
                                        classroom__mode=Classroom.OPERATION_MODE.kindergarten).prefetch_related(
            "food_restrictions")

        children_dict = {}
        for classroom in self.classrooms_kindergarten:
            children_dict[classroom] = {}
            for age_group in self.age_groups:
                children_dict[classroom][age_group] = {}

                for day in self.day_list:
                    children_dict[classroom][age_group][day.isoweekday()] = {
                        "normal": {"list": [], "total": 0}, "restrict": {"list": [], "total": 0},
                    }
        ctps = ChildToPeriod.objects.filter(start_date__lte=self.dates_range[-1],
                                            end_date__gte=self.dates_range[0], ).values_list("period__start_time",
                                                                                             "period__end_time",
                                                                                             "period__weekday",
                                                                                             "child__id",
                                                                                             "period__type")
        for child in children:
            frs = child.food_restrictions.all()
            for day in self.day_list:
                ctp_list = [ctp for ctp in ctps if
                            ctp[2] == day.isoweekday() and ctp[3] == child.id and ctp[4] in self.PERIOD_ACCEPTED]
                for period in ctp_list:
                    time_range_day = DateTimeRange(day, day)
                    # get period from day child
                    time_eat_start = datetime.datetime.combine(day, datetime.time(hour=12, minute=0))
                    time_eat_end = datetime.datetime.combine(day, datetime.time(hour=13, minute=0))
                    time_eat_range = DateTimeRange(time_eat_start, time_eat_end)

                    for date in time_range_day.range(datetime.timedelta(days=1)):
                        # create time range of period
                        start_date = datetime.datetime.combine(date, period[0])
                        end_date = datetime.datetime.combine(date, period[1])
                        time_range_period = DateTimeRange(start_date, end_date)
                        # if time range period is in time range absence
                        if time_eat_range.is_intersection(time_range_period):
                            if child:
                                try:
                                    child.age_group
                                except KeyError:
                                    exc_type, value, traceback = sys.exc_info()
                                    messages.warning("[Kitchen][Warning] Age group for [%s] is not set - [%s]" % child)

                                    logger.warning("[Kitchen][Warning] Age group for [%s] is not set - [%s]" % (
                                        child, exc_type.__name__))
                                else:
                                    if frs.count() > 0:
                                        if child not in \
                                            children_dict[child.classroom][child.age_group][date.isoweekday()][
                                                "restrict"][
                                                "list"]:
                                            if child.classroom and child.age_group:
                                                children_dict[child.classroom][child.age_group][date.isoweekday()][
                                                    "restrict"][
                                                    "list"].append(child)
                                                children_dict[child.classroom][child.age_group][date.isoweekday()][
                                                    "restrict"][
                                                    "total"] += 1
                                                # on ajoute au total
                                                self.total_dict_kindergarten['age_group'][child.age_group.id]["days"][
                                                    date.isoweekday()][
                                                    "restrict_dict"][child] = {}

                                                for food_restriction in self.food_restrictions:
                                                    self.total_dict_kindergarten['age_group'][child.age_group.id][
                                                        "days"][
                                                        date.isoweekday()][
                                                        "restrict_dict"][child][food_restriction.id] = None
                                                for fr in frs:
                                                    self.total_dict_kindergarten['age_group'][child.age_group.id][
                                                        "days"][
                                                        date.isoweekday()][
                                                        "restrict_dict"][child][fr.id] = fr
                                                self.total_dict_kindergarten['age_group'][child.age_group.id]["days"][
                                                    date.isoweekday()][
                                                    "restrict"] += 1

                                    else:
                                        if child.classroom and child.age_group:
                                            children_dict[child.classroom][child.age_group][date.isoweekday()][
                                                "normal"][
                                                "list"].append(child)
                                            children_dict[child.classroom][child.age_group][date.isoweekday()][
                                                "normal"][
                                                "total"] += 1
                                            #  on ajoute au total
                                            self.total_dict_kindergarten['age_group'][child.age_group.id]["days"][
                                                date.isoweekday()][
                                                "normal_list"].append(child)
                                            self.total_dict_kindergarten['age_group'][child.age_group.id]["days"][
                                                date.isoweekday()][
                                                "normal"] += 1

        presences_children = Presence.objects.select_related("child", "classroom").filter(
            child__in=list(children), date__range=[self.dates_range[0], self.dates_range[-1]]).order_by('date')

        for presence in presences_children:
            if presence.child and presence.child.classroom and presence.child.age_group:
                if presence.child not in \
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "normal"]["list"] and presence.child not in \
                    children_dict[presence.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "restrict"]["list"]:
                    frs = presence.child.food_restrictions.all()
                    if frs.count() > 0:
                        self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["days"][
                            presence.date.isoweekday()][
                            "restrict_dict"][presence.child] = {}
                        for food_restriction in self.food_restrictions:
                            self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["days"][
                                presence.date.isoweekday()][
                                "restrict_dict"][presence.child][food_restriction.id] = None
                        for fr in frs:
                            self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["days"][
                                presence.date.isoweekday()][
                                "restrict_dict"][presence.child][fr.id] = fr
                        children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                            "restrict"]["total"] += 1
                        self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["days"][
                            presence.date.isoweekday()][
                            "restrict"] += 1
                    else:
                        children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                            "normal"]["list"].append(
                            presence.child)
                        children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                            "normal"]["total"] += 1
                        self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["days"][
                            presence.date.isoweekday()][
                            "normal"] += 1
                else:
                    logger.warning("[Kitchen][Warning] Age group or Classroom for [%s] is not set" % presence.child)

        #     absences
        date_list = [day.date() for day in self.day_list]

        absences = Absence.objects.filter(child__in=list(children), start_date__lte=self.dates_range[-1],
                                          end_date__gte=self.dates_range[0])
        for absence in absences:
            if make_naive(absence.start_date) > make_naive(absence.end_date):
                messages.error(self.request,
                               _("The absence {} has a start date after the end date.").format(absence))
            else:
                time_range_absence = DateTimeRange(make_naive(absence.start_date), make_naive(absence.end_date))
                # get period from day child
                # time_eat_start = datetime.datetime.combine(day, datetime.time(hour=12, minute=0))
                # time_eat_end = datetime.datetime.combine(day, datetime.time(hour=13, minute=0))
                # time_eat_range = DateTimeRange(time_eat_start, time_eat_end)

                for date in time_range_absence.range(datetime.timedelta(days=1)):
                    # create time range of period
                    if date.date() in date_list:
                        if absence.child and absence.child.classroom and absence.child.age_group:
                            if absence.child in \
                                children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                    "normal"][
                                    "list"]:
                                children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                    "normal"][
                                    "list"].remove(absence.child)
                                children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                    "normal"][
                                    "total"] -= 1
                                self.total_dict_kindergarten['age_group'][absence.child.age_group.id]["days"][
                                    date.isoweekday()][
                                    "normal"] -= 1
                            elif absence.child in \
                                children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                    "restrict"][
                                    "list"]:
                                children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                    "restrict"][
                                    "list"].remove(absence.child)
                                children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                    "restrict"][
                                    "total"] -= 1
                                self.total_dict_kindergarten['age_group'][absence.child.age_group.id]["days"][
                                    date.isoweekday()][
                                    "restrict"] -= 1
                        else:
                            logger.warning(
                                "[Kitchen][Warning] Age group or Classroom for [%s] is not set" % absence.child)

        return children_dict

    def create_total_dict(self):
        total_dict = {"age_group": {}}
        for age_group in self.age_groups:
            total_dict['age_group'][age_group.id] = {
                "name": age_group.name,
                "days": {}
            }
            for day in self.day_list:
                total_dict['age_group'][age_group.id]["days"][day.isoweekday()] = {
                    "normal": 0,
                    "normal_list": [],
                    "restrict": 0,
                    "restrict_dict": {},
                }
        return total_dict

    def create_total_dict_kindergarten(self):
        total_dict = {"age_group": {}}
        for age_group in self.age_groups:
            total_dict['age_group'][age_group.id] = {
                "name": age_group.name,
                "days": {}
            }
            for day in self.day_list:
                total_dict['age_group'][age_group.id]["days"][day.isoweekday()] = {
                    "normal": 0,
                    "normal_list": [],
                    "restrict": 0,
                    "restrict_dict": {},
                }
        return total_dict

    def create_food_restrictions_dict(self):
        food_restrictions_dict = {}
        return food_restrictions_dict


class KitchenView2(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """ View for select day for kitchen"""
    permission_required = ("nobinobi_daily_follow_up.can_view_kitchen",)
    template_name = "nobinobi_kitchen/kitchen_view2.html"

    def __init__(self):
        super().__init__()
        self.date = None
        self.dates_range = None
        self.classrooms = None
        self.classrooms_kindergarten = None
        self.age_groups = None
        self.day_list = None
        self.total_dict = None
        self.total_dict_kindergarten = None
        self.children_dict = None
        self.children_dict_kindergarten = None
        self.food_restrictions = None
        self.food_restrictions_dict = None
        self.PERIOD_ACCEPTED = [TYPE_PERIOD_CHOICES.morning, TYPE_PERIOD_CHOICES.day]

    def get_context_data(self, **kwargs):
        context = super(KitchenView2, self).get_context_data()
        context['title'] = _("Kitchen View")
        self.date = self.kwargs.get("date")
        context['now'] = timezone.localtime()
        context['date'] = self.date
        self.dates_range = week_span_from_date(self.date)

        # on avance l'heure de fin au soir
        self.dates_range[-1] = datetime.datetime.combine(self.dates_range[-1],
                                                         datetime.time(hour=23, minute=59, second=59,
                                                                       microsecond=999999))

        #  =
        context['week_before'] = arrow.get(self.dates_range[0]).shift(weeks=-1)
        context['week_after'] = arrow.get(self.dates_range[-1]).shift(weeks=+1)
        # self.classrooms = Classroom.objects.all().values("id", "name", "capacity", 'mode')
        self.classrooms = list(Classroom.objects.filter(mode=Classroom.OPERATION_MODE.creche))
        self.classrooms_kindergarten = list(Classroom.objects.filter(mode=Classroom.OPERATION_MODE.kindergarten))
        self.age_groups = get_list_or_404(AgeGroup)
        context['age_groups'] = self.age_groups
        self.food_restrictions = list(FoodRestriction.objects.all())
        context['food_restrictions'] = self.food_restrictions
        self.day_list = self.create_day_list(self.dates_range)
        context["day_list"] = self.day_list
        self.total_dict = self.create_total_dict()
        self.total_dict_kindergarten = self.create_total_dict_kindergarten()
        self.children_dict = self.create_children_dict
        self.children_dict_kindergarten = self.create_children_dict_kindergarten()
        self.food_restrictions_dict = self.create_food_restrictions_dict()
        context["children_dict"] = self.children_dict
        context["total_dict"] = self.total_dict
        context["children_dict_kindergarten"] = self.children_dict_kindergarten
        context["total_dict_kindergarten"] = self.total_dict_kindergarten
        return context

    @staticmethod
    def create_day_list(dates_range):
        day_list = []
        for date in dates_range:
            day_list.append(date)

        return day_list

    @property
    def create_children_dict(self):
        children = Child.objects.filter(status=Child.STATUS.in_progress,
                                        classroom__mode=Classroom.OPERATION_MODE.creche,
                                        age_group__isnull=False).prefetch_related(
            "food_restrictions")

        children_dict = {}
        for classroom in self.classrooms:
            children_dict[classroom] = {}
            for age_group in self.age_groups:
                children_dict[classroom][age_group] = {}

                for day in self.day_list:
                    children_dict[classroom][age_group][day.isoweekday()] = {
                        "normal": {"list": [], "total": 0}, "restrict": {"list": [], "total": 0},
                    }
        ctps = ChildToPeriod.objects.filter(start_date__lte=self.dates_range[-1],
                                            end_date__gte=self.dates_range[0], ).values_list("period__start_time",
                                                                                             "period__end_time",
                                                                                             "period__weekday",
                                                                                             "child__id",
                                                                                             "period__type")
        for child in children:
            frs = child.food_restrictions.all()
            for day in self.day_list:
                ctp_list = [ctp for ctp in ctps if
                            ctp[2] == day.isoweekday() and ctp[3] == child.id and ctp[4] in self.PERIOD_ACCEPTED]
                for period in ctp_list:
                    time_range_day = DateTimeRange(day, day)
                    # get period from day child
                    time_eat_start = datetime.datetime.combine(day, datetime.time(hour=11, minute=30))
                    time_eat_end = datetime.datetime.combine(day, datetime.time(hour=13, minute=30))
                    time_eat_range = DateTimeRange(time_eat_start, time_eat_end)

                    for date in time_range_day.range(datetime.timedelta(days=1)):
                        # create time range of period
                        start_date = datetime.datetime.combine(date, period[0])
                        end_date = datetime.datetime.combine(date, period[1])
                        time_range_period = DateTimeRange(start_date, end_date)
                        # if time range period is in time range absence
                        if time_eat_range.is_intersection(time_range_period):
                            if child:
                                if frs.count() > 0:
                                    if child not in \
                                        children_dict[child.classroom][child.age_group][date.isoweekday()]["restrict"][
                                            "list"]:
                                        children_dict[child.classroom][child.age_group][date.isoweekday()]["restrict"][
                                            "list"].append(child)
                                        children_dict[child.classroom][child.age_group][date.isoweekday()]["restrict"][
                                            "total"] += 1
                                        # on ajoute au total
                                        self.total_dict['age_group'][child.age_group.id]["classroom"][child.classroom][
                                            "days"][date.isoweekday()][
                                            "restrict_dict"][child] = {}

                                        for food_restriction in self.food_restrictions:
                                            self.total_dict['age_group'][child.age_group.id]["classroom"][
                                                child.classroom]["days"][date.isoweekday()][
                                                "restrict_dict"][child][food_restriction.id] = None
                                        for fr in frs:
                                            self.total_dict['age_group'][child.age_group.id]["classroom"][
                                                child.classroom]["days"][date.isoweekday()][
                                                "restrict_dict"][child][fr.id] = fr
                                        self.total_dict['age_group'][child.age_group.id]["classroom"][child.classroom][
                                            "days"][date.isoweekday()][
                                            "restrict"] += 1

                                else:
                                    children_dict[child.classroom][child.age_group][date.isoweekday()]["normal"][
                                        "list"].append(child)
                                    children_dict[child.classroom][child.age_group][date.isoweekday()]["normal"][
                                        "total"] += 1
                                    #  on ajoute au total
                                    self.total_dict['age_group'][child.age_group.id]["classroom"][child.classroom][
                                        "days"][date.isoweekday()][
                                        "normal_list"].append(child)
                                    self.total_dict['age_group'][child.age_group.id]["classroom"][child.classroom][
                                        "days"][date.isoweekday()][
                                        "normal"] += 1

        presences_children = Presence.objects.select_related("child", "classroom").filter(
            child__in=list(children), date__range=[self.dates_range[0], self.dates_range[-1]]).order_by('date')

        for presence in presences_children:
            if presence.child not in \
                children_dict[presence.child.classroom][presence.child.age_group][
                    presence.date.isoweekday()]["normal"]["list"] and presence.child not in \
                children_dict[presence.classroom][presence.child.age_group][presence.date.isoweekday()]["restrict"][
                    "list"]:
                frs = presence.child.food_restrictions.all()
                if frs.count() > 0:
                    self.total_dict['age_group'][presence.child.age_group.id]["classroom"][presence.child.classroom][
                        "days"][presence.date.isoweekday()][
                        "restrict_dict"][presence.child] = {}
                    for food_restriction in self.food_restrictions:
                        self.total_dict['age_group'][presence.child.age_group.id]["classroom"][
                            presence.child.classroom]["days"][presence.date.isoweekday()][
                            "restrict_dict"][presence.child][food_restriction.id] = None
                    for fr in frs:
                        self.total_dict['age_group'][presence.child.age_group.id]["classroom"][
                            presence.child.classroom]["days"][presence.date.isoweekday()][
                            "restrict_dict"][presence.child][fr.id] = fr
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "restrict"]["total"] += 1
                    self.total_dict['age_group'][presence.child.age_group.id]["classroom"][presence.child.classroom][
                        "days"][presence.date.isoweekday()][
                        "restrict"] += 1
                else:
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "normal"]["list"].append(
                        presence.child)
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "normal"]["total"] += 1
                    self.total_dict['age_group'][presence.child.age_group.id]["classroom"][presence.child.classroom][
                        "days"][presence.date.isoweekday()][
                        "normal"] += 1

        #     absences
        date_list = [day.date() for day in self.day_list]

        absences = Absence.objects.filter(child__in=list(children), start_date__lte=self.dates_range[-1],
                                          end_date__gte=self.dates_range[0])
        for absence in absences:
            if make_naive(absence.start_date) > make_naive(absence.end_date):
                messages.error(self.request,
                               _("The absence {} has a start date after the end date.").format(absence))
            else:
                time_range_absence = DateTimeRange(make_naive(absence.start_date), make_naive(absence.end_date))
                # get period from day child
                # time_eat_start = datetime.datetime.combine(day, datetime.time(hour=12, minute=0))
                # time_eat_end = datetime.datetime.combine(day, datetime.time(hour=13, minute=0))
                # time_eat_range = DateTimeRange(time_eat_start, time_eat_end)

                for date in time_range_absence.range(datetime.timedelta(days=1)):
                    # create time range of period
                    if date.date() in date_list:
                        if absence.child in \
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "normal"][
                                "list"]:
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "normal"][
                                "list"].remove(absence.child)
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "normal"][
                                "total"] -= 1
                            self.total_dict['age_group'][absence.child.age_group.id]["classroom"][
                                absence.child.classroom][
                                "days"][date.isoweekday()][
                                "normal"] -= 1
                            self.total_dict['age_group'][absence.child.age_group.id]["classroom"][
                                absence.child.classroom][
                                "days"][date.isoweekday()][
                                "normal_list"].remove(absence.child)
                        elif absence.child in \
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "restrict"][
                                "list"]:
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "restrict"][
                                "list"].remove(absence.child)
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "restrict"][
                                "total"] -= 1
                            self.total_dict['age_group'][absence.child.age_group.id]["classroom"][
                                absence.child.classroom][
                                "days"][date.isoweekday()][
                                "restrict"] -= 1
                            del (
                                self.total_dict['age_group'][absence.child.age_group.id]["classroom"][
                                    absence.child.classroom][
                                    "days"][date.isoweekday()][
                                    "restrict_dict"][absence.child])

        return children_dict

    def create_children_dict_kindergarten(self):
        children = Child.objects.filter(status=Child.STATUS.in_progress,
                                        classroom__mode=Classroom.OPERATION_MODE.kindergarten).prefetch_related(
            "food_restrictions")

        children_dict = {}
        for classroom in self.classrooms_kindergarten:
            children_dict[classroom] = {}
            for age_group in self.age_groups:
                children_dict[classroom][age_group] = {}

                for day in self.day_list:
                    children_dict[classroom][age_group][day.isoweekday()] = {
                        "normal": {"list": [], "total": 0}, "restrict": {"list": [], "total": 0},
                    }
        ctps = ChildToPeriod.objects.filter(start_date__lte=self.dates_range[-1],
                                            end_date__gte=self.dates_range[0], ).values_list("period__start_time",
                                                                                             "period__end_time",
                                                                                             "period__weekday",
                                                                                             "child__id",
                                                                                             "period__type")
        for child in children:
            frs = child.food_restrictions.all()
            for day in self.day_list:
                ctp_list = [ctp for ctp in ctps if
                            ctp[2] == day.isoweekday() and ctp[3] == child.id and ctp[4] in self.PERIOD_ACCEPTED]
                for period in ctp_list:
                    time_range_day = DateTimeRange(day, day)
                    # get period from day child
                    time_eat_start = datetime.datetime.combine(day, datetime.time(hour=12, minute=0))
                    time_eat_end = datetime.datetime.combine(day, datetime.time(hour=13, minute=0))
                    time_eat_range = DateTimeRange(time_eat_start, time_eat_end)

                    for date in time_range_day.range(datetime.timedelta(days=1)):
                        # create time range of period
                        start_date = datetime.datetime.combine(date, period[0])
                        end_date = datetime.datetime.combine(date, period[1])
                        time_range_period = DateTimeRange(start_date, end_date)
                        # if time range period is in time range absence
                        if time_eat_range.is_intersection(time_range_period):
                            if child:
                                if frs.count() > 0:
                                    if child not in \
                                        children_dict[child.classroom][child.age_group][date.isoweekday()]["restrict"][
                                            "list"]:
                                        children_dict[child.classroom][child.age_group][date.isoweekday()]["restrict"][
                                            "list"].append(child)
                                        children_dict[child.classroom][child.age_group][date.isoweekday()]["restrict"][
                                            "total"] += 1
                                        # on ajoute au total
                                        self.total_dict_kindergarten['age_group'][child.age_group.id]["classroom"][
                                            child.classroom]["days"][
                                            date.isoweekday()][
                                            "restrict_dict"][child] = {}

                                        for food_restriction in self.food_restrictions:
                                            self.total_dict_kindergarten['age_group'][child.age_group.id]["classroom"][
                                                child.classroom]["days"][
                                                date.isoweekday()][
                                                "restrict_dict"][child][food_restriction.id] = None
                                        for fr in frs:
                                            self.total_dict_kindergarten['age_group'][child.age_group.id]["classroom"][
                                                child.classroom]["days"][
                                                date.isoweekday()][
                                                "restrict_dict"][child][fr.id] = fr
                                        self.total_dict_kindergarten['age_group'][child.age_group.id]["classroom"][
                                            child.classroom]["days"][
                                            date.isoweekday()][
                                            "restrict"] += 1

                                else:
                                    children_dict[child.classroom][child.age_group][date.isoweekday()]["normal"][
                                        "list"].append(child)
                                    children_dict[child.classroom][child.age_group][date.isoweekday()]["normal"][
                                        "total"] += 1
                                    #  on ajoute au total
                                    self.total_dict_kindergarten['age_group'][child.age_group.id]["classroom"][
                                        child.classroom]["days"][
                                        date.isoweekday()][
                                        "normal_list"].append(child)
                                    self.total_dict_kindergarten['age_group'][child.age_group.id]["classroom"][
                                        child.classroom]["days"][
                                        date.isoweekday()][
                                        "normal"] += 1

        presences_children = Presence.objects.select_related("child", "classroom").filter(
            child__in=list(children), date__range=[self.dates_range[0], self.dates_range[-1]]).order_by('date')

        for presence in presences_children:
            if presence.child not in \
                children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                    "normal"]["list"] and presence.child not in \
                children_dict[presence.classroom][presence.child.age_group][presence.date.isoweekday()][
                    "restrict"]["list"]:
                frs = presence.child.food_restrictions.all()
                if frs.count() > 0:
                    self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["classroom"][
                        presence.child.classroom]["days"][
                        presence.date.isoweekday()][
                        "restrict_dict"][presence.child] = {}
                    for food_restriction in self.food_restrictions:
                        self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["classroom"][
                            presence.child.classroom]["days"][
                            presence.date.isoweekday()][
                            "restrict_dict"][presence.child][food_restriction.id] = None
                    for fr in frs:
                        self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["classroom"][
                            presence.child.classroom]["days"][
                            presence.date.isoweekday()][
                            "restrict_dict"][presence.child][fr.id] = fr
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "restrict"]["total"] += 1
                    self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["classroom"][
                        presence.child.classroom]["days"][
                        presence.date.isoweekday()][
                        "restrict"] += 1
                else:
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "normal"]["list"].append(
                        presence.child)
                    children_dict[presence.child.classroom][presence.child.age_group][presence.date.isoweekday()][
                        "normal"]["total"] += 1
                    self.total_dict_kindergarten['age_group'][presence.child.age_group.id]["classroom"][
                        presence.child.classroom]["days"][
                        presence.date.isoweekday()][
                        "normal"] += 1

        #     absences
        date_list = [day.date() for day in self.day_list]

        absences = Absence.objects.filter(child__in=list(children), start_date__lte=self.dates_range[-1],
                                          end_date__gte=self.dates_range[0])
        for absence in absences:
            if make_naive(absence.start_date) > make_naive(absence.end_date):
                messages.error(self.request,
                               _("The absence {} has a start date after the end date.").format(absence))
            else:
                time_range_absence = DateTimeRange(make_naive(absence.start_date), make_naive(absence.end_date))
                # get period from day child
                # time_eat_start = datetime.datetime.combine(day, datetime.time(hour=12, minute=0))
                # time_eat_end = datetime.datetime.combine(day, datetime.time(hour=13, minute=0))
                # time_eat_range = DateTimeRange(time_eat_start, time_eat_end)

                for date in time_range_absence.range(datetime.timedelta(days=1)):
                    # create time range of period
                    if date.date() in date_list:
                        if absence.child in \
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "normal"][
                                "list"]:
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "normal"][
                                "list"].remove(absence.child)
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "normal"][
                                "total"] -= 1
                            self.total_dict_kindergarten['age_group'][absence.child.age_group.id]["classroom"][
                                absence.child.classroom]["days"][
                                date.isoweekday()][
                                "normal"] -= 1
                        elif absence.child in \
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "restrict"][
                                "list"]:
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "restrict"][
                                "list"].remove(absence.child)
                            children_dict[absence.child.classroom][absence.child.age_group][date.isoweekday()][
                                "restrict"][
                                "total"] -= 1
                            self.total_dict_kindergarten['age_group'][absence.child.age_group.id]["classroom"][
                                absence.child.classroom]["days"][
                                date.isoweekday()][
                                "restrict"] -= 1
        return children_dict

    def create_total_dict(self):
        total_dict = {"age_group": {}}
        for age_group in self.age_groups:
            total_dict['age_group'][age_group.id] = {
                "name": age_group.name,
                "classroom": {},
            }

            for classroom in self.classrooms:
                total_dict['age_group'][age_group.id]["classroom"][classroom] = {
                    "days": {}
                }
                for day in self.day_list:
                    total_dict['age_group'][age_group.id]["classroom"][classroom]["days"][day.isoweekday()] = {
                        "normal": 0,
                        "normal_list": [],
                        "restrict": 0,
                        "restrict_dict": {},
                    }
        return total_dict

    def create_total_dict_kindergarten(self):
        total_dict = {"age_group": {}}
        for age_group in self.age_groups:
            total_dict['age_group'][age_group.id] = {
                "name": age_group.name,
                "classroom": {},

            }
            for classroom in self.classrooms_kindergarten:
                total_dict['age_group'][age_group.id]["classroom"][classroom] = {
                    "days": {}
                }
                for day in self.day_list:
                    total_dict['age_group'][age_group.id]["classroom"][classroom]["days"][day.isoweekday()] = {
                        "normal": 0,
                        "normal_list": [],
                        "restrict": 0,
                        "restrict_dict": {},
                    }
        return total_dict

    def create_food_restrictions_dict(self):
        food_restrictions_dict = {}
        return food_restrictions_dict
