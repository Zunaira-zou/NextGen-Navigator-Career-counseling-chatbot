# NextGen Navigator — Career Counseling Chatbot

NextGen Navigator is an interactive, desktop + CLI career counseling assistant that guides students through a 20-question career quiz, an AI-powered multi-turn counseling chat, and generates a country-specific 4-phase career roadmap that can be saved as a text file. It's designed for educators, career counselors, and students who want a practical, repeatable way to explore career options and actionable next steps.

Badges:  
- License: Apache License Version 2.0

## Key features
- Career Quiz — 20 targeted questions that score preferences across multiple career fields.
- AI Counseling — short, multi-turn responses from an LLM (via OpenRouter) tailored to the user.
- Country Guidance — market-specific roadmap and salary expectations for target countries.
- 4-Phase Roadmap — concrete, time-phased actions (0–2, 2–5, 5–8, 8+ years).
- Saved Output — generated roadmaps are saved as a .txt file for students.
- Two interfaces:
  - CLI app (app.py) — lightweight terminal flow.
  - Desktop GUI (frontend.py) — Tkinter-based polished interface.

## Stack
- Language(s): Python 3.8+
- Runtime / UI: Standard Python, Tkinter for the GUI
- Notable libraries:
  - requests — HTTP API calls to OpenRouter
  - python-dotenv — load API key from .env
  - tkinter — desktop UI (standard lib)
  - threading, collections — UI and state management


How it fits together
- app.py provides the command-line user flow: gather user info, run the 20-question quiz, call the OpenRouter API for short chat answers and to generate a 4-phase roadmap, then save the roadmap to a text file.
- frontend.py provides a Tkinter desktop application with the same capabilities (chat, interactive quiz, roadmap generation), keeping conversation history and saving the generated roadmap to disk.
- Both interfaces rely on an environment variable OPENROUTER_API_KEY and call OpenRouter's chat completions endpoint (configured to use the "openai/gpt-3.5-turbo" model in this project).

## Requirements
- Python 3.8 or newer
- Internet connection
- OpenRouter API key (stored as environment variable OPENROUTER_API_KEY)

## Quick start — local (CLI)
1. Clone:
   git clone https://github.com/Zunaira-zou/NextGen-Navigator-Career-counseling-chatbot.git
2. Create & activate a virtual environment:
   - macOS / Linux:
     python3 -m venv venv
     source venv/bin/activate
   - Windows (PowerShell):
     python -m venv venv
     .\venv\Scripts\Activate.ps1
3. Install dependencies:
   pip install requests python-dotenv
   (tkinter is part of the standard library on most distributions; on some Linux distros you may need to install it separately, e.g. `sudo apt install python3-tk`.)
4. Create a `.env` in the project root with your API key:
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   (Do not commit `.env` to version control.)
5. Run the CLI app:
   python app.py

## Quick start — desktop GUI
1. Follow steps 1–4 above to clone, create env, install deps, and set OPENROUTER_API_KEY.
2. Run:
   python frontend.py
3. The GUI will ask for name, age, and education, then you can chat, take the quiz, or generate a roadmap.

## Typical usage notes
- Chat: designed to return concise (≤ 50 words) bullet-point answers.
- Quiz: 20 questions; results are displayed in a percentage-style ranking of career fields.
- Roadmap generation: choose a field and target country; the app sends a prompt to the LLM and displays/saves a 4-phase roadmap. Roadmaps are saved as files named like <UserName>_<Field>_roadmap.txt.

## Files of interest
- app.py — CLI main loop, quiz definition, scoring logic, chat and roadmap API calls, file saving.
- frontend.py — Tkinter-based UX, quiz dialogs, chat UI, and roadmap generator.
- sampleoutput.txt — example of generated roadmap / sample output to see expected format.
- Screenshot 2026-04-23 072336.png — UI preview.

## Security & privacy
- API keys must be stored in environment variables (.env) and must not be committed to the repository.
- The app sends user prompts and context to the OpenRouter service — do not include personally identifying or sensitive data in the prompts if you want to preserve privacy.

## Troubleshooting
- "ERROR: No API key found!" — ensure you created a .env file or exported OPENROUTER_API_KEY to your environment.
- Tkinter missing on Linux — install system package `python3-tk` (or equivalent for your distro).
- Network/API errors — check your internet connection and whether the API key is valid/active.

## Extending the project
- Add a requirements.txt or pyproject.toml for dependency pinning.
- Improve scoring model and expand career mappings in quiz data.
- Add tests for quiz scoring and prompt generation.
- Provide an offline fallback or rate-limited queuing for API calls.
- Add internationalization and richer salary data sources for country-specific salary estimates.

## Contributing
Contributions are welcome. Suggested workflow:
1. Fork the repo
2. Create a feature branch
3. Open a PR with a clear description and example usage
Please do not include API keys or other secrets in PRs.

## License
This project is licensed under the Apache License Version 2.0 — see the LICENSE file for details.

## Author / Contact
Zunaira — thank you for checking out the project! For questions or collaboration ideas, open an issue or PR in this repository.
