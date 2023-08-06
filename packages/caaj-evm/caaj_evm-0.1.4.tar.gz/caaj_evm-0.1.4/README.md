# CAAJ tools for EVM

## docker
### for start

```
$ docker-compose up -d
```

### for end

```
$ docker-compose down
```

### for remove

```
$ docker-compose down --rmi all --volumes --remove-orphans
```

## how to test


```
$ pip install -e .[dev]
$ python /app/setup.py test
```
