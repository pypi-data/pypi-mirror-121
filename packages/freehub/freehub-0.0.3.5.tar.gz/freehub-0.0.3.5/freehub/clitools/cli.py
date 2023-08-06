from freehub import apis
import os
os.environ['ANSI_COLORS_DISABLED']="1"
import shutil
import fire

class Cli:
    '''
    address: [[[{host}/]{username}/]{repo_name}:]{branch_name}[/{relative_path}]
    '''
    @classmethod
    def download(cls,address,path=None,overwrite=False):
        path=path or './'
        address=apis.get_complete_address(address)
        apis.freehub_download(address,path,overwrite=overwrite)
    @classmethod
    def upload(cls,path,address,overwrite=True):
        address = apis.get_complete_address(address)
        apis.freehub_upload(path,address,overwrite=overwrite)
    @classmethod
    def login(cls):
        apis.freehub_login()
    @classmethod
    def logout(cls):
        apis.freehub_logout()
    @classmethod
    def search(cls,pattern:str):
        pattern=apis.get_complete_address(pattern)
        apis.freehub_search(pattern)

    @classmethod
    def list(cls):
        return cls.search('.*')

def main():
    fire.Fire(Cli)
if __name__ == '__main__':
    main()