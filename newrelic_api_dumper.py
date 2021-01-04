#!/usr/bin/env python3

# https://rpm.newrelic.com/api/explore

import argparse
import json
import os
import requests

from entities import entities


BASE_URL = 'https://api.newrelic.com/v2'


def mkdir(_dir):
    if not os.path.exists(_dir):
        os.mkdir(_dir)


def get_all_data(entity):
    url = '{}/{}.json'.format(BASE_URL, entity)
    r = requests.get(url, headers=headers)
    # r.status_code:
    # 200 - OK
    # 401 - key is incorrect
    # 403 - key is correct, but access is restricted

    json_data = r.json()
    if entity in json_data:
        return json_data[entity]

    return json_data


def entity_to_file(entity, outfile=''):
    print('...', entity)
    if not outfile:
        outfile = entity.replace('/', '_') + '.json'

    all_data = get_all_data(entity)

    f = open('{}/{}'.format(output_dir, outfile), 'w')
    f.write(json.dumps(all_data, indent=2))
    f.close()

    return all_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dump all available data having New Relic API key')
    parser.add_argument('-k', '--key', required=True, help='New Relic API key')
    parser.add_argument('-o', '--output', default='output', help='Local directory to dump data')
    args = parser.parse_args()

    headers = {
        'X-Api-Key': args.key
    }

    output_dir = args.output
    mkdir(output_dir)


    applications = entity_to_file('applications')

    for application in applications:
        application_id = application['id']

        application_hosts = entity_to_file('applications/{}/hosts'.format(application_id))['application_hosts']
        for application_host in application_hosts:
            host_id = application_host['id']
            entity_to_file('applications/{}/hosts/{}/metrics'.format(application_id, host_id))

        application_instances = entity_to_file('applications/{}/instances'.format(application_id))['application_instances']
        for application_instance in application_instances:
            instance_id = application_instance['id']
            entity_to_file('applications/{}/instances/{}/metrics'.format(application_id, instance_id))

        entity_to_file('applications/{}/deployments'.format(application_id))
        entity_to_file('applications/{}/metrics'.format(application_id))

    for entity in entities:
        entity_to_file(entity)
