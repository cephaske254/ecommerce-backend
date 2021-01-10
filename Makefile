flush:
	python3 manage.py flush

run:
	python3 manage.py runserver 0.0.0.0:8000

make:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

freeze:
	pip freeze > requirements.txt