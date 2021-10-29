# cambridge

This is a django + webpack project, styled with bootstrap!

# Setup

```
npm install

pip install -r requirements.txt
python manage.py migrate
```

# Running the site

```
npm run build  # generates javascript bundles and puts css in place for django to serve
python manage.py runserver  # launches django server
```

# Random scripts

Running a random script on production can be a little hard. You can save the script as a django management command and execute it via heroku run, but for a one-off script, it's easier to run python via the django shell. Here are examples of each:

```
heroku run 'python manage.py shell -' < myscript.py
heroku run 'python manage.py load_some_csv -' < some_csv.csv
```

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
