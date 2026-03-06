# New Life Fellowship Streaming MVP (Django)

A Django + Tailwind MVP video streaming platform inspired by GTN-style layouts.

## Updated folder structure

```text
new-life-fellowship/
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── videos/
│   ├── speakers/
│   ├── categories/
│   └── live/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── live/live.html
│   ├── videos/
│   ├── speakers/
│   └── categories/
├── static/
│   ├── css/
│   └── js/
└── media/
    ├── videos/
    ├── thumbnails/
    └── speakers/
```

## Core MVP features

- Homepage with hero banner, Watch Live strip, featured videos, featured speakers, topics, and latest videos.
- Live TV page at `/live/` with embedded HTML5 player and current program details.
- Video library at `/videos/` with grid cards, pagination, and category/topic filters.
- Video detail page at `/videos/<slug>/` with player, metadata, and related videos.
- Speakers directory and detail pages with each speaker's videos.
- Topics listing and topic detail pages.
- Full Django admin management for videos, speakers, categories, topics, and live streams.

## Data model

### Video
- title
- slug
- description
- video_file
- thumbnail
- speaker
- category
- topics (many-to-many)
- duration
- created_at
- is_featured
- is_published

### Speaker
- name
- slug
- photo
- bio

### Category
- name
- slug
- description

### Topic
- name
- slug
- description

### LiveStream
- title
- stream_url
- current_program
- description
- is_active

## Local run instructions

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```
5. Run dev server:
   ```bash
   python manage.py runserver
   ```

Visit:
- `/`
- `/live/`
- `/videos/`
- `/speakers/`
- `/topics/`
- `/admin/`

## PythonAnywhere deployment instructions

1. Upload project and create a virtualenv.
2. Install dependencies with pip.
3. Set environment variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=<your-domain>`
4. Run:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
5. Configure static/media mappings in PythonAnywhere web tab:
   - `/static/` → `<project>/staticfiles`
   - `/media/` → `<project>/media`
6. Reload web app.

## MVP verification checklist

- [ ] Homepage renders hero + sections
- [ ] `/live/` plays configured stream URL
- [ ] `/videos/` filtering + pagination work
- [ ] `/videos/<slug>/` plays uploaded video + shows related content
- [ ] `/speakers/` and `/speakers/<slug>/` render correctly
- [ ] `/topics/` and `/topics/<slug>/` render correctly
- [ ] Admin can create/edit Video, Speaker, Category, Topic, LiveStream
- [ ] Uploads save under media folders
- [ ] `collectstatic` completes successfully
