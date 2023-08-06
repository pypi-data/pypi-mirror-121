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

import logging
from sys import stdout

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.translation import gettext as _

USERNAME_KITCHEN = "Cuisinier"


@receiver(post_migrate)
def create_group_kitchen(sender, **kwargs):
    from nobinobi_daily_follow_up.models import Presence
    presence_type = ContentType.objects.get_for_model(Presence)

    permission, perm_created = Permission.objects.get_or_create(codename='can_view_kitchen',
                                                                name='Can view Kitchen',
                                                                content_type=presence_type)  # creating permissions
    if perm_created:
        logging.info(_('Permission Kitchen created'))
        stdout.write(_("Permission Kitchen created successfully."))

    group, created = Group.objects.get_or_create(name='Kitchen')
    if created:
        logging.info(_('Group Kitchen created'))
        stdout.write(_("Group Kitchen created successfully."))
        # Code to add permission to group ???
    group.permissions.add(permission)
    stdout.write(_("Permission {} added to {} successfully.\n").format(permission, group))

    # create user cuisine
    user, created_user = User.objects.get_or_create(username=USERNAME_KITCHEN,
                                                    defaults={
                                                        "is_active": True,
                                                        "is_staff": False,
                                                        "password": "CuisinierAccess"
                                                    })
    user.groups.add(group)
    if created_user:
        stdout.write(_("User {} created and added to {} successfully.\n").format(user.username, group))
