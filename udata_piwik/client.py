# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import requests

from datetime import date

from flask import current_app

log = logging.getLogger(__name__)


def analyze(method, **kwargs):
    """Retrieve JSON stats from Piwik for a given `method` and parameters."""
    base_url = 'http://{0}/index.php'.format(current_app.config['PIWIK_URL'])
    data = {
        'module': 'API',
        'idSite': current_app.config['PIWIK_ID'],
        'method': method,
        'format': kwargs.pop('format', 'json'),
    }
    if 'date' in kwargs:
        dt = kwargs.pop('date')
        if isinstance(dt, date):
            dt = dt.isoformat()
        kwargs['date'] = dt
    data.update(kwargs)
    r = requests.get(base_url, params=data)
    return r.json()


def track(url, **kwargs):
    """Track a request to a given `url` by issuing a POST against Piwik."""
    base_url = 'http://{0}/piwik.php'.format(current_app.config['PIWIK_URL'])
    data = {
        'rec': 1,
        'idsite': current_app.config['PIWIK_ID'],
        'url': url,
        'token_auth': current_app.config['PIWIK_AUTH']
    }
    data.update(kwargs)
    requests.post(base_url, data=data)
