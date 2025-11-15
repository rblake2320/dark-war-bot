import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";

// Conditional analytics loading - only load if configured
const analyticsEndpoint = import.meta.env.VITE_ANALYTICS_ENDPOINT;
const analyticsWebsiteId = import.meta.env.VITE_ANALYTICS_WEBSITE_ID;

if (analyticsEndpoint && analyticsWebsiteId) {
  // Dynamically inject analytics script
  const script = document.createElement('script');
  script.async = true;
  script.defer = true;
  script.src = analyticsEndpoint;
  script.setAttribute('data-website-id', analyticsWebsiteId);
  document.head.appendChild(script);
  console.log('Analytics loaded');
} else {
  console.log('Analytics disabled - no endpoint configured');
}

createRoot(document.getElementById("root")!).render(<App />);
