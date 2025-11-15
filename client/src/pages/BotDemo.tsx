import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { APP_LOGO } from "@/const";
import { ArrowLeft, Play, Square } from "lucide-react";
import { useState } from "react";
import { Link } from "wouter";

interface BotFeature {
  id: string;
  name: string;
  enabled: boolean;
}

export default function BotDemo() {
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [features, setFeatures] = useState<BotFeature[]>([
    { id: "building", name: "Building Upgrading", enabled: true },
    { id: "gathering", name: "Resource Gathering", enabled: true },
    { id: "shield", name: "Auto Shield", enabled: true },
    { id: "alliance", name: "Alliance Tasks", enabled: false },
    { id: "research", name: "Technology Research", enabled: true },
    { id: "troops", name: "Troop Training", enabled: false },
    { id: "heal", name: "Heal Troops", enabled: true },
    { id: "arena", name: "Arena Battles", enabled: false },
  ]);

  const toggleFeature = (id: string) => {
    setFeatures((prev) =>
      prev.map((f) => (f.id === id ? { ...f, enabled: !f.enabled } : f))
    );
  };

  const startBot = () => {
    setIsRunning(true);
    setLogs(["[INFO] Bot started successfully", "[INFO] Initializing game connection..."]);

    const enabledFeatures = features.filter((f) => f.enabled);

    setTimeout(() => {
      setLogs((prev) => [...prev, "[INFO] Connected to Dark War Survival"]);
    }, 1000);

    setTimeout(() => {
      setLogs((prev) => [...prev, `[INFO] Loaded ${enabledFeatures.length} active features`]);
    }, 2000);

    let delay = 3000;
    enabledFeatures.forEach((feature, index) => {
      setTimeout(() => {
        setLogs((prev) => [...prev, `[SUCCESS] ${feature.name} - Executing...`]);
      }, delay + index * 1500);
    });

    setTimeout(() => {
      setLogs((prev) => [...prev, "[INFO] Bot is running. Press Stop to terminate."]);
    }, delay + enabledFeatures.length * 1500);
  };

  const stopBot = () => {
    setIsRunning(false);
    setLogs((prev) => [...prev, "[INFO] Bot stopped by user", "[INFO] Disconnecting..."]);
    setTimeout(() => {
      setLogs((prev) => [...prev, "[INFO] Bot terminated successfully"]);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <img src={APP_LOGO} alt="Bot Logo" className="w-10 h-10" />
              <span className="text-xl font-bold">Dark War Bot Demo</span>
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

      <main className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Configuration Panel */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Bot Configuration</CardTitle>
                <CardDescription>
                  Enable or disable features you want the bot to automate
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {features.map((feature) => (
                  <div
                    key={feature.id}
                    className="flex items-center justify-between py-2 border-b border-border last:border-0"
                  >
                    <span className="text-sm font-medium">{feature.name}</span>
                    <Switch
                      checked={feature.enabled}
                      onCheckedChange={() => toggleFeature(feature.id)}
                      disabled={isRunning}
                    />
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Bot Control</CardTitle>
                <CardDescription>Start or stop the automation bot</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4">
                  <Button
                    onClick={startBot}
                    disabled={isRunning}
                    className="flex-1"
                    size="lg"
                  >
                    <Play className="w-4 h-4 mr-2" />
                    Start Bot
                  </Button>
                  <Button
                    onClick={stopBot}
                    disabled={!isRunning}
                    variant="destructive"
                    className="flex-1"
                    size="lg"
                  >
                    <Square className="w-4 h-4 mr-2" />
                    Stop Bot
                  </Button>
                </div>
                {isRunning && (
                  <div className="mt-4 p-3 bg-primary/10 rounded-lg border border-primary/20">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                      <span className="text-sm font-medium text-primary">Bot is running...</span>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Activity Log */}
          <div>
            <Card className="h-full">
              <CardHeader>
                <CardTitle>Activity Log</CardTitle>
                <CardDescription>Real-time bot activity and status updates</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg p-4 h-[500px] overflow-y-auto font-mono text-sm">
                  {logs.length === 0 ? (
                    <p className="text-muted-foreground">
                      No activity yet. Start the bot to see logs.
                    </p>
                  ) : (
                    <div className="space-y-2">
                      {logs.map((log, index) => (
                        <div
                          key={index}
                          className={`${
                            log.includes("[SUCCESS]")
                              ? "text-green-400"
                              : log.includes("[ERROR]")
                              ? "text-red-400"
                              : "text-foreground"
                          }`}
                        >
                          {log}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Info Section */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>About This Demo</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              This is a demonstration of the Dark War Survival Bot interface. The actual bot is a
              Windows application that connects to the game and automates various tasks to help you
              manage multiple accounts efficiently.
            </p>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="p-4 bg-card border border-border rounded-lg">
                <h4 className="font-semibold mb-2 text-primary">Automated Tasks</h4>
                <p className="text-sm text-muted-foreground">
                  The bot can handle building upgrades, resource gathering, troop training, and
                  more.
                </p>
              </div>
              <div className="p-4 bg-card border border-border rounded-lg">
                <h4 className="font-semibold mb-2 text-primary">Multi-Account Support</h4>
                <p className="text-sm text-muted-foreground">
                  Manage unlimited accounts simultaneously without manual intervention.
                </p>
              </div>
              <div className="p-4 bg-card border border-border rounded-lg">
                <h4 className="font-semibold mb-2 text-primary">24/7 Operation</h4>
                <p className="text-sm text-muted-foreground">
                  The bot runs continuously, ensuring your accounts progress even when you're away.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
