# Copyright 2013 Openstack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import logging

from oslo.config import cfg

GLOBAL_CONF = cfg.CONF

wafflehaus_global_opts = [
    cfg.BoolOpt('runtime_reconfigurable', default=False,
                help='Will enable header reconfiguration'),
]

GLOBAL_CONF.register_opts(wafflehaus_global_opts, 'WAFFLEHAUS')


class WafflehausBase(object):

    def __init__(self, app, conf):
        self.conf = conf
        self.app = app
        logname = __name__
        self.log = logging.getLogger(conf.get('log_name', logname))
        self.testing = (conf.get('testing') in
                        (True, 'True', 'true', 't', '1', 'on', 'yes', 'y'))
        self.enabled = (conf.get('enabled', False) in
                        (True, 'True', 'true', 't', '1', 'on', 'yes', 'y'))
        self.reconfigure = GLOBAL_CONF.WAFFLEHAUS.runtime_reconfigurable

    def _override(self, req):
        pass

    def _override_caller(self, req):
        if not self.reconfigure:
            return
        self._override(req)

    def __call__(self, req):
        self._override_caller(req)
