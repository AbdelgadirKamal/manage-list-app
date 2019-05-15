import os
import logging
import git
import yaml
from pymemcache.client import base
import socket

LOG_LEVEL = os.getenv('LOG_LEVEL', logging.WARNING)
logging.basicConfig()
_logger = logging.getLogger(__name__)
_logger.setLevel(LOG_LEVEL)

repo_url = os.getenv('GIT_REPO_URL')
repo_dir = os.getenv('GIT_REPO_PATH')
blacklist_file = os.getenv('GIT_BLACKLIST_FILE')
memcached_timeout = int(os.getenv('MEMCACHED_TIMEOUT', '0'))
memcached_service = os.getenv('MEMCACHED_SERVICE')
memcached_port = int(os.getenv('MEMCACHED_SERVICE_PORT', '11211'))
_,_,memcached_ips = socket.gethostbyname_ex(memcached_service)
memcached_servers = [(ip, memcached_port) for ip in memcached_ips]

def read_repo():
    if os.path.exists(repo_dir):
      repo = git.Repo(repo_dir)
      repo.remotes.origin.pull()
    else:
      repo = git.Repo.clone_from(repo_url, repo_dir)
    assert not repo.bare

def write_memcached(server):
    memcached = base.Client(server)
    for blocked in blacklist['blacklist']:
      try:
        set = memcached.set(blocked['site'], blocked['response'])
        if not set:
          _logger.error('Memcache set failed for: %s' % server)
          return
        else:
          _logger.debug('Memcache set of %s is successful in server %s' % (blocked['site'], server))
      except: 
          _logger.error('Memcache set exception occurred for: %s.' % server)
          return
    set = memcached.set('UPDATE_SUCCESS', 'True', expire=memcached_timeout)

def main():
    global blacklist
    read_repo()
    blacklist = yaml.load(open(blacklist_file), Loader=yaml.FullLoader)
    for server in memcached_servers:
      write_memcached(server)

if __name__ == '__main__':
    main()
