# rpa-nano
RPA for nano services

### Official homepage

[https://introvesia.com](https://introvesia.com)

## RPA Router

RPA Router is an API to handle request.

### Run the server

```bash
cd rpaNanoRouter
python manage.py runserver
```

### DB migration

```bash
python manage.py migrate
```

### Create superuser

```bash
python manage.py createsuperuser
```

## APIs

1. `GET rpa/up` - Starts container up.
2. `GET rpa/down` - Shuts container down.
3. `GET rpa/active` - Get active containers.
4. `GET rpa/image` - Get images.
5. `GET rpa/volume` - Get volumes.
6. `GET rpa/copy` - Copy data from shared directory on the host to a container.
