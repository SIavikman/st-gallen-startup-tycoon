#!/usr/bin/env python3
"""
Swiss Events Manager - St. Galler Startup Events with Swiss humor
Event system for the Startup Tycoon game combining traditional St. Gallen locations
with comprehensive Swiss startup ecosystem events.
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
            # Macro-Events (low probability since they affect everyone)
            ("Economic Boom", self.economic_boom_event, 0.03),
            ("Recession Hit", self.recession_event, 0.03),
            ("Interest Rate Rise", self.interest_rate_rise_event, 0.04),
            ("Tax Reduction", self.tax_reduction_event, 0.04),
            
            # St. Gallen Specific Location Events
            ("HSG Career Fair Boom", self.hsg_career_fair_event, 0.06),
            ("HSG Library Crisis", self.hsg_library_crisis_event, 0.05),
            ("Trischli Night Disaster", self.trischli_disaster_event, 0.07),
            ("Trischli Marketing Success", self.trischli_success_event, 0.06),
            ("Olma Bratwurst Partnership", self.olma_partnership_event, 0.06),
            ("Rosenberg Institute Investment", self.rosenberg_investment_event, 0.04),
            ("Drei Weihern Summer Party", self.drei_weihern_party_event, 0.08),
            
            # Positive Business Events
            ("Startup Award", self.startup_award_event, 0.05),
            ("Viral TikTok", self.viral_tiktok_event, 0.06),
            ("Good Press", self.good_press_event, 0.08),
            ("St. Gallen Innovation Grant", self.innovation_grant_event, 0.05),
            ("Tourist Season Boom", self.tourist_boom_event, 0.07),
            
            # Negative Business Events
            ("Server Crash", self.server_crash_event, 0.08),
            ("Legal Fine", self.legal_fine_event, 0.07),
            ("Employee Quits", self.employee_quits_event, 0.09),
            ("Big Customer Leaves", self.big_customer_leaves_event, 0.06),
            ("Social Media Shitstorm", self.social_media_shitstorm_event, 0.05),
            ("Fraud Accusations", self.fraud_accusations_event, 0.04),
            ("CEO Affair", self.ceo_affair_event, 0.03),
            ("Swiss Bureaucracy Strike", self.bureaucracy_event, 0.10),
            ("Appenzeller Cheese Crisis", self.cheese_crisis_event, 0.04),
            
            # Funny/Absurd Events
            ("Startup Dog", self.startup_dog_mascot_event, 0.07),
            ("Intern Disaster", self.intern_deletes_data_event, 0.08),
            ("Founder Misses Pitch", self.founder_misses_pitch_event, 0.06),
            ("Comic Sans Code", self.comic_sans_code_event, 0.05),
            
            # Mini-Games (lower probability)
            ("Trade Fair Gamble", self.trade_fair_gamble_event, 0.05),
            ("Startup Quiz", self.startup_quiz_event, 0.04),
            ("Dragons Den", self.dragons_den_event, 0.03),
        ]
    
    def trigger_random_event(self, company) -> str:
        """Trigger a random event based on probabilities."""
        roll = random.random()
        cumulative_prob = 0
        
        for event_name, event_func, probability in self.events:
            cumulative_prob += probability
            if roll <= cumulative_prob:
                return event_func(company)
        
        # Fallback - normal operations
        return "📊 Perfect day in beautiful St. Gallen! Everything runs smoothly!"

    # ===== ECONOMIC MACRO-EVENTS =====
    
    def economic_boom_event(self, company):
        """Economic boom - marketing works double"""
        if not hasattr(company, 'marketing_boost'):
            company.marketing_boost = 0
        company.marketing_boost = 2  # Next 2 marketing actions double effective
        
        # Immediate effect
        customer_gain = random.randint(15, 25)
        company.customers += customer_gain
        
        return (f"📈 Economic boom in Switzerland! +{customer_gain} customers immediately. "
               f"Marketing actions will have DOUBLE EFFECT for the next 2 turns!")

    def recession_event(self, company):
        """Recession - everyone loses 10% customers"""
        customer_loss = max(1, int(company.customers * 0.10))
        company.customers = max(0, company.customers - customer_loss)
        
        return (f"📉 Recession hits Switzerland! Lost: {customer_loss} customers (-10%). "
               f"Time for creative cost-cutting measures!")

    def interest_rate_rise_event(self, company):
        """Interest rate rise - fixed costs increase"""
        additional_costs = 500
        company.monthly_expenses += additional_costs
        
        return (f"📊 SNB raises key interest rate! Monthly fixed costs increase by {additional_costs} CHF. "
               f"Expensive times for startups...")

    def tax_reduction_event(self, company):
        """Tax reduction - everyone saves costs"""
        cost_saving = 500
        company.monthly_expenses = max(100, company.monthly_expenses - cost_saving)
        
        return (f"🎉 Tax reduction for startups! Monthly costs reduced by {cost_saving} CHF. "
               f"Thank you, Federal Council!")

    # ===== ST. GALLEN LOCATION EVENTS =====
    
    def hsg_career_fair_event(self, company):
        """HSG career fair attracts wealthy students"""
        customer_gain = random.randint(20, 40)
        reputation_gain = random.uniform(0.2, 0.4)
        company.customers += customer_gain
        company.reputation += reputation_gain
        
        return (f"🎓 HSG career fair was a hit! Rich students love your startup! "
               f"+{customer_gain} customers, reputation boosted!")
    
    def hsg_library_crisis_event(self, company):
        """Students stressed about no study spaces"""
        if company.product_quality > 2.0:
            customer_gain = random.randint(30, 50)
            company.customers += customer_gain
            return (f"📚 HSG students desperate for study solutions! Your quality product saves the day! "
                   f"+{customer_gain} customers!")
        else:
            customer_loss = random.randint(5, 15)
            company.customers = max(0, company.customers - customer_loss)
            return (f"📚 HSG students tried your product but it wasn't good enough for their standards! "
                   f"-{customer_loss} customers")
    
    def trischli_disaster_event(self, company):
        """Employees party too hard at the famous nightclub"""
        employee_cost = company.employees * random.randint(200, 500)
        company.balance -= employee_cost
        
        return (f"🍺 Your employees partied too hard at Trischli and called in sick! "
               f"Productivity lost: -{employee_cost:,} CHF")
    
    def trischli_success_event(self, company):
        """Nightclub partnership brings exposure"""
        customer_gain = random.randint(25, 45)
        company.customers += customer_gain
        company.reputation += random.uniform(0.1, 0.3)
        
        return (f"🎉 Your startup sponsored a Trischli event! Long queue = great exposure! "
               f"+{customer_gain} customers!")
    
    def olma_partnership_event(self, company):
        """Traditional sausage collaboration opportunity"""
        revenue_boost = random.randint(1500, 3000)
        company.balance += revenue_boost
        customer_gain = random.randint(15, 30)
        company.customers += customer_gain
        
        return (f"🌭 Partnered with traditional Olma Bratwurst stand! Tourists love it! "
               f"+{revenue_boost:,} CHF, +{customer_gain} customers!")
    
    def rosenberg_investment_event(self, company):
        """Elite millionaire kids consider investment"""
        if company.reputation > 2.5:
            investment = random.randint(5000, 8000)
            company.balance += investment
            return (f"💎 Rosenberg millionaire kids invested in your startup! Elite approval! "
                   f"+{investment:,} CHF!")
        else:
            return (f"💎 Rosenberg kids looked at your startup but said "
                   f"'not exclusive enough, darling' 💅")
    
    def drei_weihern_party_event(self, company):
        """Team building event at the popular lakes"""
        if random.random() < 0.7:  # 70% chance positive
            customer_gain = random.randint(20, 40)
            company.customers += customer_gain
            company.reputation += random.uniform(0.2, 0.4)
            return (f"🖖 Your team's Drei Weihern party was legendary! Great networking! "
                   f"+{customer_gain} customers, reputation boosted!")
        else:
            damage = random.randint(800, 1500)
            company.balance -= damage
            return (f"🖖 Drei Weihern party got out of hand... cleanup costs and fines: "
                   f"-{damage:,} CHF")

    # ===== POSITIVE COMPANY EVENTS =====
    
    def startup_award_event(self, company):
        """Startup award won"""
        prize_money = 3000
        reputation_gain = 0.5
        
        company.balance += prize_money
        company.reputation += reputation_gain
        
        # Additional customer gain through publicity
        customer_gain = random.randint(10, 20)
        company.customers += customer_gain
        
        return (f"🏆 Won St. Gallen Startup Award! +{prize_money:,} CHF prize money, "
               f"massive reputation boost, +{customer_gain} new customers through media buzz!")

    def viral_tiktok_event(self, company):
        """Viral TikTok video"""
        customer_gain = random.randint(70, 90)
        reputation_gain = random.uniform(0.3, 0.5)
        
        company.customers += customer_gain
        company.reputation += reputation_gain
        
        return (f"📱 Your TikTok video goes viral! #StartupLife trending in Switzerland. "
               f"+{customer_gain} new customers are now following you!")

    def good_press_event(self, company):
        """Good press article"""
        reputation_gain = 0.3
        customer_gain = random.randint(15, 25)
        
        company.reputation += reputation_gain
        company.customers += customer_gain
        
        newspapers = ["St. Galler Tagblatt", "NZZ", "Blick", "20 Minuten", "Handelszeitung"]
        newspaper = random.choice(newspapers)
        
        return (f"📰 Positive article in {newspaper}! 'St. Gallen Startup Revolutionizes Market.' "
               f"Reputation strengthened, +{customer_gain} interested customers!")
    
    def innovation_grant_event(self, company):
        """Local government funding opportunity"""
        grant = random.randint(2000, 5000)
        company.balance += grant
        
        return (f"🏛️ St. Gallen city innovation grant received! Local government supports you! "
               f"+{grant:,} CHF!")
    
    def tourist_boom_event(self, company):
        """International visitors boost business"""
        revenue_boost = random.randint(2000, 4000)
        company.balance += revenue_boost
        customer_gain = random.randint(15, 35)
        company.customers += customer_gain
        
        return (f"🎿 Tourist season brings international attention! "
               f"+{revenue_boost:,} CHF, +{customer_gain} customers!")

    # ===== NEGATIVE COMPANY EVENTS =====
    
    def server_crash_event(self, company):
        """Server crash"""
        quality_loss = random.uniform(0.15, 0.25)
        reputation_loss = random.uniform(0.15, 0.25)
        customer_loss = random.randint(8, 15)
        
        company.product_quality = max(0.1, company.product_quality - quality_loss)
        company.reputation = max(0.1, company.reputation - reputation_loss)
        company.customers = max(0, company.customers - customer_loss)
        
        return (f"💥 Server crash! Customers are angry. Quality and reputation suffer, "
               f"{customer_loss} customers jump ship. Time for better IT infrastructure!")

    def legal_fine_event(self, company):
        """Legal fine"""
        fine = random.randint(1800, 2200)
        
        # Research protection helps
        if company.research_protection > 0:
            fine = max(500, fine - (company.research_protection * 300))
            protection_text = " (Reduced by Research Protection!)"
        else:
            protection_text = ""
        
        company.balance -= fine
        company.reputation -= random.uniform(0.1, 0.2)
        
        violations = ["Data protection violation", "Anti-competitive behavior", "Tax irregularity"]
        violation = random.choice(violations)
        
        return (f"⚖️ Legal penalty: {violation}! -{fine:,} CHF fine{protection_text}. "
               f"Lawyer was more expensive than expected...")

    def employee_quits_event(self, company):
        """Employee quits"""
        if company.employees <= 1:
            return "👋 An employee wanted to quit, but you're alone in the team anyway!"
        
        company.employees -= 1
        quality_loss = random.uniform(0.1, 0.2)
        customer_loss = random.randint(5, 12)
        
        company.product_quality = max(0.1, company.product_quality - quality_loss)
        company.customers = max(0, company.customers - customer_loss)
        
        quit_reasons = ["better offer", "burnout", "moving to Zurich", "wants to start own startup"]
        reason = random.choice(quit_reasons)
        
        return (f"👋 Key employee quits due to '{reason}'. -1 Employee, "
               f"quality suffers, {customer_loss} customers unhappy.")

    def big_customer_leaves_event(self, company):
        """Big customer switches to competition"""
        customer_loss = random.randint(25, 35)
        revenue_loss = random.randint(800, 1200)
        
        company.customers = max(0, company.customers - customer_loss)
        company.balance -= revenue_loss
        company.reputation -= random.uniform(0.1, 0.2)
        
        return (f"😤 Big customer switches to competition! -{customer_loss} customers lost, "
               f"-{revenue_loss:,} CHF lost revenue. Ouch!")

    def social_media_shitstorm_event(self, company):
        """Shitstorm on social media"""
        reputation_loss = random.uniform(0.4, 0.6)
        customer_loss = random.randint(20, 40)
        
        company.reputation = max(0.1, company.reputation - reputation_loss)
        company.customers = max(0, company.customers - customer_loss)
        
        shitstorm_reasons = ["bad customer service", "problematic tweets", "greenwashing accusations", "overpriced products"]
        reason = random.choice(shitstorm_reasons)
        
        return (f"💩 Social media shitstorm due to '{reason}'! Reputation in the gutter, "
               f"{customer_loss} customers boycott you. Time for damage control!")

    def fraud_accusations_event(self, company):
        """Fraud accusations"""
        reputation_loss = random.uniform(0.8, 1.2)
        fine = random.randint(1200, 1800)
        customer_loss = random.randint(15, 30)
        
        company.reputation = max(0.1, company.reputation - reputation_loss)
        company.balance -= fine
        company.customers = max(0, company.customers - customer_loss)
        
        return (f"🚨 Fraud accusations in the media! -{fine:,} CHF legal costs, "
               f"reputation destroyed, {customer_loss} customers jump ship. Presumption of innocence? Not here!")

    def ceo_affair_event(self, company):
        """CEO affair with HR - absurd but realistic"""
        reputation_loss = random.uniform(0.3, 0.5)
        customer_loss = random.randint(8, 20)
        legal_costs = random.randint(800, 1500)
        
        company.reputation = max(0.1, company.reputation - reputation_loss)
        company.customers = max(0, company.customers - customer_loss)
        company.balance -= legal_costs
        
        if company.employees > 2:
            company.employees -= 1  # HR quits
            additional_text = " HR manager has quit!"
        else:
            additional_text = ""
        
        return (f"💔 CEO affair scandal in Blick newspaper! -{legal_costs:,} CHF PR costs, "
               f"reputation damaged, {customer_loss} customers distance themselves.{additional_text}")
    
    def bureaucracy_event(self, company):
        """Swiss bureaucracy delays"""
        if company.research_protection > 0:
            return (f"📋 Swiss bureaucracy slowed things down, but your research team "
                   f"navigated it perfectly! No impact!")
        else:
            delay_cost = random.randint(1000, 2500)
            company.balance -= delay_cost
            return (f"📋 Swiss bureaucracy strikes again! Paperwork delays cost you: "
                   f"-{delay_cost:,} CHF")
    
    def cheese_crisis_event(self, company):
        """Local suppliers affected"""
        cost_increase = random.randint(500, 1200)
        company.balance -= cost_increase
        
        return (f"🧀 Appenzeller cheese crisis affects local supply chain! "
               f"Operating costs up: -{cost_increase:,} CHF")

    # ===== FUNNY / ABSURD EVENTS =====

    def startup_dog_mascot_event(self, company):
        """Startup dog becomes mascot"""
        customer_gain = random.randint(18, 22)
        reputation_gain = random.uniform(0.25, 0.35)
        monthly_costs = random.randint(150, 250)
        
        company.customers += customer_gain
        company.reputation += reputation_gain
        company.monthly_expenses += monthly_costs
        
        dog_names = ["Bitzli", "Rüdiger", "Fondue", "Heidi", "Wilhelm Tell"]
        dog_name = random.choice(dog_names)
        
        return (f"🐕 Startup dog '{dog_name}' becomes viral mascot! +{customer_gain} customers love him, "
               f"reputation rises, but +{monthly_costs} CHF/month for dog food and care!")

    def intern_deletes_data_event(self, company):
        """Intern deletes data"""
        customer_loss = random.randint(8, 12)
        quality_loss = random.uniform(0.1, 0.2)
        recovery_costs = random.randint(500, 1000)
        
        company.customers = max(0, company.customers - customer_loss)
        company.product_quality = max(0.1, company.product_quality - quality_loss)
        company.balance -= recovery_costs
        
        return (f"🤦‍♂️ Intern deletes important data! 'Oops, wrong folder...' "
               f"-{customer_loss} customers due to outages, -{recovery_costs:,} CHF data recovery. "
               f"Backup next time!")

    def founder_misses_pitch_event(self, company):
        """Founder misses pitch"""
        company.no_revenue_this_month = True
        
        reputation_loss = random.uniform(0.2, 0.3)
        company.reputation = max(0.1, company.reputation - reputation_loss)
        
        miss_reasons = ["overslept", "stuck in traffic", "wrong address", "phone alarm failed"]
        reason = random.choice(miss_reasons)
        
        return (f"😴 Founder misses important investor pitch due to '{reason}'! "
               f"No revenue this month, reputation suffers. Embarrassing!")

    def comic_sans_code_event(self, company):
        """Code in Comic Sans"""
        quality_loss = random.uniform(0.15, 0.25)
        reputation_gain = random.uniform(0.15, 0.25)
        
        company.product_quality = max(0.1, company.product_quality - quality_loss)
        company.reputation += reputation_gain
        
        return (f"🤪 Intern rewrites all code in Comic Sans font! "
               f"Quality suffers (-{quality_loss:.1f}), but everyone laughs about it (+Reputation). "
               f"At least you're famous now!")

    # ===== MINI-GAME EVENTS =====

    def trade_fair_gamble_event(self, company):
        """Trade fair pitch gamble - returns interactive event"""
        cost = 1000
        
        if company.balance < cost:
            return f"💸 Trade fair pitch offered, but budget insufficient! Need {cost:,} CHF."
        
        return {
            'type': 'interactive',
            'event_name': 'trade_fair',
            'title': '🎪 TRADE FAIR PITCH OPPORTUNITY',
            'description': f'Cost: {cost:,} CHF<br>50% Chance: +100 customers<br>50% Chance: Flop, money gone<br>Your Budget: {company.balance:,} CHF',
            'options': [
                {'id': 'yes', 'text': 'Pitch at trade fair', 'data': {'cost': cost}},
                {'id': 'no', 'text': 'Decline opportunity', 'data': {}}
            ]
        }

    def startup_quiz_event(self, company):
        """Startup quiz - returns interactive event"""
        questions = [
            {"q": "What percentage of Swiss startups fail in the first 5 years?", 
             "options": [{"id": "A", "text": "50%"}, {"id": "B", "text": "70%"}, {"id": "C", "text": "90%"}], "correct": "C"},
            {"q": "What does 'MVP' mean in the startup world?", 
             "options": [{"id": "A", "text": "Most Valuable Player"}, {"id": "B", "text": "Minimum Viable Product"}, {"id": "C", "text": "Maximum Venture Profit"}], "correct": "B"},
            {"q": "Which city has the largest startup ecosystem in Switzerland?", 
             "options": [{"id": "A", "text": "Zurich"}, {"id": "B", "text": "Geneva"}, {"id": "C", "text": "St. Gallen"}], "correct": "A"},
            {"q": "What is the most famous nightclub in St. Gallen?", 
             "options": [{"id": "A", "text": "Palazzo"}, {"id": "B", "text": "Trischli"}, {"id": "C", "text": "Einstein"}], "correct": "B"},
        ]
        
        question = random.choice(questions)
        
        return {
            'type': 'interactive',
            'event_name': 'quiz',
            'title': '🧠 STARTUP QUIZ BONUS ROUND',
            'description': f'{question["q"]}<br>Correct answer = +2,000 CHF bonus!',
            'options': [{'id': opt['id'], 'text': opt['text'], 'data': {'correct': question['correct']}} for opt in question['options']]
        }

    def dragons_den_event(self, company):
        """Dragons' Den Switzerland - returns interactive event"""
        cost = 500
        
        if company.balance < cost:
            return f"📺 'Dragons' Den' invitation, but travel too expensive! Need {cost:,} CHF."
        
        return {
            'type': 'interactive',
            'event_name': 'dragons_den',
            'title': '🦈 DRAGONS\' DEN SWITZERLAND',
            'description': f'TV appearance chance!<br>Cost: {cost:,} CHF (travel, hotel)<br>50% Chance: +5,000 CHF investment<br>50% Chance: Embarrassment, -0.5 reputation<br>Your Budget: {company.balance:,} CHF',
            'options': [
                {'id': 'yes', 'text': 'Enter the Dragons\' Den', 'data': {'cost': cost}},
                {'id': 'no', 'text': 'Decline invitation', 'data': {}}
            ]
        }

    # ===== HUMOROUS MESSAGES =====

    def get_humorous_endgame_message(self, company, rank, total_players):
        """Returns humorous end messages based on performance"""
        score = company.calculate_score()
        balance = company.balance
        
        # Victory messages (1st place)
        if rank == 1:
            if balance > 50000:
                return "🏆 Congratulations! You're richer than the Migros cashier on payday!"
            elif balance > 30000:
                return "👑 Your coffers are so full, you could almost afford a studio in Zurich!"
            elif balance > 20000:
                return "💰 Your treasure chest is fuller than the HSG library during finals!"
            else:
                return "🎉 Congrats! You have more customers than FC St. Gallen has fans in Kybunpark!"
        
        # Middle places
        elif rank <= total_players // 2:
            middle_messages = [
                "📈 Solid performance! You were more successful than SBB's punctuality.",
                "👍 Not bad! You achieved more than a tourist trying to pronounce Chuchichäschtli.",
                "⚖️ Balanced like a Swiss bank account - neither poor nor rich, but stable!",
                "🎯 Midfield like Switzerland at Eurovision - always participating, rarely at the top.",
                "🏔️ Decent like Swiss chocolate - not the best, but still pretty sweet!"
            ]
            return random.choice(middle_messages)
        
        # Poor performance
        else:
            if balance < -2000:
                return "💸 Game Over: You went bankrupt faster than a Basel resident finding affordable housing in Zurich."
            elif balance < 5000:
                return "📉 Game Over: Your cash fell deeper than the fog line in November."
            elif company.reputation < 0.5:
                return "😬 Your reputation is so bad, even spam emails are more popular."
            else:
                return "🌭 Unfortunately failed, but hey - at least there's fresh bratwurst at Olma!"
        
        # Fallback
        return "🎮 Game Over! Time for a new round of St. Gallen Startup Tycoon!"

    def get_bankruptcy_message(self):
        """Special messages for bankruptcy"""
        bankruptcy_messages = [
            "💀 Bankrupt! You're broke like a Swiss person without health insurance.",
            "🚨 Bankruptcy! Even your emergency fund has quit.",
            "📉 Broke! You have less money than a student after the first week of semester.",
            "💸 Bankrupt! Your account balance is more negative than February weather in St. Gallen.",
            "🍴 Game Over! Time to move back in with mom and eat Cervelat.",
            "💔 Bankrupt! Your startup dream crashed harder than the Swiss national football team's World Cup hopes."
        ]
        return random.choice(bankruptcy_messages)

    def get_special_achievement_messages(self, company):
        """Special achievement messages for exceptional performance"""
        achievements = []
        
        if company.customers > 500:
            achievements.append("🌟 'Customer Magnet': More fans than an alphorn concert!")
        
        if company.reputation > 3.0:
            achievements.append("⭐ 'Reputation King': More popular than Rösti on Sunday!")
        
        if company.product_quality > 3.0:
            achievements.append("🔧  'Quality Guru': More precise than a Swiss watch!")
        
        if company.employees > 10:
            achievements.append("👥 'Team Builder': More employees than some mountain huts have beds!")
        
        if company.balance > 100000:
            achievements.append("💎 'Money Magnate': Richer than a Zurich banker!")
        
        if hasattr(company, 'months_survived') and company.months_survived == 12 and company.balance > 0:
            achievements.append("🏔️ 'Survival Artist': Survived 12 months like a real Swiss winter!")
        
        if company.customers > 200 and company.reputation > 2.0:
            achievements.append("🎓 'HSG Favorite': Even the snobby business students approve!")
        
        if company.balance > 50000 and company.employees > 5:
            achievements.append("🏢 'St. Gallen Success Story': From Drei Weihern dreamer to business mogul!")
        
        return achievements
