self.addEventListener("install", e => {
    console.log("Service Worker Installed.");
});

self.addEventListener("activate", e => {
    console.log("Service Worker Activated.");
});

self.addEventListener("push", event => {
    const data = event.data.json();
    event.waitUntil(
        self.registration.showNotification(data.title, {
            body: data.body,
            icon: data.icon,
            badge: data.badge,
            data: {url: data.url}
        })
    );
});

self.addEventListener("notificationclick", event => {
    event.notification.close();
    event.waitUntil(clients.openWindow(event.notification.data.url));
});
