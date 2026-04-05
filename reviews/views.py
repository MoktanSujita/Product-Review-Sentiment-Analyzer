from django.shortcuts import render
from textblob import TextBlob
# Create your views here.
def home(request):
    result = None
    sentiment = None

    if request.method == 'POST':
        url = request.POST.get('url')

        fake_reviews =[
            "This product is amazing! I love it.",
            "Very bad quality, not worth the money.",
            "I am extremely satisfied with this purchase.",
        ]   

        combined_text = "".join(fake_reviews)
        blob =TextBlob(combined_text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

            result = f"Polarity Score: {polarity}"
    return render(request, "reviews_list.html",{
            "result" : result,
            "sentiment" : sentiment 
        })