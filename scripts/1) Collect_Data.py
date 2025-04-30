import trafilatura
import csv

# List of URLs to scrape
urls = [
    "https://www.mentalhealth.gov/basics/what-is-mental-health",
    "https://www.samhsa.gov/mental-health/what-is-mental-health/facts",
    "https://www.nimh.nih.gov/health/topics/anxiety-disorders",
    "https://www.nimh.nih.gov/health/statistics/generalized-anxiety-disorder",
    "https://www.nimh.nih.gov/health/statistics/social-anxiety-disorder",
    "https://www.nimh.nih.gov/health/publications/so-stressed-out-fact-sheet",
    "https://www.cdc.gov/mental-health/about/index.html",
    "https://www.cdc.gov/mental-health/index.html",
    "https://medlineplus.gov/mentalhealth.html",
    "https://medlineplus.gov/anxiety.html",
    "https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response",
    "https://www.who.int/health-topics/mental-health#tab=tab_1",
    "https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response",
    "https://www.who.int/news-room/fact-sheets/detail/mental-health-in-emergencies",
    "https://www.who.int/news-room/fact-sheets/detail/mental-health-and-forced-displacement",
    "https://www.who.int/news-room/fact-sheets/detail/mental-health-at-work",
    "https://www.who.int/news-room/fact-sheets/detail/adolescent-mental-health",
    "https://www.who.int/news-room/fact-sheets/detail/mental-health-of-older-adults",
    "https://www.who.int/news-room/fact-sheets/detail/mental-disorders",
    "https://www.who.int/news-room/fact-sheets/detail/anxiety-disorders",
    "https://www.who.int/news-room/fact-sheets/detail/bipolar-disorder",
    "https://www.who.int/news-room/fact-sheets/detail/depression",
    "https://www.who.int/news-room/fact-sheets/detail/schizophrenia",
    "https://www.who.int/news-room/fact-sheets/detail/suicide",
    "https://www.who.int/news-room/questions-and-answers/item/mental-health-promoting-and-protecting-human-rights",
    "https://www.who.int/news-room/questions-and-answers/item/stress",
    "https://www.who.int/news-room/questions-and-answers/item/suicide",
]

data = []
total_word_count = 0

for url in urls:
    downloaded = trafilatura.fetch_url(url)
    result = trafilatura.extract(downloaded)
    if result:
        word_count = len(result.split())
        total_word_count += word_count
        print(f"{url} — {word_count} words")
        data.append((url, result))

print(f"\n✅ Total Word Count: {total_word_count} words")

# Save to CSV
with open("data\mental_health_data.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["source_url", "text"])
    writer.writerows(data)