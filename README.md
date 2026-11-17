# Simple Landing Page Project

This is a practice project for building a single-page landing application using Python (Flask) and HTML (Pico.css).

## Features
- Single-page layout (Home, About Us, Forms, Auth, User Detail).
- User authentication (Register, Sign In, Sign Out) using Flask sessions.
- Secure password storage using Werkzeug hashing.
- Form submission stored locally in a `data.json` file.
- Publicly accessible via Cloudflare Tunnel.

## Prerequisites
- Python 3.x
- Git

## How to Run Locally
1. Clone the repository.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install Flask: `pip install Flask`
5. Run the app: `python app.py`
6. Open `http://127.0.0.1:8000` in your browser.

## How to Publish (Cloudflare Tunnel)
1. Install `cloudflared`.
2. Run the Flask app.
3. In a new terminal, run: `cloudflared tunnel --url http://localhost:8000`
4. Use the generated `.trycloudflare.com` link.