# Praekelt.org Fabric scripts

[Fabric](https://pypi.org/project/Fabric/) is a Python package which
makes it easy to script commands on remote machines. This repo has
a couple of Fabric scripts which are useful for engineers.

Unfortunately the latest version of Fabric (currently 1.14.0) only
works on Python 2.

## Installation

```
pip install -r requirements.txt
```

## Example usage

Get all running containers matching a search string:

```
fab production_workers container_matching:molo-gem
```

Get all apps running a certain image:

```
fab production_controller get_apps_matching_images:molo-gem

App name                            Container image                      Domains
----------------------------------  -----------------------------------  ---------------------------------
Springster Vietnam Celery           praekeltfoundation/molo-gem:eb78e57
Springster Vietnam                  praekeltfoundation/molo-gem:eb78e57  unique-app-id-1234.seed.p16n.org
                                                                         vn.gem.molo.unicore.io
                                                                         vn.heyspringster.com
Springster Myanmar Celery           praekeltfoundation/molo-gem:eb78e57
```

Get all apps serving a specific domain:

```
fab production_controller get_apps_matching_domains:heyspringster.com

Domain                        App ID                App name                                    Container image
----------------------------  --------------------  ------------------------------------------  -----------------------------------------------
bj.heyspringster.com          /unique-app-744       Springster French                           praekeltfoundation/molo-gem:eb78e57
www.heyspringster.com         /unique-app-793       Springster global static site www redirect  praekeltfoundation/docker-nginx-redirect:latest
```
