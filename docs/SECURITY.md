# Security Architecture

## 1. Secrets Management
- No secrets committed to source control (`.env` strictly git-ignored).
- `.env.example` provides the template.
- Frontend receives ZERO API keys; only public Supabase URL/Anon keys.

## 2. CORS & CSRF
- `FRONTEND_ORIGIN` enforced tightly. No wildcards (`*`) when handling credentials.

## 3. JWT & Authorization
- Supabase Auth handles identity.
- Backend middleware verifies JWT signatures and enforces server-side Role Based Access Control (RBAC).

## 4. Database Security
- Row Level Security (RLS) is explicitly enabled on all user-owned tables (`user_profiles`, `watchlists`, `alerts`).
