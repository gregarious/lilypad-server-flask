# Lillypad Server

A Flask-based HTTP server hosting the Lilypad API.

## Current status

Basic single-file, first iteration of a MongoDB-backed API.

Currently just supporting GET/DELETE on a basic Student resource (first/last
name only), and GET/POST to a Student resource collection.

## Installation

1.  Install `virtualenv` and `virtualenvwrapper` using [these instructions](http://docs.python-guide.org/en/latest/dev/virtualenvs.html)
    - If you don't have `pip` installed, [check out this guide](http://docs.python-guide.org/en/latest/#getting-started)
      for a full how-to on a good way to set up a local Python installation.

2. Create a new virtual environment for Lilypad:

        $ mkvirtualenv lilypad

3. Install dependencies into the new environment:

        $ pip install -r requirements.txt

4. If settings other than those declared in config/default.py are needed, a
    local configuration file is necessary. Create this file (use
    `config/deploy.cfg.sample` as a template) and ensure a shell environment
    variable called `LILYPAD_DEPLOY_SETTINGS` is set to the new file name
    when the app is run.

    The recommended way to do this is to add the following line to your
    `.virtualenvs/lilypad/bin/postactivate`:

        export LILYPAD_DEPLOY_SETTINGS=/path/to/settings/file

    And this to `.virtualenvs/lilypad/bin/predeactivate`:

        unset LILYPAD_DEPLOY_SETTINGS

    This way, any time the virtualenv is active, the local deployment settings
    will be in place.

5. Launch the app:

        python app/app.py
