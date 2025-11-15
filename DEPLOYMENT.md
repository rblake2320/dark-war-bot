# Deployment Guide

This guide covers deploying the Dark War Survival Bot website to various platforms with production-ready configurations.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Build Process](#build-process)
3. [Platform-Specific Guides](#platform-specific-guides)
4. [Security Configuration](#security-configuration)
5. [Performance Optimization](#performance-optimization)
6. [Monitoring & Analytics](#monitoring--analytics)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- Node.js 18+ and pnpm
- Git repository access
- Environment variables configured

### Recommended
- Domain name
- SSL certificate (most platforms provide free)
- CDN setup (for static assets)

---

## Build Process

### Development Build
```bash
pnpm install
pnpm dev
```
Access at `http://localhost:3000`

### Production Build
```bash
pnpm install --prod
pnpm build
```

Output directory: `client/dist/`

### Build Verification
```bash
# Check build output
ls -lh client/dist/

# Test production build locally
pnpm preview
```

---

## Platform-Specific Guides

### 1. Vercel (Recommended for Static Sites)

**Automatic Deployment**:
1. Connect GitHub repository to Vercel
2. Configure build settings:
   - Framework: Vite
   - Root Directory: `./`
   - Build Command: `pnpm build`
   - Output Directory: `client/dist`
3. Add environment variables in Vercel dashboard
4. Deploy

**Security Headers** (`vercel.json`):
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Permissions-Policy",
          "value": "camera=(), microphone=(), geolocation=()"
        }
      ]
    }
  ]
}
```

---

### 2. Netlify

**Automatic Deployment**:
1. Connect GitHub repository
2. Build settings:
   - Build command: `pnpm build`
   - Publish directory: `client/dist`
3. Add environment variables
4. Deploy

**Security Headers** (`netlify.toml`):
```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"

[[headers]]
  for = "/*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.css"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

---

### 3. Cloudflare Pages

**Automatic Deployment**:
1. Connect GitHub repository
2. Build configuration:
   - Build command: `pnpm build`
   - Build output directory: `client/dist`
3. Deploy

**Security Headers** (`_headers` in `client/public/`):
```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/*.js
  Cache-Control: public, max-age=31536000, immutable

/*.css
  Cache-Control: public, max-age=31536000, immutable
```

---

### 4. GitHub Pages

**Manual Deployment**:
```bash
# Build
pnpm build

# Deploy to gh-pages branch
pnpm add -D gh-pages
npx gh-pages -d client/dist
```

**Automatic Deployment** (GitHub Actions):
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install pnpm
        run: npm install -g pnpm
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Build
        run: pnpm build
      
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./client/dist
```

---

### 5. Docker Deployment

**Dockerfile**:
```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source
COPY . .

# Build
RUN pnpm build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/client/dist /usr/share/nginx/html

# Copy nginx config with security headers
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf** (with security headers):
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

    # Caching for static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
```

**Build and run**:
```bash
docker build -t dark-war-bot .
docker run -p 8080:80 dark-war-bot
```

---

### 6. Traditional VPS (Ubuntu/Debian)

**Setup**:
```bash
# Install Node.js and pnpm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pnpm

# Install nginx
sudo apt-get install -y nginx

# Clone repository
git clone https://github.com/yourusername/dark-war-bot.git
cd dark-war-bot

# Build
pnpm install
pnpm build

# Copy to nginx directory
sudo cp -r client/dist/* /var/www/html/

# Configure nginx (use nginx.conf above)
sudo nano /etc/nginx/sites-available/default

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

---

## Security Configuration

### Content Security Policy (CSP)

Add to your platform's header configuration:
```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://analytics.yourdomain.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://api.yourdomain.com;
```

### HTTPS/SSL

**Vercel/Netlify/Cloudflare**: Automatic SSL
**Custom Domain**: Use Let's Encrypt:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Performance Optimization

### 1. Asset Optimization

**Images**:
- Use WebP format
- Compress with tools like ImageOptim
- Implement lazy loading

**Code Splitting**:
Already configured in Vite - automatic

**Minification**:
Automatic in production build

### 2. CDN Configuration

**Cloudflare CDN**:
1. Add site to Cloudflare
2. Update DNS records
3. Enable caching rules
4. Enable Brotli compression

### 3. Caching Strategy

**Static Assets**: 1 year
**HTML**: No cache (for SPA routing)
**API Responses**: Based on data freshness

---

## Monitoring & Analytics

### Analytics Setup

Already configured in `client/src/main.tsx`:
- Set `VITE_ANALYTICS_ENDPOINT`
- Set `VITE_ANALYTICS_WEBSITE_ID`

Supports Umami, Plausible, or similar privacy-focused analytics.

### Uptime Monitoring

**Recommended Services**:
- UptimeRobot (free)
- Pingdom
- StatusCake

**Health Check Endpoint**:
For static sites, monitor the main page:
```
https://yourdomain.com/
```

### Error Tracking

**Sentry Integration**:
```bash
pnpm add @sentry/react
```

Add to `client/src/main.tsx`:
```typescript
import * as Sentry from "@sentry/react";

if (import.meta.env.PROD) {
  Sentry.init({
    dsn: "YOUR_SENTRY_DSN",
    environment: "production",
  });
}
```

---

## Troubleshooting

### Build Fails

**Issue**: `pnpm build` fails
**Solution**:
```bash
# Clean and rebuild
rm -rf node_modules client/dist
pnpm install
pnpm build
```

### Blank Page After Deployment

**Issue**: Site shows blank page
**Solutions**:
1. Check browser console for errors
2. Verify base path in `vite.config.ts`
3. Check nginx/server routing for SPA
4. Verify environment variables

### 404 on Page Refresh

**Issue**: SPA routes return 404
**Solution**: Configure server to redirect all routes to `index.html`

**Vercel** (`vercel.json`):
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

**Netlify** (`netlify.toml`):
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Slow Load Times

**Solutions**:
1. Enable CDN
2. Optimize images
3. Enable compression (Gzip/Brotli)
4. Check bundle size: `pnpm build --analyze`

---

## Environment Variables

### Required Variables

See project settings in Manus dashboard for:
- `VITE_APP_TITLE`
- `VITE_APP_LOGO`
- `VITE_APP_ID`

### Optional Variables

- `VITE_ANALYTICS_ENDPOINT` - Analytics script URL
- `VITE_ANALYTICS_WEBSITE_ID` - Analytics site ID

---

## Post-Deployment Checklist

- [ ] Site loads correctly
- [ ] All pages accessible
- [ ] Mobile responsive
- [ ] Analytics tracking
- [ ] SSL certificate valid
- [ ] Security headers configured
- [ ] Performance score > 90 (Lighthouse)
- [ ] SEO meta tags present
- [ ] Favicon displays
- [ ] Social media previews work

---

## Support

For deployment issues:
1. Check platform-specific documentation
2. Review build logs
3. Test locally with `pnpm preview`
4. Check GitHub issues
5. Contact platform support

---

**Last Updated**: November 15, 2025
