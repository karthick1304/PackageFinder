from setuptools import setup, find_packages

setup(
    name='pkgfindr',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
         'click'

    ],
     entry_points='''
     [console_scripts]
     pkgfinder=pkgfindr:pkgfindr

     '''
    

)