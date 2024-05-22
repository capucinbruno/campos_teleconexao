# CAMPOS DE TELECONEXÃO

## Instalação

```s
poetry add scitools-iris matplotlib
poetry add iris-sample-data
conda env list
conda create -n campos_env python=3.9
conda dactivate
conda activate campos_env  
conda install -c conda-forge numpy matplotlib cartopy iris windspharm
conda env remove -n campos_env

```