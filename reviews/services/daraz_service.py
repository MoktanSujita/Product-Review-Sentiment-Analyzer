import requests

def fetch_all_reviews(item_id):
    all_reviews = []
    page = 1

    while True:
        response = requests.get(
            "https://my.daraz.com.np/pdp/review/getReviewList",
            params={
                "itemId": item_id,
                "pageSize": 20,
                "pageNo": page
            },
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        if response.status_code != 200:
            break

        data = response.json()
        items = data.get("model", {}).get("items", [])

        if not items:
            break

        for r in items:
            text = r.get("reviewContent")
            if text:
                all_reviews.append(text.strip())

        page += 1

    return all_reviews