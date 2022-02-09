
# Package Finder
This Tool Provides Several Utilites to work with python packages that exist in conda and pip repositories




## Current Features

- Generate Report of a Package existense and version 
   of a package from several conda channels .
- Generate a report of packages that are missing in 
  conda channels against the packages that were frequently 
  downloaded in the last thirty days

## Requested Features

- Upload a csv file to get the comparison report of pakcage existense in 
  different channels in anaconda repository 
- Ability to select and generate grayskull recipes to 
  PR receipes to conda forge staged recipes
- Able to add and remove channels from the CLI

## Config File Details

The config.channels file is a config file that is read by a config parser object .It can scale up to add more channels .It can work on conda repository staged in any type of server and other repositories like nexus.

```

[conda-forge]
name = conda-forge
noarchurl = https://conda.anaconda.org/conda-forge/noarch/repodata.json
winurl = https://conda.anaconda.org/conda-forge/win-64/repodata.json
linuxurl = https://conda.anaconda.org/conda-forge/linux-64/repodata.json

[pytorch]
name = pytorch
noarchurl = https://conda.anaconda.org/pytorch/noarch/repodata.json
winurl = https://conda.anaconda.org/pytorch/win-64/repodata.json
linuxurl = https://conda.anaconda.org/pytorch/linux-64/repodata.json

```

  


## Execution 

Currently the code is not packaged . Clone the repository to Local.
This command will generate a csv report with the packages channels(Currently defaulted to conda-forge) in the config file
```bash

  cd packagefinder

  python pkgfindr.py find-packages numpy

```

This command will generate a Report Comparing the packages that were
frequently downloaded from pip in last thirty days against the conda channels you have in the config file.

```bash

  cd packagefinder

  python pkgfindr.py build-packages 

```


    
