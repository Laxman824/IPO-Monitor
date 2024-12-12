
self.addEventListener('push', function(event) {
    const options = {
        body: event.data.text(),
        icon: '/icon.png',
        badge: '/badge.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: '1'
        },
        actions: [
            {
                action: 'explore',
                title: 'View Details',
                icon: 'check.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: 'cross.png'
            }
        ]
    };

    event.waitUntil(
        self.registration.showNotification('IPO GMP Alert', options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    if (event.action === 'explore') {
        clients.openWindow("https://ipo-monitor-gmp.streamlit.app/Dashboard");
    }
});