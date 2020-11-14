# -*- coding: utf-8 -*-

"""
Copyright (C) Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from logging import getLogger

# Dropbox
from dropbox import Dropbox as DropboxClient

# Zato
from zato.common.util.api import get_component_name, parse_extra_into_dict
from zato.common.util.eval_ import as_list
from zato.server.connection.wrapper import Wrapper

# ################################################################################################################################

logger = getLogger(__name__)

# ################################################################################################################################
# ################################################################################################################################

class CloudDropbox(Wrapper):
    """ Wraps a Dropbox connection client.
    """
    wrapper_type = 'Dropbox connection'
    required_secret_attr = 'secret'
    required_secret_label = 'an OAuth 2 access token'

    def __init__(self, *args, **kwargs):
        super(CloudDropbox, self).__init__(*args, **kwargs)
        self._client = None  # type: DropboxClient

# ################################################################################################################################

    def _init_impl(self):

        with self.update_lock:

            user_agent = '{}/{}'.format(self.config.user_agent, get_component_name('zato.cloud.dropbox'))
            scope = as_list(self.config.default_scope, ',')

            config = {
                'user_agent': user_agent,
                'oauth2_access_token': self.server.decrypt(self.config.secret),
                'oauth2_access_token_expiration': int(self.config.oauth2_access_token_expiration or 0),
                'scope': scope,
                'max_retries_on_error': int(self.config.max_retries_on_error or 0),
                'max_retries_on_rate_limit': int(self.config.max_retries_on_rate_limit or 0),
                'timeout': int(self.config.timeout),
                'headers': parse_extra_into_dict(self.config.http_headers),
            }

            # Create the actual connection object
            self._client = DropboxClient(**config)

            # Confirm the connection was established
            self.ping()

            # We can assume we are connected now
            self.is_connected = True

# ################################################################################################################################

    def _delete(self):
        if self._client:
            self._client.close()

# ################################################################################################################################

    def _ping(self):
        self._client.files_list_folder(self.config.default_directory)

# ################################################################################################################################
# ################################################################################################################################
