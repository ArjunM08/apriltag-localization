import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

//General scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a1a);

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000,
);
camera.position.set(0, 3, 6);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.update();

//field plane
const fieldGeometry = new THREE.PlaneGeometry(10, 10);
const fieldMaterial = new THREE.MeshBasicMaterial({
  color: 0x333333,
  side: THREE.DoubleSide,
});
const field = new THREE.Mesh(fieldGeometry, fieldMaterial);
field.position.set(0, 0, -2);
scene.add(field);

//AprilTag
const tagGeometry = new THREE.BoxGeometry(0.8, 1, 0.05);
const tagMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const tagMesh = new THREE.Mesh(tagGeometry, tagMaterial);
tagMesh.position.set(0, 0, -2); // on the "wall"
tagMesh.rotation.y = 0;
scene.add(tagMesh);

//Camera box
const camGeometry = new THREE.BoxGeometry(0.4, 0.4, 0.6);
const camMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
const camMesh = new THREE.Mesh(camGeometry, camMaterial);
camMesh.position.set(0, 0.2, 2);
scene.add(camMesh);

//Heading line
const arrowHelper = new THREE.ArrowHelper(
  new THREE.Vector3(0, 0, 1), // default direction (forward in Three.js)
  camMesh.position, // origin at camera box
  1.5, // length
  0x0000ff, // color
);


scene.add(arrowHelper);

//Resize handler
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

//Animation loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();

  // keep arrow attached to camera box and facing the same direction as the camera box
  arrowHelper.position.copy(camMesh.position);

  const direction = new THREE.Vector3(0, 0, -1).applyQuaternion(camMesh.quaternion);
  direction.multiplyScalar(-1);
  arrowHelper.setDirection(direction);

  renderer.render(scene, camera);
}
animate();

// ── WebSocket ─────────────────────────────────────────────────────────────────
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = () => console.log("WebSocket connected");
ws.onerror = (e) => console.error("WebSocket error", e);
ws.onclose = () => console.warn("WebSocket closed");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  // update camera box position
  camMesh.position.set(data.x, data.y, data.z);

  // update rotation with matrix
  const R = data.R;
  const m = new THREE.Matrix4();
  m.set(
    R[0][0],
    R[0][1],
    R[0][2],
    0,
    R[1][0],
    R[1][1],
    R[1][2],
    0,
    R[2][0],
    R[2][1],
    R[2][2],
    0,
    0,
    0,
    0,
    1,
  );
  camMesh.setRotationFromMatrix(m);
};
