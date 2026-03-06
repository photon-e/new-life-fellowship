# New Life Fellowship Streaming Platform Blueprint

## 1) High-Level System Architecture

### 1.1 Logical Architecture
- **Client Layer**: Browser and mobile web clients rendered primarily via Django templates + Tailwind CSS.
- **Edge Layer (Nginx)**:
  - TLS termination
  - Static file serving (`/static/`) and media proxy rules
  - Reverse proxy to Django (Gunicorn/Uvicorn)
  - Optional secure HLS segment proxying and token checks
- **Application Layer (Django)**:
  - Monolith-style service with modular Django apps
  - Handles authentication, catalog, subscriptions, watch pages, playback token generation, analytics events API, and admin workflows
  - Background processing via Celery workers (transcoding orchestration, metadata extraction, scheduled jobs)
- **Data Layer**:
  - PostgreSQL for transactional data (users, videos, entitlements, subscriptions, watch progress)
  - Redis for caching/session backend/rate-limiting queues (recommended)
- **Storage + Delivery Layer**:
  - Cloud object storage for source videos, HLS manifests, HLS segments, thumbnails, subtitles
  - CDN in front of storage for global low-latency delivery
- **Async/Processing Layer**:
  - Media pipeline worker (FFmpeg jobs in containers) to transcode uploads to HLS ABR renditions
  - Optional webhook/callback system for job completion

### 1.2 Runtime/Deployment Architecture
- Docker Compose (dev/staging) or Kubernetes/ECS (prod) with containers:
  - `nginx`
  - `web` (Django + Gunicorn)
  - `worker` (Celery)
  - `beat` (Celery scheduler)
  - `postgres`
  - `redis`
- Nginx routes:
  - `/` -> Django app
  - `/static/` -> static files
  - `/hls/` -> signed proxy pass to cloud storage or CDN URL redirect

---

## 2) Core Features of the Platform

1. **User & Identity**
   - Registration, login, logout, password reset, optional social auth
   - Profile management and device/session management

2. **Content Catalog**
   - Browse by categories/series/tags
   - Search and filtering
   - Featured, trending, and recently added rails

3. **Video Playback**
   - Adaptive playback (HLS)
   - Resume watching from saved progress
   - Multi-bitrate quality switching
   - Subtitle/audio track support

4. **Monetization & Access Control**
   - Free, subscription, rental, or entitlement-based access
   - Plan management and entitlement checks before playback URL issuance

5. **Operational Content Management**
   - Upload and ingest videos
   - Transcoding job tracking and publishing workflow
   - Metadata editing and scheduling

6. **Engagement**
   - Watch history
   - Continue watching rail
   - Likes/favorites/watchlist (optional)

7. **Analytics & Observability**
   - Playback events (start, quartiles, complete, errors)
   - Admin dashboard KPIs
   - Structured logging/metrics/alerts

---

## 3) Django App Structure

Recommended app split (modular monolith):

- `core`: shared utilities, base models, health checks, settings helper hooks
- `accounts`: custom user model, auth, profiles, device sessions
- `catalog`: videos, series, seasons, episodes, categories, tags, search indexing hooks
- `media_pipeline`: upload intake, encoding job records, FFmpeg integration, subtitle ingestion
- `playback`: tokenized playback URLs, watch progress, playback sessions/events
- `billing`: plans, subscriptions, payments, invoices, entitlements
- `cms`: editorial collections, banners, featured rails, publish scheduling
- `analytics`: aggregation jobs and reporting models
- `api` (optional): JSON endpoints for SPA/mobile compatibility and player telemetry ingestion

Design principle: keep domain logic in service classes (`services.py`) and thin views/forms.

---

## 4) Database Models (PostgreSQL)

### 4.1 Identity & Access
- **User** (`accounts_user`)
  - `id`, `email` (unique), `password_hash`, `is_active`, `is_staff`, timestamps
- **UserProfile**
  - `user` (1:1), display fields, preferences, parental settings
