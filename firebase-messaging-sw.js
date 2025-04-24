importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey: "AIzaSyDeeTLSC1ta_j1ePLqprMTFa6SlznNFKE0",
    projectId: "navbharattest-ff0c0",
    messagingSenderId: "254125828844",
    appId: "1:254125828844:web:b155c8317d6c412b5a93c9"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log('[SW] Received background message:', payload);
    return self.registration.showNotification(payload.notification.title, {
        body: payload.notification.body,
        icon: payload.notification.icon
    });
});