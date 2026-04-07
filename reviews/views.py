from django.shortcuts import render
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup


def analyze_review(request):
    # Step 1: Default values (before user does anything)
    result = None

    # Step 2: Check if user submitted the form
    if request.method == "POST":

        # Step 3: Get input from form
        review_text = request.POST.get("review_text")
        product_url = request.POST.get("product_url")

        # Step 4: If user entered TEXT → analyze directly
        if review_text:
            blob = TextBlob(review_text)
            polarity = blob.sentiment.polarity

            result = {
                "type": "text",
                "content": review_text,
                "polarity": round(polarity, 2),
                "sentiment": get_sentiment_label(polarity)
            }

        # Step 5: If user entered URL → scrape + analyze
        elif product_url:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(product_url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract reviews
                review_elements = soup.find_all("span", {"data-hook": "review-body"})
                reviews = [r.get_text().strip() for r in review_elements]

                # Analyze all reviews
                positive, negative, neutral = 0, 0, 0

                for review in reviews:
                    polarity = TextBlob(review).sentiment.polarity

                    if polarity > 0:
                        positive += 1
                    elif polarity < 0:
                        negative += 1
                    else:
                        neutral += 1

                result = {
                    "type": "url",
                    "total": len(reviews),
                    "positive": positive,
                    "negative": negative,
                    "neutral": neutral
                }

            except Exception as e:
                result = {"error": str(e)}

        # Step 6: If nothing entered
        else:
            result = {"error": "Please enter text or URL"}

    # Step 7: Show page
    return render(request, "reviews_list.html", {"result": result})


# Helper function (keeps logic clean)
def get_sentiment_label(polarity):
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    return "Neutral"