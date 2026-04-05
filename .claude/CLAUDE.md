# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run dev server (port 5001, debug mode)
python app.py

# Run tests
pytest
```

No build step or linter is configured.

## Architecture

**Stack**: Flask 3.1.3 (Python) + Jinja2 templates + Vanilla JS + SQLite

This is a server-side rendered app. Flask routes in `app.py` render Jinja2 templates directly — no API layer, no frontend framework, no build process.

**Template inheritance**: All pages extend `templates/base.html`, which provides the navbar, footer, and blocks (`title`, `head`, `content`, `scripts`). Page-specific CSS is loaded via the `head` block.

**Database**: `database/db.py` is the module for SQLite integration (not yet implemented). The db file is `expense_tracker.db` (gitignored).

**Client-side JS**: `static/js/main.js` is a placeholder. Any page-specific JS lives inline in template `{% block scripts %}` blocks (see the YouTube modal in `landing.html`).

## Design System

CSS custom properties are defined in `:root` in `static/css/style.css`. Use these variables for colors, spacing, and typography rather than hardcoding values. Page-specific styles go in a new `static/css/<page>.css` file, loaded via the template `head` block.

## Project Status

Many routes in `app.py` are stubs (return placeholder strings). Implementation is planned incrementally: auth backend → user profile → expense CRUD. The `file.txt` in the root tracks the implementation roadmap.
