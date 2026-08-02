# 🚀 The Lead Qualifier

An AI agent that reads a CSV list of leads, researches each company on the web, and automatically qualifies them against your ICP (Ideal Customer Profile) — right inside a simple Streamlit UI.

Upload a CSV with an `email` column → the agent extracts the company from each domain → searches the web to find out what the company does → decides **YES** or **NO** based on your qualification criteria → lets you download only the qualified leads as a clean CSV.

---

## ✨ Features

- **Zero-setup UI** — drag-and-drop a CSV, click one button, watch results stream in live.
- **Web-grounded decisions** — uses [Tavily Search](https://tavily.com/) so the AI isn't just guessing from a company name; it actually looks the company up.
- **Live, color-coded feedback** — qualified leads appear in green, disqualified ones in yellow, as the agent works through the list.
- **One-click export** — download a CSV containing only the qualified leads, ready to import into your CRM.
- **Configurable criteria** — the qualification rule (currently "Software or Technology companies only") lives in a single system prompt you can edit in one place.

---

## 🧠 How It Works

```
CSV upload
   │
   ▼
Extract company name from each email domain (e.g. sales@stripe.com → "stripe")
   │
   ▼
LangChain agent (Gemini 2.5 Flash + Tavily Search tool)
   │  "Search for {company} and qualify them"
   ▼
Agent researches the company, responds YES/NO + one-line reason
   │
   ▼
Result shown live in the UI (✅ success / ❌ warning)
   │
   ▼
YES leads collected → downloadable qualified_leads.csv
```

The agent is built with LangChain's `create_agent`, using:
- **Model:** Google Gemini 2.5 Flash (`temperature=0.0` for consistent, deterministic qualification)
- **Tool:** Tavily web search (`max_results=1`) so the agent grounds its answer in a real search result rather than relying purely on the model's own knowledge

---

## 📁 Project Structure

```
lead-qualifier/
├── app.py               # Main Streamlit application
├── requirements.txt      # Python dependencies
├── .env.example          # Template for required API keys
├── .gitignore
├── sample_leads.csv      # Example input file to test the app
└── README.md
```

---

## ✅ Prerequisites

- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com/app/apikey) API key (for Gemini)
- A [Tavily](https://app.tavily.com/) API key (for web search)

---

## ⚙️ Installation

1. **Clone or download this project**, then move into the folder:
   ```bash
   cd lead-qualifier
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API keys:**
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and paste in your real keys:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

---

## ▶️ Usage

1. Run the app:
   ```bash
   streamlit run app.py
   ```

2. Your browser will open automatically at `http://localhost:8501`.

3. Upload a CSV file with an **`email`** column (see `sample_leads.csv` for the expected format).

4. Click **"Qualify Leads"** and watch the agent research each company live.

5. Once finished, click **"⬇️ Download Qualified Leads (CSV)"** to export only the companies that passed qualification.

### Expected CSV format

```csv
email
sales@stripe.com
info@somecompany.com
contact@shopify.com
```

Only the first column is used — the company name is derived automatically from the domain (`stripe.com` → `stripe`).

---

## 🛠️ Customizing the Qualification Criteria

The qualification logic lives entirely in the agent's `system_prompt` inside `app.py`:

```python
system_prompt=(
    "You are a strict lead qualifier. Use the search tool to find out what the company does. "
    "We ONLY want to sell to Software or Technology companies. "
    "Respond strictly with 'YES' or 'NO', followed by a one-sentence reason."
)
```

Edit this string to match your own ICP — for example, target company size, industry, geography, or any other criteria you want the agent to check for.

---

## ⚠️ Limitations

- **Rate limits:** processing large CSVs makes one search + one LLM call per lead, which can be slow and may hit API rate limits on large batches.
- **Search accuracy:** qualification is only as good as the top search result Tavily returns for the company name — ambiguous or very new company names may return irrelevant results.
- **No retry/error handling yet:** a failed API call on one row will currently stop the whole batch (see Roadmap below).
- **Sequential processing:** leads are processed one at a time, not in parallel.


## 🧰 Tech Stack

| Layer            | Tool                              |
|-------------------|------------------------------------|
| UI                | [Streamlit](https://streamlit.io/) |
| Agent framework   | [LangChain](https://python.langchain.com/) |
| LLM               | Google Gemini 2.5 Flash            |
| Web search        | [Tavily](https://tavily.com/)      |
| Config            | python-dotenv                      |

---

## 📄 License

MIT
---

## 🙋 Author

Built by Sohail Ahmad
