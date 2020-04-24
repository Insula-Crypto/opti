# crypto_portfolio_opti

In order to launch properly the scripts, it is preferrable to use a docker container. If you do not have docker installed, please refer to https://docs.docker.com/engine/install/.

Once docker is installed, you have to build and run the Dockerfile provided in the repo to have a proper working environment:
```bash
docker build -t enigmampc/catalyst .
```
```bash
docker run -v /path/to/your/notebooks:/projects -v ~/.catalyst:/root/.catalyst -p 8888:8888/tcp --name catalyst -it enigmampc/catalyst
```

To access Jupyter when running docker locally (you may need to add NAT rules):
 https://127.0.0.1:8888      <- Please note HTTPS, not HTTP

Default password is 'jupyter'. To provide another, see:
 http://jupyter-notebook.readthedocs.org/en/latest/public_server.html#preparing-a-hashed-password

Once generated, you can pass the new value via `docker run --env` the first time you start the container.

You can also run an algo using the docker exec command. For example:
```bash
docker exec -it catalyst catalyst run -f /projects/my_algo.py --start 2015-1-1 --end 2016-1-1 /projects/result.pickle
```
