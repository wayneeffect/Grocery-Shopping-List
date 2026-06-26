# Grocery Shopping List

A simple web-based grocery shopping list built with Flask and SQLite.

## Features
- Add items with quantity and category
- Mark items as completed
- Delete items
- Persistent storage with SQLite
- Mobile-friendly design

## Local Setup
1. Clone the repo
2. `pip install -r requirements.txt`
3. `python app.py`
4. Open http://127.0.0.1:5000

## Deploy to Render
1. Push this repo to GitHub
2. Go to [Render.com](https://render.com), create a new Web Service
3. Connect your GitHub repo
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Deploy!

The app will be live with automatic deploys on push.
