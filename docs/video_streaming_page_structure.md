# Video Streaming Website Page Structure (Django Templates + Tailwind CSS)

## 1) List of all pages

1. Homepage (`/`)
2. Video detail/watch page (`/videos/<slug>/`)
3. Category browsing page (`/categories/<slug>/`)
4. Creator page (`/creators/<slug>/`)
5. Search results page (`/search/?q=`)
6. User profile page (`/profile/`)
7. Watch history page (`/profile/history/`)
8. Playlist page (`/playlists/<slug>/`)

---

## 2) Wireframe descriptions

## A. Homepage layout

**Goal:** Drive discovery and retention with clear featured content and rails.

**Top-to-bottom wireframe:**
- **Sticky Header**
  - Left: Logo
  - Center: Global nav links
  - Right: Search button/input, notifications, avatar menu
- **Hero Banner**
  - Large featured video background/poster
  - Title, short synopsis, CTA buttons (`Watch Now`, `Add to Playlist`)
- **Continue Watching Rail** (authenticated users)
  - Horizontal cards with progress bars
- **Category Rails**
  - “Trending”, “New Releases”, “Most Watched”, and per-category rows
- **Featured Creator Rail**
  - Circular avatars + creator names
- **Footer**
  - Secondary nav, legal links, social links

**Template split recommendation:**
- `templates/base/base.html`
- `templates/videos/home.html`
- `templates/base/partials/header.html`
- `templates/base/partials/footer.html`
- `templates/videos/partials/video_rail.html`

## B. Video detail page

**Goal:** Maximize watch starts and content depth.

**Top-to-bottom wireframe:**
- **Header** (same global header)
- **Primary section (desktop 2-column / mobile stacked):**
  - Left: Video player area (16:9)
  - Right: Metadata card
    - Title, creator, category tags, publish date
    - Action buttons: Like, Share, Save
- **Description block** (expand/collapse for long text)
- **Episode/Related Videos rail**
- **Comments / engagement section** (optional)

**Template split recommendation:**
- `templates/videos/detail.html`
- `templates/videos/partials/player.html`
- `templates/videos/partials/video_meta.html`
- `templates/videos/partials/related_videos.html`

## C. Category browsing page

**Goal:** Let users quickly explore videos inside one taxonomy node.

**Top-to-bottom wireframe:**
- **Header**
- **Category hero strip**
  - Category title, description, item count
- **Filter + Sort row**
  - Sort dropdown (newest, most viewed)
  - Optional chips (duration, creator, tags)
- **Responsive video grid**
  - Cards with poster, title, creator, duration, views
- **Pagination / infinite load trigger**

**Template split recommendation:**
- `templates/categories/detail.html`
- `templates/videos/partials/video_card.html`
- `templates/base/partials/pagination.html`

## D. Creator page

**Goal:** Build channel identity and promote creator’s catalog.

**Top-to-bottom wireframe:**
- **Header**
- **Creator banner/profile header**
  - Cover image, avatar, name, bio, follow/subscribe button
- **Creator stats row**
  - Followers, total videos, total views
- **Content tabs**
  - Videos, Playlists, About
- **Selected tab content area**
  - Video grid or playlist list

**Template split recommendation:**
- `templates/creators/detail.html`
- `templates/creators/partials/creator_header.html`
- `templates/creators/partials/creator_tabs.html`

## E. Search page

**Goal:** Return relevant results fast with narrowing controls.

**Top-to-bottom wireframe:**
- **Header with focused search input**
- **Search context row**
  - Query summary (`Results for "<term>"`), count, sort dropdown
- **Left filter sidebar (desktop) / slide-over (mobile)**
  - Content type, category, upload date, duration
- **Right results column**
  - Mixed list or grid of result cards
  - Highlight matched terms
- **No results state**
  - Suggestions and fallback links

**Template split recommendation:**
- `templates/videos/search.html`
- `templates/videos/partials/search_filters.html`
- `templates/videos/partials/search_result_item.html`

## F. User profile page

**Goal:** Central hub for account and personalization.

**Top-to-bottom wireframe:**
- **Header**
- **Profile header card**
  - Avatar, display name, email, edit profile action
