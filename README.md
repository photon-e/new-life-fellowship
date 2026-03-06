# New Life Fellowship Streaming MVP (Django)

A deployable Django MVP for a streaming-style website based on the architecture, data model, and UI planning documents in `docs/`.

## What this MVP includes

- Homepage with featured videos, latest uploads, and categories
- Video library with responsive grid + pagination
- Video detail page with HTML5 video player and related videos
- Category listing and category detail pages
- Django admin management for categories and videos
- Media uploads to:
  - `media/videos/`
  - `media/thumbnails/`
- Tailwind CSS styling via CDN (dark, responsive UI)
- SQLite-first configuration for simple deployment (including PythonAnywhere)

## Project structure

```text
new-life-fellowship/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── categories/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── videos/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── videos/
│   │   ├── video_list.html
│   │   └── video_detail.html
│   └── categories/
│       ├── category_list.html
│       └── category_detail.html
├── media/
│   ├── videos/
│   └── thumbnails/
├── manage.py
└── db.sqlite3 (generated after migrate)
```

## Data model (MVP subset)

### Category
- `name`
- `slug`
- `description`

### Video
- `title`
- `slug`
- `description`
- `video_file` (stored in `media/videos/`)
- `thumbnail` (stored in `media/thumbnails/`)
- `visibility` (`draft` or `published`)
- `is_featured`
- `primary_category`
- `categories` (many-to-many)

## Local setup

1. Create and activate a virtual environment.
2. Install Django and Pillow:

```bash
pip install django pillow
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Create an admin user:

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Open:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

## Admin usage

- Add categories in **Categories**
- Add videos in **Videos**
  - Upload `.mp4` video file
  - Upload thumbnail image
  - Set `visibility=published`
  - Optionally mark as `is_featured`

## PythonAnywhere deployment notes

This project is PythonAnywhere-friendly by default:

- SQLite database in project root
- No Docker
- No external APIs
- No background queue requirements

### Environment variables

Configure (in PythonAnywhere web app settings):

- `DEBUG=False`
- `SECRET_KEY=<your-secret-key>`
- `ALLOWED_HOSTS=<your-pythonanywhere-domain>`

### Static/media settings

Already configured in `config/settings.py`:

- `STATIC_ROOT = BASE_DIR / "staticfiles"`
- `MEDIA_ROOT = BASE_DIR / "media"`

Run collectstatic during deployment:

```bash
python manage.py collectstatic --noinput
```

In PythonAnywhere **Web > Static files** map:

- `/static/` -> `/home/<username>/<project>/staticfiles`
- `/media/` -> `/home/<username>/<project>/media`

## MVP verification checklist

- [ ] Homepage loads and shows featured/latest sections
- [ ] Navigation links (Home, Videos, Categories) work
- [ ] Video library shows cards in responsive grid
- [ ] Pagination works in `/videos/`
- [ ] Video detail plays uploaded MP4 file in HTML5 player
- [ ] Related videos appear on video detail page
- [ ] Categories list page loads
- [ ] Category detail page lists videos in selected category
- [ ] Admin can create/edit/delete categories and videos
- [ ] Uploaded files are saved under `media/videos` and `media/thumbnails`
- [ ] `collectstatic` succeeds for deployment
