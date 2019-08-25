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

# Adding Translations

When writing new strings, surround blocks of text with `{% blocktrans %}...{% endblocktrans %}`.
If any variables appear within the text, they should be translated (or `{% trans $var noop %}`) independently.

    python manage.py makemessages  # add blocks to translation file
    # fill in translations in .po files
    python manage.py compilemessages  # convert .po to .mo optimized format
