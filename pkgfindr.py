import click
from utils import getRepoData
import fire
import sys
import configparser
import os
import pathlib
import pandas as pd


class packageFinder:
    def __init__(self):

        # Read configuration file
        config = configparser.ConfigParser()
        home = str(os.getcwd())
        print(home)
        config_file = f'{home}\\config.channels'
        print(config_file)
        self.channels=[]
        self.get_pip_data()

        # Just read the configuration file if exist and validate.
        # Otherwise, depends on value passed in arguments
        try:
             config.read(config_file)
             print(config.read(config_file))
             self.channels.append([config['conda-forge']['name'],config['conda-forge']['noarchurl'],config['conda-forge']['winurl'],config['conda-forge']['linuxurl']])
             self.channels.append([config['pytorch']['name'],config['pytorch']['noarchurl'],config['pytorch']['winurl'],config['pytorch']['linuxurl']])
             for obj in self.channels:
                 print(obj)

             
        
             if config_name.isalpha:
                #  current_config = config[config.sections()[config.sections().index(config_name)]]
                 print("hello")
                 self.reponame = config['conda-forge']['name']
                 self.repourl  = config['conda-forge']['noarchurl']
                 print(config['conda-forge']['name'])
                 print(config['conda-forge']['noarchurl'])
                 for each_section in config.sections():                     
                     for (each_key, each_val) in config.items(each_section):
                        print(each_key)
                        print(each_val)                        
             else:
                 current_config = config[config.sections()[0]]
        except:
            if not os.path.exists(config_file):
                 print("Warning: configuration file ~/.channel does not exist")
            else:
                 print("Warning: your configuration file ~/.channel is not valid")
        

    def get_pip_data(self):

        header_list = ["Package", "Version", "Total Downloads"]
        self.pip_raw_data=pd.read_csv('pip_data.csv',names=header_list)
        print(self.pip_raw_data)

   
    def find_packages(self,package_name='',platform_name=''):
        """
        Import a list of packages either stored from a package directory or from a list of urls to
        download to the fscr and nexus repository
        Args:
            packages_url: (optional) file containing list of package urls
            package_directory: (optional) directory containing packages
            require_confirm: (default True) require user confirmation at various steps in the process

        
        """
        versions=[]
        print("Hello!" + package_name +"!")
        print(self.channels[0],"printing channels 1")
        print(self.channels[1],"printing channels 2")
        


        
        pname = str(package_name)
     
        # sourceData=self.get_conda_pkgs(self.repourl)
        print(self.channels,"printing channels")
        
        for channel_name,nurl,lurl,winurl in self.channels:
            sourceData=self.get_conda_pkgs(nurl)
            platforms = [nurl,lurl,winurl]
            for platform_url in platforms:
                sourceData=self.get_conda_pkgs(platform_url)
                for package in sourceData["packages"]:
                    print(sourceData["packages"][package]["name"])
                    srcpackage = sourceData["packages"][package]["name"]
                    if srcpackage == pname:
                        print("package Available")
                        print(sourceData["packages"][package]["name"],sourceData["packages"][package]["version"])   
                        
                        versions.append ([channel_name,sourceData["packages"][package]["name"],sourceData["packages"][package]["version"],platform_url.split('/')[4]])
        # print(versions)
        df = pd.DataFrame(versions)
      
        print(df.to_string(index=False))
      

 

    def get_conda_pkgs(self,repourl):
         condapkgs=getRepoData(repourl)
         return condapkgs
  


if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv:
        help_mode = True

    # Redirect blank --help call to command without arguments
    if len(sys.argv) == 2 and sys.argv[1] == '--help':
        sys.argv = [sys.argv[0]]
    if len(sys.argv) == 3 and sys.argv[1][0] == '-' and sys.argv[2] == '--help':
        sys.argv = [sys.argv[0]]

    fire.Fire(packageFinder, name='packageFinder')