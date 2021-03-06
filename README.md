# boxOfficeCrawler

## Installation

1) Just run 

```bash
pip install -r requirements.txt
```

in projects home directory.

2) Rename `example.db.py` to `db.py` and enter your MongoDB connection string to the file.

## Setup

`movies.json` contains setup data for movie scraping. Movies and their boxofficemojo.com Id, that was extracted from the URL of each movie, can be enlisted in the JSON file in order to be scraped.

```javascript
[{
	"name": "Birdman",
	"boxOfficeId": "birdman",
	"totalGross": 2000000
	"release": new Date(),
	"history": []
}]
```

The scraping results are:

* Domestic Total Gross in $USD

## Usage

### Crawling historic box office data in a daily fashion

```python
python crawlHistories.py
```

### Crawl all available movies

```python
python crawlMovies.py
```

## Data sources

Daily View: http://www.boxofficemojo.com/movies/?page=daily&view=chart&id=birdman.htm
