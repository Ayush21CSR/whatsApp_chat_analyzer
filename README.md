# WhatsApp Chat Analyzer

Analyze WhatsApp chat exports with interactive dashboards: basic stats, sentiment, timelines, busiest users, word clouds, emoji usage, and heatmaps — all in Streamlit.

![App Screenshot](docs/screenshot.png)

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

## 🧭 Pipeline (High Level)

```text
Upload .txt → Preprocess to DataFrame → Choose User → Pick Analysis →
Compute Metrics (helper.py) → Visualize (matplotlib/seaborn) → Streamlit UI
```

You can include this diagram in `docs/`:

![Pipeline](docs/pipeline.png)

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

## 🛠️ Metrics & NLP (`helper.py`)

Expected functions used by `app.py` (adapt to your implementation):

* `fetch_stats(selected_user, df)` → `(num_messages, num_words, num_media, num_links)`
* `sentiment_analysis(selected_user, df)` → dict with percentages & average VADER scores
* `sentiment_timeline(selected_user, df)` → DataFrame(date, sentiment\_score)
* `monthly_timeline(selected_user, df)` → counts per month
* `daily_timeline(selected_user, df)` → counts per day
* `week_activity_map(selected_user, df)` → counts per weekday
* `month_activity_map(selected_user, df)` → counts per month
* `most_busy_users(df)` → (Series for chart, DataFrame table)
* `create_wordcloud(selected_user, df)` → `WordCloud` image
* `most_common_words(selected_user, df)` → DataFrame(word, count)
* `emoji_helper(selected_user, df)` → DataFrame(emoji, count)
* `get_extreme_sentiment_messages(selected_user, df, sentiment_type, top_n)` → list\[(msg, score)]

> Add/rename as per your code; update `app.py` accordingly.

---

## 🧪 Usage Walkthrough

1. Launch the app and **upload** the exported `.txt`
2. Pick **Overall** or a **specific user** from the dropdown
3. Choose an **analysis type** (or **Complete Analysis**)
4. Explore interactive plots and tables; expanders show top ± messages
5. Use **Download** buttons (if you add them) for exporting results

---

## 🧯 Troubleshooting

* **Encoding issues** (weird characters like `Ã©`): ensure you decode as **UTF‑8** in `preprocessor`.
* **Datetime parse errors**: WhatsApp exports vary by locale; add multiple `pd.to_datetime` formats (12/24h, comma vs hyphen) and fallback parsing.
* **Large chats feel slow**: precompute features, cache with `@st.cache_data`, or sample for heavy plots (wordcloud).
* **Missing users**: some messages are system notifications → filtered as `group_notification`.
* **No emojis detected**: ensure you’re not stripping non-ASCII; use `emoji` lib and count by codepoint.

---

## 🔒 Privacy

All analysis happens locally in your browser session unless you add cloud storage. Do **not** upload sensitive chats to third‑party servers.

---

## 🗺️ Roadmap (Ideas)

* Export **PDF/CSV** reports from the dashboard
* Per-user **conversation networks** (mentions/replies)
* **Topic modeling** / keyword trends over time
* Multi-chat aggregation & comparisons
* Advanced **toxicity** / moderation scoring

---

## 📜 License

MIT (or your preferred license). Add a `LICENSE` file.

---

## 🙏 Acknowledgments

* VADER Sentiment (Hutto & Gilbert)
* Streamlit community
* Matplotlib / Seaborn / WordCloud

---

## 🤝 Contributing

PRs welcome! Please open an issue with a minimal reproducible example.
