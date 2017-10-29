# heroku config:set DISABLE_COLLECTSTATIC=1
release: python manage.py migrate
web: npm run build && python manage.py collectstatic --noinput && gunicorn citycouncil.prod_wsgi --log-file -
