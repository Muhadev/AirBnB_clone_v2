#!/usr/bin/python3
"""
Fabric script to genereate tgz archive
execute: fab -f 1-pack_web_static.py do_pack
"""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ["54.236.46.198", "52.91.123.123"]


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if all operations have been done correctly, otherwise False.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Get the filename without extension
        filename = archive_path.split('/')[-1].split('.')[0]

        # Create the release folder
        run('mkdir -p /data/web_static/releases/{}/'.format(filename))

        # Uncompress the archive to the release folder
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            filename + '.tgz', filename))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename + '.tgz'))

        # Move the contents to the current folder
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(filename, filename))

        # Remove the now empty web_static folder
        run('rm -rf /data/web_static/releases/{}/web_static'.format(filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('ln -s /data/web_static/releases/{}/ '
            '/data/web_static/current'.format(filename))

        print('New version deployed!')

        return True

    except Exception as e:
        print(e)
        return False
