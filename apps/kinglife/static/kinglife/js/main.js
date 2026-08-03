// PWA Deferred Installation Prompt Handler
let deferredPwaPrompt = null;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPwaPrompt = e;
    console.log("PWA install prompt captured");
});

function triggerPwaInstallPrompt() {
    if (deferredPwaPrompt) {
        deferredPwaPrompt.prompt();
        deferredPwaPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                if (typeof showToast === 'function') showToast("🎉 Merci d'avoir installé l'application KINGLIFE !", "success");
            }
            deferredPwaPrompt = null;
        });
    } else {
        if (typeof showToast === 'function') {
            showToast("📱 Pour installer l'application : Cliquez sur le menu de votre navigateur (3 points ou Partager) puis 'Ajouter à l'écran d'accueil'.", "info", 8000);
        } else {
            alert("📱 Pour installer l'application : Cliquez sur le menu de votre navigateur puis 'Ajouter à l'écran d'accueil'.");
        }
    }
}

function markSingleSiteNotifRead(notifId) {
    const card = document.getElementById('site-notif-card-' + notifId) || document.getElementById('notif-card-' + notifId);
    if (card) {
        card.style.transition = 'opacity 0.3s, transform 0.3s';
        card.style.opacity = '0.3';
    }

    fetch("/notifications/marquer-lues/", {
        method: 'POST',
        headers: {
            'X-CSRFToken': (typeof getCookie === 'function') ? getCookie('csrftoken') : '',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ notif_id: notifId })
    }).then(res => res.json()).then(data => {
        if (card) card.remove();
        const badge = document.getElementById('site-notif-badge') || document.getElementById('notif-badge');
        if (badge && typeof data.unread_count !== 'undefined') {
            if (data.unread_count > 0) {
                badge.innerText = data.unread_count;
            } else {
                badge.style.display = 'none';
            }
        }
        if (typeof showToast === 'function') showToast("✓ Notification marquée comme lue", "info", 2000);
    });
}
function markSingleNotifRead(notifId) {
    markSingleSiteNotifRead(notifId);
}

// Global Mobile Side Drawer Toggle for Bottom Nav & Header
function toggleMobileDrawerMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const headerActions = document.querySelector('.header-actions');
    const mobileToggle = document.querySelector('.mobile-toggle');

    if (navMenu) {
        const isOpen = navMenu.classList.toggle('active');
        if (headerActions) headerActions.classList.toggle('active');
        if (mobileToggle) mobileToggle.innerHTML = isOpen ? '✕' : '☰';
        document.body.style.overflow = isOpen ? 'hidden' : '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Header Scroll Effect
    const header = document.querySelector('.main-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // Scroll To Top
    const backToTopBtn = document.querySelector('.back-to-top');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Scroll Down Indicator
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            const businessSection = document.querySelector('.business-section');
            if (businessSection) {
                businessSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Business Slider Arrows (Simulated horizontal scroll / sliding)
    const prevBtn = document.querySelector('.slider-btn-prev');
    const nextBtn = document.querySelector('.slider-btn-next');
    const cardsGrid = document.querySelector('.business-cards-grid');

    if (prevBtn && nextBtn && cardsGrid) {
        nextBtn.addEventListener('click', () => {
            cardsGrid.scrollBy({ left: 300, behavior: 'smooth' });
        });
        prevBtn.addEventListener('click', () => {
            cardsGrid.scrollBy({ left: -300, behavior: 'smooth' });
        });
    }

    // Mobile Navbar Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            toggleMobileDrawerMenu();
        });

        // Close mobile menu when clicking a nav link or mobile auth button
        document.querySelectorAll('.nav-link, .mobile-user-btn').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                const headerActions = document.querySelector('.header-actions');
                if (headerActions) headerActions.classList.remove('active');
                if (mobileToggle) mobileToggle.innerHTML = '☰';
                document.body.style.overflow = '';
            });
        });
    }
});


/* PWA Install Prompt Logic */
let deferredPrompt;

