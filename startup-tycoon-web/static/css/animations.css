/* Game Over & Success Animation CSS for St. Gallen Startup Tycoon */
:root {
  --bg: #0b0b10;
  --accent: #ff2d55;
  --accent-2: #ffcc00;
  --success-accent: #00ff88;
  --success-accent-2: #00cc44;
  --text: #e6e6ee;
}

/* Base reset for animations */
* { box-sizing: border-box; }

/* Game Over & Success Overlays */
.go-overlay {
  position: fixed;
  inset: 0;
  display: none;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(6px) saturate(120%);
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(255, 45, 85, 0.15), transparent 60%),
    radial-gradient(800px 400px at 50% 110%, rgba(255, 204, 0, 0.1), transparent 60%),
    rgba(7, 7, 10, 0.7);
  z-index: 9999;
  overflow: hidden;
}

.success-overlay {
  position: fixed;
  inset: 0;
  display: none;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(6px) saturate(130%);
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(0, 255, 136, 0.15), transparent 60%),
    radial-gradient(800px 400px at 50% 110%, rgba(0, 204, 68, 0.1), transparent 60%),
    rgba(7, 12, 7, 0.8);
  z-index: 9999;
  overflow: hidden;
}

.go-overlay.is-open, 
.success-overlay.is-open { 
  display: flex; 
}

/* Scanlines / CRT retro effect for both overlays */
.go-overlay::before,
.success-overlay::before {
  content: "";
  position: absolute; 
  inset: 0;
  background: repeating-linear-gradient(
    to bottom,
    rgba(255,255,255,0.04) 0px,
    rgba(255,255,255,0.04) 1px,
    transparent 2px,
    transparent 3px
  );
  mix-blend-mode: overlay;
  pointer-events: none;
  animation: flicker 2.5s infinite linear;
}

@keyframes flicker {
  0%, 19%, 21%, 23%, 80%, 100% { opacity: 0.6; }
  20%, 22% { opacity: 0.2; }
  24%, 25% { opacity: 0.8; }
}

/* Main card containers - Game Over & Success */
.go-card,
.success-card {
  position: relative;
  width: min(92vw, 680px);
  padding: 44px 28px 28px;
  border-radius: 24px;
  text-align: center;
  color: var(--text);
  overflow: hidden;
  transform: translateY(16px) scale(0.98);
  opacity: 0;
  animation: card-in 420ms cubic-bezier(.2,.9,.2,1) forwards;
}

/* Game Over styling */
.go-card {
  background: linear-gradient(180deg, rgba(22,22,30,0.95), rgba(10,10,14,0.95));
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.6),
    0 0 0 1px rgba(255, 255, 255, 0.06),
    0 0 80px 0 rgba(255, 45, 85, 0.25) inset;
}

/* Success styling */
.success-card {
  background: linear-gradient(180deg, rgba(14,30,18,0.95), rgba(8,20,10,0.95));
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.6),
    0 0 0 1px rgba(255, 255, 255, 0.06),
    0 0 80px 0 rgba(0, 255, 136, 0.25) inset;
}

@keyframes card-in {
  to { 
    opacity: 1; 
    transform: translateY(0) scale(1); 
  }
}

/* Game Over & Success titles with effects */
.go-title,
.success-title {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: clamp(42px, 8vw, 92px);
  letter-spacing: 0.06em;
  margin: 0 0 10px;
  font-weight: 800;
  position: relative;
  color: var(--text);
}

/* Game Over styling */
.go-title {
  text-shadow:
    0 0 22px rgba(255, 45, 85, 0.4),
    0 0 44px rgba(255, 204, 0, 0.15);
  animation: title-fade 1200ms ease-out forwards, glow-pulse 2200ms ease-in-out infinite;
}

/* Success styling */
.success-title {
  text-shadow:
    0 0 22px rgba(0, 255, 136, 0.4),
    0 0 44px rgba(0, 204, 68, 0.15);
  animation: title-fade 1200ms ease-out forwards, success-glow-pulse 2200ms ease-in-out infinite;
}

@keyframes title-fade { 
  from { 
    opacity: 0; 
    letter-spacing: -0.03em; 
    filter: blur(6px);
  } 
  to { 
    opacity: 1; 
    letter-spacing: .06em; 
    filter: blur(0);
  } 
}