- **DeviceSession**
  - `user` (FK), `device_id`, `user_agent`, `last_seen_at`, `ip`

### 4.2 Content Domain
- **VideoAsset**
  - Core entity for playable content (movie/episode/clip/sermon)
  - Fields: `title`, `slug`, `description`, `duration_seconds`, `content_rating`, `publish_status`, `published_at`
- **Series** / **Season** / **EpisodeMap**
  - Hierarchy for episodic content
- **Category**, **Tag**, **VideoCategory**, **VideoTag**
  - Classification and discovery
- **ThumbnailAsset**
  - `video` FK, `image_url`, `kind` (poster/landscape), dimensions
- **SubtitleTrack**
  - `video` FK, `language`, `format`, `url`

### 4.3 Media Processing
- **SourceUpload**
  - `video` FK, original file path, checksum, size, uploaded_by, status
- **TranscodeJob**
  - `source_upload` FK, profile, state, error, started/completed timestamps
- **HLSVariant**
  - `video` FK, `resolution`, `bitrate_kbps`, `playlist_url`
- **MediaManifest**
  - `video` FK, `master_playlist_url`, DRM metadata (nullable)

### 4.4 Monetization
- **Plan**
  - `name`, `price`, `billing_cycle`, `is_active`
- **Subscription**
  - `user` FK, `plan` FK, status, period start/end, provider refs
- **Entitlement**
  - polymorphic rule linking user/plan to video/category/series access
- **PaymentTransaction**
  - gateway transaction IDs, amount, status, raw payload JSONB

### 4.5 Playback & Analytics
- **PlaybackSession**
  - `user` FK nullable, `video` FK, started_at, ended_at, device, app_version
- **WatchProgress**
  - unique (`user`, `video`) with `position_seconds`, `completed`, `updated_at`
- **PlaybackEvent**
  - session FK, event_type, position_seconds, client timestamp, metadata JSONB

### 4.6 CMS/Operations
- **Collection** and **CollectionItem**
  - Home rails (e.g., “Trending”, “Recently Added”)
- **Banner**
  - hero slider assets, CTA links, scheduling windows

Indexes/constraints recommendations:
- GIN index on search vectors (`title`, `description`)
- Composite index for watch progress lookups (`user_id`, `updated_at DESC`)
- Partial indexes for active subscriptions and published videos

---

## 5) Suggested Folder Structure

```text
new-life-fellowship/
├─ docker/
│  ├─ nginx/
│  │  ├─ nginx.conf
│  │  └─ site.conf
│  ├─ web/Dockerfile
│  └─ worker/Dockerfile
├─ compose.yml
├─ manage.py
├─ requirements/
│  ├─ base.txt
│  ├─ dev.txt
│  └─ prod.txt
├─ config/
│  ├─ settings/
│  │  ├─ base.py
│  │  ├─ dev.py
│  │  └─ prod.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
├─ apps/
│  ├─ core/
│  ├─ accounts/
│  ├─ catalog/
│  ├─ media_pipeline/
│  ├─ playback/
│  ├─ billing/
│  ├─ cms/
│  ├─ analytics/
│  └─ api/
├─ templates/
│  ├─ base.html
│  ├─ components/
│  └─ pages/
├─ static/
│  ├─ css/
│  │  └─ tailwind.css
│  ├─ js/
│  └─ images/
├─ scripts/
│  ├─ ffmpeg/
│  └─ maintenance/
└─ tests/
   ├─ unit/
   ├─ integration/
   └─ e2e/
```

---

## 6) Video Storage Strategy

1. **Raw Upload Bucket**
   - Private bucket/container for source uploads
   - Server-side encryption and lifecycle policies

2. **Processed Delivery Bucket**
   - HLS master manifests + variant playlists + segments
   - Public via CDN or private + signed URL policy

