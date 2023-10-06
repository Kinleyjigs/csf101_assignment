import requests
import webbrowser
import rumps

class NewsApp(rumps.App):
    def __init__(self, *args, **kwargs):
        super(NewsApp, self).__init__(*args, **kwargs)
        self.menu.add(rumps.MenuItem("Fetch News", callback=self.fetch_news))

    @rumps.clicked("Fetch News")
    def fetch_news(self, _):
        main_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=48d37aa8af2d451a83f01168d796be12"
        try:
            news_data = requests.get(main_url, timeout=3)
            news_data.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            rumps.alert(f"HTTP Error: {errh}")
            return
        except requests.exceptions.ConnectionError as errc:
            rumps.alert(f"Error Connecting: {errc}")
            return
        except requests.exceptions.Timeout as errt:
            rumps.alert(f"Timeout Error: {errt}")
            return
        except requests.exceptions.RequestException as err:
            rumps.alert(f"Something went wrong: {err}")
            return

        if "articles" in news_data.json():
            articles = news_data.json()["articles"]
            for i, article in enumerate(articles):
                self.menu.add(rumps.MenuItem(article['title'], callback=lambda _, article=article: webbrowser.open(article['url'])))
        else:
            rumps.alert("No articles found in the response.")

if __name__ == "__main__":
    NewsApp("Python News").run()
######
