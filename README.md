# Product Review Sentiment Analyzer

## Overview
The **Product Review Sentiment Analyzer** is a Django-based web application that performs sentiment analysis on product reviews.

Users can:
- Enter a **manual review**, or
- Provide a **Daraz product URL** to analyze all available reviews

The system processes the input using NLP techniques and generates insights such as sentiment distribution, key terms, and overall product perception.

---

## Features

- Manual review sentiment analysis  
- Daraz product review scraping  
- Sentiment classification (Positive, Negative, Neutral)  
- Sentiment distribution with percentages  
- Top words extraction per sentiment  
- Sample review display  
- Data storage using Django models  
- Chart-ready output (Chart.js compatible)

---

## Tech Stack

**Backend**
- Django
- Python

**NLP**
- TextBlob
- NLTK

**Frontend**
- HTML, CSS
- Chart.js

**Other Tools**
- Requests

---

## Project Structure

```
product_analyzer/
│
├── reviews/
│   ├── views.py
│   ├── models.py
│   ├── services/
│   │   └── daraz_service.py
│
├── templates/
│   └── reviews_list.html
│
├── static/
│   └── css/
│
├── manage.py
├── requirements.txt
```

---

## Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd product_analyzer
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

Activate environment:
```bash
# Linux / Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download NLP Resources
```bash
python -m textblob.download_corpora
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Run Server
```bash
python manage.py runserver
```

---

## Usage

### Manual Review
- Enter text in the input field
- Submit to get:
  - Sentiment label
  - Polarity score

---

### URL-Based Analysis
Paste a Daraz product URL:
```
https://www.daraz.com.np/products/...
```

The system will:
- Extract product ID
- Fetch reviews
- Analyze sentiments

---

## How It Works

### 1. Input Detection
- Text → Direct analysis  
- URL → Scraping + batch processing  

### 2. Review Extraction
- Extracts `itemId` using regex  
- Calls Daraz API:
```
/pdp/review/getReviewList
```

### 3. Sentiment Analysis
```python
from textblob import TextBlob

polarity = TextBlob(text).sentiment.polarity
```

**Classification Rules:**
- > 0.2 → Positive  
- < -0.2 → Negative  
- Otherwise → Neutral  

---

## Example Output

```
Total Reviews: 120
Positive: 70 (58.3%)
Negative: 30 (25%)
Neutral: 20 (16.7%)

Overall Sentiment: Positive
```

---

## Limitations

- Depends on Daraz API availability  
- Basic NLP model (TextBlob)  
- Limited handling of sarcasm  
- English-focused analysis  

---

## Future Improvements

- Advanced NLP models (e.g., BERT)  
- Multi-language support  
- UI/UX improvements  
- User authentication  
- Multi-platform support  
