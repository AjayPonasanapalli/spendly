# Spec: Registration

## Overview
Implement user registration so new visitors can create a Spendly account. This step wires up the existing `POST /register` form (the template and GET route already exist) to validate input, reject duplicate emails, hash the password, insert the user into the database, and redirect to the login page on success. It also configures `app.secret_key` so Flask's flash/session machinery is available for this and all future steps.

## Depends on
- Step 01 — Database Setup (users table must exist, `get_db()` must work)

## Routes
- `GET /register` — render registration form — public *(already exists, no change needed)*
- `POST /register` — validate form, insert user, redirect — public *(new handler)*

## Database changes
No new tables or columns. Uses the existing `users` table:
- `name` TEXT NOT NULL
- `email` TEXT UNIQUE NOT NULL
- `password_hash` TEXT NOT NULL
- `created_at` TEXT DEFAULT (datetime('now'))

## Templates
- **Modify:** `templates/register.html`
  - Re-render the form with the submitted `name` and `email` values preserved on error (sticky inputs)
  - Pass `error` variable for validation/duplicate-email messages (slot already exists in template)

## Files to change
- `app.py`
  - Add `app.secret_key` (use `os.urandom(24)` for dev; note it must be a fixed value in production)
  - Add `request` to Flask imports
  - Convert the `register` view to handle both GET and POST (`methods=["GET", "POST"]`)
  - On POST: validate → insert → redirect to `/login`

## Files to create
- None

## New dependencies
No new dependencies. Uses:
- `werkzeug.security.generate_password_hash` (already installed)
- `flask.request`, `flask.redirect`, `flask.url_for` (already in Flask)

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — no string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate server-side (do not rely solely on HTML `required`):
  - `name` must not be blank
  - `email` must not be blank
  - `password` must be at least 8 characters
- Catch `sqlite3.IntegrityError` to detect duplicate email — show user-friendly message
- On success: `redirect(url_for('login'))` — do not auto-login the user (that is Step 3)
- Close the DB connection in a `finally` block or use a `with` statement

## Definition of done
- [ ] `GET /register` renders the form (unchanged behaviour)
- [ ] Submitting the form with valid, unique data inserts a new row in `users` and redirects to `/login`
- [ ] The inserted password is stored as a hash, never plaintext
- [ ] Submitting with a duplicate email re-renders the form with the message "An account with that email already exists."
- [ ] Submitting with a password shorter than 8 characters re-renders with "Password must be at least 8 characters."
- [ ] Submitting with a blank name re-renders with "Name is required."
- [ ] Name and email fields retain their values after a failed submission
- [ ] App starts without errors after adding `secret_key`
