# Setup and Installation

## Prerequisites

- **Python**: Version 3.10+ (Developed on 3.14)
- **Pip**: Python package manager
- **Cloudinary Account**: Required for user avatar storage

## Installation Steps

1. **Clone the repository**

   ```bash
   git clone <repository_url>
   cd PHOTO_ALBUM_DESIGNER
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory. You can copy `.env.example` if it exists.
   Required variables:

   ```env
   # Django
   SECRET_KEY=your_secret_key_here
   DEBUG=True

   # Cloudinary (File Storage)
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

5. **Database Setup**
   The project uses SQLite by default. Run migrations to initialize the database:

   ```bash
   python manage.py migrate
   ```

6. **Create Superuser (Admin)**
   To access the admin panel (`/admin/`):

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Server**
   ```bash
   python manage.py runserver
   ```
   The application will be available at `http://127.0.0.1:8000/`.

## Running Tests

(Instructions for running tests if applicable)

```bash
python manage.py test
```
