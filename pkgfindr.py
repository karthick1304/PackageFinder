from utils import getRepoData
import fire
import sys
import configparser
import os
import pathlib
import pandas as pd
import numpy as np


class packageFinder:
    def __init__(self):

        # Read configuration file
        config = configparser.ConfigParser()
        home = str(os.getcwd())
        config_file = f'{home}\\config.channels'
        self.channels=[]
        self.get_pip_data()
        
        # Just read the configuration file if exist and validate.
        # Otherwise, depends on value passed in arguments
        try:
             config.read(config_file)
             print(config.read(config_file))
             self.channels.append([config['conda-forge']['name'],config['conda-forge']['noarchurl'],config['conda-forge']['winurl'],config['conda-forge']['linuxurl']])
             self.channels.append([config['pytorch']['name'],config['pytorch']['noarchurl'],config['pytorch']['winurl'],config['pytorch']['linuxurl']])        
             self.accumulate_packages()
        except:
            if not os.path.exists(config_file):
                 print("Warning: configuration file ~/.channel does not exist")
            else:
                 print("Warning: your configuration file ~/.channel is not valid")
        

    def get_pip_data(self):

        header_list = ["Package", "Version", "Total Downloads"]
        self.pip_raw_data=pd.read_csv('pip_data.csv',names=header_list)
    
    def build_packages(self):
        """
        Generates a Report of conda package availibility comparing last 30 days of frequently downloaded packages in 
        pip and if its available in conda 
        Args:
            repodata.json of channels in the config file
        

        """
        self.pip_pkgs_df=pd.read_csv('pip_count.csv')
        build_report_df = self.pip_pkgs_df.merge(self.df_list_of_packages,left_on='packages',right_on='packages',how='left')
        build_report_df.to_csv('build.csv',index=False)
        print("Build Report Generated")
        

    
    def accumulate_packages(self):
        list_of_packages=[]
        for channel_name,nurl,lurl,winurl in self.channels:
            sourceData=self.get_conda_pkgs(nurl)
            platforms = [nurl,lurl,winurl]
            for platform_url in platforms:
                sourceData=self.get_conda_pkgs(platform_url)
                for package in sourceData["packages"]:
                    list_of_packages.append ([sourceData["packages"][package]["name"],sourceData["packages"][package]["version"],channel_name,platform_url.split('/')[4]])
                        
                    
        self.df_list_of_packages = pd.DataFrame(list_of_packages)
        self.df_list_of_packages.rename({0:'packages',1:'version',2:'channel',3:'platform'},axis=1,inplace=True)
        print("Accumulating Package Repository from channels in config file")

    
    def find_packages(self,package_name='',platform_name=''):
        """
        Imports a set of packacges from the conda channels that are specified in the config file and also 
        checks if available in pip.
        Args:
            packages_name: Name of the package you want to Search
                
        """
        versions=[]
        pkg_name = str(package_name)
        for channel_name,nurl,lurl,winurl in self.channels:
            sourceData=self.get_conda_pkgs(nurl)
            platforms = [nurl,lurl,winurl]
            for platform_url in platforms:
                sourceData=self.get_conda_pkgs(platform_url)
                for package in sourceData["packages"]:
                    srcpackage = sourceData["packages"][package]["name"]
                    if srcpackage == pkg_name:                        
                        versions.append ([channel_name,sourceData["packages"][package]["name"],sourceData["packages"][package]["version"],platform_url.split('/')[4]])
        df = pd.DataFrame(versions)
        df.to_csv('package_report.csv',index=False)
        print("Package Report Generated")
      
    def get_conda_pkgs(self,repourl):
         condapkgs=getRepoData(repourl)
         return condapkgs
  

if __name__ == '__main__':
  
    fire.Fire(packageFinder, name='packageFinder')