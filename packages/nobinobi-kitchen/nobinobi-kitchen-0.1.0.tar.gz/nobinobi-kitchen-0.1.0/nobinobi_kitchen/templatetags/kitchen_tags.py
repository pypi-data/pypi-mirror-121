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

from django import template

register = template.Library()


@register.filter
def get_dict_true(dict_values):
    response = None
    for value in dict_values.values():
        if value['normal']['total'] == 0 and value['restrict']['total'] == 0:
            if response is None:
                response = False
        else:
            response = True
    return response


@register.filter
def get_dict_total_true(dict_values):
    response = None
    for value in dict_values['days'].values():
        if value['normal'] == 0 and value['restrict'] == 0:
            if response is None:
                response = False
        else:
            response = True
    return response
