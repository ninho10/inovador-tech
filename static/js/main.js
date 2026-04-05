/**
 * Lógica principal do site Inovador Tech
 * Main logic for Inovador Tech website
 */

document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('mainNav');
    const cursor = document.getElementById('custom-cursor');
    const cursorGlow = document.getElementById('cursor-glow');

    // Movimentação do Cursor Customizado
    // Custom Cursor Movement
    document.addEventListener('mousemove', (e) => {
        // Mostra o cursor ao mover o mouse
        cursor.style.display = 'block';
        cursorGlow.style.display = 'block';
        
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        
        // O brilho segue com um leve atraso
        cursorGlow.style.left = (e.clientX - 15) + 'px';
        cursorGlow.style.top = (e.clientY - 15) + 'px';
    });

    // Esconde o cursor quando o mouse sai da janela
    document.addEventListener('mouseleave', () => {
        cursor.style.display = 'none';
        cursorGlow.style.display = 'none';
    });

    // Efeito de clique no cursor
    // Cursor click effect
    document.addEventListener('mousedown', () => cursor.style.transform = 'scale(0.8)');
    document.addEventListener('mouseup', () => cursor.style.transform = 'scale(1)');

    // Altera o fundo da navbar ao rolar a página
    // Changes navbar background on scroll
    window.onscroll = () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };

    // Inicialização do TSParticles
    // TSParticles Initialization
    if (typeof tsParticles !== 'undefined') {
        tsParticles.load("tsparticles", {
            fpsLimit: 60,
            particles: {
                number: { value: 60, density: { enable: true, value_area: 800 } },
                color: { value: "#00f3ff" },
                shape: { type: "circle" },
                opacity: { value: 0.3, random: true },
                size: { value: 2, random: true },
                links: {
                    enable: true,
                    distance: 150,
                    color: "#00f3ff",
                    opacity: 0.1,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 0.8,
                    direction: "none",
                    random: false,
                    straight: false,
                    out_mode: "out",
                    bounce: false,
                }
            },
            interactivity: {
                detect_on: "canvas",
                events: {
                    onhover: { enable: true, mode: "grab" },
                    onclick: { enable: true, mode: "push" },
                    resize: true
                },
                modes: {
                    grab: { distance: 140, line_linked: { opacity: 0.5 } },
                    push: { particles_nb: 4 }
                }
            },
            retina_detect: true
        });
    }

    // Smooth scroll para links internos
    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    console.log("Inovador Tech: Interface de Alta Tecnologia Pronta!");
});
