# API Reference

The project exposes a comprehensive RESTful API documented via Swagger/OpenAPI.

## Accessing Documentation

Once the server is running, visit:

- **Swagger UI**: [`http://127.0.0.1:8000/api/schema/swagger-ui/`](http://127.0.0.1:8000/api/schema/swagger-ui/)
- **ReDoc**: [`http://127.0.0.1:8000/api/schema/redoc/`](http://127.0.0.1:8000/api/schema/redoc/)

## Authentication

The API uses **Token Authentication**.

- **Header**: `Authorization: Token <your_token_key>`
- **Obtain Token**: POST `/api-token-auth/` (if configured) or via the Registration endpoint.

## Key Endpoints

### Authentication & Users

- `POST /api/register/`: Create a new account. Returns Auth Token.
- `POST /api/logout/`: Invalidate current token.
- `GET/PUT /api/profile/`: Retrieve or update current user profile.
- `PUT /api/change-password/`: Change account password.

### Albums & Photos

- `GET /api/albums/`: List all albums belonging to the authenticated user.
- `POST /api/albums/`: Create a new album.
- `POST /api/albums/{id}/upload-photos/`: Upload multiple photos to an album.
- `POST /api/albums/{id}/generate-collage/`: Trigger backend logic to create a collage from album photos.

### Bug Reports

- `GET /api/bug-reports/`: List user's bug reports.
- `GET /api/bug-reports/export-excel/` (Admin only): Download all reports as Excel file.
