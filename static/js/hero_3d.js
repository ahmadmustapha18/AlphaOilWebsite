
// 3D Hero Section for Alpha Cooking Oil
// Implements a fluid-like scene with floating golden bubbles using Three.js

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('hero-3d-container');
    if (!container) return;

    // SCENE SETUP
    const scene = new THREE.Scene();
    // No background — let CSS gradient show through

    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 15;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setClearColor(0x000000, 0);
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // LIGHTING
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xF6C343, 1.5); // Golden light
    pointLight.position.set(10, 10, 10);
    pointLight.castShadow = true;
    scene.add(pointLight);

    const pointLight2 = new THREE.PointLight(0xFFD84D, 0.8); // Additional warm light
    pointLight2.position.set(-10, -10, 5);
    scene.add(pointLight2);

    // HIGHLY OPTIMIZED BUBBLES
    const bubbles = [];
    const bubbleCount = 8; // Further reduced for smooth performance
    const geometry = new THREE.SphereGeometry(1, 16, 16); // Lower poly count

    // Simplified Material for better performance
    const material = new THREE.MeshStandardMaterial({
        color: 0xF6C343,
        metalness: 0.3,
        roughness: 0.2,
        transparent: true,
        opacity: 0.8
    });

    for (let i = 0; i < bubbleCount; i++) {
        const bubble = new THREE.Mesh(geometry, material);

        // Random positions (spread out more)
        bubble.position.x = (Math.random() - 0.5) * 50;
        bubble.position.y = (Math.random() - 0.5) * 35;
        bubble.position.z = (Math.random() - 0.5) * 25 - 5;

        // Random sizes
        const scale = Math.random() * 1.5 + 0.5;
        bubble.scale.set(scale, scale, scale);

        // Individual animation properties
        bubble.userData = {
            speedY: Math.random() * 0.02 + 0.005,
            speedX: (Math.random() - 0.5) * 0.01,
            wobbleSpeed: Math.random() * 0.05,
            wobbleOffset: Math.random() * Math.PI * 2,
            initialY: bubble.position.y
        };

        scene.add(bubble);
        bubbles.push(bubble);
    }

    // MOUSE INTERACTION
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX - windowHalfX) / 200;
        mouseY = (event.clientY - windowHalfY) / 200;
    });

    // ANIMATION LOOP
    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);

        const time = clock.getElapsedTime();

        targetX = mouseX * 2;
        targetY = mouseY * 2;

        // Smooth camera movement based on mouse
        camera.position.x += (mouseX * 5 - camera.position.x) * 0.05;
        camera.position.y += (-mouseY * 5 - camera.position.y) * 0.05;
        camera.lookAt(scene.position);

        bubbles.forEach((bubble) => {
            // Floating up
            bubble.position.y += bubble.userData.speedY;
            bubble.position.x += Math.sin(time * bubble.userData.wobbleSpeed + bubble.userData.wobbleOffset) * 0.01;

            // Reset if goes too high
            if (bubble.position.y > 15) {
                bubble.position.y = -20;
                bubble.position.x = (Math.random() - 0.5) * 40;
            }

            // Mouse repulsion/attraction can be added here
            // Simple rotation
            bubble.rotation.x += 0.001;
            bubble.rotation.y += 0.002;
        });

        renderer.render(scene, camera);
    }

    animate();

    // HANDLE RESIZE
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
});
