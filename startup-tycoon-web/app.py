from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import sqlite3
import random
import os
from datetime import datetime

from startup_tycoon_main import Company, ActionType, StartupTycoonGame, Loan
from swiss_events_manager import SwissEventManager

app = Flask(__name__)
app.secret_key = 'change-this-later'

def init_db():
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            final_score INTEGER NOT NULL,
            final_balance INTEGER NOT NULL,
            customers INTEGER NOT NULL,
            employees INTEGER NOT NULL,
            reputation REAL NOT NULL,
            product_quality REAL NOT NULL,
            research_protection INTEGER DEFAULT 0,
            months_survived INTEGER NOT NULL,
            is_bankrupt BOOLEAN DEFAULT 0,
            outstanding_debt INTEGER DEFAULT 0,
            date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_score(company_dict, final_score):
    """Save score only if survived 12 months and not bankrupt"""
    if company_dict.get('is_bankrupt', True) or company_dict.get('months_survived', 0) < 12:
        return
        
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    
    outstanding_debt = sum(loan['amount'] for loan in company_dict.get('loans', []))
    
    c.execute('''
        INSERT INTO scores 
        (player_name, final_score, final_balance, customers, employees, 
         reputation, product_quality, research_protection, months_survived, 
         is_bankrupt, outstanding_debt) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        company_dict['owner_name'],
        final_score,
        company_dict['balance'],
        company_dict['customers'],
        company_dict['employees'],
        company_dict['reputation'],
        company_dict['product_quality'],
        company_dict['research_protection'],
        company_dict['months_survived'],
        company_dict['is_bankrupt'],
        outstanding_debt
    ))
    conn.commit()
    conn.close()

def get_leaderboard(limit=10):
    """Load leaderboard from database"""
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute('''
        SELECT player_name, final_score, final_balance, customers, employees,
               reputation, product_quality, research_protection, months_survived, 
               is_bankrupt, outstanding_debt, date_played 
        FROM scores 
        WHERE is_bankrupt = 0 AND months_survived >= 12
        ORDER BY final_score DESC 
        LIMIT ?
    ''', (limit,))
    results = c.fetchall()
    conn.close()
    
    return [{
        'name': r[0], 'score': r[1], 'balance': r[2], 
        'customers': r[3], 'employees': r[4], 'reputation': r[5],
        'product_quality': r[6], 'research_protection': r[7],
        'months_survived': r[8], 'is_bankrupt': r[9],
        'outstanding_debt': r[10], 'date': r[11]
    } for r in results]

def company_to_dict(company):
    """Convert Company object to dictionary for session storage"""
    return {
        'owner_name': company.owner_name,
        'balance': company.balance,
        'customers': company.customers,
        'employees': company.employees,
        'reputation': company.reputation,
        'product_quality': company.product_quality,
        'research_protection': company.research_protection,
        'month': company.month,
        'marketing_boost': company.marketing_boost,
        'no_revenue_this_month': company.no_revenue_this_month,
        'months_survived': company.months_survived,
        'is_bankrupt': company.is_bankrupt,
        'loans': [{'amount': loan.amount, 'months_remaining': loan.months_remaining, 'monthly_payment': loan.monthly_payment} for loan in company.loans],
        'history': company.history
    }

def dict_to_company(data):
    """Convert dictionary back to Company object"""
    company = Company(data['owner_name'])
    for key, value in data.items():
        if key != 'loans':
            setattr(company, key, value)
    
    company.loans = []
    for loan_data in data.get('loans', []):
        loan = Loan(loan_data['amount'], loan_data['months_remaining'], loan_data['monthly_payment'])
        company.loans.append(loan)
    
    return company

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/leaderboard')
def leaderboard():
    board = get_leaderboard()
    return render_template('leaderboard.html', leaderboard=board)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    """Start game with complete logic"""
    player_name = request.form.get('player_name', '').strip()
    if not player_name:
        return redirect(url_for('home', error='Name required'))
    
    company = Company(player_name)
    
    session['company'] = company_to_dict(company)
    session['current_month'] = 1
    
    return redirect(url_for('game'))

@app.route('/game')
def game():
    """Main game page"""
    if 'company' not in session:
        return redirect(url_for('home'))
    
    company_dict = session['company']
    current_month = session.get('current_month', 1)
    
    return render_template('game.html', 
                         company=company_dict,
                         current_month=current_month)

@app.route('/api/complete_turn', methods=['POST'])
def complete_turn():
    """Complete game turn: Action -> Event -> Finances -> Month advance"""
    if 'company' not in session:
        return jsonify({'success': False, 'error': 'No active game'}), 400
    
    data = request.get_json()
    action_type = data.get('action')
    
    company = dict_to_company(session['company'])
    current_month = session.get('current_month', 1)
    
    game = StartupTycoonGame()
    event_manager = SwissEventManager()
    
    try:
        # 1. Execute action
        try:
            action_enum = ActionType(action_type)
        except ValueError:
            return jsonify({'success': False, 'error': f'Invalid action: {action_type}'}), 400
        
        action = game.actions[action_enum]
        action_cost = action.cost
        balance_before_action = company.balance
        
        action_result = game.execute_action(company, action_enum)
        
        # 2. Trigger random event (only if not bankrupt)
        if not company.is_bankrupt:
            event_result = event_manager.trigger_random_event(company)
        else:
            event_result = "Company is bankrupt - no more events."
            
        # 3. Process monthly finances (only if not bankrupt)
        if not company.is_bankrupt:
            company.month = current_month
            balance_after_event = company.balance
            
            finances = company.process_monthly_finances()
            loan_status = company.process_loan_payments()
            
            balance_after_finances = company.balance
            event_change = balance_after_event - (balance_before_action - action_cost)
            
            finance_parts = [
                f"Revenue: +{finances['revenue']:,} CHF",
                f"Expenses: -{finances['expenses']:,} CHF"
            ]
            
            if action_cost > 0:
                finance_parts.append(f"Invested: -{action_cost:,} CHF")
            
            if event_change != 0:
                if event_change > 0:
                    finance_parts.append(f"Event: +{event_change:,} CHF")
                else:
                    finance_parts.append(f"Event: {event_change:,} CHF")
            
            if loan_status:
                finance_parts.append(loan_status)
            
            total_change = balance_after_finances - balance_before_action
            if total_change >= 0:
                finance_parts.append(f"Total Change: +{total_change:,} CHF")
            else:
                finance_parts.append(f"Total Change: {total_change:,} CHF")
            
            finance_parts.append(f"New Balance: {balance_after_finances:,} CHF")
            finance_text = "\n".join(finance_parts)
        else:
            finance_text = "No finances - Company bankrupt."
        
        # 4. Advance month
        current_month += 1
        session['current_month'] = current_month
        company.months_survived = current_month - 1
        
        # 5. Check if game over
        game_over = (current_month > 12 or 
                    company.is_bankrupt or 
                    company.balance < -5000)
        
        session['company'] = company_to_dict(company)
        
        return jsonify({
            'success': True,
            'action_result': action_result,
            'event_result': event_result,
            'finance_result': finance_text,
            'new_month': current_month,
            'game_over': game_over,
            'company': company_to_dict(company)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/game_over')
def game_over():
    """Show game end page"""
    if 'company' not in session:
        return redirect(url_for('home'))
    
    company_dict = session['company']
    
    final_score = (company_dict['balance'] + 
                  (company_dict['customers'] * 10) + 
                  (company_dict['reputation'] * 1000) + 
                  (company_dict['product_quality'] * 1000))
    
    save_score(company_dict, int(final_score))
    leaderboard = get_leaderboard()
    
    # Initialize event manager for humorous messages
    event_manager = SwissEventManager()
    
    # Calculate player's rank for contextual humor
    # Find where this player would rank in the leaderboard
    player_rank = 1
    total_players = len(leaderboard) + 1  # +1 for current player
    
    for i, entry in enumerate(leaderboard):
        if final_score > entry['score']:
            player_rank = i + 1
            break
        else:
            player_rank = i + 2  # Player ranks after this entry
    
    # If leaderboard is empty or player has lowest score
    if not leaderboard:
        player_rank = 1
        total_players = 1
    elif final_score <= (leaderboard[-1]['score'] if leaderboard else 0):
        player_rank = len(leaderboard) + 1
    
    # Convert dict back to Company object temporarily for the message functions
    temp_company = dict_to_company(company_dict)
    
    # Get humorous messages
    humorous_message = event_manager.get_humorous_endgame_message(
        temp_company, player_rank, total_players
    )
    
    bankruptcy_message = None
    if company_dict.get('is_bankrupt', False):
        bankruptcy_message = event_manager.get_bankruptcy_message()
    
    achievements = event_manager.get_special_achievement_messages(temp_company)
    
    # Clean up session
    session.pop('company', None)
    session.pop('current_month', None)
    
    return render_template('game_over.html', 
                         company=company_dict,
                         final_score=int(final_score),
                         leaderboard=leaderboard,
                         humorous_message=humorous_message,
                         bankruptcy_message=bankruptcy_message,
                         achievements=achievements)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'API endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Invalid request'}), 400

init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

