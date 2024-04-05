#!/usr/bin/python3
"""Do deploy web static module"""
import os
from fabric import api

api.env.user = 'ubuntu'
api.env.hosts = ['34.229.255.107', '18.204.7.214']

def do_deploy(archive_path):
    """
    Fabric script that distributes an archive to web servers using do_deploy
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = os.path.basename(archive_path)
        just_name = os.path.splitext(file_name)[0]
        api.put(archive_path, "/tmp/")
        api.run("mkdir -p /data/web_static/releases/{}".format(just_name))
        api.run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(
                                                        file_name, just_name))
        api.run("rm /tmp/{}".format(file_name))
        path_r = "/data/web_static/releases/"
        api.run('mv {0}{1}/web_static/* {0}{1}/'.format(path_r, just_name))
        api.run('rm -rf /data/web_static/releases/{}/web_static'.format(
                                                                just_name))
        api.run("rm -rf /data/web_static/current")
        api.run("ln -s /data/web_static/releases/{} \
                    /data/web_static/current".format(just_name))
        return True
    except Exception as e:
        print("Exception:", e)
        return False
