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
        '''
        - search branch under any repo
        - search files under any branch
        :param pattern:
        :return:
        '''
        pattern=apis.get_complete_address(pattern)
        apis.freehub_search(pattern)
    @classmethod
    def ls(cls, address:str=None):
        '''

        :param repo:
        :return:
        - list branches under any repo
        - list files under any branch
        '''
        if not address:
            return cls.branch.list()
        if address.endswith(':'):
            return cls.branch.list(address.rstrip(':'))
        address = apis.get_complete_address(address)
        pattern=address.rstrip('/')+'/*'
        return cls.search(pattern)
    @classmethod
    def cat(cls, address):
        '''
        output file content to stdout (that is : print content)
        :param address:
        :return:
        '''
        address = apis.get_complete_address(address)
        apis.freehub_cat(address)

    @classmethod
    def run(cls,address:str):
        address = apis.get_complete_address(address)
        return apis.freehub_run(address)

    @classmethod
    def version(cls):
        print('freehub-0.0.6')
    class branch:
        @classmethod
        def search(cls,pattern:str):
            pattern = apis.get_complete_address(pattern)
            apis.freehub_branch_search(pattern)
        @classmethod
        def list(cls,repo:str=None):
            pattern = repo + ':*' if repo else '*'
            return cls.search(pattern)
    @classmethod
    def pyrun(cls,address:str):
        return cls.py.run(address)
    class py:
        @classmethod
        def run(cls,address:str):
            address = apis.get_complete_address(address)
            file_path = apis.fetch(address)
            os.system('python %s'%(file_path))
def main():
    fire.Fire(Cli)
if __name__ == '__main__':
    main()