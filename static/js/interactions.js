
// Interaction Scripts for Alpha Cooking Oil
// Uses VanillaTilt.js and GSAP

document.addEventListener('DOMContentLoaded', () => {

    // 1. Initialize VanillaTilt on cards
    if (typeof VanillaTilt !== 'undefined') {
        VanillaTilt.init(document.querySelectorAll(".product-showcase, .info-card, .feature-card, .retailer-card"), {
            max: 10,
            speed: 400,
            glare: true,
            "max-glare": 0.3,
            scale: 1.02
        });
    }

    // 2. GSAP Scroll Animations
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);

        // Animate Sections on scroll
        gsap.utils.toArray('.section').forEach(section => {
            gsap.from(section, {
                opacity: 0,
                y: 50,
                duration: 1,
                scrollTrigger: {
                    trigger: section,
                    start: "top 80%",
                    end: "top 50%",
                    toggleActions: "play none none reverse"
                }
            });
        });

        // Staggered animation for products
        gsap.from(".product-showcase", {
            opacity: 0,
            y: 50,
            duration: 0.8,
            stagger: 0.2,
            scrollTrigger: {
                trigger: ".products-grid",
                start: "top 75%"
            }
        });

        // Staggered animation for features
        gsap.from(".feature-card", {
            opacity: 0,
            scale: 0.9,
            duration: 0.6,
            stagger: 0.2,
            scrollTrigger: {
                trigger: ".features-grid",
                start: "top 75%"
            }
        });
    }
});
