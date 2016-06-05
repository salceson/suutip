# Projekt ŚUU/TIP

## Mikroserwisy

* IP Diagnostics service
* Users service
* Aggreagate service

## Dockery

* Aby zbudować kontener dla serwisu `service1` (analogicznie dla innych):

```
cd service1
docker build -t service1:latest .
```

* Aby uruchomić kontener dla serwisu `service1`:

```
docker run --name s1 -d -p 5001:5000 service1:latest 
```

* Aby uruchomić kontener dla serwisu `service2`:

```
docker run --name s2 -d -p 5002:5000 service2:latest 
```

* Aby uruchomić kontener dla serwisu `service3`:

```
docker run --name s3 --link s1:s1 --link s2:s2 -d -p 5003:5000 service3:latest 
```

## NetStatus

NetStatus to mini appka z restowym API. Służy głównie do prezentacji ruchu sieciowego.

Wymagany Python 3.

Zależności dociągamy poleceniem:

```
pip install -r requirements.txt
```

Uruchomienie:

```
./manage.py bower_install
./manage.py migrate
./manage.py runserver 8000
```
