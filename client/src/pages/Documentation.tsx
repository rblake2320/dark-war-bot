import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { APP_LOGO } from "@/const";
import { ArrowLeft, Book, Code, Download, Shield, Terminal } from "lucide-react";
import { Link } from "wouter";

export default function Documentation() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <img src={APP_LOGO} alt="Bot Logo" className="w-10 h-10" />
              <span className="text-xl font-bold">Documentation</span>
            </div>
            <Link href="/">
              <Button variant="outline" size="sm">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Home
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Complete Bot Documentation
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Everything you need to implement, configure, and run the Dark War Survival automation bot
          </p>
        </div>

        {/* Quick Links */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          <Card className="hover:border-primary transition-colors cursor-pointer">
            <CardHeader>
              <Terminal className="w-8 h-8 text-primary mb-2" />
              <CardTitle>Quick Start</CardTitle>
              <CardDescription>Get up and running in minutes</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Install dependencies, create templates, and launch your first bot instance.
              </p>
              <Button variant="outline" className="w-full">
                View Guide
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:border-primary transition-colors cursor-pointer">
            <CardHeader>
              <Code className="w-8 h-8 text-primary mb-2" />
              <CardTitle>Implementation</CardTitle>
              <CardDescription>Detailed technical guide</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Complete walkthrough of bot architecture, configuration, and customization.
              </p>
              <Button variant="outline" className="w-full">
                Read More
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:border-primary transition-colors cursor-pointer">
            <CardHeader>
              <Shield className="w-8 h-8 text-primary mb-2" />
              <CardTitle>Anti-Detection</CardTitle>
              <CardDescription>Stay safe and undetected</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Advanced strategies to avoid detection and minimize ban risk.
              </p>
              <Button variant="outline" className="w-full">
                Learn More
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Main Documentation Sections */}
        <div className="space-y-8">
          {/* Installation */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Download className="w-5 h-5" />
                Installation
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">System Requirements</h4>
                <ul className="list-disc list-inside text-muted-foreground space-y-1">
                  <li>Windows 10/11 (64-bit)</li>
                  <li>Python 3.11 or higher</li>
                  <li>BlueStacks 5 or compatible emulator</li>
                  <li>8GB RAM minimum (16GB+ recommended)</li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold mb-2">Installation Steps</h4>
                <div className="bg-muted rounded-lg p-4 font-mono text-sm">
                  <div className="space-y-2">
                    <div># Clone the repository</div>
                    <div>git clone https://github.com/rblake2320/dark-war-bot.git</div>
                    <div className="mt-3"># Navigate to bot directory</div>
                    <div>cd dark-war-bot/bot</div>
                    <div className="mt-3"># Install dependencies</div>
                    <div>pip install -r requirements.txt</div>
                    <div className="mt-3"># Create configuration</div>
                    <div>python main.py --create-config</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Configuration */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="w-5 h-5" />
                Configuration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">
                The bot uses a JSON configuration file to customize behavior. Edit <code className="bg-muted px-2 py-1 rounded">config.json</code> to adjust settings:
              </p>

              <div className="bg-muted rounded-lg p-4 font-mono text-sm overflow-x-auto">
                <pre>{`{
  "bot_settings": {
    "base_interval": 60,        // Seconds between actions
    "variance": 0.3,            // ±30% randomization
    "template_threshold": 0.8,  // Match confidence
    "enable_breaks": true
  },
  "tasks": {
    "gather_resources": {
      "enabled": true,
      "weight": 0.5
    }
  }
}`}</pre>
              </div>
            </CardContent>
          </Card>

          {/* Features */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Book className="w-5 h-5" />
                Key Features
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold mb-2">Template Matching</h4>
                  <p className="text-sm text-muted-foreground">
                    Uses OpenCV for reliable UI element detection. Create templates by capturing screenshots of game buttons and icons.
                  </p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Human-like Behavior</h4>
                  <p className="text-sm text-muted-foreground">
                    Bezier curve mouse movement, randomized timing, and occasional mistakes to mimic human gameplay.
                  </p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Multi-Instance Support</h4>
                  <p className="text-sm text-muted-foreground">
                    Run multiple bot instances simultaneously for managing multiple game accounts efficiently.
                  </p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Comprehensive Logging</h4>
                  <p className="text-sm text-muted-foreground">
                    Detailed logs with color coding help you monitor bot activity and troubleshoot issues.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Anti-Detection */}
          <Card className="border-primary/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-primary">
                <Shield className="w-5 h-5" />
                Anti-Detection Strategies
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">
                The bot implements multiple anti-detection strategies to minimize ban risk:
              </p>

              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                  <div>
                    <h5 className="font-semibold">Timing Randomization</h5>
                    <p className="text-sm text-muted-foreground">
                      Actions have ±30-50% variance to avoid predictable patterns
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                  <div>
                    <h5 className="font-semibold">Bezier Curve Movement</h5>
                    <p className="text-sm text-muted-foreground">
                      Mouse moves along natural curved paths instead of straight lines
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                  <div>
                    <h5 className="font-semibold">Break Simulation</h5>
                    <p className="text-sm text-muted-foreground">
                      Random breaks every 2-4 hours to simulate human behavior
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                  <div>
                    <h5 className="font-semibold">Mistake Simulation</h5>
                    <p className="text-sm text-muted-foreground">
                      Occasional misclicks and delays to appear more human
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-primary/10 border border-primary/20 rounded-lg p-4 mt-4">
                <p className="text-sm">
                  <strong>⚠️ Important:</strong> While these strategies reduce detection risk, using automation violates most game Terms of Service. Use at your own risk on farm accounts only.
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Resources */}
          <Card>
            <CardHeader>
              <CardTitle>Additional Resources</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                <a
                  href="https://github.com/rblake2320/dark-war-bot"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block"
                >
                  <Button variant="outline" className="w-full justify-start">
                    <Code className="w-4 h-4 mr-2" />
                    View on GitHub
                  </Button>
                </a>
                <Link href="/demo">
                  <Button variant="outline" className="w-full justify-start">
                    <Terminal className="w-4 h-4 mr-2" />
                    Try Interactive Demo
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
