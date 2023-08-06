# -*- coding: utf-8 -*-

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

from django.urls import path, register_converter, include
from nobinobi_daily_follow_up.utils import IsoDateConverter

from nobinobi_kitchen.views import KitchenSelectView, KitchenView, KitchenView2

app_name = 'nobinobi_kitchen'

register_converter(IsoDateConverter, 'isodate')

urlpatterns = [
    path('kitchen/', include([
        path('', KitchenSelectView.as_view(), name="kitchen_select"),
        path('<isodate:date>/', KitchenView.as_view(), name='kitchen_view'),
        path('2/<isodate:date>/', KitchenView2.as_view(), name='kitchen_view2'),
    ]))
]
