# Photo Album Designer

**Photo Album Designer** is a Django 6.0 based web system for managing photo albums, automatically creating collages, and organizing personal media collections. It features both a server-side rendered web interface and a complete REST API.

## 🚀 Key Features

- **User Profiles**: Custom profiles with Cloudinary-hosted avatars.
- **Albums & Photos**: Upload, extended management of personal photo collections.
- **Automated Collages**: Tools to generate collages from album photos.
- **Hybrid Interface**: Full support for both Web UI (Django Templates) and REST API (DRF).
- **Diagnostics**: Built-in bug reporting system.

## 🛠 Tech Stack

- **Backend**: Python 3.10+, Django 6.0, Django Rest Framework
- **Storage**: Cloudinary (Avatars), Local File System (Albums)
- **Database**: SQLite (Default)
- **Documentation**: Swagger/OpenAPI

## 📚 Documentation

Full documentation is available in the [`docs/`](docs/) directory:

- [Setup and Installation](docs/setup.md)
- [System Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [User Guide](docs/user_guide.md)

## ⚡ Quick Start

1. **Clone & Setup**:

   ```bash
   git clone <repo_url>
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create `.env` based on `.env.example` and add your Cloudinary credentials.

3. **Run**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` to start.
