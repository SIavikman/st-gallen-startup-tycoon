#!/usr/bin/env python3
"""
Startup Tycoon - St. Gallen Edition
A text-based business simulation game where players run startup companies in St. Gallen.

Features:
- Solo and Multiplayer modes (2-4 players)
- 12-month gameplay with strategic decisions
- St. Gallen themed random events and Swiss humor
- Loan system for bankrupt companies
- Clean, modular code structure with classes
- Rich feedback and scoring system
"""

import random
import json
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Import the Swiss events
from swiss_events_manager import SwissEventManager


class ActionType(Enum):
    MARKETING = "marketing"
    DEVELOPMENT = "development"
    HIRING = "hiring"
    RESEARCH = "research"
    EXPANSION = "expansion"
    NOTHING = "nothing"
    TAKE_LOAN = "take_loan"
    GO_BANKRUPT = "go_bankrupt"


class EventType(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class GameAction:
    name: str
    cost: int
    description: str
    action_type: ActionType


@dataclass
class Loan:
    amount: int
    months_remaining: int
    monthly_payment: int


class Company:
    """Represents a player's startup company in St. Gallen."""
    
    def __init__(self, owner_name: str):
        self.owner_name = owner_name
        self.balance = 10000  # Starting money in CHF
        self.customers = 50
        self.employees = 1
        self.reputation = 1.0
        self.product_quality = 1.0
        self.research_protection = 0  # Reduces random event impact
        self.monthly_revenue = 0
        self.monthly_expenses = 500  # Base operating costs
        self.history = []
        self.month = 1
        self.loans = []  # List of active loans
        self.is_bankrupt = False
        
        # Swiss events specific attributes
        self.marketing_boost = 0  # For economic boom effect
        self.no_revenue_this_month = False  # For missed pitch event
        self.months_survived = 0
        
    def calculate_score(self) -> int:
        """Calculate company's total score/value."""
        total_debt = sum(loan.amount for loan in self.loans)
        return int(self.balance + (self.customers * 10) + 
                  (self.reputation * 1000) + (self.product_quality * 1000) - total_debt)
    
    def can_afford(self, cost: int) -> bool:
        """Check if company can afford an action."""
        return self.balance >= cost
    
    def is_in_debt(self) -> bool:
        """Check if company has negative balance."""
        return self.balance < 0
    
    def get_total_debt(self) -> int:
        """Calculate total outstanding loan debt."""
        return sum(loan.amount for loan in self.loans)
    
    def get_monthly_loan_payments(self) -> int:
        """Calculate total monthly loan payments."""
        return sum(loan.monthly_payment for loan in self.loans)
    
    def process_loan_payments(self) -> str:
        """Process monthly loan payments and return status."""
        if not self.loans:
            return ""
        
        total_payment = self.get_monthly_loan_payments()
        self.balance -= total_payment
        
        # Update loan terms
        completed_loans = []
        for loan in self.loans:
            loan.months_remaining -= 1
            loan.amount = max(0, loan.amount - loan.monthly_payment)
            if loan.months_remaining <= 0 or loan.amount <= 0:
                completed_loans.append(loan)
        
        # Remove completed loans
        for loan in completed_loans:
            self.loans.remove(loan)
        
        status = f"💳 Loan payments: -{total_payment:,} CHF"
        if completed_loans:
            status += f" ({len(completed_loans)} loan(s) paid off!)"
        
        return status
    
    def take_emergency_loan(self) -> str:
        """Take an emergency loan to avoid bankruptcy."""
        loan_amount = 5000
        monthly_payment = 2000  # High interest emergency loan
        months = 3
        
        self.loans.append(Loan(loan_amount, months, monthly_payment))
        self.balance += loan_amount
        
        return f"🏛️ Emergency loan approved! +{loan_amount:,} CHF (Repay {monthly_payment:,} CHF/month for {months} months)"
    
    def process_monthly_finances(self) -> Dict[str, int]:
        """Calculate and apply monthly revenue and expenses."""
        # Check if no revenue this month (e.g., missed pitch)
        if self.no_revenue_this_month:
            self.monthly_revenue = 0
            self.no_revenue_this_month = False  # Reset for next month
        else:
            # Revenue based on customers, quality, reputation, and some randomness
            base_revenue_per_customer = 5 + random.uniform(0, 3)
            self.monthly_revenue = int(self.customers * self.product_quality * 
                                     self.reputation * base_revenue_per_customer)
        
        # Expenses increase with employees
        self.monthly_expenses = max(100, 500 + (self.employees * 2000))
        
        # Apply financial changes
        net_income = self.monthly_revenue - self.monthly_expenses
        self.balance += net_income
        
        # Track survival
        self.months_survived = self.month
        
        return {
            'revenue': self.monthly_revenue,
            'expenses': self.monthly_expenses,
            'net_income': net_income
        }
    
    def add_history_entry(self, entry: str):
        """Add an entry to the company's history."""
        self.history.append(f"Month {self.month}: {entry}")
    
    def get_status_display(self) -> str:
        """Get formatted status display."""
        debt_info = ""
        if self.loans:
            total_debt = self.get_total_debt()
            monthly_payments = self.get_monthly_loan_payments()
            debt_info = f"│ 💳 Outstanding Debt: {total_debt:,} CHF ({monthly_payments:,} CHF/month)\n"
        
        status_emoji = "💀" if self.is_bankrupt else ("⚠️" if self.is_in_debt() else "✅")
        
        return f"""
┌─── {self.owner_name}'s St. Gallen Startup {status_emoji} ───┐
│ 💰 Balance: {self.balance:,} CHF
│ 👥 Customers: {self.customers:,}
│ 👨‍💼 Employees: {self.employees}
│ ⭐ Reputation: {self.reputation:.1f}
│ 📈 Product Quality: {self.product_quality:.1f}
{debt_info}│ 📊 Company Score: {self.calculate_score():,}
└─────────────────────────────────────────────────────────────┘
"""


class StartupTycoonGame:
    """Main game controller class for St. Gallen Startup Tycoon."""
    
    def __init__(self):
        self.companies: List[Company] = []
        self.current_month = 1
        self.max_months = 12
        self.current_player_index = 0
        self.game_mode = "solo"  # "solo" or "multiplayer"
        self.game_over = False
        self.event_manager = SwissEventManager()
        
        # Define available actions
        self.actions = {
            ActionType.MARKETING: GameAction(
                "HSG Campus Marketing", 1500,
                "Target wealthy HSG students with premium marketing campaign",
                ActionType.MARKETING
            ),
            ActionType.DEVELOPMENT: GameAction(
                "Swiss Quality Development", 2000,
                "Invest in R&D to meet Swiss quality standards",
                ActionType.DEVELOPMENT
            ),
            ActionType.HIRING: GameAction(
                "Recruit Talent", 3000,
                "Hire from HSG graduates or international talent pool",
                ActionType.HIRING
            ),
            ActionType.RESEARCH: GameAction(
                "Market Research", 1000,
                "Study St. Gallen market trends and local preferences",
                ActionType.RESEARCH
            ),
            ActionType.EXPANSION: GameAction(
                "Regional Expansion", 4000,
                "Expand operations across Eastern Switzerland",
                ActionType.EXPANSION
            ),
            ActionType.NOTHING: GameAction(
                "Chill at Drei Weihern", 0,
                "Take a relaxing day by the lakes, save money but miss opportunities",
                ActionType.NOTHING
            ),
            ActionType.TAKE_LOAN: GameAction(
                "Emergency Bank Loan", 0,
                "Take a 5,000 CHF emergency loan (2,000 CHF/month for 3 months)",
                ActionType.TAKE_LOAN
            ),
            ActionType.GO_BANKRUPT: GameAction(
                "Declare Bankruptcy", 0,
                "Give up and close the company",
                ActionType.GO_BANKRUPT
            )
        }
    
    def display_welcome(self):
        """Display the game welcome screen."""
        print("\n" + "="*70)
        print("🏔️ STARTUP TYCOON - ST. GALLEN EDITION 🏔️")
        print("="*70)
        print("Build your entrepreneurial empire in beautiful St. Gallen!")
        print("Navigate HSG students, Trischli parties, and Swiss bureaucracy!")
        print("Start with 10,000 CHF and survive 12 months in Eastern Switzerland!")
        print("🎓 HSG • 🍺 Trischli • 🌭 Olma • 💎 Rosenberg • 🏖️ Drei Weihern")
        print("="*70 + "\n")
    
    def setup_game(self):
        """Handle game mode selection and player setup."""
        while True:
            print("Choose your St. Gallen adventure:")
            print("1. 🎯 Solo Mode - Build your empire alone")
            print("2. 👥 Multiplayer Mode - Compete with friends (2-4 players)")
            
            try:
                choice = input("\nEnter your choice (1-2): ").strip()
                
                if choice == "1":
                    self.game_mode = "solo"
                    name = input("Enter your entrepreneur name: ").strip() or "Entrepreneur"
                    self.companies = [Company(name)]
                    break
                    
                elif choice == "2":
                    self.game_mode = "multiplayer"
                    self.setup_multiplayer()
                    break
                    
                else:
                    print("❌ Invalid choice! Please enter 1 or 2.")
                    
            except (ValueError, KeyboardInterrupt):
                print("❌ Invalid input! Please try again.")
    
    def setup_multiplayer(self):
        """Setup multiplayer game with 2-4 players."""
        while True:
            try:
                num_players = int(input("How many entrepreneurs? (2-4): "))
                if 2 <= num_players <= 4:
                    break
                print("❌ Please enter a number between 2 and 4.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        self.companies = []
        for i in range(num_players):
            while True:
                name = input(f"Enter name for Entrepreneur {i+1}: ").strip()
                if name and len(name) <= 20:
                    self.companies.append(Company(name))
                    break
                print("❌ Please enter a valid name (1-20 characters).")
    
    def display_game_state(self):
        """Display current game state and company status."""
        print("\n" + "="*80)
        print(f"📅 MONTH {self.current_month} of {self.max_months} - St. Gallen Business Scene")
        print("="*80)
        
        if self.game_mode == "solo":
            print(self.companies[0].get_status_display())
        else:
            current_company = self.companies[self.current_player_index]
            print(f"🎮 {current_company.owner_name}'s Turn")
            print(current_company.get_status_display())
            
            # Show other players' scores for competitive context
            print("🏆 St. Gallen Startup Leaderboard:")
            sorted_companies = sorted(self.companies, key=lambda c: c.calculate_score(), reverse=True)
            for i, company in enumerate(sorted_companies, 1):
                status = "💀" if company.is_bankrupt else ("⚠️" if company.is_in_debt() else "✅")
                marker = "👑" if i == 1 else f"{i}."
                print(f"   {marker} {company.owner_name}: {company.calculate_score():,} points {status}")
            print()
    
    def display_actions(self, company: Company):
        """Display available actions for the current player."""
        if company.is_in_debt() and not company.is_bankrupt:
            print("⚠️ CRITICAL SITUATION - Company in Debt!")
            print("Choose your survival strategy:")
            print("-" * 50)
            print("1. 🏛️ Take Emergency Loan")
            print("   💡 Get 5,000 CHF immediately (Repay 2,000 CHF/month for 3 months)")
            print("   ⚡ High interest but gives you a chance to recover!")
            print()
            print("2. 💀 Declare Bankruptcy")
            print("   💡 Give up and close your St. Gallen startup")
            print("   ⚡ Game over for this company!")
            print()
        else:
            print("💼 Available St. Gallen Business Actions:")
            print("-" * 60)
            
            normal_actions = [k for k in self.actions.keys() 
                            if k not in [ActionType.TAKE_LOAN, ActionType.GO_BANKRUPT]]
            
            for i, action_type in enumerate(normal_actions, 1):
                action = self.actions[action_type]
                affordable = "✅" if company.can_afford(action.cost) else "❌"
                cost_text = f"{action.cost:,} CHF" if action.cost > 0 else "Free"
                
                print(f"{i}. {affordable} {action.name} - {cost_text}")
                print(f"   💡 {action.description}")
                print()
    
    def execute_action(self, company: Company, action_type: ActionType) -> str:
        """Execute a player action and return the result description."""
        action = self.actions[action_type]
        
        # Handle special debt actions
        if action_type == ActionType.TAKE_LOAN:
            return company.take_emergency_loan()
            
        elif action_type == ActionType.GO_BANKRUPT:
            company.is_bankrupt = True
            return "💀 Company declared bankruptcy! Game over for this entrepreneur."
        
        # Handle normal actions
        if not company.can_afford(action.cost):
            return f"❌ Cannot afford {action.name}! Need {action.cost:,} CHF but only have {company.balance:,} CHF."
        
        # Deduct cost
        company.balance -= action.cost
        result_messages = [f"💸 Invested {action.cost:,} CHF in {action.name}"]
        
        # Apply action effects with St. Gallen flavor
        if action_type == ActionType.MARKETING:
            customer_gain = random.randint(15, 35)
            reputation_gain = random.uniform(0.1, 0.3)
            
            # Apply marketing boost if active (from economic boom)
            if company.marketing_boost > 0:
                customer_gain *= 2
                reputation_gain *= 2
                company.marketing_boost -= 1
                result_messages.append("🚀 Marketing boost active - DOUBLE EFFECT!")
            
            company.customers += customer_gain
            company.reputation += reputation_gain
            result_messages.append(f"🎓 HSG students noticed your campaign! +{customer_gain} customers, reputation +{reputation_gain:.1f}")
            
        elif action_type == ActionType.DEVELOPMENT:
            quality_gain = random.uniform(0.3, 0.5)
            customer_gain = random.randint(5, 15)
            company.product_quality += quality_gain
            company.customers += customer_gain
            result_messages.append(f"🔧 Swiss-quality improvements! Product quality +{quality_gain:.1f}, attracted {customer_gain} customers")
            
        elif action_type == ActionType.HIRING:
            company.employees += 1
            productivity_boost = random.randint(8, 20)
            company.customers += productivity_boost
            company.product_quality += random.uniform(0.1, 0.2)
            result_messages.append(f"👨‍💼 Hired talented professional! Team productivity boosted, +{productivity_boost} customers")
            
        elif action_type == ActionType.RESEARCH:
            company.research_protection += 1
            market_insight = random.randint(5, 12)
            company.customers += market_insight
            result_messages.append(f"🔬 St. Gallen market research complete! Risk reduced, +{market_insight} customers from insights")
            
        elif action_type == ActionType.EXPANSION:
            customer_gain = random.randint(25, 45)
            reputation_gain = random.uniform(0.2, 0.4)
            quality_gain = random.uniform(0.2, 0.4)
            company.customers += customer_gain
            company.reputation += reputation_gain
            company.product_quality += quality_gain
            company.employees += 1
            result_messages.append(f"🏢 Eastern Switzerland expansion! +{customer_gain} customers, +1 employee, all metrics boosted")
            
        elif action_type == ActionType.NOTHING:
            # Small chance of positive outcome from relaxing
            if random.random() < 0.3:
                inspiration = random.randint(3, 8)
                company.customers += inspiration
                result_messages.append(f"🏖️ Relaxing at Drei Weihern sparked inspiration! +{inspiration} customers from word-of-mouth")
            else:
                result_messages.append("😴 Enjoyed the beautiful St. Gallen scenery but missed business opportunities")
        
        return "\n".join(result_messages)
    
    def trigger_random_event(self, company: Company) -> str:
        """Trigger a random Swiss event."""
        return self.event_manager.trigger_random_event(company)
    
    def check_bankruptcy(self, company: Company) -> bool:
        """Check if a company has gone bankrupt."""
        return company.balance < -5000  # Allow some debt
    
    def process_monthly_finances(self, company: Company) -> str:
        """Process monthly financial calculations including loan payments."""
        finances = company.process_monthly_finances()
        loan_status = company.process_loan_payments()
        
        revenue_text = f"💰 Revenue: +{finances['revenue']:,} CHF"
        expense_text = f"💸 Operating Expenses: -{finances['expenses']:,} CHF"
        
        result_lines = [revenue_text, expense_text]
        
        if loan_status:
            result_lines.append(loan_status)
        
        if finances['net_income'] >= 0:
            net_text = f"📊 Net Income: +{finances['net_income']:,} CHF ✅"
        else:
            net_text = f"📊 Net Loss: {finances['net_income']:,} CHF ❌"
            
        result_lines.append(net_text)
        
        return "\n".join(result_lines)
    
    def play_turn(self):
        """Execute a complete turn for the current player."""
        company = self.companies[self.current_player_index]
        company.month = self.current_month
        
        # Skip turn if company is bankrupt
        if company.is_bankrupt:
            print(f"💀 {company.owner_name}'s company is bankrupt - skipping turn")
            return
        
        # Display game state
        self.display_game_state()
        
        # Check for bankruptcy
        if self.check_bankruptcy(company):
            bankruptcy_msg = self.event_manager.get_bankruptcy_message()
            print(f"{bankruptcy_msg}")
            print(f"Final balance: {company.balance:,} CHF")
            company.add_history_entry("Company went bankrupt")
            company.is_bankrupt = True
            return
        
        # Display actions and get player choice
        self.display_actions(company)
        
        # Handle debt situation
        if company.is_in_debt():
            while True:
                try:
                    choice = input("Choose your action (1-2): ").strip()
                    if choice == "1":
                        action_type = ActionType.TAKE_LOAN
                        break
                    elif choice == "2":
                        action_type = ActionType.GO_BANKRUPT
                        break
                    else:
                        print("❌ Invalid choice! Please enter 1 or 2.")
                except (ValueError, KeyboardInterrupt):
                    print("❌ Invalid input! Please enter 1 or 2.")
        else:
            # Normal action selection
            normal_actions = [k for k in self.actions.keys() 
                            if k not in [ActionType.TAKE_LOAN, ActionType.GO_BANKRUPT]]
            
            while True:
                try:
                    choice = input(f"Choose your action (1-{len(normal_actions)}): ").strip()
                    action_index = int(choice) - 1
                    
                    if 0 <= action_index < len(normal_actions):
                        action_type = normal_actions[action_index]
                        break
                    else:
                        print(f"❌ Invalid choice! Please enter 1-{len(normal_actions)}.")
                        
                except (ValueError, KeyboardInterrupt):
                    print(f"❌ Invalid input! Please enter a number 1-{len(normal_actions)}.")
        
        # Execute action
        print("\n" + "-"*60)
        action_result = self.execute_action(company, action_type)
        print(action_result)
        company.add_history_entry(action_result.replace("\n", " | "))
        
        # Don't trigger events or finances if company just went bankrupt
        if company.is_bankrupt:
            input("\n⏸️  Press Enter to continue...")
            return
        
        # Trigger random event
        event_result = self.trigger_random_event(company)
        print(f"\n{event_result}")
        if "Quiz" not in event_result and "Pitch" not in event_result and "Höhle" not in event_result:
            company.add_history_entry(event_result)
        
        # Process monthly finances
        print(f"\n📈 Monthly Financial Report:")
        finance_result = self.process_monthly_finances(company)
        print(finance_result)
        company.add_history_entry(f"Monthly finances: {finance_result.replace(chr(10), ' | ')}")
        
        print(f"\n💰 New Balance: {company.balance:,} CHF")
        print(f"📊 Company Score: {company.calculate_score():,}")
        
        if company.loans:
            total_debt = company.get_total_debt()
            print(f"💳 Outstanding Debt: {total_debt:,} CHF")
        
        input("\n⏸️  Press Enter to continue...")
    
    def advance_month(self):
        """Advance to the next month/player."""
        if self.game_mode == "solo":
            self.current_month += 1
        else:
            self.current_player_index = (self.current_player_index + 1) % len(self.companies)
            if self.current_player_index == 0:  # All players had their turn
                self.current_month += 1
        
        if self.current_month > self.max_months:
            self.game_over = True
    
    def display_final_results(self):
        """Display final game results and winners."""
        print("\n" + "="*80)
        print("🎉 GAME OVER - ST. GALLEN STARTUP CHAMPIONSHIP 🎉")
        print("="*80)
        
        # Sort companies by score
        sorted_companies = sorted(self.companies, key=lambda c: c.calculate_score(), reverse=True)
        
        print("🏆 FINAL ST. GALLEN LEADERBOARD:")
        print("-" * 50)
        
        for i, company in enumerate(sorted_companies, 1):
            if i == 1:
                print(f"👑 {i}st Place: {company.owner_name}")
            elif i == 2:
                print(f"🥈 {i}nd Place: {company.owner_name}")
            elif i == 3:
                print(f"🥉 {i}rd Place: {company.owner_name}")
            else:
                print(f"   {i}th Place: {company.owner_name}")
            
            print(f"     💰 Final Balance: {company.balance:,} CHF")
            print(f"     👥 Customers: {company.customers:,}")
            print(f"     👨‍💼 Employees: {company.employees}")
            print(f"     ⭐ Reputation: {company.reputation:.1f}")
            print(f"     📈 Product Quality: {company.product_quality:.1f}")
            
            if company.loans:
                debt = company.get_total_debt()
                print(f"     💳 Outstanding Debt: {debt:,} CHF")
                
            print(f"     📊 Total Score: {company.calculate_score():,} points")
            
            if company.is_bankrupt:
                print(f"     💀 Status: BANKRUPT")
            elif company.is_in_debt():
                print(f"     ⚠️ Status: IN DEBT BUT SURVIVING")
            else:
                print(f"     ✅ Status: THRIVING")
            
            # Show special achievements
            achievements = self.event_manager.get_special_achievement_messages(company)
            for achievement in achievements:
                print(f"     {achievement}")
            
            # Show humorous end message
            humor_msg = self.event_manager.get_humorous_endgame_message(company, i, len(sorted_companies))
            print(f"     💬 {humor_msg}")
            print()
        
        # Declare winner with St. Gallen flavor
        winner = sorted_companies[0]
        if not winner.is_bankrupt:
            print(f"🎊 Congratulations {winner.owner_name}!")
            print("🏔️ You've built the most successful startup in St. Gallen!")
        else:
            print("😢 All entrepreneurs failed in St. Gallen...")
            print("🌭 Maybe it's time to consider selling Olma Bratwurst instead!")
        
        # Show company histories with St. Gallen flavor
        print("\n📜 ENTREPRENEURIAL JOURNEYS IN ST. GALLEN:")
        print("="*60)
        for company in self.companies:
            print(f"\n🏢 {company.owner_name}'s St. Gallen Adventure:")
            recent_history = company.history[-5:]  # Show last 5 entries
            for entry in recent_history:
                print(f"  📅 {entry}")
    
    def save_game_results(self):
        """Save game results to a file."""
        try:
            results = {
                'game_mode': self.game_mode,
                'location': 'St. Gallen, Switzerland',
                'companies': []
            }
            
            for company in self.companies:
                company_data = {
                    'owner_name': company.owner_name,
                    'final_balance': company.balance,
                    'customers': company.customers,
                    'employees': company.employees,
                    'reputation': company.reputation,
                    'product_quality': company.product_quality,
                    'outstanding_debt': company.get_total_debt(),
                    'score': company.calculate_score(),
                    'bankrupt': company.is_bankrupt,
                    'history': company.history
                }
                results['companies'].append(company_data)
            
            # Sort by score
            results['companies'].sort(key=lambda x: x['score'], reverse=True)
            
            # Save to file
            filename = "st_gallen_startup_tycoon_results.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"\n💾 St. Gallen startup results saved to {filename}")
            
        except Exception as e:
            print(f"❌ Could not save results: {e}")
    
    def run_game(self):
        """Main game loop."""
        self.display_welcome()
        self.setup_game()
        
        print(f"\n🚀 Starting {self.game_mode} game with {len(self.companies)} entrepreneur(s)!")
        print("🏔️ Your 12-month St. Gallen adventure begins now...")
        print("🎓 Navigate HSG students, Trischli parties, and Swiss precision!")
        print()
        
        while not self.game_over:
            self.play_turn()
            self.advance_month()
        
        self.display_final_results()
        self.save_game_results()
        
        # Ask to play again
        while True:
            play_again = input("\n🎮 Want another St. Gallen startup adventure? (y/n): ").strip().lower()
            if play_again in ['y', 'yes', 'ja']:
                # Reset game state
                self.__init__()
                self.run_game()
                break
            elif play_again in ['n', 'no', 'nein']:
                print("🏔️ Thanks for playing St. Gallen Startup Tycoon!")
                print("🌭 Hope you enjoyed your Swiss entrepreneurial journey! 🇨🇭")
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")


def main():
    """Entry point for the St. Gallen Startup Tycoon game."""
    try:
        print("🇨🇭 Welcome to the Swiss startup scene! 🇨🇭")
        game = StartupTycoonGame()
        game.run_game()
    except KeyboardInterrupt:
        print("\n\n👋 Auf Wiedersehen! Thanks for playing St. Gallen Startup Tycoon!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("📄 Please try restarting the game.")
        print("🏔️ The beautiful St. Gallen mountains are waiting for your next attempt!")


if __name__ == "__main__":
    main()