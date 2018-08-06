# -*- coding: utf-8 -*-

"""
Copyright (C) 2018, Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import logging

# Zato
from zato.common import GENERIC, PLACEHOLDER
from zato.admin.web.forms import ChangePasswordForm
from zato.admin.web.forms.outgoing.wsx import CreateForm, EditForm
from zato.admin.web.views import change_password as _change_password, CreateEdit, Delete as _Delete, Index as _Index, \
     method_allowed
from zato.common.odb.model import GenericConn

logger = logging.getLogger(__name__)

class Index(_Index):
    method_allowed = 'GET'
    url_name = 'out-wsx'
    template = 'zato/outgoing/wsx.html'
    service_name = 'zato.generic.connection.get-list'
    output_class = GenericConn
    paginate = True

    class SimpleIO(_Index.SimpleIO):
        input_required = ('cluster_id', 'type_')
        output_required = ('id', 'name', 'address')
        output_optional = ('is_active', 'is_zato', 'on_connect_service_id')
        output_repeated = True

    def handle(self):
        return {
            'create_form': CreateForm(req=self.req),
            'edit_form': EditForm(prefix='edit', req=self.req),
            'change_password_form': ChangePasswordForm()
        }

class _CreateEdit(CreateEdit):
    method_allowed = 'POST'

    class SimpleIO(CreateEdit.SimpleIO):
        input_required = ('name', 'is_active', 'is_zato', 'address', 'on_connect_service_id')
        output_required = ('id', 'name')

    def populate_initial_input_dict(self, initial_input_dict):
        initial_input_dict['type_'] = GENERIC.CONNECTION.TYPE.OUTCONN_WSX
        initial_input_dict['is_internal'] = False
        initial_input_dict['is_channel'] = False
        initial_input_dict['is_outconn'] = True
        initial_input_dict['pool_size'] = 1
        initial_input_dict['sec_use_rbac'] = False
        initial_input_dict['zzz'] = 'qqq'

    def success_message(self, item):
        print(111, item)
        return 'Successfully {} outgoing WebSocket connection `{}`'.format(self.verb, item.name)

class Create(_CreateEdit):
    url_name = 'out-wsx-create'
    service_name = 'zato.generic.connection.create'

class Edit(_CreateEdit):
    url_name = 'out-wsx-edit'
    form_prefix = 'edit-'
    service_name = 'zato.generic.connection.edit'

class Delete(_Delete):
    url_name = 'out-wsx-delete'
    error_message = 'Could not delete outgoing WebSocket connection'
    service_name = 'zato.outgoing.wsx.delete'

@method_allowed('POST')
def change_password(req):
    return _change_password(req, 'zato.generic.connection.change-password')
