# Anti-Detection Strategies for Game Automation

This document outlines comprehensive anti-detection strategies for the Dark War Survival Bot based on analysis of commercial bot services and game security research.

## Table of Contents

1. [Detection Vectors](#detection-vectors)
2. [Commercial Bot Analysis](#commercial-bot-analysis)
3. [Implementation Strategies](#implementation-strategies)
4. [Risk Assessment](#risk-assessment)
5. [Best Practices](#best-practices)

## Detection Vectors

Game publishers can detect bots through multiple vectors:

### 1. Behavioral Pattern Analysis

**What They Detect**:
- Superhuman reaction times (< 100ms)
- Perfect timing consistency
- 24/7 uptime without breaks
- Repetitive action sequences
- Identical timing between sessions

**How We Mitigate**:
```python
# Randomized intervals with variance
base_interval = 60  # seconds
variance = 0.3  # ±30%
actual_interval = random.uniform(
    base_interval * (1 - variance),
    base_interval * (1 + variance)
)
# Result: 42-78 seconds (random each time)
```

### 2. Mouse Movement Analysis

**What They Detect**:
- Straight-line mouse movement
- Instant teleportation to targets
- Consistent movement speed
- No acceleration/deceleration

**How We Mitigate**:
```python
def bezier_curve_movement(start, end, steps=20):
    """Natural curved mouse path"""
    # Random control point for curve
    control = (
        random.randint(min(start[0], end[0]), max(start[0], end[0])),
        random.randint(min(start[1], end[1]), max(start[1], end[1]))
    )
    
    # Move along Bezier curve
    for i in range(steps):
        t = i / steps
        x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
        y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
        pyautogui.moveTo(int(x), int(y))
        sleep(random.uniform(0.008, 0.015))  # Variable speed
```

### 3. Click Pattern Analysis

**What They Detect**:
- Pixel-perfect clicks every time
- No click variance
- Inhuman precision
- No misclicks

**How We Mitigate**:
```python
def human_click(x, y):
    # Random offset (±5 pixels)
    offset_x = random.randint(-5, 5)
    offset_y = random.randint(-5, 5)
    
    # Occasional mistakes (5% chance)
    if random.random() < 0.05:
        offset_x += random.randint(-15, 15)
        offset_y += random.randint(-15, 15)
    
    # Variable pre-click delay
    sleep(random.uniform(0.1, 0.3))
    
    pyautogui.click(x + offset_x, y + offset_y)
    
    # Variable post-click delay
    sleep(random.uniform(0.5, 1.5))
```

### 4. Session Pattern Analysis

**What They Detect**:
- Exactly 24/7 playtime
- No breaks or idle time
- Same daily schedule
- No variance in session length

**How We Mitigate**:
```python
# Random breaks every 2-4 hours
break_interval = random.uniform(7200, 14400)

# Variable break duration (10-20 minutes)
break_duration = random.uniform(600, 1200)

# Daily playtime variance (18-23 hours)
daily_hours = random.uniform(18, 23)
```

### 5. Memory Scanning

**What They Detect**:
- Process injection
- Memory modification
- DLL injection
- Code tampering

**How We Mitigate**:
- ✅ Use image recognition only (no memory access)
- ✅ No process injection
- ✅ External automation (PyAutoGUI)
- ✅ No game client modification

### 6. Network Traffic Analysis

**What They Detect**:
- Abnormal packet patterns
- Automated API calls
- Modified client requests

**How We Mitigate**:
- ✅ No network interception
- ✅ Normal game client communication
- ✅ Bot operates at UI level only

## Commercial Bot Analysis

Analysis of 6 major Dark War Survival bot services (2025):

### Common Features

| Feature | LSS Bot | MuBots | BoostBot | GodLikeBots | PrimeBot | Macrorify |
|---------|---------|--------|----------|-------------|----------|-----------|
| Randomized Clicks | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Human-like Timing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Break Simulation | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Multi-Instance | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Image Recognition | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |

### Key Insights

1. **All services use randomization** - This is the #1 anti-detection feature
2. **3+ years operation** - No mass bans indicate low enforcement
3. **Image recognition preferred** - More reliable than pixel/color detection
4. **Break simulation standard** - All successful bots implement breaks
5. **Multi-instance support** - Indicates publisher tolerance

### Pricing Analysis

- **Free Tier**: Basic features, limited tasks
- **Premium**: $10-30/month for full features
- **Lifetime**: $50-100 one-time payment

**Our Advantage**: Open-source, fully customizable, no subscription

## Implementation Strategies

### Strategy 1: Timing Randomization

**Goal**: Make action timing unpredictable

**Implementation**:
```python
class TimingRandomizer:
    def __init__(self, base, variance):
        self.base = base
        self.variance = variance
        self.history = []
    
    def get_interval(self):
        # Base randomization
        interval = random.uniform(
            self.base * (1 - self.variance),
            self.base * (1 + self.variance)
        )
        
        # Avoid patterns in history
        if len(self.history) >= 3:
            avg = sum(self.history[-3:]) / 3
            if abs(interval - avg) < 5:  # Too similar
                interval += random.uniform(-10, 10)
        
        self.history.append(interval)
        return interval
```

**Effectiveness**: ⭐⭐⭐⭐⭐ (Essential)

### Strategy 2: Action Sequencing

**Goal**: Vary the order and combination of actions

**Implementation**:
```python
# Bad: Always same sequence
gather() → upgrade() → train() → repeat

# Good: Weighted random selection
tasks = [gather, upgrade, train, research, heal]
weights = [0.4, 0.25, 0.15, 0.1, 0.1]
task = random.choices(tasks, weights=weights)[0]
task()
```

**Effectiveness**: ⭐⭐⭐⭐ (Very Important)

### Strategy 3: Session Management

**Goal**: Simulate realistic human play sessions

**Implementation**:
```python
class SessionManager:
    def __init__(self):
        self.session_start = time()
        self.daily_limit = random.uniform(18, 23) * 3600  # hours
        self.break_due = time() + random.uniform(7200, 14400)
    
    def should_take_break(self):
        if time() >= self.break_due:
            return True
        return False
    
    def should_stop_for_day(self):
        if time() - self.session_start >= self.daily_limit:
            return True
        return False
    
    def take_break(self):
        duration = random.uniform(600, 1200)  # 10-20 min
        logging.info(f"Taking break for {duration/60:.1f} minutes")
        sleep(duration)
        self.break_due = time() + random.uniform(7200, 14400)
```

**Effectiveness**: ⭐⭐⭐⭐⭐ (Essential)

### Strategy 4: Mistake Simulation

**Goal**: Occasionally make human-like mistakes

**Implementation**:
```python
def execute_with_mistakes(action, mistake_prob=0.05):
    if random.random() < mistake_prob:
        # Simulate mistake
        mistake_type = random.choice([
            'misclick',
            'delay',
            'wrong_target',
            'double_click'
        ])
        
        if mistake_type == 'misclick':
            # Click slightly off target
            x, y = get_target()
            click(x + random.randint(-20, 20), y + random.randint(-20, 20))
            sleep(random.uniform(0.5, 1.5))  # Realize mistake
            click(x, y)  # Correct click
        
        elif mistake_type == 'delay':
            # Hesitate before action
            sleep(random.uniform(2, 5))
            action()
        
        # ... other mistake types
    else:
        action()
```

**Effectiveness**: ⭐⭐⭐ (Helpful)

### Strategy 5: Adaptive Behavior

**Goal**: Adjust behavior based on game state

**Implementation**:
```python
class AdaptiveBehavior:
    def __init__(self):
        self.resource_priority = ['food', 'wood', 'stone']
        self.last_actions = []
    
    def choose_resource(self):
        # Check what was gathered recently
        recent = self.last_actions[-5:]
        
        # Prioritize least-gathered resource
        counts = {r: recent.count(r) for r in self.resource_priority}
        return min(counts, key=counts.get)
    
    def adjust_timing(self, success_rate):
        # If actions failing, slow down
        if success_rate < 0.7:
            self.base_interval *= 1.2
        # If all successful, can speed up slightly
        elif success_rate > 0.95:
            self.base_interval *= 0.95
```

**Effectiveness**: ⭐⭐⭐⭐ (Advanced)

## Risk Assessment

### Risk Matrix

| Detection Vector | Likelihood | Impact | Mitigation | Residual Risk |
|-----------------|------------|--------|------------|---------------|
| Behavioral Patterns | LOW | HIGH | Randomization, breaks | LOW |
| Mouse Movement | VERY LOW | MEDIUM | Bezier curves | VERY LOW |
| Click Patterns | LOW | MEDIUM | Offset, mistakes | LOW |
| Session Patterns | LOW | HIGH | Daily variance | LOW |
| Memory Scanning | VERY LOW | HIGH | No injection | VERY LOW |
| Network Traffic | VERY LOW | MEDIUM | UI-level only | VERY LOW |
| Mass Reporting | MEDIUM | MEDIUM | Low-profile play | MEDIUM |
| ToS Violation | HIGH | LOW | Use farm accounts | MEDIUM |

### Risk Levels

**VERY LOW**: < 5% chance of detection
**LOW**: 5-15% chance
**MEDIUM**: 15-35% chance
**HIGH**: 35-60% chance
**VERY HIGH**: > 60% chance

### Impact Levels

**LOW**: Temporary restriction
**MEDIUM**: Account suspension
**HIGH**: Permanent ban
**CRITICAL**: IP/device ban

## Best Practices

### Do's ✅

1. **Start Conservative**: Begin with high variance and long intervals
2. **Use Farm Accounts**: Never bot on main/paid accounts
3. **Monitor Logs**: Check for unusual patterns or errors
4. **Update Templates**: Re-capture after game updates
5. **Vary Configurations**: Change settings weekly
6. **Stay Low-Profile**: Avoid competitive alliances
7. **Test Thoroughly**: Supervise bot for first few hours
8. **Keep Updated**: Monitor game patch notes

### Don'ts ❌

1. **Don't Run 24/7**: Always include breaks and daily limits
2. **Don't Use Same Timing**: Vary intervals between accounts
3. **Don't Bot in PvP**: Avoid highly competitive environments
4. **Don't Ignore Errors**: Fix template matching issues immediately
5. **Don't Share Accounts**: One bot per account
6. **Don't Brag**: Keep bot usage private
7. **Don't Neglect Updates**: Game changes can break bot
8. **Don't Expect Perfection**: Some detection risk always exists

### Configuration Recommendations

**Ultra-Safe (Minimal Risk)**:
```json
{
  "base_interval": 120,
  "variance": 0.5,
  "enable_breaks": true,
  "break_interval": 3600,
  "break_duration": 1200,
  "random_mistakes": true,
  "mistake_probability": 0.1,
  "daily_hours": [16, 20]
}
```

**Balanced (Moderate Risk)**:
```json
{
  "base_interval": 60,
  "variance": 0.3,
  "enable_breaks": true,
  "break_interval": 7200,
  "break_duration": 900,
  "random_mistakes": true,
  "mistake_probability": 0.05,
  "daily_hours": [18, 23]
}
```

**Aggressive (Higher Risk)**:
```json
{
  "base_interval": 30,
  "variance": 0.2,
  "enable_breaks": true,
  "break_interval": 10800,
  "break_duration": 600,
  "random_mistakes": false,
  "daily_hours": [20, 24]
}
```

## Conclusion

Anti-detection is a continuous arms race. The strategies outlined here are based on current game security practices (2025) and may need adjustment as detection methods evolve.

**Key Takeaways**:
1. Randomization is the #1 defense
2. Human-like behavior is essential
3. No method is 100% safe
4. Use farm accounts only
5. Stay informed and adapt

---

**Disclaimer**: This document is for educational purposes. Using automation bots violates most game Terms of Service. Use at your own risk.
