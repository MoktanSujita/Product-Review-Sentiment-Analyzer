from django.shortcuts import render
from textblob import TextBlob
from bs4 import BeautifulSoup
import requests
import re
from collections import Counter
from .models import Review
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
           Review.objects.create(
                product_name = review_text[:50],
                product_url = "",
                sentiment = result["sentiment"]
            )

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
                positive_reviews = []
                negative_reviews = []
                neutral_reviews = []

                valid_reviews = 0
        
                for review in reviews:
                    if not review:
                        continue

                    valid_reviews += 1
                    polarity = TextBlob(review).sentiment.polarity
        
                    if polarity > 0.2:
                        positive += 1
                        positive_reviews.append(review)

                    elif polarity < -0.2:
                        negative += 1
                        negative_reviews.append(review)
                    else:
                        neutral += 1
                        neutral_reviews.append(review)
        
                total = valid_reviews

                sample_positive = positive_reviews[:3]
                sample_negative = negative_reviews[:3]
                sample_neutral = neutral_reviews[:3]                
                top_neutral_words = get_top_words(neutral_reviews)
                top_positive_words = get_top_words(positive_reviews)
                top_negative_words = get_top_words(negative_reviews)
                    

                result = {
                    "type": "url",
                    "total_reviews": total,
                    "positive": positive,
                    "negative": negative,
                    "neutral": neutral,
                    "positive_percentage": round((positive / total) * 100, 2) if total else 0,
                    "negative_percentage": round((negative / total) * 100, 2) if total else 0,
                    "overall":get_overall_sentiment(positive, negative, neutral),
                    "top_positive_words": top_positive_words,
                    "top_negative_words": top_negative_words,
                    "top_neutral_words": top_neutral_words,
                    "sample_positive": sample_positive,
                    "sample_negative": sample_negative,
                    "sample_neutral": sample_neutral,
                }
                Review.objects.create(
                  product_name = product_url,
                  product_url = product_url,
                  sentiment = result["overall"]
               )

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


stop_words = {"the", "is", "in", "and", "to", "a", "of", "it", "for", "on", "with", "was", "as", "but", "are", "this", "that" , "xa" , "k"}

def get_top_words(review_list):
    words = []
    for review in review_list:
        cleaned = re.sub(r'[^\w\s]','',review.lower())
        words.extend([w for w in cleaned.split() if w not in stop_words])

    return Counter(words).most_common(5)

def get_overall_sentiment(positive, negative, neutral):
    if positive > negative and positive > neutral:
        return "Overall Positive"
    elif negative > positive and negative > neutral:
        return "Overall Negative"
    else:
        return "Overall Neutral"
    


