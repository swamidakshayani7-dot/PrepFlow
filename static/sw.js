self.addEventListener('install', function(event) {
  console.log('Service Worker Installed');
});
self.addEventListener('activate', function(event) {
  event.waitUntil(self.clients.claim());
});


self.addEventListener('fetch', function(event) {
  // just pass through
});