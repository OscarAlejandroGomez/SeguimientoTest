#! /bin/sh
gunicorn --bind 0.0.0.0:5000 app:app