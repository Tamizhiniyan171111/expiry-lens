// static/js/service_worker.js
// A minimal service worker - required for a site to qualify as an 
// installable PWA. This basic version just lets the browser know 
// the app supports offline capability (even if minimal for now).

self.addEventListener("install", (event) => {
  console.log("Expiry Lens service worker installed.");
});

self.addEventListener("fetch", (event) => {
  // For now, we simply let all requests pass through normally.
  // This satisfies PWA requirements without changing app behavior.
  event.respondWith(fetch(event.request));
});
