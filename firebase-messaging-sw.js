importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey: "AIzaSyBDzjtF1IsD_hgUSakl5SgJ0fNKwKncsPg",
    projectId: "main-navbharat",
    messagingSenderId: "658810373879",
    appId: "1:658810373879:web:4abd4eb8a94fc0b7b8b5f2"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log('[SW] Received background message:', payload);
    return self.registration.showNotification(payload.notification.title, {
        body: payload.notification.body,
        icon: payload.notification.icon
    });
});