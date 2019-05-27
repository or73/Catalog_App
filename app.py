"""
File Path: app.py
Description: Application Init
Copyright (c) 2019. This Application has been developed by OR73.
"""
from application.setup import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
