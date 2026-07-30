const CACHE_NAME = 'kinglife-cache-v2';
const STATIC_ASSETS = [
    '/',
    '/services/',
    '/catalogue/',
    '/a-propos/',
    '/contact/',
    '/offline/',
    '/static/kinglife/css/style.css',
    '/static/kinglife/css/responsive.css',
    '/static/kinglife/css/auth_contact.css',
    '/static/kinglife/css/toast.css',
    '/static/kinglife/js/main.js',
    '/static/kinglife/js/toast.js',
    '/static/kinglife/images/logo.png'
];

/* Install Event - Pre-cache essential static assets & offline fallback */
self.addEventListener('install', event => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('[ServiceWorker] Pre-caching static assets & offline fallback');
            return cache.addAll(STATIC_ASSETS).catch(err => {
                console.warn('[ServiceWorker] Assets precache partial warning:', err);
            });
        })
    );
});

/* Activate Event - Clean up old caches */
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
            );
        }).then(() => self.clients.claim())
    );
});

/* Fetch Event - Cache First for static assets, Network First for HTML pages */
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);

    // Skip non-GET requests and admin/API routes
    if (request.method !== 'GET' || url.pathname.startsWith('/admin/') || url.pathname.startsWith('/api/')) {
        return;
    }

    // 1. Static Assets (CSS, JS, Images, Fonts) -> Cache First with Network Fallback
    if (request.destination === 'style' || request.destination === 'script' || request.destination === 'image' || request.destination === 'font' || url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(request).then(cachedResponse => {
                if (cachedResponse) {
                    fetch(request).then(networkResponse => {
                        if (networkResponse && networkResponse.status === 200) {
                            caches.open(CACHE_NAME).then(cache => cache.put(request, networkResponse));
                        }
                    }).catch(() => {});
                    return cachedResponse;
                }
                return fetch(request).then(networkResponse => {
                    if (networkResponse && networkResponse.status === 200) {
                        const responseClone = networkResponse.clone();
                        caches.open(CACHE_NAME).then(cache => cache.put(request, responseClone));
                    }
                    return networkResponse;
                });
            })
        );
        return;
    }

    // 2. HTML Navigation Pages -> Network First with Cache Fallback & Offline Page
    event.respondWith(
        fetch(request)
            .then(networkResponse => {
                if (networkResponse && networkResponse.status === 200) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(request, responseClone));
                }
                return networkResponse;
            })
            .catch(async () => {
                const cachedResponse = await caches.match(request);
                if (cachedResponse) {
                    return cachedResponse;
                }
                const offlinePage = await caches.match('/offline/');
                return offlinePage || new Response('Mode Hors-Ligne KINGLIFE SHAL U', {
                    headers: { 'Content-Type': 'text/html; charset=utf-8' }
                });
            })
    );
});

/* Web Push Notification Listener */
self.addEventListener('push', function(event) {
    let data = {
        title: 'KINGLIFE SHAL U',
        body: 'Nouvelle notification disponible.',
        url: '/',
        type: 'info'
    };

    if (event.data) {
        try {
            data = event.data.json();
        } catch (e) {
            data.body = event.data.text();
        }
    }

    const options = {
        body: data.body,
        icon: '/static/kinglife/images/logo.png',
        badge: '/static/kinglife/images/logo.png',
        data: {
            url: data.url || '/'
        },
        vibrate: [100, 50, 100],
        tag: 'kinglife-notification',
        renotify: true
    };

    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

/* Notification Click Handler */
self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    const targetUrl = (event.notification.data && event.notification.data.url) ? event.notification.data.url : '/';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function(clientList) {
            for (var i = 0; i < clientList.length; i++) {
                var client = clientList[i];
                if (client.url.includes(targetUrl) && 'focus' in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow(targetUrl);
            }
        })
    );
});
