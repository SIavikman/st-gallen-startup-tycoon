// Game Over Animation JavaScript
class GameAnimations {
    constructor() {
        this.overlay = null;
        this.init();
    }
    
    init() {
        // Erstelle das Game Over Overlay
        this.createGameOverOverlay();
    }
    
    createGameOverOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'game-over-overlay';
        overlay.className = 'go-overlay';
        overlay.innerHTML = `
            <div class="go-card">
                <h1 class="go-title">
                    GAME OVER
                    <span class="glitch">GAME OVER</span>
                </h1>
                <p class="go-sub" id="go-message">Danke fürs Spielen.</p>
                <div id="go-score" class="go-pill" style="display: none;">
                    <span class="go-dot"></span>
                    <span>Punktestand: <strong id="go-score-value">0</strong></span>
                </div>
                <div class="go-actions">
                    <button class="go-btn primary" onclick="gameAnimations.restart()">Nochmal spielen</button>
                    <button class="go-btn" onclick="gameAnimations.toLeaderboard()">Zum Leaderboard</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
        this.overlay = overlay;
    }
    
    showGameOver(playerName, score) {
        document.getElementById('go-message').textContent = `${playerName}'s St. Gallen Adventure ist zu Ende!`;
        if (score) {
            document.getElementById('go-score-value').textContent = score.toLocaleString('de-CH');
            document.getElementById('go-score').style.display = 'flex';
        }
        
        this.overlay.classList.add('is-open');
        document.documentElement.style.overflow = 'hidden';
    }
    
    hide() {
        this.overlay.classList.remove('is-open');
        document.documentElement.style.overflow = '';
    }
    
    restart() {
        this.hide();
        window.location.href = '/';
    }
    
    toLeaderboard() {
        this.hide();
        window.location.href = '/leaderboard';
    }
}

// Initialisiere die Animationen
let gameAnimations;
document.addEventListener('DOMContentLoaded', () => {
    gameAnimations = new GameAnimations();
});