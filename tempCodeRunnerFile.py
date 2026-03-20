elif "headlines" in c.lower():
    #     print("Fetching news...")
    
    # try:
    #     r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
    #     print("Status Code:", r.status_code)

    #     if r.status_code == 200:
    #         data = r.json()
    #         articles = data.get('articles', [])

    #         if not articles:
    #             speak("No news found.")
    #             return

    #         for article in articles[:5]:
    #             print(article['title'])
    #             speak(article['title'])

    #     else:
    #         speak("Failed to fetch news.")

    # except Exception as e:
    #     print("News Error:", e)
    #     speak("Error fetching news.")