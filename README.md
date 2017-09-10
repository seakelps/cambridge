# cambridge

This is a django project!

To work on it, you will probably need python 3.4 or later and django 1.11 or later.

I recommend pyenv.


# Adding Translations

When writing new strings, surround blocks of text with `{% blocktrans %}...{% endblocktrans %}`. 
If any variables appear within the text, they should be translated (or `{% trans $var noop %}`) independently.

    python manage.py makemessages  # add blocks to translation file
    # fill in translations in .po files
    python manage.py compilemessages  # convert .po to .mo optimized format
