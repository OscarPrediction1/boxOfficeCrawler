# boxOfficeCrawler

## Installation

Just run 

```bash
pip install -r requirements.txt
```

in projects home directory

## Setup

`movies.json` contains setup data for movie scraping. Movies and their boxofficemojo.com Id, that was extracted from the URL of each movie, can be enlisted in the JSON file in order to be scraped.

```javascript
[{
	"name": "Birdman",
	"boxOfficeId": "birdman",
	"release": 20141017
}]
```

The scraping results are:

* Domestic Total Gross in $USD

## Usage

### Crawling movie information

```python
python crawl.py
```

## Data sources

Daily View: http://www.boxofficemojo.com/movies/?page=daily&view=chart&id=birdman.htm