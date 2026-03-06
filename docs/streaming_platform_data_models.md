# Streaming Platform Data Model (Django ORM + PostgreSQL)

This design covers a Netflix-like backend for the requested features: videos, categories, speakers/creators, watch history, favorites, playlists, comments, likes, and live streaming channels.

## 1) Django Models

```python
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Creator(TimeStampedModel):
    display_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_name"]

    def __str__(self):
        return self.display_name


class Video(TimeStampedModel):
    class VideoType(models.TextChoices):
        VOD = "vod", "Video on Demand"
        LIVE_REPLAY = "live_replay", "Live Replay"

    class Visibility(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        UNLISTED = "unlisted", "Unlisted"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    description = models.TextField(blank=True)
    video_type = models.CharField(max_length=20, choices=VideoType.choices, default=VideoType.VOD)
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.DRAFT)
    duration_seconds = models.PositiveIntegerField(default=0)
    release_at = models.DateTimeField(null=True, blank=True)

    stream_url = models.URLField(help_text="Master manifest URL (HLS/DASH) or playback endpoint")
    thumbnail_url = models.URLField(blank=True)

    categories = models.ManyToManyField(Category, through="VideoCategory", related_name="videos")
    creators = models.ManyToManyField(Creator, through="VideoCreator", related_name="videos")

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["visibility", "release_at"]),
            models.Index(fields=["video_type", "visibility"]),
        ]

    def __str__(self):
        return self.title


class VideoCategory(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("video", "category")


class VideoCreator(models.Model):
    class Role(models.TextChoices):
        SPEAKER = "speaker", "Speaker"
        HOST = "host", "Host"
        PRODUCER = "producer", "Producer"
        DIRECTOR = "director", "Director"

    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.SPEAKER)
    credit_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ("video", "creator", "role")
        ordering = ["credit_order", "id"]


class WatchHistory(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watch_history")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="watch_events")

    watched_seconds = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    last_watched_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "video")
        indexes = [
            models.Index(fields=["user", "-last_watched_at"]),
            models.Index(fields=["video", "-last_watched_at"]),
        ]


class Favorite(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        unique_together = ("user", "video")
        indexes = [models.Index(fields=["user", "-created_at"])]


class Playlist(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="playlists")
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "title"], name="uq_playlist_user_title")
        ]
        indexes = [models.Index(fields=["user", "-updated_at"])]


class PlaylistItem(TimeStampedModel):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="items")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="playlist_items")
    position = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["playlist", "video"], name="uq_playlist_item_video"),
            models.UniqueConstraint(fields=["playlist", "position"], name="uq_playlist_item_position"),
        ]
        ordering = ["position", "id"]


class Comment(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["video", "-created_at"]),
            models.Index(fields=["parent", "created_at"]),
        ]


class Like(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "video"], name="uq_like_user_video")
        ]


class CommentLike(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "comment"], name="uq_like_user_comment")
        ]


class LiveChannel(TimeStampedModel):
    class ChannelStatus(models.TextChoices):
        OFFLINE = "offline", "Offline"
        LIVE = "live", "Live"
        ENDED = "ended", "Ended"

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(Creator, on_delete=models.PROTECT, related_name="live_channels")
    status = models.CharField(max_length=20, choices=ChannelStatus.choices, default=ChannelStatus.OFFLINE)
    stream_key_hash = models.CharField(max_length=255, unique=True)

    playback_url = models.URLField(help_text="Live playback manifest URL")
    chat_enabled = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["status", "-updated_at"])]


class LiveSession(TimeStampedModel):
    channel = models.ForeignKey(LiveChannel, on_delete=models.CASCADE, related_name="sessions")
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    peak_concurrent_viewers = models.PositiveIntegerField(default=0)

    replay_video = models.OneToOneField(
        Video,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="source_live_session",
        help_text="Optional VOD generated from this live session",
    )

    class Meta:
        indexes = [models.Index(fields=["channel", "-started_at"])]
        constraints = [
            models.CheckConstraint(
                check=Q(ended_at__isnull=True) | Q(ended_at__gte=models.F("started_at")),
                name="ck_live_session_end_after_start",
            )
        ]
```

---

## 2) Relationships Between Models

