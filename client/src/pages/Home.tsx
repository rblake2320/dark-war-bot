import { Button } from "@/components/ui/button";
import { APP_LOGO } from "@/const";
import { Menu, X } from "lucide-react";
import { useState } from "react";

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      {/* Navigation Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-sm border-b border-border">
        <nav className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <img src={APP_LOGO} alt="Bot Logo" className="w-10 h-10" />
              <span className="text-xl font-bold text-foreground">LSS Bot</span>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-6">
                  <a href="/demo" className="text-sm hover:text-primary transition-colors">
                DEMO
              </a>
              <a href="#" className="text-sm hover:text-primary transition-colors">
                DOCUMENTATION
              </a>
              <a href="#store" className="text-muted-foreground hover:text-foreground transition-colors">
                STORE
              </a>
              <a href="#accounts" className="text-muted-foreground hover:text-foreground transition-colors">
                FARM ACCOUNTS
              </a>
              <a href="#bots" className="text-muted-foreground hover:text-foreground transition-colors">
                BOTS
              </a>
              <a href="#started" className="text-muted-foreground hover:text-foreground transition-colors">
                GET STARTED
              </a>
              <a href="#guides" className="text-muted-foreground hover:text-foreground transition-colors">
                GUIDES
              </a>
              <Button variant="outline" size="sm" className="ml-4">
                SIGN IN
              </Button>
              <Button size="sm">REGISTER</Button>
            </nav>

            {/* Mobile Menu Button */}
            <button
              className="md:hidden text-foreground"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden mt-4 pb-4 flex flex-col gap-4">
              <a href="#store" className="text-muted-foreground hover:text-foreground transition-colors">
                STORE
              </a>
              <a href="#accounts" className="text-muted-foreground hover:text-foreground transition-colors">
                FARM ACCOUNTS
              </a>
              <a href="#bots" className="text-muted-foreground hover:text-foreground transition-colors">
                BOTS
              </a>
              <a href="#started" className="text-muted-foreground hover:text-foreground transition-colors">
                GET STARTED
              </a>
              <a href="#guides" className="text-muted-foreground hover:text-foreground transition-colors">
                GUIDES
              </a>
              <div className="flex gap-2 mt-2">
                <Button variant="outline" size="sm" className="flex-1">
                  SIGN IN
                </Button>
                <Button size="sm" className="flex-1">
                  REGISTER
                </Button>
              </div>
            </div>
          )}
        </nav>
      </header>

      {/* Hero Section */}
      <main className="flex-1 mt-16">
        <section
          className="relative py-20 md:py-32 overflow-hidden"
          style={{
            backgroundImage: "url(/hero-bg.jpg)",
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        >
          <div className="absolute inset-0 bg-background/80 backdrop-blur-sm"></div>
          <div className="container relative z-10 text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-4 text-foreground">
              Dark War Survival Bot
            </h1>
            <h2 className="text-2xl md:text-3xl text-muted-foreground mb-8">
              #1 DWS Bot Working In 2025
            </h2>

            {/* Video Placeholder */}
            <div className="max-w-4xl mx-auto mb-8 aspect-video bg-card rounded-lg border border-border flex items-center justify-center">
              <div className="text-center">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-primary/20 flex items-center justify-center">
                  <svg
                    className="w-10 h-10 text-primary"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </div>
                <p className="text-muted-foreground">Video Demo</p>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <a href="/demo">
                <Button size="lg" className="min-w-[250px] bg-primary hover:bg-primary/90">
                  TRY DEMO – INTERACTIVE
                </Button>
              </a>
              <Button size="lg" variant="outline" className="min-w-[250px]">
                CHECK OUT THE MOBILE VERSION
              </Button>
            </div>
          </div>
        </section>

        {/* Introduction Section */}
        <section className="py-16 bg-card">
          <div className="container max-w-4xl">
            <p className="text-lg text-card-foreground leading-relaxed">
              Our Dark War Survival Bot is the ultimate tool for Dark War. It will assist you by
              playing on all of your farms. It's able to complete the most difficult tasks such as
              gathering resources, upgrading structures, researching technology and participating in
              different events. Save time and money by using LSS Bot's Dark War Bot. The bot brings
              in an insane value, you have to play on multiple farms every single day if you don't
              want to fall behind on the game. Completing all the tedious and slow tasks manually
              every day is very draining and let's be honest not very fun. This Dark War Survival
              Bot will do it all for you automatically. You will be able to not only have fun but
              enjoy the game even more than you did previously as you'll progress much faster.
            </p>
          </div>
        </section>

        {/* Try For Free Section */}
        <section className="py-16 bg-background">
          <div className="container">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <h3 className="text-3xl font-bold mb-4 text-foreground">TRY FOR FREE</h3>
                <p className="text-lg text-muted-foreground mb-4">
                  Download our Dark War bot for <span className="text-primary font-bold">free</span>{" "}
                  on your Windows 10+ PC.
                </p>
                <p className="text-lg text-muted-foreground">
                  Our software will take care of all your accounts. Forget about the tedious grind
                  and let our Dark War Survival bot do the boring work for you.
                </p>
              </div>
              <div className="bg-card rounded-lg border border-border overflow-hidden">
                <img
                  src="/bot-config.png"
                  alt="Bot Configuration Interface"
                  className="w-full h-auto"
                />
              </div>
            </div>
          </div>
        </section>

        {/* Unlimited Accounts Section */}
        <section className="py-16 bg-card">
          <div className="container">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="order-2 md:order-1 bg-background rounded-lg border border-border overflow-hidden">
                <img
                  src="/bot-accounts.png"
                  alt="Multi-Account Management"
                  className="w-full h-auto"
                />
              </div>
              <div className="order-1 md:order-2">
                <h3 className="text-3xl font-bold mb-4 text-card-foreground">
                  UNLIMITED ACCOUNTS
                </h3>
                <p className="text-lg text-muted-foreground mb-4">
                  This Dark War Survival bot can play on{" "}
                  <span className="text-primary font-bold">any amount</span> of accounts and it does
                  not need a break.
                </p>
                <p className="text-lg text-muted-foreground mb-4">
                  Earn in-game resources at a much{" "}
                  <span className="text-primary font-bold">lower cost</span>. Grow your farms much
                  faster using our Dark War Game bot.
                </p>
                <p className="text-lg text-muted-foreground">
                  Our bot can play on multiple accounts at the same time, no human can compete and
                  maintain dozen of accounts simultaneously without needing a break.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 bg-background">
          <div className="container">
            <div className="text-center mb-12">
              <h3 className="text-4xl font-bold mb-4 text-foreground">
                MOST ADVANCED AUTO FEATURES
              </h3>
              <p className="text-xl text-muted-foreground">Tasks No Other Bot Can Complete</p>
            </div>

            {/* Features Table */}
            <div className="max-w-6xl mx-auto">
              <div className="grid md:grid-cols-3 gap-8">
                {/* Column 1 */}
                <div className="space-y-4">
                  <div className="bg-card rounded-lg p-4 border border-border">
                    <h4 className="font-semibold text-card-foreground mb-2">Supports</h4>
                    <ul className="space-y-2 text-muted-foreground">
                      <li>Building Upgrading</li>
                      <li>Gathering</li>
                      <li>Host Rally</li>
                      <li>Shield</li>
                      <li>Task Rewards</li>
                      <li>Battle Rewards</li>
                      <li>Collect Mail Rewards</li>
                    </ul>
                  </div>
                </div>

                {/* Column 2 */}
                <div className="space-y-4">
                  <div className="bg-card rounded-lg p-4 border border-border">
                    <h4 className="font-semibold text-card-foreground mb-2">Supports</h4>
                    <ul className="space-y-2 text-muted-foreground">
                      <li>Alliance Tasks</li>
                      <li>Troop Training</li>
                      <li>Heal Troops</li>
                      <li>Calls</li>
                      <li>Attack Monsters</li>
                      <li>Arena</li>
                      <li>Assign Survivors</li>
                    </ul>
                  </div>
                </div>

                {/* Column 3 */}
                <div className="space-y-4">
                  <div className="bg-card rounded-lg p-4 border border-border">
                    <h4 className="font-semibold text-card-foreground mb-2">Supports</h4>
                    <ul className="space-y-2 text-muted-foreground">
                      <li>Hero Recruitment</li>
                      <li>Use Inventory Items</li>
                      <li>Exploration</li>
                      <li>Research</li>
                      <li>Black Market</li>
                      <li>VIP</li>
                      <li>Shop Rewards</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div className="text-center mt-12">
              <p className="text-2xl font-bold text-primary mb-6">AND MUCH MORE!</p>
              <a href="/demo">
                <Button size="lg" className="min-w-[250px]">
                  GET STARTED FOR FREE
                </Button>
              </a>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-card border-t border-border py-12">
          <div className="container">
            <div className="grid md:grid-cols-4 gap-8">
              {/* Our Bots */}
              <div>
                <h4 className="font-bold text-card-foreground mb-4">OUR BOTS</h4>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>
                    <a href="#" className="hover:text-primary transition-colors">
                      Last Shelter Survival Bot
                    </a>
                  </li>
                  <li>
                    <a href="#" className="hover:text-primary transition-colors">
                      Rise of Castles Bot
                    </a>
                  </li>
                  <li>
                    <a href="#" className="hover:text-primary transition-colors">
                      Ants Underground Kingdom Bot
                    </a>
                  </li>
                  <li>
                    <a href="#" className="hover:text-primary transition-colors">
                      The Walking Dead Survivors Bot
                    </a>
                  </li>
                  <li>
                    <a href="#" className="hover:text-primary transition-colors">
                      The Grand Mafia Bot
                    </a>
                  </li>
                  <li>
                    <a href="#" className="hover:text-primary transition-colors">
                      Rise of Kingdoms Bot
                    </a>
                  </li>
                </ul>
              </div>

              {/* Links & Services */}
              <div>
                <h4 className="font-bold text-card-foreground mb-4">LINKS & SERVICES</h4>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li>
                    <a href="#" className="hover:text-primary transition-colors">
                      Terms of Service
                    </a>
                  </li>
                  <li>
                    <a href="#" className="hover:text-primary transition-colors">
                      Privacy Policy
                    </a>
                  </li>
                  <li>
                    <a href="#" className="hover:text-primary transition-colors">
                      Premium Plans
                    </a>
                  </li>
                </ul>
              </div>

              {/* Contact Us */}
              <div>
                <h4 className="font-bold text-card-foreground mb-4">CONTACT US</h4>
                <a
                  href="mailto:support@lssbot.com"
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  support@lssbot.com
                </a>
              </div>

              {/* Follow Us */}
              <div>
                <h4 className="font-bold text-card-foreground mb-4">FOLLOW US</h4>
                <div className="flex gap-4">
                  <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z" />
                    </svg>
                  </a>
                  <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
                    </svg>
                  </a>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-8 border-t border-border text-center text-sm text-muted-foreground">
              © 2025 LSS Bot
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
