#Career Navigator AI 

import os
import requests
from dotenv import load_dotenv

load_dotenv() 
API_KEY = os.getenv("OPENROUTER_API_KEY")

class CareerNavigator:
    def __init__(self):
        self.user_name = ""
        self.user_age = ""
        self.user_education = ""
        self.quiz_results = {}
        self.conversation_history = []
        
        # 20 Quiz Questions
        self.quiz_questions = [
            {
                "question": "How do you feel about solving complex technical problems?",
                "options": {
                    "A": {"text": "Love it - I enjoy coding and logic", "scores": {"Technology/IT": 10, "Engineering": 8}},
                    "B": {"text": "Sometimes - if it's interesting", "scores": {"Technology/IT": 5, "Science/Research": 5}},
                    "C": {"text": "Not really - I prefer people interactions", "scores": {"Marketing/Sales": 8, "Education/Teaching": 8}},
                    "D": {"text": "Hate it - gives me headache", "scores": {"Creative/Design": 6, "Hospitality/Travel": 6}}
                }
            },
            {
                "question": "What's your ideal work environment?",
                "options": {
                    "A": {"text": "Office with a team", "scores": {"Business/Finance": 8, "Marketing/Sales": 8}},
                    "B": {"text": "Remote/WFH - alone time", "scores": {"Technology/IT": 9, "Creative/Design": 8}},
                    "C": {"text": "Hospital/Clinic with patients", "scores": {"Healthcare/Medicine": 10, "Education/Teaching": 5}},
                    "D": {"text": "Outdoor/Field work", "scores": {"Engineering": 8, "Hospitality/Travel": 7}}
                }
            },
            {
                "question": "How important is salary to you?",
                "options": {
                    "A": {"text": "Extremely - I want high income", "scores": {"Business/Finance": 10, "Technology/IT": 9, "Law/Legal": 9}},
                    "B": {"text": "Important but not everything", "scores": {"Engineering": 7, "Healthcare/Medicine": 7}},
                    "C": {"text": "Average salary is fine", "scores": {"Education/Teaching": 8, "Creative/Design": 7}},
                    "D": {"text": "Passion matters more", "scores": {"Science/Research": 9, "Hospitality/Travel": 8}}
                }
            },
            {
                "question": "Do you like working with numbers and data?",
                "options": {
                    "A": {"text": "Love it - Excel is my friend", "scores": {"Business/Finance": 10, "Technology/IT": 8}},
                    "B": {"text": "Okay with basic math", "scores": {"Engineering": 7, "Science/Research": 8}},
                    "C": {"text": "Not really - prefer words", "scores": {"Creative/Design": 8, "Marketing/Sales": 7, "Law/Legal": 8}},
                    "D": {"text": "Hate it completely", "scores": {"Healthcare/Medicine": 5, "Hospitality/Travel": 7}}
                }
            },
            {
                "question": "How do you feel about public speaking?",
                "options": {
                    "A": {"text": "Love it - I'm a natural", "scores": {"Marketing/Sales": 10, "Education/Teaching": 9, "Law/Legal": 9}},
                    "B": {"text": "Can do it if needed", "scores": {"Business/Finance": 7, "Hospitality/Travel": 7}},
                    "C": {"text": "Nervous but manageable", "scores": {"Technology/IT": 4, "Creative/Design": 5}},
                    "D": {"text": "Absolutely hate it", "scores": {"Science/Research": 8, "Engineering": 7}}
                }
            },
            {
                "question": "What type of problems do you enjoy solving?",
                "options": {
                    "A": {"text": "Technical/mechanical issues", "scores": {"Engineering": 10, "Technology/IT": 9}},
                    "B": {"text": "Business/strategy problems", "scores": {"Business/Finance": 10, "Law/Legal": 8}},
                    "C": {"text": "People/relationship issues", "scores": {"Healthcare/Medicine": 8, "Education/Teaching": 9}},
                    "D": {"text": "Creative/design challenges", "scores": {"Creative/Design": 10, "Technology/IT": 5}}
                }
            },
            {
                "question": "Do you prefer structured or flexible work?",
                "options": {
                    "A": {"text": "Highly structured with clear rules", "scores": {"Law/Legal": 10, "Business/Finance": 8}},
                    "B": {"text": "Some structure is good", "scores": {"Engineering": 7, "Education/Teaching": 7}},
                    "C": {"text": "Flexible and creative freedom", "scores": {"Creative/Design": 10, "Technology/IT": 8}},
                    "D": {"text": "Complete freedom - no boss", "scores": {"Hospitality/Travel": 8}}
                }
            },
            {
                "question": "How important is helping others in your career?",
                "options": {
                    "A": {"text": "Very important - want to serve", "scores": {"Healthcare/Medicine": 10, "Education/Teaching": 10}},
                    "B": {"text": "Somewhat important", "scores": {"Law/Legal": 7, "Hospitality/Travel": 7}},
                    "C": {"text": "Not a priority", "scores": {"Technology/IT": 4, "Business/Finance": 4}},
                    "D": {"text": "I prefer working alone", "scores": {"Science/Research": 8, "Creative/Design": 6}}
                }
            },
            {
                "question": "Do you like traveling for work?",
                "options": {
                    "A": {"text": "Love it - adventure!", "scores": {"Hospitality/Travel": 10, "Marketing/Sales": 8}},
                    "B": {"text": "Occasional travel is fine", "scores": {"Business/Finance": 6, "Engineering": 5}},
                    "C": {"text": "Prefer staying local", "scores": {"Healthcare/Medicine": 7, "Education/Teaching": 8}},
                    "D": {"text": "Hate traveling completely", "scores": {"Technology/IT": 9, "Science/Research": 7}}
                }
            },
            {
                "question": "What's your creativity level?",
                "options": {
                    "A": {"text": "Very creative - love art/design", "scores": {"Creative/Design": 10, "Marketing/Sales": 7}},
                    "B": {"text": "Somewhat creative", "scores": {"Technology/IT": 6, "Education/Teaching": 5}},
                    "C": {"text": "Not very creative", "scores": {"Business/Finance": 8, "Law/Legal": 8}},
                    "D": {"text": "Analytical is my strength", "scores": {"Science/Research": 9, "Technology/IT": 8}}
                }
            },
            {
                "question": "Do you like managing people?",
                "options": {
                    "A": {"text": "Love leading teams", "scores": {"Business/Finance": 9, "Marketing/Sales": 9}},
                    "B": {"text": "Can do it if needed", "scores": {"Education/Teaching": 7, "Healthcare/Medicine": 6}},
                    "C": {"text": "Prefer being individual contributor", "scores": {"Technology/IT": 8, "Creative/Design": 8}},
                    "D": {"text": "Hate managing others", "scores": {"Engineering": 7, "Law/Legal": 6}}
                }
            },
            {
                "question": "How do you feel about continuous learning?",
                "options": {
                    "A": {"text": "Love it - always studying", "scores": {"Technology/IT": 10, "Science/Research": 10}},
                    "B": {"text": "Okay with occasional training", "scores": {"Business/Finance": 7, "Engineering": 7}},
                    "C": {"text": "Prefer learning on the job", "scores": {"Marketing/Sales": 6, "Hospitality/Travel": 6}},
                    "D": {"text": "Want fixed knowledge", "scores": {"Law/Legal": 5, "Education/Teaching": 5}}
                }
            },
            {
                "question": "What's your attention to detail?",
                "options": {
                    "A": {"text": "Extremely detail-oriented", "scores": {"Law/Legal": 10, "Science/Research": 9}},
                    "B": {"text": "Good with details", "scores": {"Business/Finance": 8, "Engineering": 8}},
                    "C": {"text": "Average - big picture person", "scores": {"Marketing/Sales": 7, "Creative/Design": 6}},
                    "D": {"text": "Details bore me", "scores": {"Hospitality/Travel": 5, "Education/Teaching": 5}}
                }
            },
            {
                "question": "Do you like working with technology?",
                "options": {
                    "A": {"text": "Love it - tech enthusiast", "scores": {"Technology/IT": 10, "Engineering": 8}},
                    "B": {"text": "Comfortable with basic tech", "scores": {"Business/Finance": 6, "Science/Research": 6}},
                    "C": {"text": "Prefer minimal technology", "scores": {"Education/Teaching": 5, "Healthcare/Medicine": 5}},
                    "D": {"text": "Avoid technology when possible", "scores": {"Creative/Design": 4, "Hospitality/Travel": 4}}
                }
            },
            {
                "question": "How do you handle stress and pressure?",
                "options": {
                    "A": {"text": "Thrive under pressure", "scores": {"Business/Finance": 9, "Law/Legal": 9}},
                    "B": {"text": "Manage it well", "scores": {"Technology/IT": 7, "Engineering": 7}},
                    "C": {"text": "Prefer low-stress environment", "scores": {"Education/Teaching": 8, "Science/Research": 7}},
                    "D": {"text": "Avoid stress completely", "scores": {"Creative/Design": 6, "Hospitality/Travel": 6}}
                }
            },
            {
                "question": "What's your preferred project type?",
                "options": {
                    "A": {"text": "Short-term, fast results", "scores": {"Marketing/Sales": 9, "Hospitality/Travel": 8}},
                    "B": {"text": "Long-term, in-depth projects", "scores": {"Science/Research": 10, "Engineering": 8}},
                    "C": {"text": "Mix of both", "scores": {"Business/Finance": 7, "Creative/Design": 7}},
                    "D": {"text": "Ongoing, consistent work", "scores": {"Healthcare/Medicine": 8, "Education/Teaching": 8}}
                }
            },
            {
                "question": "Do you like competition?",
                "options": {
                    "A": {"text": "Love competition - want to win", "scores": {"Business/Finance": 9, "Marketing/Sales": 9}},
                    "B": {"text": "Healthy competition is good", "scores": {"Technology/IT": 6, "Engineering": 6}},
                    "C": {"text": "Prefer collaboration over competition", "scores": {"Education/Teaching": 8, "Healthcare/Medicine": 8}},
                    "D": {"text": "Hate competition completely", "scores": {"Creative/Design": 7, "Science/Research": 7}}
                }
            },
            {
                "question": "How important is job stability?",
                "options": {
                    "A": {"text": "Extremely important", "scores": {"Healthcare/Medicine": 9, "Education/Teaching": 9}},
                    "B": {"text": "Important but open to risk", "scores": {"Engineering": 7, "Law/Legal": 7}},
                    "C": {"text": "Not a major concern", "scores": {"Technology/IT": 5, "Creative/Design": 5}},
                    "D": {"text": "Prefer high-risk high-reward", "scores": {"Marketing/Sales": 7}}
                }
            },
            {
                "question": "Do you like writing and documentation?",
                "options": {
                    "A": {"text": "Love writing - very expressive", "scores": {"Law/Legal": 9, "Marketing/Sales": 8}},
                    "B": {"text": "Okay with basic writing", "scores": {"Education/Teaching": 7, "Business/Finance": 6}},
                    "C": {"text": "Prefer minimal writing", "scores": {"Technology/IT": 5, "Engineering": 5}},
                    "D": {"text": "Hate writing completely", "scores": {"Healthcare/Medicine": 4, "Hospitality/Travel": 5}}
                }
            },
            {
                "question": "What's your ideal career growth path?",
                "options": {
                    "A": {"text": "Climb corporate ladder", "scores": {"Business/Finance": 10, "Law/Legal": 9}},
                    "B": {"text": "Become an expert/specialist", "scores": {"Technology/IT": 9, "Science/Research": 9}},
                    "C": {"text": "Start my own business", "scores": {"Marketing/Sales": 8, "Creative/Design": 7}},
                    "D": {"text": "Steady growth is fine", "scores": {"Education/Teaching": 8, "Healthcare/Medicine": 7}}
                }
            }
        ]
    
    def calculate_percentages(self, scores):
        """Convert raw scores to percentages"""
        if not scores:
            return {}
        max_possible = 200
        percentages = {}
        for career, score in scores.items():
            percentage = (score / max_possible) * 100
            percentages[career] = round(percentage, 1)
        return dict(sorted(percentages.items(), key=lambda x: -x[1]))
    
    def run_quiz(self):        
        scores = {}
        
        for i, q in enumerate(self.quiz_questions, 1):
            print(f"\n Q{i}/20: {q['question']}")
            print("-" * 40)
            for opt, details in q['options'].items():
                print(f"   {opt}. {details['text']}")
            
            answer = input(f"\nYour answer ({'/'.join(q['options'].keys())}): ").upper()
            while answer not in q['options']:
                answer = input(f"Choose {', '.join(q['options'].keys())}: ").upper()
            
            for career, points in q['options'][answer]['scores'].items():
                if career not in scores:
                    scores[career] = 0
                scores[career] += points
            
            if i % 5 == 0:
                print(f"\n Progress: {i}/20 ({i*5}%)\n")
        
        self.quiz_results = self.calculate_percentages(scores)
        
        print(" YOUR TOP CAREER MATCHES ")
        
        for career, percentage in list(self.quiz_results.items())[:5]:
            bar = " " * int(percentage/2) + " " * (50 - int(percentage/2))
            print(f"{career:<20} {percentage:>5}%  {bar}")
        
        print("\n These are suggestions! You can choose ANY field for your roadmap.\n")
        return self.quiz_results
    
    def chat(self, user_message):
        """Simple chat with short responses"""
        self.conversation_history.append({"role": "user", "content": user_message})
        
        system_prompt = f"""You are Career Navigator AI. User: {self.user_name}, Age: {self.user_age}, Education: {self.user_education}

RULES:
- Keep responses UNDER 50 WORDS
- Use bullet points (•)
- Be direct and helpful
- No long paragraphs
"""
        
        messages = [{"role": "system", "content": system_prompt}] + self.conversation_history[-20:]
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-3.5-turbo", "messages": messages, "max_tokens": 250},
                timeout=30
            )
            
            if response.status_code == 200:
                ai_reply = response.json()["choices"][0]["message"]["content"]
                self.conversation_history.append({"role": "assistant", "content": ai_reply})
                return ai_reply
            else:
                return f" Error: {response.status_code}"
        except Exception as e:
            return f" Connection error: {str(e)}"
    
    def show_available_fields(self):
        """Show all available career fields"""
        fields = [
            "1. Technology/IT",
            "2. Business/Finance",
            "3. Healthcare/Medicine",
            "4. Engineering",
            "5. Creative/Design",
            "6. Education/Teaching",
            "7. Law/Legal",
            "8. Marketing/Sales",
            "9. Science/Research",
            "10. Hospitality/Travel"
        ]        
        print(" AVAILABLE CAREER FIELDS:")
        for field in fields:
            print(f"   {field}")
        print("-"*40)
    
    def generate_roadmap(self):        
        # Show quiz results if available (just for reference)
        if self.quiz_results:
            print("\n Your quiz top matches (for reference):")
            top_3 = list(self.quiz_results.items())[:3]
            for career, percentage in top_3:
                print(f"   • {career}: {percentage}%")
        
        # Let user choose their field
        print("\n" + "="*60)
        self.show_available_fields()
        
        print("\n Tip: You can choose ANY field - not just your top match!")
        print("   Type the exact field name or number\n")
        
        field_choice = input("Which career field interests you? ").strip()
        
        # Map numbers to field names
        field_map = {
            "1": "Technology/IT",
            "2": "Business/Finance", 
            "3": "Healthcare/Medicine",
            "4": "Engineering",
            "5": "Creative/Design",
            "6": "Education/Teaching",
            "7": "Law/Legal",
            "8": "Marketing/Sales",
            "9": "Science/Research",
            "10": "Hospitality/Travel"
        }
        
        # Convert number to field name if needed
        if field_choice in field_map:
            selected_field = field_map[field_choice]
        else:
            selected_field = field_choice
        
        # Ask for country
        print("\n" + "-"*40)
        country = input(" Which country do you want to settle in? ").strip()
        
        print(f"\n Generating roadmap for: {selected_field}")
        print(f" Target country: {country}")
        print("\nCreating your 4-phase roadmap...\n")
        
        # Generate the roadmap
        roadmap_prompt = f"""Create a 4-PHASE career roadmap for {selected_field} in {country}.

User Info: {self.user_name}, Age: {self.user_age}, Education: {self.user_education}

Format EXACTLY like this (use bullet points • ):

PHASE 1 (0-2 years): Education & Entry Level
• [Specific action 1 for {selected_field} in {country}]
• [Specific action 2]
• [Specific action 3]

PHASE 2 (2-5 years): Building Experience
• [Specific action 1]
• [Specific action 2]
• [Specific action 3]

PHASE 3 (5-8 years): Growth & Specialization
• [Specific action 1]
• [Specific action 2]
• [Specific action 3]

PHASE 4 (8+ years): Leadership & Mastery
• [Specific action 1]
• [Specific action 2]
• [Specific action 3]

SALARY EXPECTATIONS in {country} local currency:
• Entry level (0-2 years):
• Mid level (2-5 years):
• Senior level (5-8 years):
• Expert level (8+ years):

Keep each bullet under 20 words. Be SPECIFIC to {country} market."""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-3.5-turbo", 
                    "messages": [
                        {"role": "system", "content": "You are a career roadmap expert. Give ONLY the 4-phase format requested. Use bullet points. Be practical and specific."}, 
                        {"role": "user", "content": roadmap_prompt}
                    ], 
                    "max_tokens": 1200
                },
                timeout=45
            )
            
            if response.status_code == 200:
                roadmap = response.json()["choices"][0]["message"]["content"]
                
                print("\n" + "="*60)
                print(f" YOUR {selected_field.upper()} ROADMAP FOR {country.upper()} ")
                print("="*60 + "\n")
                print(roadmap)
                print("\n" + "="*60)
                
                # Save to file
                filename = f"{self.user_name}_{selected_field.replace('/', '_')}_roadmap.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("="*60 + "\n")
                    f.write(f"CAREER ROADMAP for {self.user_name}\n")
                    f.write("="*60 + "\n\n")
                    f.write(f"Selected Field: {selected_field}\n")
                    f.write(f"Target Country: {country}\n")
                    f.write(f"Age: {self.user_age}\n")
                    f.write(f"Education: {self.user_education}\n\n")
                    f.write(roadmap)
                    f.write("\n\n" + "="*60 + "\n")
                    f.write("Generated by Career Navigator AI\n")
                
                print(f"\n Roadmap saved to: {filename}\n")
                print("Want another roadmap? Just choose a different field!\n")
                
            else:
                print(f" API Error: {response.status_code}")
                print("Please try again in a moment.\n")
                
        except Exception as e:
            print(f" Error: {str(e)}")
            print("Check your internet connection and API key.\n")
    
    def run(self):
        """Main app"""
        print("\n" + "="*60)
        print(" CAREER NAVIGATOR AI ")
        print("="*60)
        
        self.user_name = input("\n Your name: ").strip()
        self.user_age = input(" Your age: ").strip()
        self.user_education = input(" Your education level: ").strip()
        
        print(f"\n Welcome {self.user_name}! Let's find your career path. ✨\n")
        
        while True:
            print(" MAIN MENU")
            print("1.  Chat (ask career questions)")
            print("2.  Take Career Quiz (20 questions)")
            print("3.  Generate Roadmap (choose your field + country)")
            print("4. Exit")
            print("-"*40)
            
            choice = input("\nYour choice (1-4): ").strip()
            
            if choice == "1":
                print("\n CHAT MODE (short answers)")
                print("Type 'menu' to return\n")
                while True:
                    msg = input("You: ").strip()
                    if msg.lower() == 'menu':
                        break
                    if msg:
                        print("\n: ", end="")
                        response = self.chat(msg)
                        print(f"{response}\n")
            
            elif choice == "2":
                self.run_quiz()
            
            elif choice == "3":
                self.generate_roadmap()
            
            elif choice == "4":
                print("\n Good luck with your career journey! \n")
                break
            
            else:
                print("\n Choose 1-4\n")

# Run it
if __name__ == "__main__":
    if not API_KEY:
        print("\n ERROR: No API key found!")
    else:
        app = CareerNavigator()
        app.run()
