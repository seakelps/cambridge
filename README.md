# cambridge

This is a django + webpack project, styled with bootstrap!
(sorry about the webpack, but haven't been able to update...)

We used to host on Heroku but are moving to render.com

# Setup

0. Clone the codebase

1. Download/install docker however you choose. https://www.docker.com/products/docker-desktop/


# Running the site

1. `docker compose build`

This command will do all the requirements downloading and package installation necessary. Everything but static files and database migrations.

2. `docker compose run static npm run build`

3. `docker compose run web python manage.py collectstatic`

4. `docker compose run web python manage.py migrate`

(or `makemigrations` if you're making )

5. `docker compose up`

serves the site


# Adding data locally

## manually

1. add a local django admin/super user:

`docker compose run web python manage.py createsuperuser`

2. log in:

http://localhost:8000/admin/login/?next=/admin/

3. create models via the admin as needed

## via script

coming soon! (hopefully)


# useful commands

`docker compose run web /bin/bash -c "black . && isort --profile black`


# Adding Translations

When writing new strings, surround blocks of text with `{% blocktrans %}...{% endblocktrans %}`.
If any variables appear within the text, they should be translated (or `{% trans $var noop %}`) independently.

    python manage.py makemessages  # add blocks to translation file
    # fill in translations in .po files
    python manage.py compilemessages  # convert .po to .mo optimized format
    
    
# Updating from year to year - 
Make a PR with a checklist:
- [ ] update the how to vote page
- [ ] add new candidates
- [ ] change the years found in text (landing page, etc.)
- [ ] change the money functions or finally update them for generic years (sorry)
- [ ] figure out the new ocpf.us format
