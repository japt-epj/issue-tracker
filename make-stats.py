#!/usr/bin/env python3

import csv
import itertools
import json
import os
import re
import requests
import sys
import urllib.request


def read_token():
    if os.path.exists('secret_token'):
        with open('secret_token', 'r') as file:
            return file.read().replace('\n', '')
    else:
        return ''


def get_time(scope, body):
    pattern = '{}:(.*)'.format(scope)
    matcher = re.compile(pattern)
    time = matcher.search(body)
    return ('' if time is None
            else time.group(1).strip())


def get_stats(issue):
    estimate = get_time('Estimate', issue['body'])
    actual = get_time('Actual', issue['body'])

    return {
        'Id': issue['number'],
        'Title': issue['title'],
        'Estimate': estimate,
        'Actual': actual
    }


def get_issues_response(page):
    print('Fetching page', page)
    request = urllib.request.Request(url.format(page), headers=header)

    with urllib.request.urlopen(request) as response:
        return json.load(response)


def get_all_issues():
    last_url = next((strip_page(link)
                     for link in get_links()
                     if link['rel'] == 'last'))

    last = int(last_url['url'])
    return [get_issues_response(i) for i in range(1, last + 1)]


def write_csv(stats):
    with open('stats.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, stats[0].keys())
        writer.writeheader()
        writer.writerows(stats)


def issues_to_stats(issues):
    return [get_stats(issue) for issue in issues]


def get_links():
    request = urllib.request.Request(url.format(1), headers=header)
    with urllib.request.urlopen(request) as response:
        return (requests.utils.parse_header_links(response.info()['Link'])
                if response.info()['Link']
                else empty_list)


def strip_page(link):
    link['url'] = int(link['url'].split('=')[1])
    return link


def write_all_issues():
    all_issues = get_all_issues()
    flattened = list(itertools.chain.from_iterable(all_issues))
    statistics = issues_to_stats(flattened)
    write_csv(statistics)


url = sys.argv[1] + "?page="
header = {
    'Authorization': 'token ' + read_token(),
    'Accept': 'application/json'
}
empty_list = [{'url': 'page=1', 'rel': 'last'}]


write_all_issues()
