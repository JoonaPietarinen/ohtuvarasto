#!/usr/bin/env python
"""Run the Flask web application."""
from web.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
