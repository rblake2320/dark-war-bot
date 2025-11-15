# Dark War Survival Bot - Implementation Guide

This comprehensive guide walks you through implementing and running the Dark War Survival automation bot.

## Table of Contents

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Template Creation](#template-creation)
5. [Configuration](#configuration)
6. [Running the Bot](#running-the-bot)
7. [Anti-Detection Strategies](#anti-detection-strategies)
8. [Multi-Instance Setup](#multi-instance-setup)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

## Overview

The Dark War Survival Bot uses computer vision (OpenCV) and automation (PyAutoGUI) to play the game automatically. It recognizes UI elements through template matching and performs human-like actions.

### How It Works

1. **Screen Capture**: Takes screenshots of the game window
2. **Template Matching**: Finds UI elements (buttons, icons) using OpenCV
3. **Action Execution**: Clicks buttons with human-like mouse movement
4. **Task Management**: Cycles through configured tasks with randomization
5. **Anti-Detection**: Implements timing variance, breaks, and natural behavior

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 (64-bit)
- **CPU**: Intel i5 or AMD Ryzen 5
- **RAM**: 8GB
- **GPU**: Integrated graphics
- **Storage**: 5GB free space

### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **CPU**: Intel i7/i9 or AMD Ryzen 7/9
- **RAM**: 16GB+ (32GB for multi-instance)
- **GPU**: NVIDIA GTX 1060 or better
- **Storage**: 10GB+ SSD

### Optimal Setup (Multi-Instance)
- **CPU**: Intel i9-14900K or AMD Ryzen 9 7950X
- **RAM**: 64GB+ (128GB recommended)
- **GPU**: NVIDIA RTX 4070 or better
- **Storage**: NVMe SSD

## Installation

### Step 1: Install BlueStacks

1. Download [BlueStacks 5](https://www.bluestacks.com/) (latest version)
2. Run installer and follow prompts
3. Enable hardware virtualization in BIOS (VT-x/AMD-V)
4. Launch BlueStacks and complete setup
5. Install Dark War Survival from Play Store

**BlueStacks Configuration**:
- Resolution: 1920x1080 (Full HD)
- DPI: 240
- CPU Cores: 4
- RAM: 4GB per instance
- Graphics: DirectX or OpenGL (test both)

### Step 2: Install Python

1. Download [Python 3.11+](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
```bash
python --version
pip --version
```

### Step 3: Install Bot Dependencies

```bash
# Navigate to bot directory
cd dark-war-bot/bot

# Install required packages
pip install -r requirements.txt

# For Windows users (window detection)
pip install pywin32
```

### Step 4: Verify Installation

```bash
# Test window detection
python main.py --detect-window

# Create default configuration
python main.py --create-config
```

## Template Creation

Templates are PNG images of UI elements the bot needs to recognize.

### Required Templates

Create these templates in `bot/templates/` directory:

| Template File | Description | How to Capture |
|--------------|-------------|----------------|
| `food_node.png` | Food resource on map | Screenshot food icon on world map |
| `wood_node.png` | Wood resource on map | Screenshot wood icon on world map |
| `stone_node.png` | Stone resource on map | Screenshot stone icon on world map |
| `gather_btn.png` | Gather button | Screenshot "Gather" button |
| `upgrade_btn.png` | Upgrade button | Screenshot building upgrade button |
| `confirm_btn.png` | Confirmation button | Screenshot "Confirm" or "OK" button |
| `barracks.png` | Barracks building | Screenshot barracks icon |
| `train_btn.png` | Train troops button | Screenshot "Train" button |
| `research_btn.png` | Research button | Screenshot research button |
| `heal_btn.png` | Heal troops button | Screenshot "Heal" button |

### Template Creation Process

1. **Take Screenshot**:
   - Open Dark War Survival in BlueStacks
   - Navigate to the UI element
   - Press `Print Screen` or use Snipping Tool

2. **Crop Element**:
   - Open screenshot in image editor (Paint, GIMP, Photoshop)
   - Crop tightly around the UI element
   - Include some surrounding context
   - Save as PNG with exact filename

3. **Test Template**:
   ```python
   import cv2
   template = cv2.imread('templates/gather_btn.png')
   print(f"Template size: {template.shape}")
   cv2.imshow('Template', template)
   cv2.waitKey(0)
   ```

### Template Best Practices

- **Resolution**: Match your BlueStacks resolution (1920x1080)
- **Format**: Always use PNG (lossless)
- **Size**: Keep templates small (50x50 to 200x200 pixels)
- **Uniqueness**: Ensure template is unique on screen
- **Consistency**: Use same game settings/theme for all templates
- **Updates**: Re-capture after game updates

## Configuration

Edit `config.json` to customize bot behavior.

### Basic Configuration

```json
{
  "bot_settings": {
    "base_interval": 60,        // Seconds between actions
    "variance": 0.3,            // ±30% randomization
    "template_threshold": 0.8,  // Match confidence (0.7-0.9)
    "enable_breaks": true,
    "break_interval": 7200,     // Break every 2 hours
    "break_duration": 900       // 15 minute breaks
  }
}
```

### Task Configuration

```json
{
  "tasks": {
    "gather_resources": {
      "enabled": true,
      "weight": 0.5,      // 50% of actions
      "interval": 45      // Min 45s between gathers
    },
    "upgrade_building": {
      "enabled": true,
      "weight": 0.3,      // 30% of actions
      "interval": 120
    },
    "train_troops": {
      "enabled": true,
      "weight": 0.2,      // 20% of actions
      "interval": 180
    }
  }
}
```

### Anti-Detection Configuration

```json
{
  "anti_detection": {
    "use_bezier_movement": true,    // Curved mouse paths
    "random_mistakes": true,         // Occasional misclicks
    "mistake_probability": 0.05,     // 5% chance
    "vary_daily_playtime": true,
    "min_daily_hours": 18,
    "max_daily_hours": 23
  }
}
```

## Running the Bot

### Basic Usage

```bash
# Start bot with default config
python main.py

# Use custom config
python main.py --config my_config.json

# Enable verbose logging
python main.py --verbose
```

### Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --config PATH       Configuration file (default: config.json)
  --verbose, -v       Enable debug logging
  --detect-window     Test window detection and exit
  --create-config     Create default config and exit
```

### Running in Background

**Windows (PowerShell)**:
```powershell
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden
```

**Linux/Mac**:
```bash
nohup python main.py > bot.log 2>&1 &
```

### Stopping the Bot

- Press `Ctrl+C` in terminal
- Or close the terminal window
- Or kill the Python process

## Anti-Detection Strategies

### 1. Timing Randomization

```python
# Base interval: 60 seconds
# Variance: ±30%
# Actual interval: 42-78 seconds (random)
```

**Configuration**:
```json
{
  "bot_settings": {
    "base_interval": 60,
    "variance": 0.3  // Increase to 0.4-0.5 for more randomness
  }
}
```

### 2. Mouse Movement Humanization

The bot uses **Bezier curves** for natural mouse movement:

```python
# Instead of: straight line A → B
# Uses: curved path A → C → B
```

**Configuration**:
```json
{
  "anti_detection": {
    "use_bezier_movement": true
  }
}
```

### 3. Random Breaks

Simulates human breaks:

```python
# Every 2 hours: 10-20 minute break
# Variance in break timing and duration
```

**Configuration**:
```json
{
  "bot_settings": {
    "enable_breaks": true,
    "break_interval": 7200,   // 2 hours
    "break_duration": 900     // 15 minutes
  }
}
```

### 4. Mistake Simulation

Occasionally makes "mistakes":

```python
# 5% chance to:
# - Miss click slightly
# - Click wrong button
# - Delay action
```

**Configuration**:
```json
{
  "anti_detection": {
    "random_mistakes": true,
    "mistake_probability": 0.05
  }
}
```

### 5. Daily Playtime Variance

Varies total daily playtime:

```python
# Monday: 20 hours
# Tuesday: 18 hours
# Wednesday: 22 hours
# etc.
```

**Configuration**:
```json
{
  "anti_detection": {
    "vary_daily_playtime": true,
    "min_daily_hours": 18,
    "max_daily_hours": 23
  }
}
```

## Multi-Instance Setup

Run multiple accounts simultaneously.

### Hardware Requirements

For each instance:
- **CPU**: 1-2 cores
- **RAM**: 4GB
- **GPU**: Shared

**Example**: 128GB RAM system can run 20+ instances

### BlueStacks Multi-Instance Manager

1. Open BlueStacks Multi-Instance Manager
2. Click "Instance" → "Fresh Instance"
3. Configure each instance:
   - Name: `DWS_Account_1`, `DWS_Account_2`, etc.
   - Resolution: 1920x1080
   - CPU: 2 cores
   - RAM: 4GB
4. Start all instances
5. Install Dark War Survival on each

### Bot Configuration for Multi-Instance

Create separate config for each account:

**account1.json**:
```json
{
  "bot_settings": {
    "base_interval": 60,
    "variance": 0.3
  },
  "instance": {
    "name": "Account 1",
    "window_title": "BlueStacks App Player - DWS_Account_1"
  }
}
```

**account2.json**:
```json
{
  "bot_settings": {
    "base_interval": 65,  // Slightly different
    "variance": 0.35
  },
  "instance": {
    "name": "Account 2",
    "window_title": "BlueStacks App Player - DWS_Account_2"
  }
}
```

### Running Multiple Instances

**Option 1: Separate Terminals**
```bash
# Terminal 1
python main.py --config account1.json

# Terminal 2
python main.py --config account2.json

# Terminal 3
python main.py --config account3.json
```

**Option 2: Background Processes**
```bash
python main.py --config account1.json &
python main.py --config account2.json &
python main.py --config account3.json &
```

**Option 3: Batch Script (Windows)**
```batch
@echo off
start /min python main.py --config account1.json
timeout /t 10
start /min python main.py --config account2.json
timeout /t 10
start /min python main.py --config account3.json
```

## Troubleshooting

### Common Issues and Solutions

#### Template Not Found

**Error**: `Template not found: templates/gather_btn.png`

**Solution**:
1. Check file exists in `bot/templates/`
2. Verify exact filename (case-sensitive)
3. Ensure PNG format

#### Low Match Confidence

**Error**: `Template 'gather_btn.png' not found (confidence 0.65)`

**Solutions**:
1. Lower threshold: `"template_threshold": 0.7`
2. Re-capture template at current resolution
3. Ensure game UI hasn't changed
4. Check for UI scaling issues

#### Window Not Detected

**Error**: `Emulator window not detected`

**Solutions**:
1. Ensure BlueStacks is running
2. Install pywin32: `pip install pywin32`
3. Run as administrator
4. Manually specify window title in config

#### Click Misalignment

**Problem**: Bot clicks wrong locations

**Solutions**:
1. Ensure BlueStacks window is not moved
2. Use fullscreen or fixed position
3. Re-capture templates
4. Check screen scaling (should be 100%)

#### High CPU/RAM Usage

**Problem**: Bot uses too many resources

**Solutions**:
1. Increase `base_interval` to 90-120
2. Reduce screenshot frequency
3. Close unnecessary programs
4. Limit number of instances

## Best Practices

### Safety Guidelines

1. **Use Farm Accounts**: Never bot on main account
2. **Start Slow**: Begin with 1-2 hours/day, gradually increase
3. **Vary Patterns**: Change config regularly
4. **Monitor Logs**: Check for errors and unusual patterns
5. **Stay Updated**: Update templates after game patches

### Optimal Settings

**Conservative (Low Risk)**:
```json
{
  "bot_settings": {
    "base_interval": 90,
    "variance": 0.5,
    "enable_breaks": true,
    "break_interval": 3600
  },
  "anti_detection": {
    "random_mistakes": true,
    "mistake_probability": 0.1
  }
}
```

**Aggressive (High Risk, High Reward)**:
```json
{
  "bot_settings": {
    "base_interval": 30,
    "variance": 0.2,
    "enable_breaks": false
  }
}
```

### Performance Optimization

1. **Template Size**: Keep templates small (< 100KB each)
2. **Screenshot Region**: Capture only game window, not full screen
3. **Logging**: Use INFO level in production, DEBUG only for troubleshooting
4. **Cleanup**: Clear old log files regularly

### Maintenance

- **Weekly**: Review logs for errors
- **Bi-weekly**: Update templates if game UI changed
- **Monthly**: Review and adjust configuration
- **After Updates**: Re-capture all templates

## Next Steps

1. ✅ Complete installation
2. ✅ Create all required templates
3. ✅ Configure `config.json`
4. ✅ Test with `--detect-window`
5. ✅ Run bot for 1 hour (supervised)
6. ✅ Review logs and adjust
7. ✅ Gradually increase runtime
8. ✅ Set up multi-instance (optional)

## Additional Resources

- **Main README**: `../README.md`
- **Bot README**: `../bot/README.md`
- **Configuration Reference**: `config.json`
- **Source Code**: `bot/core/dark_war_bot.py`

---

**Disclaimer**: Automation violates game ToS. Use at your own risk. This guide is for educational purposes only.
