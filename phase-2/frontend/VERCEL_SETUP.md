# Vercel Deployment Setup

## Environment Variables

Add these environment variables in **Vercel Dashboard → Settings → Environment Variables**:

### Required Variables:

```bash
# Authentication
BETTER_AUTH_SECRET="your-jwt-secret-here"
BETTER_AUTH_URL="https://your-domain.vercel.app"

# Backend API
NEXT_PUBLIC_API_URL="https://your-backend-url.com"

# Database (if using PostgreSQL)
DATABASE_URL="postgresql://user:password@host:port/database"

# Build Configuration
TURBOPACK=0
```

### Important Notes:

1. **TURBOPACK=0**: This forces Vercel to use webpack instead of Turbopack for better module resolution compatibility.

2. **BETTER_AUTH_SECRET**: Generate a strong random string (minimum 32 characters).
   ```bash
   # Generate using:
   openssl rand -base64 32
   ```

3. **BETTER_AUTH_URL**: Update this to your actual Vercel deployment URL after first deploy.

4. **NEXT_PUBLIC_API_URL**: Your FastAPI backend URL (must be publicly accessible).

## Build Settings

Vercel automatically detects Next.js projects. Default settings:

- **Framework Preset**: Next.js
- **Build Command**: `next build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

These are configured in `vercel.json` if you need to customize.

## Troubleshooting

### Module Resolution Errors (`Can't resolve '@/lib/...'`)

**Solution**: Ensure `TURBOPACK=0` is set in environment variables.

**Why**: Turbopack has different path resolution behavior. We use `jsconfig.json` and `tsconfig.json` with `baseUrl: "."` for proper alias resolution.

### Build Fails Locally But Not on Vercel (or vice versa)

1. Delete `.next` folder: `rm -rf .next`
2. Clear node_modules: `rm -rf node_modules && npm install`
3. Test build: `npm run build`

### Authentication Issues

1. Verify `BETTER_AUTH_URL` matches your deployment URL
2. Ensure `BETTER_AUTH_SECRET` is the same across all environments
3. Check that backend API is accessible from Vercel

## Deployment Checklist

- [ ] Set all required environment variables in Vercel Dashboard
- [ ] Update `BETTER_AUTH_URL` to actual deployment URL
- [ ] Verify backend API is publicly accessible
- [ ] Test authentication flow after deployment
- [ ] Check browser console for CORS errors
- [ ] Verify API calls are reaching backend

## Local Development

For local development, use `.env.local` (never commit this file):

```bash
# .env.local
BETTER_AUTH_SECRET="local-dev-secret"
BETTER_AUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000"
DATABASE_URL="postgresql://localhost:5432/todoapp"
```
