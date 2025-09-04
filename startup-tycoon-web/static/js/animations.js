// Game Over & Success Animation JavaScript
class GameAnimations {
    constructor() {
        this.gameOverOverlay = null;
        this.successOverlay = null;
        this.init();
    }
    
    init() {
        this.createGameOverOverlay();
        this.createSuccessOverlay();
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
        this.gameOverOverlay = overlay;
    }
    
    createSuccessOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'success-overlay';
        overlay.className = 'success-overlay';
        overlay.innerHTML = `
            <div class="confetti" id="confetti-container"></div>
            <div class="success-card">
                <h1 class="success-title">
                    GRATULIERE!
                    <span class="sparkle">GRATULIERE!</span>
                </h1>
                <p class="success-sub" id="success-message">Du hast alle 12 Monate in St. Gallen überlebt!</p>
                <div id="success-score" class="success-pill" style="display: none;">
                    <span class="success-dot"></span>
                    <span>Endpunktzahl: <strong id="success-score-value">0</strong></span>
                </div>
                <div class="success-actions">
                    <button class="go-btn success" onclick="gameAnimations.restart()">Nochmal spielen</button>
                    <button class="go-btn" onclick="gameAnimations.toLeaderboard()">Zum Leaderboard</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
        this.successOverlay = overlay;
    }
    
    createConfetti() {
        const container = document.getElementById('confetti-container');
        if (!container) return;
        
        // Clear existing confetti
        container.innerHTML = '';
        
        // Create 50 confetti pieces
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti-piece';
            
            // Random horizontal position
            confetti.style.left = Math.random() * 100 + '%';
            
            // Random delay for staggered effect
            confetti.style.animationDelay = Math.random() * 3 + 's';
            
            // Random size variation
            const size = 4 + Math.random() * 8;
            confetti.style.width = size + 'px';
            confetti.style.height = size + 'px';
            
            container.appendChild(confetti);
        }
    }
    
    showGameOver(playerName, score, months_survived, is_bankrupt) {
        // Determine if it's a success (12 months survived and not bankrupt) or failure
        if (months_survived >= 12 && !is_bankrupt) {
            this.showSuccess(playerName, score);
        } else {
            this.showFailure(playerName, score, months_survived, is_bankrupt);
        }
    }
    
    showSuccess(playerName, score) {
        document.getElementById('success-message').textContent = 
            `${playerName}, du hast alle 12 Monate in St. Gallen überlebt! Du bist ein wahrer Startup-Champion!`;
        
        if (score) {
            document.getElementById('success-score-value').textContent = score.toLocaleString('de-CH');
            document.getElementById('success-score').style.display = 'flex';
        }
        
        this.successOverlay.classList.add('is-open');
        document.documentElement.style.overflow = 'hidden';
        
        // Start confetti animation
        this.createConfetti();
        
        // Auto-redirect after 6 seconds if user doesn't interact
        setTimeout(() => {
            if (this.successOverlay.classList.contains('is-open')) {
                this.toLeaderboard();
            }
        }, 6000);
    }
    
    showFailure(playerName, score, months_survived, is_bankrupt) {
        let message = `${playerName}'s St. Gallen Adventure ist zu Ende!`;
        
        if (is_bankrupt) {
            message += ` Leider bankrott nach ${months_survived} Monaten.`;
        } else if (months_survived < 12) {
            message += ` ${months_survived} von 12 Monaten geschafft.`;
        }
        
        document.getElementById('go-message').textContent = message;
        
        if (score) {
            document.getElementById('go-score-value').textContent = score.toLocaleString('de-CH');
            document.getElementById('go-score').style.display = 'flex';
        }
        
        this.gameOverOverlay.classList.add('is-open');
        document.documentElement.style.overflow = 'hidden';
        
        // Auto-redirect after 4 seconds if user doesn't interact
        setTimeout(() => {
            if (this.gameOverOverlay.classList.contains('is-open')) {
                this.toLeaderboard();
            }
        }, 4000);
    }
    
    hide() {
        this.gameOverOverlay.classList.remove('is-open');
        this.successOverlay.classList.remove('is-open');
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
    
    // Compatibility method for existing code
    showGameOverAnimation(playerName, score) {
        // Default to failure if only these parameters are provided
        this.showFailure(playerName, score, 0, true);
    }
}

// Initialisiere die Animationen
let gameAnimations;
document.addEventListener('DOMContentLoaded', () => {
    gameAnimations = new GameAnimations();
});
