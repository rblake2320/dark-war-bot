# Dark War Survival Bot 🤖

A modern, feature-rich automation bot website for Dark War Survival game with an interactive demo interface. Built with React 19, TypeScript, and Tailwind CSS 4.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-19-61dafb.svg)](https://reactjs.org/)

## ✨ Features

### 🆕 Enhanced Version Features

This enhanced fork includes:
- **Full Python Bot Implementation**: Complete working bot with OpenCV and PyAutoGUI
- **Anti-Detection Strategies**: Bezier curve movement, timing randomization, break simulation
- **Multi-Instance Support**: Run multiple accounts simultaneously
- **Comprehensive Documentation**: Implementation guides, anti-detection strategies, troubleshooting
- **Configuration System**: JSON-based configuration with validation
- **Window Detection**: Automatic BlueStacks/emulator window detection
- **Logging System**: Detailed logging with color support

### Website Features
- **Modern Dark Theme**: Sleek dark interface with purple accent colors
- **Responsive Design**: Fully responsive layout that works on all devices
- **Interactive Demo**: Live bot simulation with real-time activity logging
- **Feature Showcase**: Comprehensive display of all bot capabilities
- **Smooth Animations**: Enhanced user experience with smooth scrolling and transitions

### Bot Capabilities

The Dark War Survival Bot automates 21+ game tasks including:

- **Resource Management**: Building upgrades, resource gathering, inventory management
- **Combat Operations**: Troop training, healing, monster attacks, arena battles
- **Alliance Activities**: Alliance tasks, survivor assignments, rally hosting
- **Progression**: Research, hero recruitment, exploration missions
- **Economy**: Black market, shop rewards, task/battle/mail rewards
- **Protection**: Automatic shield activation

## 🚀 Quick Start

### Website Development

For website development:

### Prerequisites

- Node.js 22.x or higher
- pnpm (recommended) or npm

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dark-war-bot.git

# Navigate to project directory
cd dark-war-bot

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

The application will be available at `http://localhost:3000`

### Python Bot Usage

For running the actual automation bot:

```bash
# Navigate to bot directory
cd bot

# Install Python dependencies
pip install -r requirements.txt

# Create configuration
python main.py --create-config

# Run the bot
python main.py
```

See [Bot Implementation Guide](docs/guides/BOT_IMPLEMENTATION_GUIDE.md) for detailed instructions.

### Build for Production

```bash
# Create production build
pnpm build

# Preview production build
pnpm preview
```

## 📁 Project Structure

```
dark-war-bot/
├── bot/                    # Python bot implementation (NEW)
│   ├── core/              # Main bot logic
│   ├── utils/             # Utility modules
│   ├── config/            # Configuration management
│   ├── templates/         # UI template images
│   ├── main.py            # Entry point
│   ├── requirements.txt   # Python dependencies
│   └── README.md          # Bot documentation
├── docs/                   # Documentation (NEW)
│   └── guides/            # Implementation guides
├── client/                 # Frontend application
│   ├── public/            # Static assets
│   │   ├── robot-logo.png
│   │   ├── hero-bg.jpg
│   │   ├── bot-config.png
│   │   └── bot-accounts.png
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   │   ├── Home.tsx   # Landing page
│   │   │   ├── BotDemo.tsx # Interactive demo
│   │   │   └── NotFound.tsx
│   │   ├── contexts/      # React contexts
│   │   ├── hooks/         # Custom hooks
│   │   ├── lib/           # Utility functions
│   │   ├── App.tsx        # Main app component
│   │   ├── const.ts       # Constants
│   │   └── index.css      # Global styles
│   └── index.html
├── server/                # Placeholder for compatibility
├── shared/                # Shared constants
├── BOT_README.md          # Bot documentation
├── CHANGELOG.md           # Version history
├── CONTRIBUTING.md        # Contribution guidelines
└── README.md              # This file
```

## 🎨 Technology Stack

- **Frontend Framework**: React 19 with TypeScript
- **Styling**: Tailwind CSS 4 with custom dark theme
- **UI Components**: shadcn/ui component library
- **Routing**: Wouter for lightweight client-side routing
- **Build Tool**: Vite for fast development and optimized builds
- **Icons**: Lucide React for modern iconography

## 🛠️ Development

### Available Scripts

```bash
pnpm dev          # Start development server
pnpm build        # Build for production
pnpm preview      # Preview production build
pnpm lint         # Run ESLint
pnpm type-check   # Run TypeScript type checking
```

### Environment Variables

The project uses environment variables for configuration. See `.env.example` for available options:

```env
VITE_APP_TITLE=Dark War Survival Bot
VITE_APP_LOGO=/robot-logo.png
```

### Code Style

This project uses:
- **ESLint** for code linting
- **TypeScript** for type safety
- **Prettier** for code formatting (recommended)

## 🎯 Key Pages

### Home Page (`/`)
The main landing page featuring:
- Hero section with video demo placeholder
- Feature highlights
- Bot configuration previews
- Multi-account management showcase
- Comprehensive feature table
- Footer with links and contact information

### Bot Demo (`/demo`)
Interactive demonstration page with:
- Configurable bot features
- Start/Stop controls
- Real-time activity logging
- Status indicators
- Feature descriptions

## 🔧 Customization

### Theme Colors

The color scheme is defined in `client/src/index.css` using OKLCH color space:

```css
--primary: oklch(0.65 0.25 285);  /* Purple accent */
--background: oklch(0.141 0.005 285.823);  /* Dark background */
```

### Logo

Update the logo by replacing `/client/public/robot-logo.png` and updating the constant in `client/src/const.ts`:

```typescript
export const APP_LOGO = "/robot-logo.png";
```

## 📝 Future Enhancements

Potential features to add:
- User authentication system
- Real video content integration
- Download system for Windows bot
- User dashboard with saved configurations
- Analytics and usage tracking
- Multi-language support
- API integration for real bot control

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Design inspired by [lssbot.com](https://www.lssbot.com)
- UI components from [shadcn/ui](https://ui.shadcn.com)
- Icons from [Lucide](https://lucide.dev)

## 📧 Contact

For questions or support, please contact: support@lssbot.com

---

**Note**: This is a demonstration website showcasing bot capabilities. The actual bot would be a separate Windows application.

Made with ❤️ by the LSS Bot Team
