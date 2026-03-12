
// 3D Product Viewer using Three.js
// Renders a rotating 3D cylinder textured with the product image in a modal

document.addEventListener('DOMContentLoaded', () => {
    // Create Modal Elements
    const modal = document.createElement('div');
    modal.id = 'product-3d-modal';
    Object.assign(modal.style, {
        display: 'none',
        position: 'fixed',
        zIndex: '2000',
        left: '0',
        top: '0',
        width: '100%',
        height: '100%',
        overflow: 'hidden',
        backgroundColor: 'rgba(0,0,0,0.8)',
        backdropFilter: 'blur(5px)',
        alignItems: 'center',
        justifyContent: 'center'
    });

    const modalContent = document.createElement('div');
    Object.assign(modalContent.style, {
        position: 'relative',
        width: '80%',
        maxWidth: '600px',
        height: '60%',
        backgroundColor: '#fff',
        borderRadius: '20px',
        overflow: 'hidden',
        boxShadow: '0 0 50px rgba(246, 195, 67, 0.5)'
    });

    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = '&times;';
    Object.assign(closeBtn.style, {
        position: 'absolute',
        top: '10px',
        right: '25px',
        color: '#333',
        fontSize: '40px',
        fontWeight: 'bold',
        cursor: 'pointer',
        zIndex: '10'
    });

    const canvasContainer = document.createElement('div');
    canvasContainer.id = 'canvas-container-3d';
    canvasContainer.style.width = '100%';
    canvasContainer.style.height = '100%';

    modalContent.appendChild(closeBtn);
    modalContent.appendChild(canvasContainer);
    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    // Three.js Variables
    let scene, camera, renderer, bottle;
    let animationId;

    // Close Modal
    function closeModal() {
        modal.style.display = 'none';
        if (animationId) cancelAnimationFrame(animationId);
        if (renderer) {
            renderer.dispose();
            canvasContainer.innerHTML = '';
        }
    }

    closeBtn.onclick = closeModal;
    window.onclick = function (event) {
        if (event.target == modal) {
            closeModal();
        }
    }

    // Launch Viewer Function
    window.launch3DViewer = function (imageUrl) {
        modal.style.display = 'flex';
        init3DScene(imageUrl);
    }

    function init3DScene(textureUrl) {
        const container = document.getElementById('canvas-container-3d');
        const width = container.clientWidth;
        const height = container.clientHeight;

        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff);

        camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
        camera.position.z = 5;

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(width, height);
        container.appendChild(renderer.domElement);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
        dirLight.position.set(2, 2, 5);
        scene.add(dirLight);

        // Bottle Geometry (Simple Cylinder for now)
        const geometry = new THREE.CylinderGeometry(0.8, 0.8, 2.5, 32);

        // Texture
        const textureLoader = new THREE.TextureLoader();
        // Use a placeholder or the actual image if it works as a texture (might wrap weirdly but proves the concept)
        // Ideally we'd map specifically, but for "cool factor" wrapping is often enough
        textureLoader.load(textureUrl, (texture) => {
            const material = new THREE.MeshStandardMaterial({
                map: texture,
                metalness: 0.1,
                roughness: 0.3
            });
            bottle = new THREE.Mesh(geometry, material);
            scene.add(bottle);
            animate();
        });
    }

    function animate() {
        animationId = requestAnimationFrame(animate);
        if (bottle) {
            bottle.rotation.y += 0.01;
            bottle.rotation.x = 0.1; // Slight tilt
        }
        renderer.render(scene, camera);
    }
});
