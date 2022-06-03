#!/usr/bin/env python3
# Copyright 2017-2022, UB JCS, Goethe University Frankfurt am Main
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from time import sleep
import requests

# See: https://www.base-search.net/about/download/base_interface.pdf
API_URL = "https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi"
LIST_REPOSITORIES = "ListRepositories"
LIST_PROFILE = "ListProfile"
PERFORM_SEARCH = "PerformSearch"
PROXIES = {"http": "socks5://127.0.0.1:9911", "https": "socks5://127.0.0.1:9911"}


def list_repositories(coll=None):
    """Wraper around the ListRepositories API call.
    coll: string to specify a subsection of BASE. For valid values cf. the docs
    above
    """
    params = {"func": LIST_REPOSITORIES, "format": "json"}
    if coll is not None:
        params["coll"] = coll
    response = requests.get(API_URL, params=params, proxies=PROXIES)
    response.raise_for_status()
    data = response.json()
    return data


def iter_list_repositories(coll=None):
    """Iterate over all respos (in the collection). As opposed to list_repositories,
    the structure is changed to single dicts that contain all information.
    """
    repos = list_repositories(coll=coll)
    for internal_name, record in repos["collection"]["list_repositories"].items():
        record["internal_name"] = internal_name
        yield record


def get_profile(record):
    """Turns a profile retrieved via "list_profile" into a usable python
    structure. This includes convertig data into appropriate types.
    """
    for key, value in record.items():
        if key.startswith("num_"):
            try:
                value = int(value)
                record[key] = value
            except ValueError:
                pass
    try:
        record["activation_date"] = datetime.fromisoformat(
            record.get("activation_date")
        )
    except ValueError:
        pass
    return record


def list_profile(target, wait=0):
    """Wrapper around the "ListProfile" API call. target is the internal identifier
    of a repo. wait is used to introduce a delay when doing many calls in a row.
    """
    if not target:
        raise ValueError("No target.")
    sleep(wait)
    params = {"func": LIST_PROFILE, "target": target, "format": "json"}
    response = requests.get(API_URL, params=params, proxies=PROXIES)
    response.raise_for_status()
    profile = get_profile(response.json())
    profile["internal_name"] = target
    return profile


def perform_search(query, **kwargs):
    """Wrapper around the PerformSearch API call."""
    if not query:
        raise ValueError("No query.")
    params = {"func": PERFORM_SEARCH, "query": query, "format": "json"}
    if kwargs:
        for key, value in kwargs.items():
            if not key in params:
                params[key] = value
            else:
                raise ValueError(f"Duplicate key: {key}.")
    response = requests.get(API_URL, params=params, proxies=PROXIES)
    return response.json()
