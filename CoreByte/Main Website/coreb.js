// Navigation Scroll Effect
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');

mobileMenuBtn.addEventListener('click', function() {
    mobileMenuBtn.classList.toggle('active');
    mobileMenu.classList.toggle('active');
});

// Close mobile menu when clicking on links
const mobileLinks = document.querySelectorAll('.mobile-link');
mobileLinks.forEach(link => {
    link.addEventListener('click', function() {
        mobileMenuBtn.classList.remove('active');
        mobileMenu.classList.remove('active');
    });
});

// Smooth scroll to section
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        const navHeight = document.getElementById('navbar').offsetHeight;
        const elementPosition = element.offsetTop - navHeight;
        window.scrollTo({
            top: elementPosition,
            behavior: 'smooth'
        });
    }
}

// Navigation links smooth scroll
const navLinks = document.querySelectorAll('.nav-link, .mobile-link');
navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        scrollToSection(targetId);
    });
});

// Contact Form Handling
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    };
    
    // Mock form submission
    showToast('Message Sent! Thank you for reaching out. We\'ll get back to you soon.');
    
    // Reset form
    contactForm.reset();
});

// Toast Notification
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe animated elements
const animatedElements = document.querySelectorAll('.animate-fade-in-up, .animate-fade-in, .animate-slide-in-left, .animate-slide-in-right');
animatedElements.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    observer.observe(element);
});

// Add hover effect to cards
const cards = document.querySelectorAll('.game-card, .feature-card');
cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.borderColor = 'var(--primary)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.borderColor = 'var(--border)';
    });
});

// Console log for development
console.log('%cCoreB yte Studios', 'color: #00D9FF; font-size: 24px; font-weight: bold;');
console.log('%cGaming Website Loaded Successfully', 'color: #39FF14; font-size: 14px;');