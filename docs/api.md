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

#### Albums

- `GET /api/albums/`: List all albums. Supports **Filtering** (by `created_at`), **Search** (`title`, `description`), and **Ordering**.
- `POST /api/albums/`: Create a new album.
- `GET /api/albums/export-excel/`: Download full album report in Excel.
- `GET /api/albums/user_albums_stats/`: Get statistics (count, total photos).
- `GET /api/albums/template_recommendations/`: Get smart template suggestions.

**Detail Operations:**

- `POST /api/albums/{id}/upload-photos/`: Upload multiple photos.
- `POST /api/albums/{id}/generate-collage/`: Create collage.
- `POST /api/albums/{id}/duplicate_album/`: Clone the album.
- `POST /api/albums/{id}/publish/`: Set album as public (requires 3+ photos).
- `POST /api/albums/{id}/share/`: Share album.
- `POST /api/albums/{id}/generate_share_link/`: Create a temporary link.

#### Photos

- `GET /api/photos/`: List photos. Filter by `album`, `is_favorite`.
- `POST /api/photos/{id}/edit/`: Apply filters (-100 to 100) and adjustments.
- `POST /api/photos/{id}/reset_edits/`: Revert changes.
- `POST /api/photos/{id}/reorder/`: Change photo order.

### Bug Reports

- `GET /api/bug-reports/`: List user's bug reports.
- `GET /api/bug-reports/export-excel/` (Admin only): Download all reports as Excel file.
