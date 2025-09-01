# WhatsApp Chat Analyzer

Analyze WhatsApp chat exports with interactive dashboards: basic stats, sentiment, timelines, busiest users, word clouds, emoji usage, and heatmaps — all in Streamlit.


---
 
## ✨ Features

* **Upload** WhatsApp `.txt` export (Android/iOS supported)
* **Basic stats:** total messages, words, media, links
* **Sentiment analysis:** VADER-based distribution + timeline + top ± messages
* **Activity timelines:** monthly & daily trends
* **User insights:** busiest users leaderboard (for group chats)
* **Word analytics:** word cloud & most common words
* **Emoji analytics:** top emojis + usage table
* **Heatmap:** weekday × hour message density
* **Per-user or overall** analysis via sidebar controls

---


## 🗂️ Project Structure

```text
whatsapp-chat-analyzer/
├─ app.py                  # Streamlit app (UI & routing)
├─ preprocessor.py         # .txt → pandas.DataFrame
├─ helper.py               # metrics, NLP utilities, plots data
├─ requirements.txt        # Python dependencies
├─ docs/
│  ├─ screenshot.png
│  └─ pipeline.png
└─ README.md
```

---

## ⚙️ Installation

### 1) Create & activate a virtual environment

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` (example):**

```txt
streamlit
pandas
numpy
matplotlib
seaborn
wordcloud
emoji
urlextract
nltk
vaderSentiment
regex
```

> If you use any extra libs in `helper.py`/`preprocessor.py`, add them here.

### 3) One-time NLTK data (for VADER)

```python
import nltk
nltk.download('vader_lexicon')
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually [http://localhost:8501](http://localhost:8501)).

---

## 📤 Exporting WhatsApp Chats

1. **Open chat** (individual or group)
2. **More / Export chat**
3. Choose **Without media** (recommended)
4. Save the **`.txt`** file and upload it in the app sidebar

> Both **Android** and **iOS** exports are supported. The preprocessor handles common date/time formats.

---

## 🧹 Preprocessing Expectations (`preprocessor.py`)

Your `preprocessor.preprocess(text: str) -> pandas.DataFrame` should return a DataFrame with at least:

| column                      | dtype            | notes                               |
| --------------------------- | ---------------- | ----------------------------------- |
| `date`                      | `datetime64[ns]` | combined date & time (parsed)       |
| `user`                      | `string`         | sender name or `group_notification` |
| `message`                   | `string`         | raw message text                    |
| `only_date`                 | `date`           | (optional) calendar date only       |
| `year` `month` `day` `hour` | ints             | (optional) derived features         |

Typical parsing steps:

* Regex split of lines into **date, time, user, message**
* Convert to `datetime` with `pd.to_datetime(...)`
* Mark system messages as `group_notification`

---


## 🧪 Usage Walkthrough

1. Launch the app and **upload** the exported `.txt`
2. Pick **Overall** or a **specific user** from the dropdown
3. Choose an **analysis type** (or **Complete Analysis**)
4. Explore interactive plots and tables; expanders show top ± messages
5. Use **Download** buttons (if you add them) for exporting results

---