// Capture beforeinstallprompt event
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;

    const pwaWidget = document.getElementById('pwa-install-widget');
    if (pwaWidget && !sessionStorage.getItem('pwa_banner_dismissed')) {
        setTimeout(() => {
            pwaWidget.classList.remove('hidden');
            pwaWidget.classList.add('show');
        }, 1200);
    }

    const preloaderInstallBtn = document.getElementById('preloader-pwa-install-btn');
    if (preloaderInstallBtn) {
        preloaderInstallBtn.style.display = 'inline-block';
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const pwaWidget = document.getElementById('pwa-install-widget');
    const pwaInstallBtn = document.getElementById('pwa-install-btn');
    const pwaCloseBtn = document.getElementById('pwa-close-btn');
    const iosHint = document.getElementById('pwa-ios-instructions');

    // Detect iOS
    const isIos = /iphone|ipad|ipod/i.test(window.navigator.userAgent);
    const isStandalone = window.navigator.standalone || window.matchMedia('(display-mode: standalone)').matches;

    if (isIos && !isStandalone && pwaWidget && !sessionStorage.getItem('pwa_banner_dismissed')) {
        setTimeout(() => {
            pwaWidget.classList.remove('hidden');
            pwaWidget.classList.add('show');
            if (iosHint) iosHint.classList.remove('hidden');
            if (pwaInstallBtn) pwaInstallBtn.style.display = 'none';
        }, 1500);
    }

    // Install Button Click Handler
    if (pwaInstallBtn) {
        pwaInstallBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                deferredPrompt = null;
                if (pwaWidget) {
                    pwaWidget.classList.remove('show');
                    setTimeout(() => pwaWidget.classList.add('hidden'), 500);
                }
            } else {
                alert("Pour installer l'application : utilisez le menu de votre navigateur (ex: 'Ajouter à l'écran d'accueil' ou 'Installer l'application').");
            }
        });
    }

    // Close Button Click Handler
    if (pwaCloseBtn && pwaWidget) {
        pwaCloseBtn.addEventListener('click', () => {
            pwaWidget.classList.remove('show');
            setTimeout(() => pwaWidget.classList.add('hidden'), 500);
            sessionStorage.setItem('pwa_banner_dismissed', 'true');
        });
    }

    // Preloader Install Button
    const preloaderInstallBtn = document.getElementById('preloader-pwa-install-btn');
    if (preloaderInstallBtn) {
        preloaderInstallBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                await deferredPrompt.userChoice;
                deferredPrompt = null;
                preloaderInstallBtn.style.display = 'none';

                const preloader = document.getElementById('kinglife-preloader');
                if (preloader) {
                    preloader.style.opacity = '0';
                    setTimeout(() => { preloader.style.display = 'none'; }, 500);
                }
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // Preloader logic
    const preloader = document.getElementById('kinglife-preloader');
    if (preloader) {
        if (!sessionStorage.getItem('kinglife_preloader_shown')) {
            const message = document.querySelector('.kl-preloader-message');
            if (message) {
                setTimeout(() => {
                    message.textContent = "Préparation de votre espace...";
                }, 800);
            }

            setTimeout(() => {
                if (preloader.style.display !== 'none') {
                    preloader.style.opacity = '0';
                    setTimeout(() => { preloader.style.display = 'none'; }, 500);
                }
                sessionStorage.setItem('kinglife_preloader_shown', 'true');
            }, 1200);
        } else {
            preloader.style.display = 'none';
        }
    }
});


/* ==========================================================================
   WEB PUSH NOTIFICATION CLIENT & TEST BUTTON
   ========================================================================== */
function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

async function registerWebPushSubscription() {
    if (!('serviceWorker' in navigator) || !('PushManager' in window)) return;

    try {
        const registration = await navigator.serviceWorker.ready;
        let subscription = await registration.pushManager.getSubscription();

        if (!subscription && Notification.permission === 'granted') {
            const vapidPublicKey = 'BJ4iNXUZBrhY_hjNW0gaiSGhDrYb1ARJAk-Q7ezyiyHyPeuZxtPPob-zuxeuUAhQxlqHgETkmwkN8w2Qh5kRPFk';
            const convertedVapidKey = urlBase64ToUint8Array(vapidPublicKey);

            subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: convertedVapidKey
            });
        }

        if (subscription) {
            await fetch('/api/push/subscribe/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ subscription: subscription })
            });
        }
    } catch (err) {
        console.warn('Notice WebPush subscription:', err);
    }
}

async function requestPushPermissionAndSubscribe() {
    if (!('Notification' in window)) return;
    if (Notification.permission === 'default') {
        const permission = await Notification.requestPermission();
        if (permission === 'granted') {
            await registerWebPushSubscription();
        }
    } else if (Notification.permission === 'granted') {
        await registerWebPushSubscription();
    }
}

async function testPushNotification() {
    if ('Notification' in window && Notification.permission !== 'granted') {
        const permission = await Notification.requestPermission();
        if (permission !== 'granted') {
            alert("Veuillez autoriser les notifications dans votre navigateur pour tester la fonctionnalité !");
            return;
        }
    }

    await registerWebPushSubscription();

    try {
        const response = await fetch('/api/push/test/', { method: 'POST' });
        const res = await response.json();
        if (res.status === 'success') {
            if (typeof showToast === 'function') {
                showToast("🔔 Notification Push de test envoyée !", "success");
            } else {
                alert("🔔 Notification Push de test envoyée ! Regardez les notifications de votre appareil.");
            }
        } else {
            alert("Notice : " + (res.message || "Impossible d'envoyer la notification"));
        }
    } catch (e) {
        console.error(e);
        alert("Erreur lors du test de notification push.");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    requestPushPermissionAndSubscribe();

    document.querySelectorAll('.btn-test-push-notif').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            testPushNotification();
        });
    });
});
