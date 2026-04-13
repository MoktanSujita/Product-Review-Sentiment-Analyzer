from django.shortcuts import render
from textblob import TextBlob
from bs4 import BeautifulSoup
import requests
import re
# Create your views here.
def analyze_review(request):
    result = None

    if request.method == 'POST':
        review_text = request.POST.get("review_text")
        product_url = request.POST.get("product_url")

        if review_text:
           blob =TextBlob(review_text)
           polarity = blob.sentiment.polarity

           result ={
                "type": "text",
               "content": review_text,
               "polarity":round(polarity, 2),
               "sentiment": get_sentiment_label(polarity)
           }

        elif product_url:
            try:
        
                # Extract item_id from Daraz URL
                match = re.search(r'i(\d+)', product_url)
        
                if not match:
                    return render(request, "reviews_list.html", {
                        "result": {"error": "Invalid Daraz URL"}
                    })
        
                item_id = match.group(1)
        
                # Daraz API URL
                api_url = "https://my.daraz.com.np/pdp/review/getReviewList"
        
                response = requests.get(
                        api_url,
                        params = {
                        "itemId": item_id,
                        "pageSize": 10,
                        "pageNo": 1
                        },
                        headers = {
                        "User-Agent": "Mozilla/5.0",
                        "Accept": "application/json"
                        },
                        timeout=10,
                    )        
        
                data = response.json()
        
                # Correct JSON parsing
                items = data.get("model", {}).get("items", [])
                reviews = [r.get("reviewContent", "").strip()
                            for r in items
                            if r.get("reviewContent")
                           ]
        
                if not reviews:
                    return render(request, "reviews_list.html", {
                        "result": {"error": "No reviews found for this product"}
                    })
                    
        
                #  Initialize counters
                positive = negative = neutral = 0
                valid_reviews = 0
        
                for review in reviews:
                    if not review:
                        continue

                    valid_reviews += 1
                    polarity = TextBlob(review).sentiment.polarity
        
                    if polarity > 0.2:
                        positive += 1
                    elif polarity < -0.2:
                        negative += 1
                    else:
                        neutral += 1
        
                total = valid_reviews

                result = {
                    "type": "url",
                    "total_reviews": total,
                    "positive": positive,
                    "negative": negative,
                    "neutral": neutral,
                    "positive_percentage": round((positive / total) * 100, 2) if total else 0,
                    "negative_percentage": round((negative / total) * 100, 2) if total else 0,
                    "overall":get_overall_sentiment(positive, negative, neutral)
                }

            except Exception as e:
                result = {"error": str(e)}
    else:
        result= {"error": "please enter text or url"}
    return render(request, "reviews_list.html", {"result": result})
    
def get_sentiment_label(polarity):
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    return "Neutral"

def get_overall_sentiment(positive, negative, neutral):
    if positive > negative and positive > neutral:
        return "Overall Positive"
    elif negative > positive and negative > neutral:
        return "Overall Negative"
    else:
        return "Overall Neutral"

