# Mr.VCT
A discord bot for valorant esports and some more stuff

## VLR.gg Scraper

This repository includes a Python program to fetch the latest matches and events from [vlr.gg](https://www.vlr.gg), a popular Valorant esports website.

### Features

- 🎮 Fetch latest Valorant matches with scores and details
- 🔴 Get currently live matches
- 📅 Retrieve upcoming events and tournaments
- 🏆 Access event details including prize pools, dates, and locations
- 📊 Clean, structured JSON output

### Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage

#### Basic Usage

Run the scraper with default settings:

```bash
python vlr_scraper.py
```

This will display:
- Latest matches (5 most recent)
- Currently live matches
- Upcoming events (5 next events)

#### Programmatic Usage

Use the scraper in your own Python code:

```python
from vlr_scraper import VLRScraper

# Create scraper instance
scraper = VLRScraper()

# Get latest matches
matches = scraper.get_latest_matches(limit=10)
for match in matches:
    print(f"{match['team1']} vs {match['team2']}")
    print(f"Status: {match['status']}")

# Get live matches
live_matches = scraper.get_live_matches()
for match in live_matches:
    print(f"LIVE: {match['team1']} vs {match['team2']}")

# Get upcoming events
events = scraper.get_upcoming_events(limit=5)
for event in events:
    print(f"Event: {event['name']}")
    print(f"Dates: {event['dates']}")
```

#### Example Scripts

Run the example usage script to see various use cases:

```bash
python example_usage.py
```

### API Reference

#### VLRScraper Class

##### `get_latest_matches(limit=10)`
Fetch the latest matches from vlr.gg.

**Parameters:**
- `limit` (int): Maximum number of matches to return (default: 10)

**Returns:**
- List of dictionaries containing match information:
  - `team1`: Name of first team
  - `team2`: Name of second team
  - `score1`: Score of first team (if available)
  - `score2`: Score of second team (if available)
  - `status`: Match status (e.g., "LIVE", "Upcoming", time)
  - `event`: Tournament/event name
  - `format`: Match format (e.g., "BO3", "BO5")
  - `url`: Full URL to match page

##### `get_live_matches()`
Fetch currently live matches from vlr.gg.

**Returns:**
- List of dictionaries containing live match information (same structure as get_latest_matches)

##### `get_upcoming_events(limit=10)`
Fetch upcoming events and tournaments from vlr.gg.

**Parameters:**
- `limit` (int): Maximum number of events to return (default: 10)

**Returns:**
- List of dictionaries containing event information:
  - `name`: Event name
  - `dates`: Event dates
  - `prize`: Prize pool (if available)
  - `location`: Event location/region
  - `status`: Event status
  - `url`: Full URL to event page

### Data Structure Examples

#### Match Data
```json
{
  "team1": "Sentinels",
  "team2": "LOUD",
  "score1": "2",
  "score2": "1",
  "status": "Completed",
  "event": "VCT Champions 2024",
  "format": "BO3",
  "url": "https://www.vlr.gg/123456/sentinels-vs-loud"
}
```

#### Event Data
```json
{
  "name": "VCT Champions 2024",
  "dates": "Aug 1 - Aug 25, 2024",
  "prize": "$1,000,000",
  "location": "Seoul, South Korea",
  "status": "Upcoming",
  "url": "https://www.vlr.gg/event/1234/vct-champions-2024"
}
```

### Use Cases

- **Discord Bots**: Integrate match updates into Discord servers
- **Data Analysis**: Collect historical match data for analysis
- **Live Notifications**: Monitor for live matches and send alerts
- **Tournament Tracking**: Keep track of upcoming tournaments and events
- **Team Following**: Filter matches by specific teams

### Error Handling

The scraper includes built-in error handling:
- Network errors are caught and logged
- Empty results return empty lists instead of raising exceptions
- Parsing errors are handled gracefully

### Notes

- The scraper respects vlr.gg's website structure as of the implementation date
- Website structure changes may require updates to the parsing logic
- Use responsibly and avoid excessive requests that could overload the server
- Consider adding delays between requests for large-scale scraping

### Dependencies

- `requests>=2.31.0`: HTTP library for making requests
- `beautifulsoup4>=4.12.0`: HTML parsing library

### License

This project is intended for educational and personal use.
