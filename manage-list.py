import os
import logging
import git
import yaml
from pymemcache.client import base

repo_url = os.getenv('GIT_REPO_URL')
repo_dir = os.getenv('GIT_REPO_PATH')
blacklist_file = os.getenv('GIT_BLACKLIST_FILE')
memcached_ip = os.getenv('MEMCACHED_SERVICE_IP')
memcached_port = int(os.getenv('MEMCACHED_SERVICE_PORT'))

def read_repo():
    if os.path.exists(repo_dir):
      repo = git.Repo(repo_dir)
      repo.remotes.origin.pull()
    else:
      repo = git.Repo.clone_from(repo_url, repo_dir)
    assert not repo.bare

def write_memcached():
    blacklist = yaml.load(open(blacklist_file), Loader=yaml.FullLoader)
    memcached = base.Client((memcached_ip, memcached_port))
    for blocked in blacklist['blacklist']:
      try:
        set = memcached.set(blocked['site'], blocked['response'])
        if not set:
	  logging.error('Memcache set failed.')
      except: 
          logging.error('Memcache set exception occurred.')

def main():
    read_repo()
    write_memcached()

if __name__ == '__main__':
    main()
