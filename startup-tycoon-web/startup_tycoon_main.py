#!/usr/bin/env python3
"""
Startup Tycoon - St. Gallen Edition
Web-based business simulation game for St. Gallen startups.
"""

import random
from typing import Dict
from dataclasses import dataclass
from enum import Enum

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
        self.research_protection = 0
        self.monthly_revenue = 0
        self.monthly_expenses = 500
        self.history = []
        self.month = 1
        self.loans = []
        self.is_bankrupt = False
        
        # Swiss events specific attributes
        self.marketing_boost = 0
        self.no_revenue_this_month = False
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
        
        completed_loans = []
        for loan in self.loans:
            loan.months_remaining -= 1
            loan.amount = max(0, loan.amount - loan.monthly_payment)
            if loan.months_remaining <= 0 or loan.amount <= 0:
                completed_loans.append(loan)
        
        for loan in completed_loans:
            self.loans.remove(loan)
        
        status = f"💳 Loan payments: -{total_payment:,} CHF"
        if completed_loans:
            status += f" ({len(completed_loans)} loan(s) paid off!)"
        
        return status
    
    def take_emergency_loan(self) -> str:
        """Take an emergency loan to avoid bankruptcy."""
        loan_amount = 5000
        monthly_payment = 2000
        months = 3
        
        self.loans.append(Loan(loan_amount, months, monthly_payment))
        self.balance += loan_amount
        
        return f"🏛️ Emergency loan approved! +{loan_amount:,} CHF (Repay {monthly_payment:,} CHF/month for {months} months)"
    
    def process_monthly_finances(self) -> Dict[str, int]:
        """Calculate and apply monthly revenue and expenses."""
        if self.no_revenue_this_month:
            self.monthly_revenue = 0
            self.no_revenue_this_month = False
        else:
            base_revenue_per_customer = 5 + random.uniform(0, 3)
            self.monthly_revenue = int(self.customers * self.product_quality * 
                                     self.reputation * base_revenue_per_customer)
        
        self.monthly_expenses = max(100, 500 + (self.employees * 2000))
        
        net_income = self.monthly_revenue - self.monthly_expenses
        self.balance += net_income
        
        self.months_survived = self.month
        
        return {
            'revenue': self.monthly_revenue,
            'expenses': self.monthly_expenses,
            'net_income': net_income
        }
    
    def add_history_entry(self, entry: str):
        """Add an entry to the company's history."""
        self.history.append(f"Month {self.month}: {entry}")


class StartupTycoonGame:
    """Main game controller class for St. Gallen Startup Tycoon."""
    
    def __init__(self):
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
