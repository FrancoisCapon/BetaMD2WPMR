FROM debian:bullseye-slim

# https://stackoverflow.com/questions/27273412/cannot-install-packages-inside-docker-ubuntu-image
RUN apt-get update -yq

RUN apt-get install -yq python3 python3-pip

# https://squidfunk.github.io/mkdocs-material/getting-started/
RUN pip install mkdocs-material

# https://pypi.org/project/markdown-captions/
RUN pip install markdown-captions

RUN pip install beautifulsoup4

RUN mkdir /project
WORKDIR /project

# md2wpmr-project $ docker build -t fcapon/mkdocs .
# $ docker run -it -v $(pwd):/project -p 8000:8000 fcapon/mkdocs
# root@ebe42ba82686:/project# pip install -e md2wpmr-project/
# root@5e0f2e83d8c7:/mkdocs# mkdocs serve -a 0.0.0.0:8000
# root@ebe42ba82686:/project/mkdocs#  mkdocs serve -a 0.0.0.0:8000
