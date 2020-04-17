docker run --rm -it --user root -e NB_GID=100 -p 8891:8888 -v $PWD/jupyter:/home/jovyan/host-note jupyter/scipy-notebook:latest start-notebook.sh --NotebookApp.token='' --NotebookApp.allow_origin='*'