3. **Asset Organization Convention**
   - `videos/{video_uuid}/source/original.mp4`
   - `videos/{video_uuid}/hls/master.m3u8`
   - `videos/{video_uuid}/hls/1080p/index.m3u8`
   - `videos/{video_uuid}/hls/1080p/segment_00001.ts`
   - `videos/{video_uuid}/thumbs/poster.jpg`

4. **Security Controls**
   - Signed URLs with short TTL for playback assets
   - Tokenized manifest access (user entitlement checked in Django before issuing token)
   - Bucket access restricted by IAM role/service account

5. **Lifecycle**
   - Archive/delete raw uploads after successful QC + backup window
   - Keep delivery assets long-lived; use versioning for republished media

---

## 7) Streaming Approach: HLS (Recommended)

### Why HLS over Progressive Streaming
- Adaptive bitrate for varying networks
- Better compatibility with modern players/CDNs
- Improved startup/perceived quality with tuned segment size
- Easier future DRM packaging path

### HLS Packaging Guidelines
- Multi-bitrate ladder example: 240p/360p/480p/720p/1080p
- Segment length: 4–6 seconds (VOD)
- Codec baseline: H.264 + AAC (broad compatibility)
- Generate master playlist plus variant playlists
- Player options: hls.js (web) with fallback for Safari native HLS

### Django Playback URL Flow
1. Client requests `/watch/<slug>/playback-token/`
2. Django verifies authentication + entitlement
3. Django returns signed master playlist URL or one-time tokenized proxy URL
4. Player requests manifest/segments directly via CDN (preferred) or Nginx proxy

---

## 8) Admin Panel Features

Use Django Admin + custom admin views/actions:

1. **Content Management**
   - Create/edit video metadata, categories, tags
   - Series/season/episode management
   - Schedule publish/unpublish windows

2. **Media Operations**
   - Upload source files (or ingest from object storage URL)
   - Launch/retry transcode jobs
   - Validate generated renditions, subtitles, thumbnails

3. **Access/Monetization**
   - Manage plans, subscriptions, and entitlement rules
   - Manual grant/revoke access for support cases

4. **User Support**
   - User lookup, active devices, watch history snapshots
   - Reset sessions and playback anomalies troubleshooting

5. **Analytics Dashboards**
   - Top content, completion rate, average watch time, error ratios
   - Time-series traffic and subscription conversion summaries

6. **Audit & Governance**
   - Admin action logs
   - Role-based admin permissions (editor, operator, finance, superadmin)

---

## 9) Future Scalability Considerations

1. **Service Decomposition Path**
   - Start with modular monolith; split heavy domains later:
     - playback token service
     - billing integration service
     - analytics/event pipeline service

2. **Asynchronous Event Pipeline**
   - Move playback events from sync writes to Kafka/PubSub + warehouse sink
   - Keep PostgreSQL only for operational analytics summaries

3. **Search at Scale**
   - Begin with PostgreSQL full-text search
   - Migrate to OpenSearch/Elasticsearch when catalog grows substantially

4. **Caching Strategy**
   - Redis for catalog page fragments, feature rails, entitlement cache
   - CDN cache-control tuning for manifests/segments/thumbnails

5. **Global Distribution**
   - Multi-region object storage replication
   - Regional CDNs and origin shield

6. **Security Hardening**
   - Optional DRM (Widevine/FairPlay) for premium content
   - WAF, bot protection, stricter rate limits, anomaly detection

7. **Reliability/SRE**
   - Health checks, SLOs, dashboards, alerts
   - Blue-green or rolling deployments
   - Automated backups + restore drills

8. **Data & Compliance**
   - GDPR/CCPA workflows for data export/deletion
   - Data retention policies for events/logs

---

## Suggested Initial Milestones
1. **MVP (6–10 weeks)**: auth, catalog, HLS playback, basic admin ingest, watch progress.
2. **Phase 2**: subscriptions + entitlement engine + analytics dashboards.
3. **Phase 3**: personalization rails, advanced moderation workflows, multi-region optimization.
