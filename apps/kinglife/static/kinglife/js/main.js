/* KINGLIFE SHAL U - Main JavaScript Interactivity */

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
    // Mobile Navbar Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const headerActions = document.querySelector('.header-actions');
    
    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            const isOpen = navMenu.classList.toggle('active');
            if (headerActions) headerActions.classList.toggle('active');
            mobileToggle.innerHTML = isOpen ? '✕' : '☰';
            document.body.style.overflow = isOpen ? 'hidden' : '';
        });

        // Close mobile menu when clicking a nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                if (headerActions) headerActions.classList.remove('active');
                mobileToggle.innerHTML = '☰';
                document.body.style.overflow = '';
            });
        });
    }
});
