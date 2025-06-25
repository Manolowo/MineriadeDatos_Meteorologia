// Menú móvil
document.addEventListener('DOMContentLoaded', function() {
  const navbarToggler = document.querySelector('.navbar-toggler');
  const navbarCollapse = document.querySelector('.navbar-collapse');
  
  if (navbarToggler && navbarCollapse) {
    navbarToggler.addEventListener('click', function() {
      navbarCollapse.classList.toggle('active');
      this.classList.toggle('active');
    });
  }
  
  // Smooth scrolling para enlaces del menú
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80,
          behavior: 'smooth'
        });
        
        // Cerrar menú móvil si está abierto
        if (navbarCollapse.classList.contains('active')) {
          navbarCollapse.classList.remove('active');
          navbarToggler.classList.remove('active');
        }
      }
    });
  });
  
  // Cambiar estilo del menú al hacer scroll
  window.addEventListener('scroll', function() {
    const menu = document.querySelector('.menu-container');
    if (window.scrollY > 50) {
      menu.style.background = 'rgba(255, 255, 255, 0.98)';
      menu.style.boxShadow = '0 2px 15px rgba(0, 0, 0, 0.1)';
    } else {
      menu.style.background = 'rgba(255, 255, 255, 0.95)';
      menu.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
  });
  
  // Animación al hacer scroll
  const animateOnScroll = function() {
    const elements = document.querySelectorAll('.service-card, .feature-card');
    
    elements.forEach(element => {
      const elementPosition = element.getBoundingClientRect().top;
      const screenPosition = window.innerHeight / 1.2;
      
      if (elementPosition < screenPosition) {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
      }
    });
  };
  
  // Configurar elementos animados
  document.querySelectorAll('.service-card, .feature-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  });
  
  window.addEventListener('scroll', animateOnScroll);
  animateOnScroll();
});