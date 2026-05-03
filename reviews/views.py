from django.shortcuts import render, redirect
from textblob import TextBlob
from collections import Counter
import re
from .models import Review
from .services.daraz_service import fetch_all_reviews


# MAIN VIEW
def analyze_review(request):
    result = None

    if request.method == 'POST':

        review_text = request.POST.get("review_text")
        product_url = request.POST.get("product_url")

        # nothing entered
        if not review_text and not product_url:
            result = {"error": "Please enter review text or product URL"}
            return render(request, "reviews_list.html", {"result": result})

        # CASE 1: Manual text review
        if review_text:
            polarity = TextBlob(review_text).sentiment.polarity
            sentiment = get_sentiment_label(polarity)

            result = {
                "type": "text",
                "content": review_text,
                "polarity": round(polarity, 2),
                "sentiment": sentiment
            }

            Review.objects.create(
                product_name=review_text[:50],
                product_url="",
                sentiment=sentiment
            )

        
        # CASE 2: Daraz URL analysis
        
        elif product_url:
            try:
                # extract product ID safely
                match = re.search(r'i(\d+)', product_url)

                if not match:
                    result = {"error": "Invalid Daraz URL format"}
                    return render(request, "reviews_list.html", {"result": result})

                item_id = match.group(1)

                # fetch ALL reviews from service layer
                reviews = fetch_all_reviews(item_id)

                if not reviews:
                    result = {"error": "No reviews found for this product"}
                    return render(request, "reviews_list.html", {"result": result})

                # Sentiment analysis
                positive = negative = neutral = 0
                positive_reviews = []
                negative_reviews = []
                neutral_reviews = []

                for review in reviews:
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

                total = len(reviews)

                # Build result for charts
                result = {
                    "type": "url",
                    "total_reviews": total,
                    "positive": positive,
                    "negative": negative,
                    "neutral": neutral,

                    "positive_percentage": round((positive / total) * 100, 2),
                    "negative_percentage": round((negative / total) * 100, 2),
                    "neutral_percentage": round((neutral / total) * 100, 2),

                    "overall": get_overall_sentiment(positive, negative, neutral),

                    "top_positive_words": get_top_words(positive_reviews),
                    "top_negative_words": get_top_words(negative_reviews),
                    "top_neutral_words": get_top_words(neutral_reviews),

                    "sample_positive": positive_reviews[:3],
                    "sample_negative": negative_reviews[:3],
                    "sample_neutral": neutral_reviews[:3],
                }

                Review.objects.create(
                    product_name=product_url[:80],
                    product_url=product_url,
                    sentiment=result["overall"]
                )

            except Exception as e:
                result = {"error": str(e)}

        # store for charts
        request.session["result"] = result
        return redirect("chart_page")

    return render(request, "reviews_list.html", {"result": result})


# HELPERS
def get_sentiment_label(polarity):
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    return "Neutral"


stop_words = {
    "the", "is", "in", "and", "to", "a", "of", "it", "for",
    "on", "with", "was", "as", "but", "are", "this", "that",
    "xa", "k"
}


def get_top_words(review_list):
    words = []

    for review in review_list:
        cleaned = re.sub(r'[^\w\s]', '', review.lower())
        words.extend([w for w in cleaned.split() if w not in stop_words])

    return Counter(words).most_common(3)


def get_overall_sentiment(positive, negative, neutral):
    if positive > negative and positive > neutral:
        return "Overall Positive"
    elif negative > positive and negative > neutral:
        return "Overall Negative"
    return "Overall Neutral"


# CHART PAGE
def chart_page(request):
    result = request.session.get("result", {})
    return render(request, "chart.html", {"result": result})