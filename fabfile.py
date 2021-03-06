from __future__ import with_statement
from fabric.api import *
from fabdefs import *
from contextlib import contextmanager


@contextmanager
def virtualenv():
    with cd(env.project_dir):
        with prefix(env.activate):
            yield


def set_permissions():
    """
    Ensure user www-data has access to the application folder.
    """
    sudo('chown -R www-data:www-data ' + env.project_dir)
    return


def restart():

    sudo("supervisorctl restart living_wage")
    sudo('service nginx restart')
    return


def setup():
    """
    Install dependencies and create an application directory.
    """

    # install packages
    sudo('apt-get install build-essential python python-dev')
    sudo('apt-get install python-pip supervisor')
    sudo('pip install virtualenv')

    # create application directory if it doesn't exist yet
    with settings(warn_only=True):
        if run("test -d " + env.project_dir).failed:
            # create project folder
            sudo('mkdir -p ' + env.project_dir)
        if run("test -d %s/env" % env.project_dir).failed:
            # create virtualenv
            sudo('virtualenv --no-site-packages %s/env' % env.project_dir)

    # install the necessary Python packages
    with virtualenv():
        put('requirements/base.txt', '/tmp/base.txt')
        put('requirements/production.txt', '/tmp/production.txt')
        sudo('pip install -r /tmp/production.txt')

    # install nginx
    sudo('apt-get install nginx')
    # restart nginx after reboot
    sudo('update-rc.d nginx defaults')
    with settings(warn_only=True):
        sudo('service nginx start')
    return


def configure():
    """
    Configure Nginx, supervisor & Flask. Then restart.
    """

    with settings(warn_only=True):
        # disable default site
        sudo('rm /etc/nginx/sites-enabled/default')

    # upload nginx server blocks (virtualhost)
    put(env.config_dir + '/nginx.conf', '/tmp/nginx.conf')
    sudo('mv /tmp/nginx.conf %s/living-wage.code4sa.org.conf' % env.project_dir)

    with settings(warn_only=True):
        sudo('ln -s %s/living-wage.code4sa.org.conf /etc/nginx/sites-available/' % env.project_dir)
        sudo('ln -s /etc/nginx/sites-available/living-wage.code4sa.org.conf /etc/nginx/sites-enabled/')

    # upload supervisor config
    put(env.config_dir + '/supervisor.conf', '/tmp/supervisor.conf')
    sudo('mv /tmp/supervisor.conf /etc/supervisor/conf.d/supervisor_living_wage.conf')
    sudo('supervisorctl reread')
    sudo('supervisorctl update')

    # upload flask config
    with settings(warn_only=True):
        sudo('mkdir %s/instance' % env.project_dir)
    put(env.config_dir + '/config.py', '/tmp/config.py')
    sudo('mv /tmp/config.py %s/instance/config.py' % env.project_dir)

    set_permissions()
    restart()
    return


def deploy():
    """
    Upload our package to the server.
    """

    # create a tarball of our package
    local('tar -czf app.tar.gz app/', capture=False)

    # upload the source tarball to the temporary folder on the server
    put('app.tar.gz', '/tmp/app.tar.gz')

    # enter application directory
    with cd(env.project_dir):
        # and unzip new files
        sudo('tar xzf /tmp/app.tar.gz')

    # now that all is set up, delete the tarball again
    sudo('rm /tmp/app.tar.gz')
    local('rm app.tar.gz')

    set_permissions()
    restart()
    return

