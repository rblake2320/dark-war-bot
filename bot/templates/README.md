# Bot Templates

This directory contains template images used by the bot for UI element recognition through OpenCV template matching.

## Generated Templates

The following templates have been AI-generated and are ready to use:

### Action Buttons
- `gather_btn.png` - Purple/blue "GATHER" button
- `upgrade_btn.png` - Green "UPGRADE" button with arrow
- `train_btn.png` - Orange/red "TRAIN" button with tank icon
- `confirm_btn.png` - Green "CONFIRM" button with checkmark
- `cancel_btn.png` - Red "CANCEL" button with X icon

### Resource Nodes
- `food_node.png` - Golden wheat/farm icon (circular, green background)
- `wood_node.png` - Brown logs/lumber icon (circular, brown background)
- `stone_node.png` - Gray rocks/stone icon (circular, gray background)

### Buildings
- `barracks.png` - Military barracks with crossed swords (square, red/orange)
- `hospital.png` - Medical tent with red cross (square, white/red)

## Usage

These templates are used by the bot's `find_template()` function in `core/dark_war_bot.py`:

```python
screenshot = bot.capture_screen()
location = bot.find_template(screenshot, 'gather_btn.png')
if location:
    bot.human_click(*location)
```

## Important Notes

⚠️ **These are AI-generated templates** - They may not match your actual game UI exactly.

### For Production Use:

1. **Test First**: Run the bot and check if templates are recognized
2. **Adjust Threshold**: Lower `template_threshold` in config if needed (try 0.7-0.8)
3. **Replace if Needed**: If recognition fails, capture real screenshots:
   - Open Dark War Survival in BlueStacks
   - Navigate to the UI element
   - Take screenshot (Print Screen)
   - Crop the element tightly
   - Save as PNG with same filename
   - Ensure same resolution as BlueStacks (1920x1080 recommended)

### Creating Custom Templates:

1. **Screenshot**: Capture the game UI element
2. **Crop**: Use image editor to crop tightly around element
3. **Save**: Save as PNG in this directory
4. **Name**: Use descriptive lowercase names with underscores
5. **Test**: Run bot with `--verbose` to see matching confidence

### Template Best Practices:

- **Resolution**: Match your BlueStacks resolution
- **Format**: Always PNG (lossless)
- **Size**: Keep small (50x50 to 200x200 pixels)
- **Uniqueness**: Ensure template appears only once on screen
- **Consistency**: Use same game settings/theme for all templates
- **Updates**: Re-capture after game updates

## Template Matching Confidence

The bot uses a confidence threshold (default 0.8) to match templates:

- **0.9-1.0**: Excellent match (very strict)
- **0.8-0.9**: Good match (default, recommended)
- **0.7-0.8**: Acceptable match (more flexible)
- **< 0.7**: Poor match (may cause false positives)

Adjust in `config.json`:
```json
{
  "bot_settings": {
    "template_threshold": 0.8
  }
}
```

## Troubleshooting

### Template Not Found

**Problem**: Bot can't find UI element

**Solutions**:
- Lower threshold to 0.7
- Re-capture template at current resolution
- Check if game UI has changed
- Verify template filename matches code

### False Positives

**Problem**: Bot clicks wrong elements

**Solutions**:
- Raise threshold to 0.85-0.9
- Make template more specific (include more context)
- Ensure template is unique on screen

### Slow Recognition

**Problem**: Template matching is slow

**Solutions**:
- Reduce template size
- Use smaller screenshot region
- Optimize template count

## Adding More Templates

To add templates for additional features:

1. Identify the UI element needed
2. Capture and crop screenshot
3. Save in this directory with descriptive name
4. Update bot code to use new template
5. Test and adjust threshold as needed

Example template names:
- `research_btn.png`
- `heal_btn.png`
- `alliance_help_btn.png`
- `mail_icon.png`
- `reward_claim_btn.png`
- `shield_icon.png`
- `vip_claim_btn.png`

## License

These AI-generated templates are provided as-is for use with the Dark War Survival Bot project.
