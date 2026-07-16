### NewsLens: Intelligent News Summarization and Sentiment Analysis

NewsLens is an interactive web application that helps users quickly understand long news articles. It uses Natural Language Processing (NLP) to summarize articles, detect sentiment, extract keywords and entities, and answer questions based on the supplied article.

## Live Demo

Use the deployed application here: **[Open NewsLens](https://newslens-8859.onrender.com)**

## Project Objectives

- Perform NLP preprocessing on news text.
- Generate concise article summaries.
- Detect positive, negative, or neutral sentiment.
- Extract important keywords and named entities.
- Answer user questions using article context.
- Provide an easy-to-use web interface.

## Features

- **News summarization:** Produces a concise summary of a long article.
- **Sentiment analysis:** Identifies the overall emotional tone of the article.
- **Keyword extraction:** Displays the most important topics in the article.
- **Entity extraction:** Identifies people, organizations, and locations.
- **Question answering:** Lets users ask questions about the pasted article.
- **Local processing:** Core analysis works directly from the pasted article.

## Technology Stack

| Area | Technology |
| --- | --- |
| Backend | Python, Flask |
| NLP | Regex-based preprocessing, extractive summarization, rule-based sentiment analysis |
| Frontend | HTML, CSS, JavaScript |

## Project Structure

```text
News summarizer/
├── app.py                 # Flask application and NLP logic
├── requirements.txt       # Python dependencies
├── run_newslens.bat       # One-click Windows launcher
├── templates/
│   └── index.html          # User interface layout
└── static/
    ├── style.css           # Interface styling
    └── app.js              # Client-side interaction logic
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later

### Option 1: One-click launch on Windows

Double-click `run_newslens.bat`. On the first run, it creates a virtual environment, installs dependencies, and opens the app in your default browser.

### Option 2: Run from the terminal

1. Open PowerShell or the VS Code terminal in the project folder.
2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks scripts, use Command Prompt and run:

   ```cmd
   .venv\Scripts\activate.bat
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Start the application:

   ```powershell
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in a browser.

## How to Use

1. Paste a news article into the input area, or select **Load sample**.
2. Click **Analyze article**.
3. Review the generated summary, sentiment, reading time, key topics, and entities.
4. Type a question in the **Ask the article** area and click **Ask**.

## Future Enhancements

- Support news article URLs and automatic article extraction.
- Add multilingual analysis.
- Use a trained sentiment classification model.
- Store previous analyses and user history.
- Add charts for sentiment and topic trends.

## License

This project is created for academic and educational purposes.
