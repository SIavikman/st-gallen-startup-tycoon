from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import sqlite3
import random
import os
from datetime import datetime

# Deploy test
# Import the game classes
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
    """Score nur speichern wenn 12 Monate überlebt und nicht bankrott"""
    # Nur speichern wenn nicht bankrott und 12 Monate überlebt
    if company_dict.get('is_bankrupt', True) or company_dict.get('months_survived', 0) < 12:
        return  # Nicht speichern
        
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    
    # Berechne outstanding debt
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
    """Leaderboard aus Datenbank laden - nur Top 10"""
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
    """Convert Company object to dictionary for session storage."""
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
    """Convert dictionary back to Company object."""
    company = Company(data['owner_name'])
    for key, value in data.items():
        if key != 'loans':
            setattr(company, key, value)
    
    # Restore loans
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
    """Spiel starten mit vollständiger Spiellogik"""
    player_name = request.form.get('player_name', '').strip()
    if not player_name:
        return redirect(url_for('home', error='Name erforderlich'))
    
    # Erstelle neue Company mit vollständiger Spiellogik
    company = Company(player_name)
    
    # Speichere in Session
    session['company'] = company_to_dict(company)
    session['event_manager'] = True  # Flag dass EventManager verfügbar ist
    session['current_month'] = 1
    
    return redirect(url_for('game'))

@app.route('/game')
def game():
    """Hauptspiel-Seite"""
    if 'company' not in session:
        return redirect(url_for('home'))
    
    # Lade Company aus Session
    company_dict = session['company']
    current_month = session.get('current_month', 1)
    
    return render_template('game.html', 
                         company=company_dict,
                         current_month=current_month)

@app.route('/api/complete_turn', methods=['POST'])
def complete_turn():
    """Kompletten Spielzug abwickeln: Aktion → Event → Finanzen → Monatswechsel"""
    if 'company' not in session:
        return jsonify({'success': False, 'error': 'Kein aktives Spiel'}), 400
    
    data = request.get_json()
    action_type = data.get('action')
    
    # Lade Company aus Session
    company = dict_to_company(session['company'])
    current_month = session.get('current_month', 1)
    
    # Erstelle Game instance
    game = StartupTycoonGame()
    event_manager = SwissEventManager()
    
    try:
        # 1. Aktion ausführen
        try:
            action_enum = ActionType(action_type)
        except ValueError:
            return jsonify({'success': False, 'error': f'Ungültige Aktion: {action_type}'}), 400
            
        action_result = game.execute_action(company, action_enum)
        
        # 2. Random Event triggern (nur wenn nicht bankrott)
        if not company.is_bankrupt:
            event_result = event_manager.trigger_random_event(company)
        else:
            event_result = "Unternehmen ist bankrott - keine Events mehr."
        
        # 3. Monatliche Finanzen verarbeiten (nur wenn nicht bankrott)
        if not company.is_bankrupt:
            company.month = current_month
            
            # Balance vor Finanzen merken (nach Events!)
            balance_before_finances = company.balance
            
            finances = company.process_monthly_finances()
            loan_status = company.process_loan_payments()
            
            # Neue Balance nach allen Änderungen
            balance_after_finances = company.balance
            
            finance_parts = [
                f"Einnahmen: +{finances['revenue']:,} CHF",
                f"Ausgaben: -{finances['expenses']:,} CHF"
            ]
            
            if loan_status:
                finance_parts.append(loan_status)
            
            # Gesamtveränderung anzeigen (inkl. Events)
            total_change = balance_after_finances - balance_before_finances
            if total_change >= 0:
                finance_parts.append(f"Gesamt Veränderung: +{total_change:,} CHF")
            else:
                finance_parts.append(f"Gesamt Veränderung: {total_change:,} CHF")
            
            finance_parts.append(f"Neue Balance: {balance_after_finances:,} CHF")
            
            finance_text = "\n".join(finance_parts)
        else:
            finance_text = "Keine Finanzen - Unternehmen bankrott."
        
        # 4. Monat voranschreiten
        current_month += 1
        session['current_month'] = current_month
        company.months_survived = current_month - 1
        
        # 5. Prüfen ob Spiel zu Ende (NUR 12 Monate oder Bankrott oder zu viel Schulden)
        game_over = (current_month > 12 or 
                    company.is_bankrupt or 
                    company.balance < -5000)
        
        # Session aktualisieren
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

