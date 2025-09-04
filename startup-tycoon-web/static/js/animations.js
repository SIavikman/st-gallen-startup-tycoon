// Game Over & Success Animation JavaScript for St. Gallen Startup Tycoon
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
                <p class="go-sub" id="go-message">Your St. Gallen adventure has ended.</p>
                <div id="go-score" class="go-pill" style="display: none;">
                    <span class="go-dot"></span>
                    <span>Final Score: <strong id="go-score-value">0</strong></span>
                </div>
                <div id="go-humor" class="go-humor" style="display: none; margin: 15px 0; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px; border-left: 4px solid #fff;">
                    <p style="margin: 0; font-size: 1.1em; font-style: italic;" id="go-humor-text"></p>
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
                    CONGRATULATIONS!
                    <span class="sparkle">CONGRATULATIONS!</span>
                </h1>
                <p class="success-sub" id="success-message">You survived all 12 months in St. Gallen!</p>
                <div id="success-score" class="success-pill" style="display: none;">
                    <span class="success-dot"></span>
                    <span>Final Score: <strong id="success-score-value">0</strong></span>
                </div>
                <div id="success-humor" class="success-humor" style="display: none; margin: 15px 0; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px; border-left: 4px solid #fff;">
                    <p style="margin: 0; font-size: 1.1em; font-style: italic;" id="success-humor-text"></p>
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
    
    showGameOver(playerName, score, monthsSurvived, isBankrupt, humorousMessage) {
        // Determine if it's a success (12 months survived and not bankrupt) or failure
        if (monthsSurvived >= 12 && !isBankrupt) {
            this.showSuccess(playerName, score, humorousMessage);
        } else {
            this.showFailure(playerName, score, monthsSurvived, isBankrupt, humorousMessage);
        }
    }
    
    showSuccess(playerName, score, humorousMessage) {
        const messageEl = document.getElementById('success-message');
        messageEl.textContent = `${playerName}, you survived all 12 months in St. Gallen! You are a true startup champion!`;
        
        if (score) {
            document.getElementById('success-score-value').textContent = score.toLocaleString('en-US');
            document.getElementById('success-score').style.display = 'flex';
        }
        
        if (humorousMessage) {
            document.getElementById('success-humor-text').textContent = humorousMessage;
            document.getElementById('success-humor').style.display = 'block';
        }
        
        this.successOverlay.classList.add('is-open');
        document.documentElement.style.overflow = 'hidden';
        
        // Start confetti animation
        this.createConfetti();
        
        // Auto-hide after 6 seconds
        setTimeout(() => {
            if (this.successOverlay.classList.contains('is-open')) {
                this.hide();
                this.showResults();
            }
        }, 6000);
    }
    
    showFailure(playerName, score, monthsSurvived, isBankrupt, humorousMessage) {
        let message = `${playerName}'s St. Gallen Adventure has ended!`;
        
        if (isBankrupt) {
            message += ` Unfortunately went bankrupt after ${monthsSurvived} months.`;
        } else if (monthsSurvived < 12) {
            message += ` Completed ${monthsSurvived} out of 12 months.`;
        }
        
        document.getElementById('go-message').textContent = message;
        
        if (score) {
            document.getElementById('go-score-value').textContent = score.toLocaleString('en-US');
            document.getElementById('go-score').style.display = 'flex';
        }
        
        if (humorousMessage) {
            document.getElementById('go-humor-text').textContent = humorousMessage;
            document.getElementById('go-humor').style.display = 'block';
        }
        
        this.gameOverOverlay.classList.add('is-open');
        document.documentElement.style.overflow = 'hidden';
        
        // Auto-hide after 4 seconds
        setTimeout(() => {
            if (this.gameOverOverlay.classList.contains('is-open')) {
                this.hide();
                this.showResults();
            }
        }, 4000);
    }
    
    hide() {
        this.gameOverOverlay.classList.remove('is-open');
        this.successOverlay.classList.remove('is-open');
        document.documentElement.style.overflow = '';
    }
    
    showResults() {
        // Trigger the main content to show
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
            mainContent.style.display = 'block';
        }
    }
    
    // Utility methods for navigation (if needed)
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
        this.showFailure(playerName, score, 0, true, null);
    }
}

// Initialize animations when DOM is loaded
let gameAnimations;
document.addEventListener('DOMContentLoaded', () => {
    gameAnimations = new GameAnimations();
});
