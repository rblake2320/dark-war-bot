# Dark War Survival Bot - Python Implementation

This directory contains the actual Python bot implementation for automating Dark War Survival gameplay.

## Features

- **Template Matching**: Uses OpenCV for image recognition
- **Human-like Behavior**: Bezier curve mouse movement, randomized timing
- **Anti-Detection**: Variance in actions, random breaks, mistake simulation
- **Multi-Task Support**: Resource gathering, building upgrades, troop training, and more
- **Configurable**: JSON-based configuration system
- **Window Detection**: Automatic BlueStacks/emulator window detection (Windows)
- **Logging**: Comprehensive logging with color support

## Quick Start

### 1. Install Dependencies

```bash
cd bot
pip install -r requirements.txt
```

### 2. Create Configuration

```bash
python main.py --create-config
```

This creates a `config.json` file with default settings.

### 3. Prepare Templates

Create template images for UI elements:

1. Take screenshots of game UI elements (buttons, icons)
2. Crop and save them as PNG files in `templates/` directory
3. Name them descriptively (e.g., `gather_btn.png`, `food_node.png`)

Required templates:
- `food_node.png` - Resource node on map
- `gather_btn.png` - Gather button
- `upgrade_btn.png` - Building upgrade button
- `confirm_btn.png` - Confirmation button
- `barracks.png` - Barracks building
- `train_btn.png` - Train troops button

### 4. Run the Bot

```bash
python main.py
```

Or with verbose logging:

```bash
python main.py --verbose
```

## Configuration

Edit `config.json` to customize bot behavior:

```json
{
  "bot_settings": {
    "base_interval": 60,        // Base time between actions (seconds)
    "variance": 0.3,            // ±30% randomization
    "template_threshold": 0.8,  // Image matching confidence (0-1)
    "enable_breaks": true,      // Enable random breaks
    "break_interval": 7200,     // Break every 2 hours
    "break_duration": 900       // 15 minute breaks
  },
  "tasks": {
    "gather_resources": {
      "enabled": true,
      "weight": 0.5,            // 50% chance to execute
      "interval": 45
    },
    "upgrade_building": {
      "enabled": true,
      "weight": 0.3,
      "interval": 120
    }
  }
}
```

## Project Structure

```
bot/
├── core/
│   └── dark_war_bot.py      # Main bot implementation
├── utils/
│   └── window_utils.py      # Window detection utilities
├── config/
│   └── config_manager.py    # Configuration management
├── templates/               # Template images (create this)
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Usage Examples

### Detect Emulator Window

```bash
python main.py --detect-window
```

### Custom Configuration File

```bash
python main.py --config my_config.json
```

### Verbose Logging

```bash
python main.py --verbose
```

## Anti-Detection Features

The bot implements several anti-detection strategies:

1. **Randomized Timing**: Actions have ±30% variance by default
2. **Bezier Curve Movement**: Mouse moves along curved paths, not straight lines
3. **Random Breaks**: Simulates human breaks every 2 hours
4. **Click Offset**: Adds random offset to click positions
5. **Variable Speed**: Mouse movement speed varies randomly
6. **Task Weighting**: Different tasks have different probabilities

## Advanced Features

### Multi-Instance Support

To run multiple bot instances:

1. Edit `config.json`:
```json
{
  "multi_instance": {
    "enabled": true,
    "max_instances": 4,
    "instance_delay": 30
  }
}
```

2. Run multiple instances with different configs:
```bash
python main.py --config account1.json &
python main.py --config account2.json &
```

### Discord Notifications

Add Discord webhook for notifications:

```json
{
  "notifications": {
    "discord_webhook": "https://discord.com/api/webhooks/...",
    "notify_on_error": true,
    "notify_on_milestone": true,
    "milestone_interval": 100
  }
}
```

## Troubleshooting

### Template Matching Fails

**Problem**: Bot can't find UI elements

**Solutions**:
- Re-capture templates at current screen resolution
- Adjust `template_threshold` (try 0.7-0.9)
- Ensure game UI hasn't changed
- Check template file names match code

### Window Not Detected

**Problem**: "Emulator window not detected"

**Solutions**:
- Make sure BlueStacks/emulator is running
- Try running as administrator (Windows)
- Install `pywin32`: `pip install pywin32`
- Manually specify window title in code

### High CPU Usage

**Problem**: Bot uses too much CPU

**Solutions**:
- Increase `base_interval` in config
- Add delays between screen captures
- Reduce screenshot frequency
- Close unnecessary programs

### Bot Detected

**Problem**: Account banned or flagged

**Solutions**:
- Increase `variance` to 0.4-0.5
- Enable longer breaks
- Reduce daily playtime
- Use farm accounts only
- Don't bot in competitive alliances

## Safety Guidelines

⚠️ **Important**: Using automation bots violates most game Terms of Service

- **Use at your own risk** - Account bans are possible
- **Test on farm accounts** first
- **Don't bot in PvP-heavy environments**
- **Vary your patterns** - Don't run 24/7
- **Stay updated** - Game updates may break templates

## Performance Tips

For optimal performance on high-end systems (RTX 5090 + 128GB RAM):

1. Run 4-6 instances simultaneously
2. Allocate 4GB RAM per BlueStacks instance
3. Use hardware virtualization (VT-x/AMD-V)
4. Set BlueStacks to 1920x1080 resolution
5. Disable unnecessary BlueStacks features

## Contributing

Improvements welcome! Areas for contribution:

- Additional task automation
- OCR integration for text reading
- Reinforcement learning for decision-making
- Better anti-detection algorithms
- Mobile emulator support (Android Studio, etc.)

## License

See main project LICENSE file (MIT)

## Support

For issues or questions:
- Check main project README
- Review troubleshooting section above
- Open GitHub issue with logs

---

**Disclaimer**: This bot is for educational purposes. Use responsibly and at your own risk.
