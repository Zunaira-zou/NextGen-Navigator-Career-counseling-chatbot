"""
NextGen Career Navigator - Desktop App
Run: python app_desktop.py
"""

import os
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, ttk
from dotenv import load_dotenv
from collections import defaultdict
import threading

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

class CareerNavigatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NextGen Career Navigator")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f5f0e8")
        
        # User data
        self.user_name = ""
        self.user_age = ""
        self.user_education = ""
        self.quiz_results = {}
        self.conversation_history = []
        
        # Quiz data
        self.quiz_questions = self.get_quiz_questions()
        self.current_question = 0
        self.quiz_answers = {}
        
        # Setup UI
        self.setup_ui()
        
        # Get user info
        self.get_user_info()
        
        # Welcome message
        self.add_message("bot", "Hello! I'm NextGen Navigator, your AI career counselor. Ask me anything about careers, education paths, or job markets!")
    
    def get_quiz_questions(self):
        """Return quiz questions"""
        return [
            {"question": "How do you feel about solving complex technical problems?", 
            "options": ["Love it - I enjoy coding", "Sometimes - if interesting", "Not really - prefer people", "Hate it - gives me headache"]},
            {"question": "What's your ideal work environment?",
            "options": ["Office with a team", "Remote/WFH alone", "Hospital/Clinic with patients", "Outdoor/Field work"]},
            {"question": "How important is salary to you?",
            "options": ["Extremely - high income", "Important but not everything", "Average is fine", "Passion matters more"]},
            {"question": "Do you like working with numbers and data?",
            "options": ["Love it - Excel is my friend", "Okay with basic math", "Not really - prefer words", "Hate it completely"]},
            {"question": "How do you feel about public speaking?",
            "options": ["Love it - natural", "Can do it if needed", "Nervous but manageable", "Absolutely hate it"]},
            {"question": "What type of problems do you enjoy solving?",
            "options": ["Technical/mechanical", "Business/strategy", "People/relationship", "Creative/design"]},
            {"question": "Do you prefer structured or flexible work?",
            "options": ["Highly structured", "Some structure", "Flexible creative freedom", "Complete freedom"]},
            {"question": "How important is helping others?",
            "options": ["Very important", "Somewhat important", "Not a priority", "I prefer working alone"]},
            {"question": "Do you like traveling for work?",
            "options": ["Love it - adventure", "Occasional is fine", "Prefer staying local", "Hate traveling"]},
            {"question": "What's your creativity level?",
            "options": ["Very creative", "Somewhat creative", "Not very creative", "Analytical is my strength"]},
            {"question": "Do you like managing people?",
            "options": ["Love leading teams", "Can do if needed", "Prefer individual work", "Hate managing others"]},
            {"question": "How do you feel about continuous learning?",
            "options": ["Love it - always studying", "Okay with training", "Prefer learning on job", "Want fixed knowledge"]},
            {"question": "What's your attention to detail?",
            "options": ["Extremely detailed", "Good with details", "Big picture person", "Details bore me"]},
            {"question": "Do you like working with technology?",
            "options": ["Love it - tech enthusiast", "Comfortable with basic", "Prefer minimal tech", "Avoid technology"]},
            {"question": "How do you handle stress?",
            "options": ["Thrive under pressure", "Manage it well", "Prefer low-stress", "Avoid stress completely"]},
            {"question": "What's your preferred project type?",
            "options": ["Short-term fast results", "Long-term deep projects", "Mix of both", "Ongoing consistent work"]},
            {"question": "Do you like competition?",
            "options": ["Love competition", "Healthy competition", "Prefer collaboration", "Hate competition"]},
            {"question": "How important is job stability?",
            "options": ["Extremely important", "Important but open", "Not major concern", "Prefer high-risk high-reward"]},
            {"question": "Do you like writing?",
            "options": ["Love writing", "Okay with basic", "Prefer minimal", "Hate writing"]},
            {"question": "What's your ideal career growth?",
            "options": ["Climb corporate ladder", "Become expert/specialist", "Start own business", "Steady growth is fine"]}
        ]
    
    def setup_ui(self):
        """Setup the main UI"""
        # Left Sidebar
        sidebar = tk.Frame(self.root, bg="#2c2418", width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(sidebar, bg="#2c2418")
        logo_frame.pack(fill=tk.X, padx=20, pady=30)
        
        logo_label = tk.Label(logo_frame, text="NextGen Career\nNavigator", 
                            font=("Arial", 18, "bold"), 
                            fg="#e8dcc8", bg="#2c2418")
        logo_label.pack()
        
        subtitle = tk.Label(logo_frame, text="AI Career Counselor", 
                        font=("Arial", 10), 
                        fg="#8a7a64", bg="#2c2418")
        subtitle.pack()
        
        # Menu buttons
        menu_frame = tk.Frame(sidebar, bg="#2c2418")
        menu_frame.pack(fill=tk.X, padx=15, pady=20)
        
        buttons = [
            ("💬 Chat", self.show_chat),
            ("🧠 Take Quiz", self.start_quiz),
            ("🗺️ Generate Roadmap", self.open_roadmap_dialog)
        ]
        
        for text, command in buttons:
            btn = tk.Button(menu_frame, text=text, command=command,
                        font=("Arial", 11), bg="#3d3324", fg="#e8dcc8",
                        relief=tk.FLAT, anchor="w", padx=15, pady=10)
            btn.pack(fill=tk.X, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#5c4b32"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#3d3324"))
        
        # User info
        self.user_frame = tk.Frame(sidebar, bg="#2c2418")
        self.user_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
        
        self.user_name_label = tk.Label(self.user_frame, text="Not set", 
                                        font=("Arial", 11, "bold"),
                                        fg="#e8dcc8", bg="#2c2418")
        self.user_name_label.pack()
        
        self.user_detail_label = tk.Label(self.user_frame, text="Click to setup",
                                        font=("Arial", 9),
                                        fg="#8a7a64", bg="#2c2418")
        self.user_detail_label.pack()
        
        # Right Chat Area
        chat_area = tk.Frame(self.root, bg="#faf7f2")
        chat_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat header
        header = tk.Frame(chat_area, bg="#faf7f2", height=70)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(header, text="Career Chat", 
                font=("Arial", 16, "bold"),
                fg="#2c2418", bg="#faf7f2").pack(side=tk.LEFT)
        
        tk.Label(header, text="Ask me anything about careers!",
                font=("Arial", 10),
                fg="#8a7a64", bg="#faf7f2").pack(side=tk.LEFT, padx=15)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(chat_area, 
                                                        wrap=tk.WORD,
                                                        font=("Arial", 11),
                                                        bg="#faf7f2",
                                                        fg="#2c2418",
                                                        relief=tk.FLAT,
                                                        padx=15,
                                                        pady=15)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure text tags for different message types
        self.chat_display.tag_config("bot", foreground="#2c2418", font=("Arial", 11))
        self.chat_display.tag_config("user", foreground="#5c4b32", font=("Arial", 11, "bold"))
        self.chat_display.tag_config("time", foreground="#b0a088", font=("Arial", 8))
        
        # Input area
        input_frame = tk.Frame(chat_area, bg="#faf7f2", height=80)
        input_frame.pack(fill=tk.X, padx=20, pady=15)
        
        self.message_entry = tk.Entry(input_frame, font=("Arial", 11),
                                    bg="white", fg="#2c2418",
                                    relief=tk.SOLID, bd=1)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        send_btn = tk.Button(input_frame, text="Send", command=self.send_message,
                            font=("Arial", 11, "bold"),
                            bg="#5c4b32", fg="white",
                            relief=tk.FLAT, padx=20, pady=8)
        send_btn.pack(side=tk.RIGHT)
    
    def get_user_info(self):
        """Get user info via dialog"""
        self.user_name = simpledialog.askstring("Welcome!", "What's your name?", parent=self.root)
        if not self.user_name:
            self.user_name = "User"
        
        self.user_age = simpledialog.askstring("Welcome!", "Your age:", parent=self.root)
        if not self.user_age:
            self.user_age = "Not specified"
        
        self.user_education = simpledialog.askstring("Welcome!", "Your education level:", parent=self.root)
        if not self.user_education:
            self.user_education = "Not specified"
        
        self.user_name_label.config(text=self.user_name)
        self.user_detail_label.config(text=f"{self.user_age} yrs • {self.user_education}")
    
    def add_message(self, sender, message):
        """Add a message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        from datetime import datetime
        time_str = datetime.now().strftime("%I:%M %p")
        
        if sender == "bot":
            self.chat_display.insert(tk.END, f"🤖 ", "bot")
        else:
            self.chat_display.insert(tk.END, f"👤 ", "user")
        
        self.chat_display.insert(tk.END, f"{message}\n", sender)
        self.chat_display.insert(tk.END, f"   {time_str}\n\n", "time")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        """Send user message and get AI response"""
        message = self.message_entry.get().strip()
        if not message:
            return
        
        self.message_entry.delete(0, tk.END)
        self.add_message("user", message)
        
        # Show typing indicator
        self.add_message("bot", "Typing...")
        
        # Get response in thread
        thread = threading.Thread(target=self.get_ai_response, args=(message,))
        thread.daemon = True
        thread.start()
    
    def get_ai_response(self, message):
        """Get AI response from API"""
        # Remove the typing indicator
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("end-2l", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Store conversation
        self.conversation_history.append({"role": "user", "content": message})
        
        system_prompt = f"""You are NextGen Career Navigator AI. 
        User: {self.user_name}, Age: {self.user_age}, Education: {self.user_education}
        
        RULES:
        - Keep responses UNDER 50 WORDS
        - Use bullet points (•)
        - Be direct and helpful
        - No long paragraphs"""
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 300
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                ai_response = response.json()["choices"][0]["message"]["content"]
                self.conversation_history.append({"role": "assistant", "content": ai_response})
                self.root.after(0, lambda: self.add_message("bot", ai_response))
            else:
                self.root.after(0, lambda: self.add_message("bot", f"Error: {response.status_code}"))
        except Exception as e:
            self.root.after(0, lambda: self.add_message("bot", f"Connection error: {str(e)}"))
    
    def show_chat(self):
        """Just scroll chat to bottom"""
        self.chat_display.see(tk.END)
    
    def start_quiz(self):
        """Start the career quiz"""
        self.current_question = 0
        self.quiz_answers = {}
        self.show_quiz_question()
    
    def show_quiz_question(self):
        """Show current quiz question"""
        if self.current_question >= len(self.quiz_questions):
            self.calculate_quiz_results()
            return
        
        q = self.quiz_questions[self.current_question]
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Quiz Question {self.current_question + 1}/20")
        dialog.geometry("500x400")
        dialog.configure(bg="#faf7f2")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Question
        tk.Label(dialog, text=f"Question {self.current_question + 1}/20",
                font=("Arial", 12, "bold"),
                bg="#faf7f2", fg="#2c2418").pack(pady=10)
        
        tk.Label(dialog, text=q["question"],
                font=("Arial", 11),
                bg="#faf7f2", fg="#2c2418", wraplength=450).pack(pady=10)
        
        # Options
        var = tk.StringVar()
        for i, opt in enumerate(q["options"]):
            rb = tk.Radiobutton(dialog, text=opt, variable=var, value=str(i),
                            bg="#faf7f2", fg="#2c2418", font=("Arial", 10),
                            anchor="w", padx=20)
            rb.pack(fill=tk.X, padx=20, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg="#faf7f2")
        btn_frame.pack(pady=20)
        
        def next_question():
            if var.get() == "":
                messagebox.showwarning("No selection", "Please select an answer!")
                return
            self.quiz_answers[self.current_question] = int(var.get())
            self.current_question += 1
            dialog.destroy()
            self.show_quiz_question()
        
        tk.Button(btn_frame, text="Next", command=next_question,
                bg="#5c4b32", fg="white", padx=20, pady=5).pack()
    
    def calculate_quiz_results(self):
        """Calculate and show quiz results"""
        # Simple scoring based on answers
        career_scores = {
            "Technology/IT": 0,
            "Business/Finance": 0,
            "Healthcare/Medicine": 0,
            "Engineering": 0,
            "Creative/Design": 0,
            "Marketing/Sales": 0
        }
        
        # Map answers to careers (simplified)
        for q_num, answer in self.quiz_answers.items():
            if answer == 0:  # First option usually tech/business
                career_scores["Technology/IT"] += 2
                career_scores["Engineering"] += 1
            elif answer == 1:  # Second option
                career_scores["Business/Finance"] += 2
                career_scores["Marketing/Sales"] += 1
            elif answer == 2:  # Third option
                career_scores["Healthcare/Medicine"] += 2
                career_scores["Creative/Design"] += 1
            else:  # Fourth option
                career_scores["Marketing/Sales"] += 1
                career_scores["Creative/Design"] += 1
        
        # Calculate percentages
        total = sum(career_scores.values())
        if total > 0:
            results = {k: round((v/total)*100, 1) for k, v in career_scores.items()}
        else:
            results = career_scores
        
        # Sort results
        sorted_results = sorted(results.items(), key=lambda x: -x[1])
        
        # Display results
        result_text = "📊 YOUR CAREER MATCHES:\n\n"
        for career, score in sorted_results[:5]:
            bar = "█" * int(score/2) + "░" * (50 - int(score/2))
            result_text += f"{career:<20} {score:>5}%  {bar}\n"
        
        result_text += "\n💡 These are suggestions! You can choose ANY field for your roadmap."
        
        self.add_message("bot", result_text)
        self.quiz_results = dict(sorted_results)
    
    def open_roadmap_dialog(self):
        """Open dialog for roadmap generation"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Generate Career Roadmap")
        dialog.geometry("500x400")
        dialog.configure(bg="#faf7f2")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Field selection
        tk.Label(dialog, text="Select Career Field:",
                font=("Arial", 11, "bold"),
                bg="#faf7f2", fg="#2c2418").pack(pady=(20,5))
        
        fields = ["Technology/IT", "Business/Finance", "Healthcare/Medicine", 
                "Engineering", "Creative/Design", "Education/Teaching",
                "Law/Legal", "Marketing/Sales", "Science/Research", "Hospitality/Travel"]
        
        field_var = tk.StringVar(value="Technology/IT")
        field_menu = ttk.Combobox(dialog, textvariable=field_var, values=fields, state="readonly")
        field_menu.pack(pady=5, padx=20, fill=tk.X)
        
        # Country input
        tk.Label(dialog, text="Target Country:",
                font=("Arial", 11, "bold"),
                bg="#faf7f2", fg="#2c2418").pack(pady=(15,5))
        
        country_entry = tk.Entry(dialog, font=("Arial", 10))
        country_entry.pack(pady=5, padx=20, fill=tk.X)
        country_entry.insert(0, "Pakistan")
        
        # Generate button
        def generate():
            field = field_var.get()
            country = country_entry.get().strip()
            
            if not country:
                messagebox.showwarning("Missing Info", "Please enter a country!")
                return
            
            dialog.destroy()
            self.generate_roadmap(field, country)
        
        tk.Button(dialog, text="Generate Roadmap", command=generate,
                bg="#5c4b32", fg="white", font=("Arial", 11, "bold"),
                padx=20, pady=10).pack(pady=20)
    
    def generate_roadmap(self, field, country):
        """Generate and display roadmap"""
        self.add_message("bot", f"🔄 Generating your {field} roadmap for {country}...")
        
        roadmap_prompt = f"""Create a 4-PHASE career roadmap for {field} in {country}:

PHASE 1 (0-2 years): Education & Entry Level
• [Specific action 1 for {field} in {country}]
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

SALARY EXPECTATIONS in {country}:
• Entry level:
• Mid level:
• Senior level:

Keep each bullet under 20 words. Be SPECIFIC to {country} market."""
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a career roadmap expert. Give practical advice specific to the country."},
                {"role": "user", "content": roadmap_prompt}
            ],
            "max_tokens": 1200
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=45
            )
            
            if response.status_code == 200:
                roadmap = response.json()["choices"][0]["message"]["content"]
                
                # Display roadmap
                self.add_message("bot", f"🗺️ YOUR {field.upper()} ROADMAP FOR {country.upper()}\n\n{roadmap}")
                
                # Save to file
                filename = f"{self.user_name}_{field.replace('/', '_')}_roadmap.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("="*60 + "\n")
                    f.write(f"CAREER ROADMAP for {self.user_name}\n")
                    f.write("="*60 + "\n\n")
                    f.write(f"Field: {field}\n")
                    f.write(f"Country: {country}\n\n")
                    f.write(roadmap)
                
                messagebox.showinfo("Success", f"Roadmap saved to:\n{filename}")
            else:
                self.add_message("bot", f"Error: {response.status_code}")
        except Exception as e:
            self.add_message("bot", f"Error: {str(e)}")

# Run the app
if __name__ == "__main__":
    if not API_KEY:
        print("\n❌ ERROR: No API key found!")
        print("Create .env file with: OPENROUTER_API_KEY=your_key_here\n")
        input("Press Enter to exit...")
    else:
        root = tk.Tk()
        app = CareerNavigatorApp(root)
        root.mainloop()