- **Video ↔ Category**: many-to-many through `VideoCategory`.
- **Video ↔ Creator**: many-to-many through `VideoCreator` (supports role-based credits).
- **User ↔ Video (WatchHistory)**: one user has many watch history rows; one video has many watcher rows. Unique by `(user, video)`.
- **User ↔ Video (Favorite)**: many favorites per user; unique favorite per `(user, video)`.
- **User ↔ Playlist**: one-to-many.
- **Playlist ↔ Video**: many-to-many through `PlaylistItem` with explicit ordering (`position`).
- **User ↔ Comment**: one-to-many.
- **Video ↔ Comment**: one-to-many.
- **Comment ↔ Comment (parent/replies)**: self-referential one-to-many tree.
- **User ↔ Video (Like)**: one-to-many across users/videos with unique `(user, video)`.
- **User ↔ Comment (CommentLike)**: one-to-many across users/comments with unique `(user, comment)`.
- **Creator ↔ LiveChannel**: one-to-many (channel owner).
- **LiveChannel ↔ LiveSession**: one-to-many (broadcast sessions/history).
- **LiveSession ↔ Video (replay)**: optional one-to-one link to VOD replay.

---

## 3) ER Diagram Description (Textual)

Think in four domains:

1. **Catalog domain**
   - `Video` is central.
   - `Category` and `Creator` connect through junction tables (`VideoCategory`, `VideoCreator`).

2. **Engagement domain**
   - User-content interactions point to `Video`: `WatchHistory`, `Favorite`, `Like`, `Comment`.
   - `Comment` supports threaded conversations via `parent`.
   - `CommentLike` is separate from `Like` to preserve integrity and avoid nullable polymorphic likes.

3. **Collection domain**
   - `Playlist` belongs to user.
   - `PlaylistItem` binds ordered videos to each playlist.

4. **Live domain**
   - `LiveChannel` is the always-on identity (metadata + playback endpoint + stream key hash).
   - `LiveSession` stores each concrete live run with start/end + peak viewers.
   - Finished sessions may produce a replay `Video`.

A visual crow-foot summary:

- `User 1—* WatchHistory *—1 Video`
- `User 1—* Favorite *—1 Video`
- `User 1—* Like *—1 Video`
- `User 1—* Comment *—1 Video`
- `Comment 1—* Comment (replies)`
- `User 1—* Playlist 1—* PlaylistItem *—1 Video`
- `Video *—* Category` via `VideoCategory`
- `Video *—* Creator` via `VideoCreator`
- `Creator 1—* LiveChannel 1—* LiveSession 0..1—1 Video(replay)`

---

## 4) Scalability Considerations

### A. PostgreSQL schema and indexing
- Add **composite indexes** for top queries:
  - `(user_id, last_watched_at DESC)` on `WatchHistory`
  - `(video_id, created_at DESC)` on `Comment`
  - `(playlist_id, position)` on `PlaylistItem`
- Use **partial indexes** for frequent filters (e.g., only `Video.visibility='published'`).
- For large comments/watch tables, consider **time-based partitioning** or hash partitioning by `user_id`.

### B. High-write workloads
- `WatchHistory` is write-heavy; use `INSERT ... ON CONFLICT` semantics via Django `update_or_create` patterns or raw upserts in hot paths.
- Batch analytic counters asynchronously (e.g., likes count, comment count) using Celery/Kafka workers.

### C. Read path optimization
- Cache hot entities (`Video`, playlist rails, top categories) in Redis.
- Use `select_related`/`prefetch_related` aggressively for catalog pages.
- Denormalize selected counters (`video.like_count`, `video.comment_count`) with eventual consistency.

### D. Live streaming scale
- Keep stream transport outside Django (RTMP ingest + media server/CDN).
- Django should manage metadata/control-plane only: channel status, session lifecycle, entitlements.
- Store ephemeral live viewer telemetry in Redis/Kafka; persist coarse aggregates to Postgres.

### E. Data growth and governance
- Apply retention policy to low-value events/log tables.
- Archive old watch/comment/engagement data into warehouse/lake for BI.
- Add auditing fields (`created_by`, `updated_by`) for moderation/admin operations.

### F. Safety and integrity
- Use DB-level uniqueness constraints for all dedup cases (favorites/likes/watch rows).
- Soft-delete comments (`is_deleted`) to preserve thread structure and moderation traceability.
- Hash stream keys (`stream_key_hash`) and never store raw keys.
