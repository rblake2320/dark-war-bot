# Deployment Guide

This guide covers deploying the Dark War Survival Bot website to various platforms.

## Prerequisites

- Node.js 22.x or higher
- pnpm 10.x or higher
- Git

## Environment Variables

The application requires the following environment variables:

```env
# Required
VITE_APP_TITLE=Dark War Survival Bot
VITE_APP_LOGO=/robot-logo.png

# Optional - Analytics (Umami)
VITE_ANALYTICS_ENDPOINT=
VITE_ANALYTICS_WEBSITE_ID=

# Server Configuration
PORT=3000
NODE_ENV=production
```

Create a `.env` file in the project root with these variables. See `.env.example` for reference.

## Building for Production

1. Install dependencies:
```bash
pnpm install
```

2. Run type checking:
```bash
pnpm check
```

3. Build the application:
```bash
pnpm build
```

This creates:
- `dist/public/` - Frontend static files
- `dist/index.js` - Production server

## Running in Production

Start the production server:

```bash
pnpm start
```

Or directly:
```bash
NODE_ENV=production node dist/index.js
```

The server will:
- Serve static files from `dist/public`
- Handle client-side routing
- Provide a health check endpoint at `/api/health`
- Use port 3000 by default (configurable via PORT env var)

## Health Check

The application provides a health check endpoint for monitoring:

```bash
curl http://localhost:3000/api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-15T17:35:57.482Z",
  "environment": "production"
}
```

## Platform-Specific Deployments

### Docker

Create a `Dockerfile`:

```dockerfile
FROM node:22-alpine

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm@10

# Copy package files
COPY package.json pnpm-lock.yaml ./
COPY patches ./patches

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build application
RUN pnpm build

# Expose port
EXPOSE 3000

# Set environment
ENV NODE_ENV=production

# Start server
CMD ["node", "dist/index.js"]
```

Build and run:
```bash
docker build -t dark-war-bot .
docker run -p 3000:3000 -e PORT=3000 dark-war-bot
```

### Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

Note: Configure build settings in `vercel.json`:
```json
{
  "buildCommand": "pnpm build",
  "outputDirectory": "dist/public",
  "installCommand": "pnpm install"
}
```

### Netlify

1. Build command: `pnpm build`
2. Publish directory: `dist/public`
3. Add environment variables in Netlify dashboard

### Railway / Render

1. Connect your Git repository
2. Set build command: `pnpm install && pnpm build`
3. Set start command: `pnpm start`
4. Add environment variables
5. Deploy

### Traditional VPS (Ubuntu/Debian)

1. Install Node.js 22.x and pnpm:
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
npm install -g pnpm
```

2. Clone and build:
```bash
git clone <your-repo-url>
cd dark-war-bot
pnpm install
pnpm build
```

3. Create systemd service (`/etc/systemd/system/dark-war-bot.service`):
```ini
[Unit]
Description=Dark War Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/dark-war-bot
Environment=NODE_ENV=production
Environment=PORT=3000
ExecStart=/usr/bin/node dist/index.js
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

4. Enable and start:
```bash
sudo systemctl enable dark-war-bot
sudo systemctl start dark-war-bot
```

5. Set up Nginx reverse proxy:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Security Considerations

The server includes several security features:

1. **Security Headers**
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY
   - X-XSS-Protection: 1; mode=block
   - Referrer-Policy: strict-origin-when-cross-origin

2. **Static File Caching**
   - Production: 1 year cache
   - Development: No cache

3. **Error Handling**
   - Graceful shutdown on SIGTERM/SIGINT
   - Uncaught exception handling
   - Unhandled rejection handling

4. **Request Logging**
   - Enabled in production mode
   - Logs timestamp, method, and path

## Monitoring

Monitor the application using:

1. **Health Check Endpoint**
   ```bash
   curl http://localhost:3000/api/health
   ```

2. **Server Logs**
   - Production logs include request logging
   - Check for errors in stderr

3. **Process Monitoring**
   - Use PM2 or systemd for process management
   - Set up alerts for crashes/restarts

## Troubleshooting

### Build Fails

1. Clear cache and rebuild:
```bash
rm -rf node_modules dist
pnpm install
pnpm build
```

2. Verify Node.js version:
```bash
node --version  # Should be 22.x or higher
```

### Server Won't Start

1. Check port availability:
```bash
lsof -i :3000
```

2. Verify build output:
```bash
ls -la dist/
```

3. Check environment variables:
```bash
echo $NODE_ENV
```

### Analytics Not Working

1. Verify environment variables are set:
```bash
echo $VITE_ANALYTICS_ENDPOINT
echo $VITE_ANALYTICS_WEBSITE_ID
```

2. Analytics are optional - leave empty to disable

## Updating the Application

1. Pull latest changes:
```bash
git pull
```

2. Install dependencies:
```bash
pnpm install
```

3. Rebuild:
```bash
pnpm build
```

4. Restart server:
```bash
# For systemd
sudo systemctl restart dark-war-bot

# For PM2
pm2 restart dark-war-bot

# Manual
# Kill current process and run: pnpm start
```

## Performance Optimization

1. **Enable Compression** (if not using reverse proxy):
   - Add compression middleware to server
   - Nginx/Apache will handle this in production

2. **CDN Integration**:
   - Serve static assets via CDN
   - Update asset URLs in build configuration

3. **Database Optimization** (if added):
   - Use connection pooling
   - Add appropriate indexes
   - Cache frequently accessed data

## Support

For issues or questions:
- GitHub Issues: [Your repo URL]
- Email: support@lssbot.com
- Documentation: [Your docs URL]
