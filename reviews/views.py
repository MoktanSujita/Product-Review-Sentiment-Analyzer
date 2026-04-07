from django.shortcuts import render
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

from reviews.forms import ReviewForm
# Create your views here.
def analyze_review(request):
    result = {"sentiment" :sentiment,
              "polarity" : round(polarity, 2),
              "text" : review or text
            }

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.cleaned_data['review_text']
        else:
            url = None

        if not url:
            result = "Please enter a valid URL."
            sentiment = "N/A"
        else:

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
    
                soup = BeautifulSoup(response.text, 'html.parser')
            
                title_tag = soup.find("span", {"id": "productTitle"})
                if title_tag:
                    text_to_analyze = title_tag.get_text().strip()
                else:
                    text_to_analyze = "No title found"  
                    text_to_analyze += "" + url
    
                blob = TextBlob(text_to_analyze)
                polarity = blob.sentiment.polarity
                if polarity > 0:
                    sentiment = "Positive"
                elif polarity < 0:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"
        
                result = f"Polarity Score: {polarity}"
    
            except Exception as e:
                result = f"Error fetching or analyzing URL: {e}"

    return render(request, "reviews_list.html",{
            "result" : result,
            "sentiment" : sentiment 
        })