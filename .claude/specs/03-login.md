# Spec: Login

## Overview
Implement session-based login and logout so registered users can authenticate and access protected pages. This step wires up the existing `POST /login` form to validate credentials, start a Flask session on success, and redirect to the dashboard (placeholder for now). It also implements `GET /logout` to clear the session and redirect to the landing page. After this step, the app knows who is logged in across requests.

## Depends on
- Step 01 — Database Setup (`get_db`, `users` table)
- Step 02 — Registration (`get_user_by_email` helper, hashed passwords in DB)

## Routes
- `GET /login` — render login form — public *(already exists, no change needed)*
- `POST /login` — validate credentials, set session, redirect — public *(new handler)*
- `GET /logout` — clear session, redirect to `/` — logged-in *(stub exists, needs implementation)*

## Database changes
No database changes. Reads from the existing `users` table via `get_user_by_email`.

## Templates
- **Modify:** `templates/login.html`
  - Preserve the submitted `email` value on failed login (sticky input)
  - Pass `error` variable for invalid-credential messages (slot already exists in template)

## Files to change
- `app.py`
  - Add `session` to the Flask imports
  - Convert the `login` view to handle both GET and POST (`methods=["GET", "POST"]`)
  - On POST: look up user → verify password → set session → redirect
  - Implement the `logout` view: clear session → redirect to `url_for('landing')`

## Files to create
- None

## New dependencies
No new pip packages. Uses:
- `flask.session` (already in Flask)
- `werkzeug.security.check_password_hash` (already installed)

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()` / `get_user_by_email()`
- Parameterised queries only — no string formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use a single generic error for both "email not found" and "wrong password": `"Invalid email or password."` — do not reveal which field is wrong
- Store only `user_id` and `user_name` in the session — never store the password hash
- `session.clear()` on logout — do not manually delete individual keys
- After successful login redirect to `url_for('profile')` (placeholder route already exists)

## Definition of done
- [ ] `GET /login` renders the form (unchanged behaviour)
- [ ] Valid credentials set `session['user_id']` and `session['user_name']` and redirect to `/profile`
- [ ] Wrong password re-renders the form with `"Invalid email or password."` and sticky email
- [ ] Unknown email re-renders the form with `"Invalid email or password."` and sticky email
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] Visiting `/logout` without being logged in still works without error (session.clear() is safe on empty session)
