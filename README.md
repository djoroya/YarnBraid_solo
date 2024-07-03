# Windows 

Install LS-PrePost on Windows

LSDYNA tiene que ser 4.10.8
De otra manera da problemas 

- https://ftp.lstc.com/anonymous/outgoing/lsprepost/4.10/win64/LS-PrePost-4.10.8-x64-06Nov2023_setup.exe
- https://ftp.lstc.com/anonymous/outgoing/lsprepost/4.10/linux64/lsprepost-4.10.8-common-06Nov2023.tgz

Then search the lsdyna executable file in the installation folder. Edit the setting_win.json

#  Anaconda  setup
conda create -n yarn
conda activate yarn
conda install pip

(base) djoroya@m002-gpu:~/mambaforge/envs/TECNORED/lib/python3.12/site-packages$ ls *.pth
(base) djoroya@m002-gpu:~/mambaforge/envs/TECNORED/lib/python3.12/site-packages$  code conda.pth


# unzip
tar -xvzf lsprepost-4.10.8-common-06Nov2023.tgz
