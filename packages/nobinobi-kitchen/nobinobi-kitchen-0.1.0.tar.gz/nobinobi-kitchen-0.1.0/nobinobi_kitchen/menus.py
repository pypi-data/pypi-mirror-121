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

from django.urls import reverse
from django.utils.translation import gettext as _
from menu import Menu, MenuItem

from nobinobi_kitchen.utils import has_view_kitchen

Menu.add_item(
    "main",
    MenuItem(
        title=_("Kitchen"),
        url=reverse("nobinobi_kitchen:kitchen_select"),
        icon="fas fa-apple-alt",
        check=lambda request: has_view_kitchen(request)
    ),
)

#
# Menu.add_item("main", MenuItem("Superuser Only",
#                                reverse("reports.views.superuser"),
#                                check=lambda request: request.user.is_superuser))
