# Devcontainer Space Issue


## Failed to start devcontainer - no space left on device

When this happen, open "Docker Desktop" GUI console and clean up useless Images or Containers. But this way wil run into an end, like this time.

First of all, ```df -H``` to make sure you have enough free space

已经都删干净了啊， Docker 系统中有 3 个镜像，3 个容器，8 个本地数据卷和 423 个构建缓存文件。
```bash
$ docker system df 
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          3         3         4.716GB   0B (0%)
Containers      3         0         8.592GB   8.592GB (100%)
Local Volumes   8         1         2.678GB   213kB (0%)
Build Cache     423       0         12.65GB   12.65GB
$ docker ps -a --format '{{.ID}}: {{.Size}}'

25295acb03d4: 1.29GB (virtual 2.43GB) # 注意这些不包括Image里已经有了的数据
dd26796785a2: 4.69GB (virtual 6.29GB) # 它们是你run起来container 之后增加的内容
5c90b8869d98: 2.61GB (virtual 4.59GB) # container 被删除之后就没有了

$ docker images --format '{{.ID}}: {{.Size}}'

5fdccc474b7b: 1.13GB
776bf4a068db: 1.6GB
25e71947e2a3: 1.98GB
25e71947e2a3: 1.98GB
```
### dangerous system prune --volumes

Note it will delete all stopped containers, and since there is no more containers, it will continue to delete all volumes (because they are not used by at least one container).  It will also delete all build cache of course, so you end up have to rebuild all your containers, and lost all data in devconainers which not added by yourself, excpet you the repo you have pushed up.

```bash
$ docker system prune --volumes

WARNING! This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all volumes not used by at least one container
  - all dangling images
  - all dangling build cache

$ docker system df  #和上面的比较一下！
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          3         0         4.716GB   4.716GB (100%)
Containers      0         0         0B        0B
Local Volumes   0         0         0B        0B
Build Cache     56        0         0B        0B
```


### clean up Build Cache

This is much better way when you don't have much containers or volumes to clean up.

```bash
$ docker builder prune
WARNING! This will remove all dangling build cache. Are you sure you want to continue? [y/N] y
Deleted build cache objects:
yc7b6qzhiry9wxwids79pgj6d
p4m8g1uv34lxa0hk5rw0xky9g
vwrp880gndsepaj0kxvhhr155
hj60c7xtjl9afq3xfirfx7x87
u9a0zec9to42fqf1z1b2up6s0

Total reclaimed space: 3.458MB
$ docker system df    
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          5         1         5.875GB   5.531GB (94%)
Containers      1         1         731.6kB   0B (0%)
Local Volumes   1         1         167.1MB   0B (0%)
Build Cache     76        0         0B        0B
```

