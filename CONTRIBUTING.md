# Contributing to Dark War Survival Bot

Thank you for your interest in contributing to the Dark War Survival Bot project! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Node.js 22.x or higher
- pnpm (recommended) or npm
- Git

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/dark-war-bot.git
   cd dark-war-bot
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/dark-war-bot.git
   ```
4. **Install dependencies**:
   ```bash
   pnpm install
   ```
5. **Start development server**:
   ```bash
   pnpm dev
   ```

## Development Process

### Branching Strategy

- `main` - Production-ready code
- `develop` - Development branch for integration
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

### Creating a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes in your feature branch
2. Test your changes thoroughly
3. Ensure code follows the project's coding standards
4. Update documentation if necessary

### Testing

Before submitting your changes:

```bash
# Run type checking
pnpm type-check

# Run linting
pnpm lint

# Build the project
pnpm build
```

## Pull Request Process

### Before Submitting

- [ ] Code follows the project's coding standards
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages follow the commit guidelines
- [ ] Branch is up to date with the base branch

### Submitting a Pull Request

1. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what changed and why
   - Reference to any related issues
   - Screenshots (if applicable)

3. **Wait for review** - maintainers will review your PR and may request changes

4. **Address feedback** - make requested changes and push updates

5. **Merge** - once approved, your PR will be merged

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Screenshots (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

## Coding Standards

### TypeScript

- Use TypeScript for all new code
- Define proper types and interfaces
- Avoid using `any` type
- Use meaningful variable and function names

### React

- Use functional components with hooks
- Keep components small and focused
- Use proper prop types
- Implement error boundaries where appropriate

### Styling

- Use Tailwind CSS utility classes
- Follow the existing color scheme (dark theme with purple accents)
- Ensure responsive design for all screen sizes
- Use semantic HTML elements

### File Organization

- Place components in `client/src/components/`
- Place pages in `client/src/pages/`
- Place utilities in `client/src/lib/`
- Keep files focused on a single responsibility

### Code Style

```typescript
// Good
interface BotFeature {
  id: string;
  name: string;
  enabled: boolean;
}

const MyComponent: React.FC = () => {
  const [isActive, setIsActive] = useState(false);
  
  return (
    <div className="container mx-auto">
      {/* Component content */}
    </div>
  );
};

// Avoid
const MyComponent = () => {
  let active = false; // Use const and proper naming
  
  return <div style={{margin: 'auto'}}> // Use Tailwind classes
    ...
  </div>;
};
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(demo): add real-time activity logging
fix(home): correct responsive layout on mobile
docs(readme): update installation instructions
style(components): format code with prettier
refactor(hooks): simplify state management
```

### Best Practices

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Keep the first line under 72 characters
- Reference issues and PRs in the footer

## Questions?

If you have questions about contributing, please:
- Check existing issues and discussions
- Create a new issue with the "question" label
- Contact the maintainers at support@lssbot.com

Thank you for contributing to Dark War Survival Bot! 🎉
