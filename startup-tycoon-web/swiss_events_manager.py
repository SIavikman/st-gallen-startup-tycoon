#!/usr/bin/env python3
"""
Swiss Events Manager - St. Gallen Startup Events
Event system for the Startup Tycoon web game.
"""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from startup_tycoon_main import Company


class SwissEventManager:
    """Manages all Swiss-themed events for the startup game."""
    
    def __init__(self):
        self.setup_events()
    
    def setup_events(self):
        """Initialize all events with their probabilities."""
        self.events = [
            # Macro-Events
            ("Economic Boom", self.economic_boom_event, 0.03),
            ("Recession Hit", self.recession_event, 0.03),
            ("Interest Rate Rise", self.interest_rate_rise_event, 0.04),
            ("Tax Reduction", self.tax_reduction_event, 0.04),
            
            # St. Gallen Location Events
            ("HSG Career Fair Boom", self.hsg_career_fair_event, 0.06),
            ("HSG Library Crisis", self.hsg_library_crisis_event, 0.05),
            ("Trischli Night Disaster", self.trischli_disaster_event, 0.07),
            ("Trischli Marketing Success", self.trischli_success_event, 0.06),
            ("Olma Bratwurst Partnership", self.olma_partnership_event, 0.06),
            ("Rosenberg Investment", self.rosenberg_investment_event, 0.04),
            ("Drei Weihern Party", self.drei_weihern_party_event, 0.08),
            
            # Positive Events
            ("Startup Award", self.startup_award_event, 0.05),
            ("Viral TikTok", self.viral_tiktok_event, 0.06),
            ("Good Press", self.good_press_event, 0.08),
            ("Innovation Grant", self.innovation_grant_event, 0.05),
            ("Tourist Boom", self.tourist_boom_event, 0.07),
            
            # Negative Events
            ("Server Crash", self.server_crash_event, 0.08),
            ("Legal Fine", self.legal_fine_event, 0.07),
            ("Employee Quits", self.employee_quits_event, 0.09),
            ("Big Customer Leaves", self.big_customer_leaves_event, 0.06),
            ("Social Media Shitstorm", self.social_media_shitstorm_event, 0.05),
            ("Fraud Accusations", self.fraud_accusations_event, 0.04),
            ("CEO Affair", self.ceo_affair_event, 0.03),
            ("Swiss Bureaucracy", self.bureaucracy_event, 0.10),
            ("Cheese Crisis", self.cheese_crisis_event, 0.04),
            
            # Fun Events
            ("Startup Dog", self.startup_dog_mascot_event, 0.07),
            ("Intern Disaster", self.intern_deletes_data_event, 0.08),
            ("Founder Misses Pitch", self.founder_misses_pitch_event, 0.06),
            ("Comic Sans Code", self.comic_sans_code_event, 0.05),
        ]
    
    def trigger_random_event(self, company) -> str:
        """Trigger a random event based on probabilities."""
        roll = random.random()
        cumulative_prob = 0
        
        for event_name, event_func, probability in self.events:
            cumulative_prob += probability
            if roll <= cumulative_prob:
                return event_func(company)
        
        return "📊 Perfect day in beautiful St. Gallen! Everything runs smoothly!"

    # Economic Events
    def economic_boom_event(self, company):
        company.marketing_boost = 2
        customer_gain = random.randint(15, 25)
        company.customers += customer_gain
        return f"📈 Economic boom in Switzerland! +{customer_gain} customers. Marketing actions will have DOUBLE EFFECT for the next 2 turns!"

    def recession_event(self, company):
        customer_loss = max(1, int(company.customers * 0.10))
        company.customers = max(0, company.customers - customer_loss)
        return f"📉 Recession hits Switzerland! Lost: {customer_loss} customers (-10%)."

    def interest_rate_rise_event(self, company):
        additional_costs = 500
        company.monthly_expenses += additional_costs
        return f"📊 SNB raises interest rate! Monthly costs increase by {additional_costs} CHF."

    def tax_reduction_event(self, company):
        cost_saving = 500
        company.monthly_expenses = max(100, company.monthly_expenses - cost_saving)
        return f"🎉 Tax reduction for startups! Monthly costs reduced by {cost_saving} CHF."

    # St. Gallen Location Events
    def hsg_career_fair_event(self, company):
        customer_gain = random.randint(20, 40)
        reputation_gain = random.uniform(0.2, 0.4)
        company.customers += customer_gain
        company.reputation += reputation_gain
        return f"🎓 HSG career fair success! +{customer_gain} customers, reputation boosted!"
    
    def hsg_library_crisis_event(self, company):
        if company.product_quality > 2.0:
            customer_gain = random.randint(30, 50)
            company.customers += customer_gain
            return f"📚 HSG students love your quality product! +{customer_gain} customers!"
        else:
            customer_loss = random.randint(5, 15)
            company.customers = max(0, company.customers - customer_loss)
            return f"📚 HSG students tried your product but it wasn't good enough! -{customer_loss} customers"
    
    def trischli_disaster_event(self, company):
        employee_cost = company.employees * random.randint(200, 500)
        company.balance -= employee_cost
        return f"🍺 Employees partied too hard at Trischli! Productivity lost: -{employee_cost:,} CHF"
    
    def trischli_success_event(self, company):
        customer_gain = random.randint(25, 45)
        company.customers += customer_gain
        company.reputation += random.uniform(0.1, 0.3)
        return f"🎉 Trischli event sponsorship success! +{customer_gain} customers!"
    
    def olma_partnership_event(self, company):
        revenue_boost = random.randint(1500, 3000)
        company.balance += revenue_boost
        customer_gain = random.randint(15, 30)
        company.customers += customer_gain
        return f"🌭 Olma Bratwurst partnership! +{revenue_boost:,} CHF, +{customer_gain} customers!"
    
    def rosenberg_investment_event(self, company):
        if company.reputation > 2.5:
            investment = random.randint(5000, 8000)
            company.balance += investment
            return f"💎 Rosenberg elite investment! +{investment:,} CHF!"
        else:
            return "💎 Rosenberg kids said 'not exclusive enough, darling'"
    
    def drei_weihern_party_event(self, company):
        if random.random() < 0.7:
            customer_gain = random.randint(20, 40)
            company.customers += customer_gain
            company.reputation += random.uniform(0.2, 0.4)
            return f"🏖️ Drei Weihern party was legendary! +{customer_gain} customers!"
        else:
            damage = random.randint(800, 1500)
            company.balance -= damage
            return f"🏖️ Drei Weihern party got out of hand... cleanup costs: -{damage:,} CHF"

    # Positive Events
    def startup_award_event(self, company):
        prize_money = 3000
        reputation_gain = 0.5
        company.balance += prize_money
        company.reputation += reputation_gain
        customer_gain = random.randint(10, 20)
        company.customers += customer_gain
        return f"🏆 Won St. Gallen Startup Award! +{prize_money:,} CHF, +{customer_gain} customers!"

    def viral_tiktok_event(self, company):
        customer_gain = random.randint(70, 90)
        reputation_gain = random.uniform(0.3, 0.5)
        company.customers += customer_gain
        company.reputation += reputation_gain
        return f"📱 TikTok video goes viral! +{customer_gain} new followers!"

    def good_press_event(self, company):
        reputation_gain = 0.3
        customer_gain = random.randint(15, 25)
        company.reputation += reputation_gain
        company.customers += customer_gain
        newspapers = ["St. Galler Tagblatt", "NZZ", "Blick", "20 Minuten"]
        newspaper = random.choice(newspapers)
        return f"📰 Positive article in {newspaper}! +{customer_gain} customers!"
    
    def innovation_grant_event(self, company):
        grant = random.randint(2000, 5000)
        company.balance += grant
        return f"🏛️ St. Gallen innovation grant received! +{grant:,} CHF!"
    
    def tourist_boom_event(self, company):
        revenue_boost = random.randint(2000, 4000)
        company.balance += revenue_boost
        customer_gain = random.randint(15, 35)
        company.customers += customer_gain
        return f"🎿 Tourist season brings international attention! +{revenue_boost:,} CHF, +{customer_gain} customers!"

    # Negative Events
    def server_crash_event(self, company):
        quality_loss = random.uniform(0.15, 0.25)
        reputation_loss = random.uniform(0.15, 0.25)
        customer_loss = random.randint(8, 15)
        company.product_quality = max(0.1, company.product_quality - quality_loss)
        company.reputation = max(0.1, company.reputation - reputation_loss)
        company.customers = max(0, company.customers - customer_loss)
        return f"💥 Server crash! Quality and reputation suffer, {customer_loss} customers leave!"

    def legal_fine_event(self, company):
        fine = random.randint(1800, 2200)
        if company.research_protection > 0:
            fine = max(500, fine - (company.research_protection * 300))
            protection_text = " (Reduced by Research Protection!)"
        else:
            protection_text = ""
        company.balance -= fine
        company.reputation -= random.uniform(0.1, 0.2)
        violations = ["Data protection violation", "Anti-competitive behavior", "Tax irregularity"]
        violation = random.choice(violations)
        return f"⚖️ Legal penalty: {violation}! -{fine:,} CHF fine{protection_text}"

    def employee_quits_event(self, company):
        if company.employees <= 1:
            return "👋 An employee wanted to quit, but you're alone in the team anyway!"
        company.employees -= 1
        quality_loss = random.uniform(0.1, 0.2)
        customer_loss = random.randint(5, 12)
        company.product_quality = max(0.1, company.product_quality - quality_loss)
        company.customers = max(0, company.customers - customer_loss)
        quit_reasons = ["better offer", "burnout", "moving to Zurich", "starting own startup"]
        reason = random.choice(quit_reasons)
        return f"👋 Key employee quits due to '{reason}'. -1 Employee, quality suffers, {customer_loss} customers unhappy"

    def big_customer_leaves_event(self, company):
        customer_loss = random.randint(25, 35)
        revenue_loss = random.randint(800, 1200)
        company.customers = max(0, company.customers - customer_loss)
        company.balance -= revenue_loss
        company.reputation -= random.uniform(0.1, 0.2)
        return f"😤 Big customer switches to competition! -{customer_loss} customers, -{revenue_loss:,} CHF lost"

    def social_media_shitstorm_event(self, company):
        reputation_loss = random.uniform(0.4, 0.6)
        customer_loss = random.randint(20, 40)
        company.reputation = max(0.1, company.reputation - reputation_loss)
        company.customers = max(0, company.customers - customer_loss)
        shitstorm_reasons = ["bad customer service", "problematic tweets", "greenwashing accusations", "overpriced products"]
        reason = random.choice(shitstorm_reasons)
        return f"💩 Social media shitstorm due to '{reason}'! {customer_loss} customers boycott you"

    def fraud_accusations_event(self, company):
        reputation_loss = random.uniform(0.8, 1.2)
        fine = random.randint(1200, 1800)
        customer_loss = random.randint(15, 30)
        company.reputation = max(0.1, company.reputation - reputation_loss)
        company.balance -= fine
        company.customers = max(0, company.customers - customer_loss)
        return f"🚨 Fraud accusations! -{fine:,} CHF legal costs, {customer_loss} customers leave"

    def ceo_affair_event(self, company):
        reputation_loss = random.uniform(0.3, 0.5)
        customer_loss = random.randint(8, 20)
        legal_costs = random.randint(800, 1500)
        company.reputation = max(0.1, company.reputation - reputation_loss)
        company.customers = max(0, company.customers - customer_loss)
        company.balance -= legal_costs
        if company.employees > 2:
            company.employees -= 1
            additional_text = " HR manager quit!"
        else:
            additional_text = ""
        return f"💔 CEO scandal in Blick! -{legal_costs:,} CHF PR costs, {customer_loss} customers distance themselves{additional_text}"
    
    def bureaucracy_event(self, company):
        if company.research_protection > 0:
            return "📋 Swiss bureaucracy delayed things, but your research team navigated it perfectly!"
        else:
            delay_cost = random.randint(1000, 2500)
            company.balance -= delay_cost
            return f"📋 Swiss bureaucracy strikes again! Paperwork delays cost: -{delay_cost:,} CHF"
    
    def cheese_crisis_event(self, company):
        cost_increase = random.randint(500, 1200)
        company.balance -= cost_increase
        return f"🧀 Appenzeller cheese crisis affects supply chain! Operating costs up: -{cost_increase:,} CHF"

    # Fun Events
    def startup_dog_mascot_event(self, company):
        customer_gain = random.randint(18, 22)
        reputation_gain = random.uniform(0.25, 0.35)
        monthly_costs = random.randint(150, 250)
        company.customers += customer_gain
        company.reputation += reputation_gain
        company.monthly_expenses += monthly_costs
        dog_names = ["Bitzli", "Rüdiger", "Fondue", "Heidi", "Wilhelm Tell"]
        dog_name = random.choice(dog_names)
        return f"🐕 Startup dog '{dog_name}' becomes viral mascot! +{customer_gain} customers, but +{monthly_costs} CHF/month costs"

    def intern_deletes_data_event(self, company):
        customer_loss = random.randint(8, 12)
        quality_loss = random.uniform(0.1, 0.2)
        recovery_costs = random.randint(500, 1000)
        company.customers = max(0, company.customers - customer_loss)
        company.product_quality = max(0.1, company.product_quality - quality_loss)
        company.balance -= recovery_costs
        return f"🤦‍♂️ Intern deletes important data! -{customer_loss} customers, -{recovery_costs:,} CHF recovery costs"

    def founder_misses_pitch_event(self, company):
        company.no_revenue_this_month = True
        reputation_loss = random.uniform(0.2, 0.3)
        company.reputation = max(0.1, company.reputation - reputation_loss)
        miss_reasons = ["overslept", "stuck in traffic", "wrong address", "phone alarm failed"]
        reason = random.choice(miss_reasons)
        return f"😴 Founder misses investor pitch due to '{reason}'! No revenue this month"

    def comic_sans_code_event(self, company):
        quality_loss = random.uniform(0.15, 0.25)
        reputation_gain = random.uniform(0.15, 0.25)
        company.product_quality = max(0.1, company.product_quality - quality_loss)
        company.reputation += reputation_gain
        return f"🤪 Intern rewrites code in Comic Sans! Quality suffers but everyone laughs about it (+Reputation)"