/* Glow Animations */
@keyframes glow-pulse { 
  0%,100% { 
    text-shadow: 0 0 16px rgba(255,45,85,.35), 0 0 36px rgba(255,204,0,.12);
  } 
  50% { 
    text-shadow: 0 0 28px rgba(255,45,85,.55), 0 0 64px rgba(255,204,0,.2);
  } 
}

@keyframes success-glow-pulse { 
  0%,100% { 
    text-shadow: 0 0 16px rgba(0,255,136,.35), 0 0 36px rgba(0,204,68,.12);
  } 
  50% { 
    text-shadow: 0 0 28px rgba(0,255,136,.55), 0 0 64px rgba(0,204,68,.2);
  } 
}

/* Glitch overlay effect */
.go-title .glitch {
  position: absolute; 
  inset: 0; 
  color: var(--accent);
  text-shadow: 2px 0 var(--accent), -2px 0 #00e6ff;
  mix-blend-mode: screen; 
  opacity: 0.18;
  animation: glitch-shift 900ms infinite steps(2);
  pointer-events: none;
}

/* Sparkle effect for success */
.success-title .sparkle {
  position: absolute; 
  inset: 0; 
  color: var(--success-accent);
  text-shadow: 2px 0 var(--success-accent), -2px 0 #00ffaa;
  mix-blend-mode: screen; 
  opacity: 0.25;
  animation: sparkle-shift 1200ms infinite ease-in-out;
  pointer-events: none;
}

@keyframes glitch-shift {
  0%   { transform: translate(0,0); clip-path: inset(0 0 0 0); }
  20%  { transform: translate(-2px,-1px); clip-path: inset(0 0 40% 0); }
  40%  { transform: translate(2px,1px); clip-path: inset(60% 0 0 0); }
  60%  { transform: translate(-1px,1px); clip-path: inset(10% 0 30% 0); }
  80%  { transform: translate(1px,-1px); clip-path: inset(30% 0 50% 0); }
  100% { transform: translate(0,0); clip-path: inset(0 0 0 0); }
}

@keyframes sparkle-shift {
  0%, 100%   { transform: translate(0,0) scale(1); opacity: 0.25; }
  25%  { transform: translate(1px,-1px) scale(1.02); opacity: 0.4; }
  50%  { transform: translate(-1px,1px) scale(0.98); opacity: 0.15; }
  75%  { transform: translate(1px,1px) scale(1.01); opacity: 0.35; }
}

/* Subtitle text */
.go-sub,
.success-sub {
  margin: 6px 0 18px;
  font-size: clamp(14px, 2.2vw, 18px);
  opacity: 0.92;
  color: var(--text);
}

/* Score display pill */
.go-pill,
.success-pill {
  display: inline-flex; 
  align-items: center; 
  gap: 10px;
  padding: 10px 14px; 
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.08);
  margin: 6px 0 22px;
  font-size: 14px; 
  letter-spacing: .02em;
  color: var(--text);
}

/* Game Over pill */
.go-pill {
  background: linear-gradient(180deg, rgba(255,45,85,0.12), rgba(255,45,85,0.05));
}

/* Success pill */
.success-pill {
  background: linear-gradient(180deg, rgba(0,255,136,0.12), rgba(0,255,136,0.05));
}

.go-dot { 
  width: 8px; 
  height: 8px; 
  border-radius: 50%; 
  background: var(--accent); 
  box-shadow: 0 0 14px rgba(255,45,85,.8); 
}

.success-dot { 
  width: 8px; 
  height: 8px; 
  border-radius: 50%; 
  background: var(--success-accent); 
  box-shadow: 0 0 14px rgba(0,255,136,.8); 
}

/* Button container */
.go-actions,
.success-actions { 
  display: flex; 
  gap: 12px; 
  justify-content: center; 
  flex-wrap: wrap; 
}

