from django.shortcuts import render
from textblob import TextBlob
from bs4 import BeautifulSoup
import requests
# Create your views here.
def analyze_review(request):
    result = None
    sentiment = None

    if request.method == 'POST':
        review_text = request.POST.get("review_text")
        product_url = request.POST.get("product_url")

        if review_text:
           blob =TextBlob(review_text)
           polarity = blob.sentiment.polarity

           result ={
               "url": product_url,
               "content": review_text,
               "polarity":round(polarity, 2),
               "sentiment": get_sentiment_label(polarity)
           }

        elif product_url:
            try:
                headers ={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Accept-Language": "en-US,en;q=0.5"
                }
                response = requests.get(product_url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")

                reviews = []
                review_elements = soup.find_all("div", class_="content")
                for r in review_elements:
                    reviews.append(r.get_text(strip=True))

                positive, negative, neutral = 0, 0, 0
                for review in reviews:
                    polarity = TextBlob(review).sentiment.polarity
                    if polarity> 0:
                        positive +=1
                    elif polarity < 0:
                        negative +=1
                    else:
                        neutral +=1
                
                total = len(reviews)
                score = int((positive/total) * 100) if total > 0 else 0

                result ={
                        "type": "url",
                        "total": total,
                        "score": score,
                        "positive":positive,
                        "negative": negative,
                        "neutral": neutral
                    }

            except Exception as e:

                result ={"error": str(e)}
        else:
            result= {"error": "please enter text or url"}

    return render(request, "reviews_list.html", {"result": result})
    
def get_sentiment_label(polarity):
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    return "Neutral"

