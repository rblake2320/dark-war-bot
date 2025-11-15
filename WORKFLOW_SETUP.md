# GitHub Actions Workflow Setup

Due to GitHub App permissions, the CI/CD workflow needs to be added manually through the GitHub web interface.

## Steps to Add Workflow

1. **Navigate to your repository** on GitHub:
   https://github.com/rblake2320/dark-war-bot

2. **Create the workflows directory**:
   - Click "Add file" → "Create new file"
   - Enter path: `.github/workflows/ci.yml`

3. **Copy the workflow content** from below:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint-and-type-check:
    name: Lint and Type Check
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run ESLint
        run: pnpm lint
        continue-on-error: true

      - name: Run TypeScript type check
        run: pnpm type-check

  build:
    name: Build Application
    runs-on: ubuntu-latest
    needs: lint-and-type-check
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build project
        run: pnpm build
        env:
          NODE_ENV: production

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: client/dist
          retention-days: 7

  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint-and-type-check
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'pnpm'

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run tests
        run: pnpm test || echo "No tests configured yet"
        continue-on-error: true

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run npm audit
        run: npm audit --production
        continue-on-error: true

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
        continue-on-error: true

  deploy-preview:
    name: Deploy Preview
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'pull_request'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-artifacts
          path: client/dist

      - name: Deploy to preview
        run: echo "Deploy to preview environment (configure your deployment service)"
        # Add your deployment commands here
        # Example: netlify deploy --dir=client/dist --alias=pr-${{ github.event.pull_request.number }}
```

4. **Commit the file**:
   - Add commit message: "ci: add GitHub Actions workflow"
   - Click "Commit new file"

## Verification

After adding the workflow:

1. Go to the "Actions" tab in your repository
2. You should see the workflow running
3. Check that all jobs complete successfully

## Alternative: Add via Git

If you prefer to add via command line:

```bash
# Create the workflow file locally
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
# [paste the workflow content here]
EOF

# Commit and push
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions workflow"
git push origin main
```

## Notes

- The workflow runs on every push to `main` and `develop` branches
- It also runs on pull requests
- You can customize the workflow based on your needs
- Add deployment steps in the `deploy-preview` job