/* Button styling */
.go-btn {
  --btn-bg: rgba(255,255,255,0.04);
  --btn-bd: rgba(255,255,255,0.12);
  appearance: none; 
  border: 1px solid var(--btn-bd); 
  background: var(--btn-bg);
  color: var(--text); 
  padding: 12px 18px; 
  border-radius: 14px; 
  cursor: pointer;
  font-weight: 600; 
  letter-spacing: .02em; 
  font-size: 15px;
  font-family: inherit;
  transition: transform .15s ease, box-shadow .2s ease, background .2s ease, border-color .2s ease;
  box-shadow: 0 6px 18px rgba(0,0,0,.25);
}

.go-btn:hover { 
  transform: translateY(-1px); 
  border-color: rgba(255,255,255,0.22); 
  box-shadow: 0 8px 22px rgba(0,0,0,.35); 
}

.go-btn:active { 
  transform: translateY(0); 
}

.go-btn.primary { 
  --btn-bg: linear-gradient(180deg, rgba(255,45,85,0.22), rgba(255,45,85,0.12)); 
  border-color: rgba(255,45,85,0.6); 
}

.go-btn.primary:hover {
  border-color: rgba(255,45,85,0.8);
  background: linear-gradient(180deg, rgba(255,45,85,0.3), rgba(255,45,85,0.18));
}

.go-btn.success { 
  --btn-bg: linear-gradient(180deg, rgba(0,255,136,0.22), rgba(0,255,136,0.12)); 
  border-color: rgba(0,255,136,0.6); 
}

.go-btn.success:hover {
  border-color: rgba(0,255,136,0.8);
  background: linear-gradient(180deg, rgba(0,255,136,0.3), rgba(0,255,136,0.18));
}

/* Subtle corner glow effect for Game Over */
.go-card::after {
  content: ""; 
  position: absolute; 
  inset: -2px; 
  pointer-events: none;
  background: radial-gradient(250px 120px at 0% 0%, rgba(255,45,85,.22), transparent 60%),
              radial-gradient(250px 120px at 100% 100%, rgba(255,204,0,.18), transparent 60%);
  filter: blur(18px); 
  opacity: 0.9; 
  mix-blend-mode: screen;
}

/* Success corner glow effect */
.success-card::after {
  content: ""; 
  position: absolute; 
  inset: -2px; 
  pointer-events: none;
  background: radial-gradient(250px 120px at 0% 0%, rgba(0,255,136,.22), transparent 60%),
              radial-gradient(250px 120px at 100% 100%, rgba(0,204,68,.18), transparent 60%);
  filter: blur(18px); 
  opacity: 0.9; 
  mix-blend-mode: screen;
}

/* Confetti Animation */
.confetti {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
}

.confetti-piece {
  position: absolute;
  width: 8px;
  height: 8px;
  background: var(--success-accent);
  animation: confetti-fall 3s linear infinite;
  border-radius: 2px;
}

.confetti-piece:nth-child(odd) {
  background: var(--success-accent-2);
  animation-duration: 2.5s;
  width: 6px;
  height: 12px;
}

.confetti-piece:nth-child(3n) {
  background: #ffcc00;
  animation-duration: 4s;
  border-radius: 50%;
}

.confetti-piece:nth-child(4n) {
  background: #ff6b6b;
  animation-duration: 3.5s;
  width: 10px;
  height: 4px;
}

.confetti-piece:nth-child(5n) {
  background: #4ecdc4;
  animation-duration: 2.8s;
  border-radius: 50%;
  width: 6px;
  height: 6px;
}

@keyframes confetti-fall {
  0% {
    transform: translateY(-100vh) rotateZ(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotateZ(360deg);
    opacity: 0;
  }
}

/* Accessibility: reduce animations for users who prefer less motion */
@media (prefers-reduced-motion: reduce) {
  .go-overlay::before, 
  .success-overlay::before,
  .go-title,
  .success-title, 
  .go-card,
  .success-card,
  .glitch,
  .sparkle,
  .confetti-piece {
    animation: none !important;
  }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .go-card,
  .success-card {
    padding: 32px 20px 20px;
    margin: 10px;
  }
  
  .go-title,
  .success-title {
    font-size: clamp(32px, 10vw, 72px);
  }
  
  .go-actions,
  .success-actions {
    flex-direction: column;
  }
  
  .go-btn {
    width: 100%;
    padding: 16px 18px;
  }
}

/* Dark theme compatibility */
@media (prefers-color-scheme: dark) {
  :root {
    --text: #f0f0f8;
  }
}