- **Quick stats**
  - Saved videos, playlists, watch time (optional)
- **Profile sections grid**
  - Continue watching, recent playlists, liked videos
- **Settings entry points**
  - Account, password, notification preferences

**Template split recommendation:**
- `templates/users/profile.html`
- `templates/users/partials/profile_header.html`
- `templates/users/partials/profile_sections.html`

## G. Watch history page

**Goal:** Help users resume or revisit previously watched videos.

**Top-to-bottom wireframe:**
- **Header**
- **Title row with actions**
  - “Watch History”, clear history button, date range filter
- **Chronological list grouped by day/week**
  - Thumbnail, title, watched timestamp, progress bar
- **Bulk actions**
  - Remove selected items

**Template split recommendation:**
- `templates/users/watch_history.html`
- `templates/users/partials/history_item.html`

## H. Playlist page

**Goal:** Present curated/user-generated collections with easy playback.

**Top-to-bottom wireframe:**
- **Header**
- **Playlist header block**
  - Playlist cover, title, owner, description, item count
  - CTA: Play all, shuffle, edit (owner only)
- **Video list area**
  - Ordered rows with drag handle (owner mode), duration, added date
- **Suggested videos panel** (optional)
  - Recommended additions

**Template split recommendation:**
- `templates/playlists/detail.html`
- `templates/playlists/partials/playlist_header.html`
- `templates/playlists/partials/playlist_video_row.html`

---

## 3) Recommended Tailwind components

## Shared/global components
- Sticky header/nav bar (`sticky top-0 z-50 backdrop-blur`)
- Mobile menu drawer (`fixed inset-y-0` with transition utilities)
- Search input with icon (`relative`, `pl-10`)
- Dropdown menus (profile, sort)
- Toast/alert component for actions

## Content components
- **Video card**
  - Poster thumbnail + gradient overlay
  - Title + metadata
  - Hover states (`group-hover:scale-105`)
- **Rail component**
  - Horizontal scroll container (`flex overflow-x-auto snap-x`)
- **Hero banner**
  - Background image with dark overlay (`bg-gradient-to-t from-black/80`)
- **Tag/chip component**
  - Filter chips with selected states
- **Progress bar**
  - Watch progress overlay on thumbnails

## Page-specific components
- **Video player shell** with fixed aspect (`aspect-video`)
- **Creator profile header** with cover + avatar overlap
- **Results sidebar drawer** for mobile search filters
- **Playlist row item** with optional drag handle
- **Pagination controls** (`inline-flex`, `rounded-md`, focus rings)

## Utility patterns to standardize
- Container widths: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- Card system: `rounded-xl bg-zinc-900/60 border border-zinc-800`
- Typography scale using Tailwind `text-*` + `font-semibold`
- Consistent spacing tokens (`space-y-*`, `gap-*`)
- Dark-first theme tokens for streaming-style UI

---

## 4) Navigation structure

## Primary navigation (desktop top bar)
- Home
- Categories (dropdown mega-menu)
- Creators
- Playlists
- Search (input/button)

## Secondary/user navigation (avatar menu)
- Profile
- Watch History
- My Playlists
- Account Settings
- Logout

## Mobile navigation
- Bottom nav or hamburger drawer with:
  - Home
  - Categories
  - Search
  - Playlists
  - Profile

## Suggested URL map
- `/` → homepage
- `/videos/<slug>/` → video detail/watch
- `/categories/` and `/categories/<slug>/` → category listing/detail
- `/creators/` and `/creators/<slug>/` → creator directory/detail
- `/search/?q=<query>` → search results
- `/profile/` → profile home
- `/profile/history/` → watch history
- `/playlists/` and `/playlists/<slug>/` → playlist listing/detail

## Breadcrumb pattern
- Use breadcrumbs on deep pages for orientation:
  - `Home / Category / Video`
  - `Home / Creator / Playlist`

## Cross-linking rules
- Every video card links to video detail page.
- Category chips link back to category browse pages.
- Creator names/avatars always link to creator page.
- From watch history entries, include “Resume” CTA to video detail at last position.
