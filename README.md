# CTF-Platform-Lite
I created this project as a study.

This project uses [DashGum](http://blacktie.co/2014/07/dashgum-free-dashboard/).
Thanks to Carlos.

## Requirements
- Docker
- Docker compose

## Usage 
1. Build a container
```docker-compose up```
Please wait until you see
```
db_1   | LOG:  database system is ready to accept connections
db_1   | LOG:  autovacuum launcher started
```

2. Migrate
Entering the container
```
docker exec -it ctfplatform_web_1 /bin/bash
```
and migrate.
```
./manage.py makemigrations
./manage.py migrate
```

3. Create SuperUser
```
./manage.py createsuperuser
```

4. Run test server
```
./manage.py runserver 0.0.0.0:8000
```
If you want to use this server to listen from Internet, 
prepare some web servers like nginx.

5. Access admin site
   - http://localhost:8000
6. Create Affiliates
7. Create Problems