@app.route('/api/get_company_status', methods=['GET'])
def get_company_status():
    """API-Endpoint für Live Company-Status Updates"""
    if 'company' not in session:
        return jsonify({'success': False, 'error': 'Kein aktives Spiel'}), 400
    
    company_dict = session['company']
    current_month = session.get('current_month', 1)
    
    # Berechne aktuellen Score
    score = round((company_dict['balance'] + 
             (company_dict['customers'] * 10) + 
             (company_dict['reputation'] * 1000) + 
             (company_dict['product_quality'] * 1000)),2)
    
    return jsonify({
        'success': True,
        'company': company_dict,
        'current_month': current_month,
        'score': int(score),
        'game_over': current_month > 12 or company_dict.get('is_bankrupt', False)
    })

@app.route('/api/handle_special_events', methods=['POST'])
def handle_special_events():
    """API-Endpoint für interaktive Events wie Quiz und Dragons Den"""
    if 'company' not in session:
        return jsonify({'success': False, 'error': 'Kein aktives Spiel'}), 400
    
    data = request.get_json()
    event_type = data.get('event_type')
    event_data = data.get('event_data', {})
    
    company = dict_to_company(session['company'])
    event_manager = SwissEventManager()
    
    try:
        if event_type == 'quiz_answer':
            # Quiz-Antwort verarbeiten
            correct = event_data.get('correct', False)
            if correct:
                bonus = 2000
                company.balance += bonus
                result = f"Richtig! +{bonus:,} CHF Quiz-Bonus erhalten!"
            else:
                result = "Falsche Antwort, aber trotzdem etwas gelernt!"
                
        elif event_type == 'dragons_den_decision':
            # Dragons Den Entscheidung
            participate = event_data.get('participate', False)
            cost = 500
            
            if not participate:
                result = "Dragons Den abgelehnt. Kein Risiko, kein TV-Ruhm."
            elif company.balance < cost:
                result = f"Zu wenig Geld für Dragons Den! Brauche {cost} CHF."
            else:
                company.balance -= cost
                if random.random() < 0.5:  # 50% Erfolg
                    investment = 5000
                    company.balance += investment
                    company.reputation += random.uniform(0.3, 0.5)
                    result = f"Dragons Den Erfolg! +{investment:,} CHF Investment und TV-Ruhm!"
                else:
                    company.reputation = max(0.1, company.reputation - random.uniform(0.4, 0.6))
                    result = f"Dragons Den Flop! -{cost:,} CHF verloren, Reputation beschädigt."
        else:
            return jsonify({'success': False, 'error': 'Unbekannter Event-Typ'}), 400
        
        # Company zurück in Session speichern
        session['company'] = company_to_dict(company)
        
        return jsonify({
            'success': True,
            'message': result,
            'company': company_to_dict(company)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/game_over')
def game_over():
    """Spielende-Seite anzeigen"""
    if 'company' not in session:
        return redirect(url_for('home'))
    
    company_dict = session['company']
    
    # Berechne final score
    final_score = (company_dict['balance'] + 
                  (company_dict['customers'] * 10) + 
                  (company_dict['reputation'] * 1000) + 
                  (company_dict['product_quality'] * 1000))
    
    # Speichere Score in Datenbank (nur wenn nicht bankrott und 12 Monate überlebt)
    save_score(company_dict, int(final_score))
    
    # Lade Leaderboard
    leaderboard = get_leaderboard()
    
    # Lösche Session
    session.pop('company', None)
    session.pop('current_month', None)
    session.pop('event_manager', None)
    
    return render_template('game_over.html', 
                         company=company_dict,
                         final_score=int(final_score),
                         leaderboard=leaderboard)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'API-Endpoint nicht gefunden'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Interner Server-Fehler'}), 500

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Ungültige Anfrage'}), 400

# Datenbank bei jedem App-Start initialisieren (auch für Gunicorn)
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

