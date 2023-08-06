from freehub import git_ops
from freehub.utils import *
import logging
import json
import os

_BRANCH_DICT='branch_dict'
_FAKE2TRUE: str='fake2true'
_TRUE2FAKE='true2fake'
_BRANCH_LIST='remote_branch_list'
USER_HOME=os.path.expanduser('~')
STORE_HOME=USER_HOME+'/.store'
# BRANCH_LIST_DIR=STORE_HOME+'/BranchLists'
# SHADOW_STORE_HOME=STORE_HOME+'/ShadowStores'
# STORE_TMP_DIR=STORE_HOME+'/tmp'
# STORE_CLASS_DIR=STORE_HOME+'/Store.Class'
STORE_CONFIG_FILE=STORE_HOME+'/config.json'
FREEHUB_LOCATION='https://OpenGitspace:Gitspace@123456@gitee.com/OpenGitspace/meta'
def _get_default_repo():
    cfg = read_config()
    if not cfg:
        return 'gitspace'
    else:
        return cfg.get('default_repo')
def _parse_key(key):
    if ':' in key:
        repo,remote_key=key.split(':',maxsplit=1)
    else:
        repo=_get_default_repo()
        remote_key=key
    return repo,remote_key
def _gen_location(user_name,password,repo_path):
    return 'https://%s:%s@gitee.com/%s/%s'%(user_name,password,user_name,repo_path)
def get_freehub_location(repo):
    cfg=read_config()
    if cfg and 'username' in cfg.keys() and 'password' in cfg.keys():
        return _gen_location(user_name=cfg['username'],password=cfg['password'],repo_path=repo)
    return FREEHUB_LOCATION
def read_config():
    if not os.path.exists(STORE_CONFIG_FILE):
        return None
    with open(STORE_CONFIG_FILE,'r',encoding='utf-8') as f:
        return json.load(f)
def write_config(data):
    with open(STORE_CONFIG_FILE,'w',encoding='utf-8') as f:
        json.dump(data,f)



def copy_repo_files_to(src,dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    assert os.path.isdir(dst)
    for child in os.listdir(src):
        if child=='.git':
            continue
        child_path=os.path.join(src,child)
        dst_child_path=os.path.join(dst,child)
        if os.path.isdir(child_path):
            shutil.copytree(child_path,dst_child_path)
        else:
            shutil.copy(child_path,dst_child_path)
def download_branch(remote_location,branch,dst,overwrite=False):
    check_and_make_empty_dir(dst,overwrite)
    repo=git_ops.git_init(dst)
    git_ops.create_head(repo)
    git_ops.pull_remote_branch(repo,remote_location,branch)

def upload_branch(repo,remote_location,branch,overwrite=False):
    if git_ops.exists_remote_branch(remote_location,branch):
        if not overwrite:
            raise Exception('Remote branch %s already exists at %s .'%(branch,remote_location))
        else:
            logging.warning('Will overwrite remote branch %s at %s .'%(branch,remote_location))
    else:
        logging.info('Will upload to a new branch %s at %s .'%(branch,remote_location))
    branches=git_ops.list_branch(repo)
    if not branch in branches:
        raise Exception('Local branch %s does not exist.'%(branch))
    git_ops.push_local_branch(repo, branch, remote_location)

def download_to_dir(remote_location,branch,dst,cache_dir=None,overwrite=True):
    cache_dir=cache_dir or os.path.join(STORE_HOME,branch)
    check_and_make_empty_dir(cache_dir,overwrite=True)
    download_branch(remote_location,branch,dst=cache_dir,overwrite=overwrite)
    copy_repo_files_to(cache_dir,dst)

def upload_to_remote(remote_location,branch,src,cache_dir=None,overwrite=True):
    cache_dir = cache_dir or os.path.join(STORE_HOME, branch)
    check_and_make_empty_dir(cache_dir,overwrite=True)
    dst_path=os.path.join(cache_dir,os.path.basename(src))
    if os.path.isdir(src):
        shutil.copytree(src,dst_path)
    else:
        shutil.copy(src,dst_path)
    repo=git_ops.git_init(cache_dir)
    git_ops.create_head(repo)
    git_ops.create_branch(repo,branch,force=True)
    git_ops.switch_branch(repo,branch,recover=False)
    git_ops.stage_all_changes(repo)
    git_ops.commit_current_branch(repo)
    upload_branch(repo,remote_location,branch,overwrite=overwrite)

def freehub_download(key,path,overwrite=False):
    repo, remote_key=_parse_key(key)
    download_to_dir(get_freehub_location(repo),remote_key,path,overwrite=overwrite)
def freehub_upload(path,key,overwrite=False):
    repo, remote_key = _parse_key(key)
    upload_to_remote(get_freehub_location(repo),remote_key,path,overwrite=overwrite)

def freehub_login():
    user_name=input('username:')
    password=input('password:')
    repo=input('default repository:')
    write_config(dict(
        username=user_name,
        password=password,
        default_repo=repo
    ))
    print('Login successfully.')
def freehub_logout():
    os.remove(STORE_CONFIG_FILE)
    print('Logout successfully.')


def test():
    default_remote_location = FREEHUB_LOCATION
    repo_path = '../data/OpenGitspace'
    import wk
    wk.remake(repo_path)

    # repo_path = './data/'
    # download_branch(default_remote_location,'test',repo_path)
    # upload_branch(default_remote_location,'test2',repo_path,overwrite=True)
    # download_to_dir(default_remote_location,'test',repo_path)
    # upload_to_remote(default_remote_location,'0',repo_path,overwrite=True,cache_dir='data/cache')
    # upload_to_remote(default_remote_location,'0',repo_path,overwrite=True,cache_dir='data/cache')

    wk.Folder(repo_path).open('readme.txt','w').write('yes')
    #freehub
    freehub_upload(repo_path,'0',overwrite=True)
    shutil.rmtree(repo_path)
    freehub_download('0',os.path.dirname(repo_path))
if __name__ == '__main__':
    test()







