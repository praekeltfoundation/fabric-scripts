from __future__ import unicode_literals

import json

from fabric.api import env, hide, run, sudo, task
from os import environ
from tabulate import tabulate


@task
def production_controller():
    env.hosts = ['{}.{}'.format(
        environ.get('CONTROLLER_NAME'), environ.get('HOST_DOMAIN'))]


@task
def production_workers():
    env.hosts = []
    for i in range(1, 31):
        env.hosts.append('{0}{1:02d}.{2}'.format(
            environ.get('WORKER_NAME'), i, environ.get('HOST_DOMAIN')))


@task
def container_matching(container_id):
    sudo('docker ps | grep {0} || true'.format(container_id))


@task
def get_apps_matching_images(search_image):
    with hide('output'):
        json_response = run('curl http://localhost:8080/v2/apps')
        apps = json.loads(json_response)['apps']

    rows = []

    for app in apps:
        app_image = app['container']['docker']['image']
        if search_image in app_image:
            if 'name' in app['labels']:
                app_name = app['labels']['name']
            else:
                app_name = ''
            if 'domain' in app['labels']:
                domains = app['labels']['domain'].split(' ')
            else:
                domains = []

            if len(domains) > 0:
                primary_domain = domains[0]
            else:
                primary_domain = ''

            row = [app_name, app_image, primary_domain]
            rows.append(row)

            if len(domains) > 1:
                for domain in domains[1:]:
                    rows.append(['', '', domain])

    print(tabulate(rows, headers=['App name', 'Container image', 'Domains']))


@task
def get_apps_matching_domains(domain_name):
    with hide('output'):
        json_response = run('curl http://localhost:8080/v2/apps')
        apps = json.loads(json_response)['apps']

    rows = []

    for app in apps:
        if app['instances'] == 0:
            continue

        domains = []

        image_name = app['container']['docker']['image']

        if 'domain' in app['labels']:
            domains = app['labels']['domain'].split(' ')

        if 'name' in app['labels']:
            app_name = app['labels']['name']
        else:
            app_name = ''

        for domain in domains:
            if domain_name in domain:
                row = [domain, app['id'], app_name, image_name]
                rows.append(row)

    print(tabulate(
        rows, headers=['Domain', 'App ID', 'App name', 'Container image']))
    print('{0} domains matching {1}'.format(len(rows), domain_name))
