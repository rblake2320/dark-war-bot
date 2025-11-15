# Development Guide

This guide provides detailed information for developers working on the Dark War Survival Bot project.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Development Workflow](#development-workflow)
- [Architecture Overview](#architecture-overview)
- [Code Organization](#code-organization)
- [Styling Guide](#styling-guide)
- [Component Development](#component-development)
- [State Management](#state-management)
- [Routing](#routing)
- [Build and Deployment](#build-and-deployment)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin development, ensure you have:

- **Node.js**: Version 22.x or higher
- **pnpm**: Version 8.x or higher (recommended package manager)
- **Git**: For version control
- **Code Editor**: VS Code recommended with the following extensions:
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense
  - TypeScript and JavaScript Language Features

## Project Setup

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/dark-war-bot.git
cd dark-war-bot

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

### Available Commands

```bash
pnpm dev          # Start development server (http://localhost:3000)
pnpm build        # Build for production
pnpm preview      # Preview production build
pnpm lint         # Run ESLint
pnpm type-check   # Run TypeScript type checking
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following the project's coding standards
- Test your changes locally
- Ensure no TypeScript errors

### 3. Commit Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Architecture Overview

### Technology Stack

- **Frontend**: React 19 with TypeScript
- **Styling**: Tailwind CSS 4 with custom theme
- **UI Components**: shadcn/ui
- **Routing**: Wouter (lightweight alternative to React Router)
- **Build Tool**: Vite
- **Package Manager**: pnpm

### Project Structure

```
dark-war-bot/
├── client/                    # Frontend application
│   ├── public/               # Static assets
│   │   ├── robot-logo.png   # App logo
│   │   ├── hero-bg.jpg      # Hero background
│   │   ├── bot-config.png   # Bot config screenshot
│   │   └── bot-accounts.png # Account management screenshot
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   │   ├── ui/         # shadcn/ui components
│   │   │   └── ...
│   │   ├── pages/          # Page components
│   │   │   ├── Home.tsx    # Landing page
│   │   │   ├── BotDemo.tsx # Interactive demo
│   │   │   └── NotFound.tsx
│   │   ├── contexts/       # React contexts
│   │   │   └── ThemeContext.tsx
│   │   ├── hooks/          # Custom hooks
│   │   ├── lib/            # Utility functions
│   │   ├── App.tsx         # Main app component
│   │   ├── const.ts        # Constants
│   │   ├── main.tsx        # Entry point
│   │   └── index.css       # Global styles
│   └── index.html
├── .github/                 # GitHub configuration
│   ├── workflows/          # CI/CD workflows
│   └── ISSUE_TEMPLATE/     # Issue templates
└── ...
```

## Code Organization

### Component Structure

Each component should follow this pattern:

```typescript
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface MyComponentProps {
  title: string;
  onAction?: () => void;
}

export default function MyComponent({ title, onAction }: MyComponentProps) {
  const [state, setState] = useState(false);

  return (
    <div className="container">
      <h1>{title}</h1>
      <Button onClick={onAction}>Click me</Button>
    </div>
  );
}
```

### File Naming Conventions

- **Components**: PascalCase (e.g., `BotDemo.tsx`, `FeatureCard.tsx`)
- **Utilities**: camelCase (e.g., `formatDate.ts`, `apiClient.ts`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_URL`, `MAX_RETRIES`)

## Styling Guide

### Tailwind CSS

This project uses Tailwind CSS 4 with a custom dark theme.

#### Color Palette

The theme uses OKLCH color space for better color consistency:

```css
/* Primary purple accent */
--primary: oklch(0.65 0.25 285);

/* Dark background */
--background: oklch(0.141 0.005 285.823);

/* Card background */
--card: oklch(0.21 0.006 285.885);
```

#### Common Patterns

```tsx
// Container with responsive padding
<div className="container mx-auto px-4">

// Card with border
<div className="bg-card rounded-lg border border-border p-6">

// Button with primary color
<Button className="bg-primary hover:bg-primary/90">

// Responsive grid
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

// Text colors
<p className="text-foreground">       // Main text
<p className="text-muted-foreground">  // Secondary text
<p className="text-primary">           // Accent text
```

### Custom Utilities

The project includes custom Tailwind utilities:

```css
/* Auto-centered container with responsive padding */
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}
```

## Component Development

### Using shadcn/ui Components

Import pre-built components from `@/components/ui/`:

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
```

### Creating New Components

1. Create component file in `client/src/components/`
2. Define TypeScript interfaces for props
3. Use functional components with hooks
4. Export as default

Example:

```tsx
// client/src/components/FeatureCard.tsx
interface FeatureCardProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
}

export default function FeatureCard({ title, description, icon }: FeatureCardProps) {
  return (
    <div className="bg-card rounded-lg border border-border p-6">
      {icon && <div className="mb-4">{icon}</div>}
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
}
```

## State Management

### Local State

Use React hooks for component-level state:

```tsx
const [isActive, setIsActive] = useState(false);
const [count, setCount] = useState(0);
```

### Context API

For global state, use React Context:

```tsx
// contexts/MyContext.tsx
import { createContext, useContext, useState } from "react";

const MyContext = createContext<MyContextType | undefined>(undefined);

export function MyProvider({ children }: { children: React.ReactNode }) {
  const [value, setValue] = useState<string>("");
  
  return (
    <MyContext.Provider value={{ value, setValue }}>
      {children}
    </MyContext.Provider>
  );
}

export function useMyContext() {
  const context = useContext(MyContext);
  if (!context) throw new Error("useMyContext must be used within MyProvider");
  return context;
}
```

## Routing

The project uses Wouter for routing:

```tsx
// App.tsx
import { Route, Switch } from "wouter";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Home} />
      <Route path="/demo" component={BotDemo} />
      <Route path="/404" component={NotFound} />
      <Route component={NotFound} />
    </Switch>
  );
}
```

### Navigation

```tsx
import { Link } from "wouter";

// Using Link component
<Link href="/demo">Go to Demo</Link>

// Using anchor tag
<a href="/demo">Go to Demo</a>
```

## Build and Deployment

### Development Build

```bash
pnpm dev
```

Runs on `http://localhost:3000` with hot module replacement.

### Production Build

```bash
pnpm build
```

Outputs to `client/dist/` directory.

### Preview Production Build

```bash
pnpm preview
```

### Deployment Options

The project can be deployed to:
- **Vercel**: `vercel deploy`
- **Netlify**: `netlify deploy --dir=client/dist`
- **GitHub Pages**: Configure in repository settings
- **Any static hosting**: Upload `client/dist/` contents

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Kill process on port 3000
npx kill-port 3000

# Or use a different port
pnpm dev --port 3001
```

#### TypeScript Errors

```bash
# Clear TypeScript cache
rm -rf node_modules/.cache

# Reinstall dependencies
pnpm install
```

#### Build Errors

```bash
# Clean build directory
rm -rf client/dist

# Rebuild
pnpm build
```

#### Styling Not Applied

- Check if Tailwind classes are correct
- Ensure `index.css` is imported in `main.tsx`
- Clear browser cache
- Check for conflicting CSS

### Getting Help

- Check [GitHub Issues](https://github.com/yourusername/dark-war-bot/issues)
- Review [CONTRIBUTING.md](CONTRIBUTING.md)
- Contact: support@lssbot.com

## Best Practices

### Performance

- Use lazy loading for routes
- Optimize images (use WebP format)
- Minimize bundle size
- Use production builds for deployment

### Accessibility

- Use semantic HTML
- Add ARIA labels where needed
- Ensure keyboard navigation works
- Test with screen readers

### Security

- Never commit `.env` files
- Validate all user inputs
- Use HTTPS in production
- Keep dependencies updated

### Code Quality

- Write meaningful commit messages
- Add comments for complex logic
- Keep functions small and focused
- Write reusable components

---

Happy coding! 🚀
