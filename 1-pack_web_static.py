#!/usr/bin/python3
"""
Fabric script to genereate tgz archive
execute: fab -f 1-pack_web_static.py do_pack
"""

from datetime import datetime
from fabric.api import *
import os


def do_pack():
    """
    making an archive on web_static folder
    """
    # Create the 'versions' folder if it doesn't exist
    if not os.path.exists('versions'):
        local('mkdir -p versions')

    # Generate the archive filename using the current timestamp
    now = datetime.utcnow()
    archive_name = 'web_static_{}{}{}{}{}{}.tgz'.format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    # Compress the contents of the 'web_static' folder
    result = local('tar -czvf versions/{} web_static'.format(archive_name))

    # Check if the compression was successful
    if result.succeeded:
        return 'versions/{}'.format(archive_name)
    else:
        return None
