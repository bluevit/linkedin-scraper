from flask import Flask, request, jsonify
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions

app = Flask(__name__)

@app.route("/")
def home():
    return "LinkedIn Scraper API Running"

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    keyword = data.get("keyword", "Engineer")
    location = data.get("location", "United States")

    result = []

    def on_data(d: EventData):
        result.append({
            "title": d.title,
            "company": d.company,
            "location": d.place,
            "link": d.link,
            "date": d.date,
            "description": d.description[:200]
        })

    scraper = LinkedinScraper(headless=True, max_workers=1)
    scraper.on(Events.DATA, on_data)

    query = Query(
        query=keyword,
        options=QueryOptions(
            locations=[location],
            limit=5
        )
    )

    scraper.run([query])

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
