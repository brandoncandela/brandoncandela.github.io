import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { gsap } from 'gsap';
// Adapted from itsyujay/apple-style-portfolio (MIT).
export default function Scene3D() {
 const ref = useRef<HTMLDivElement>(null);
 useEffect(() => {
  const host = ref.current;
  if (!host) return;
  let renderer: THREE.WebGLRenderer;
  try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); } catch { return; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  host.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, 1, .1, 100);
  camera.position.z = 5;
  const geometry = new THREE.SphereGeometry(1, 24, 24);
  const material = new THREE.MeshPhongMaterial({ color: 0x5aa9ff, transparent: true, opacity: .32 });
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const positions = [[-6,2,-8,.7],[6,1,-8,.9],[-5,-3,-7,.5],[5,-3,-9,.7],[-2,4,-12,.4]];
  const spheres = positions.map(([x,y,z,scale]) => {
   const mesh = new THREE.Mesh(geometry, material); mesh.position.set(x,y,z); mesh.scale.setScalar(scale); scene.add(mesh); return mesh;
  });
  scene.add(new THREE.AmbientLight(0xffffff, .7));
  const light = new THREE.DirectionalLight(0xffffff, 1); light.position.set(5,5,5); scene.add(light);
  let frame = 0;
  let active = true;
  let tweens: gsap.core.Tween[] = [];
  const render = () => renderer.render(scene, camera);
  const animate = () => { render(); frame = requestAnimationFrame(animate); };
  const update = () => {
   cancelAnimationFrame(frame); tweens.forEach(t => t.kill()); tweens = [];
   if (!motion.matches && active && !document.hidden) {
    tweens = spheres.map((s,i) => gsap.to(s.position, {y: positions[i][1]+.6, duration: 3+i*.3, yoyo:true, repeat:-1, ease:'sine.inOut'}));
    animate();
   } else render();
  };
  const resize = () => { camera.aspect=host.clientWidth/Math.max(host.clientHeight,1); camera.updateProjectionMatrix(); renderer.setSize(host.clientWidth,host.clientHeight); render(); };
  const ro = new ResizeObserver(resize); ro.observe(host);
  const io = new IntersectionObserver(([entry]) => {active=entry.isIntersecting;update();}); io.observe(host);
  motion.addEventListener('change',update); document.addEventListener('visibilitychange',update); resize(); update();
  return () => {cancelAnimationFrame(frame);tweens.forEach(t=>t.kill());ro.disconnect();io.disconnect();motion.removeEventListener('change',update);document.removeEventListener('visibilitychange',update);geometry.dispose();material.dispose();renderer.dispose();renderer.domElement.remove();};
 }, []);
 return <div ref={ref} style={{position:'absolute',inset:0}} />;
}
