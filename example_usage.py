"""
Example usage of the VLR.gg Scraper
"""

import json
from vlr_scraper import VLRScraper


def example_get_matches():
    """Example: Get latest matches"""
    print("Example 1: Getting latest matches\n")
    
    scraper = VLRScraper()
    matches = scraper.get_latest_matches(limit=3)
    
    print(json.dumps(matches, indent=2))
    print(f"\nFound {len(matches)} matches\n")


def example_get_live_matches():
    """Example: Get live matches"""
    print("Example 2: Getting live matches\n")
    
    scraper = VLRScraper()
    live_matches = scraper.get_live_matches()
    
    print(json.dumps(live_matches, indent=2))
    print(f"\nFound {len(live_matches)} live matches\n")


def example_get_events():
    """Example: Get upcoming events"""
    print("Example 3: Getting upcoming events\n")
    
    scraper = VLRScraper()
    events = scraper.get_upcoming_events(limit=3)
    
    print(json.dumps(events, indent=2))
    print(f"\nFound {len(events)} events\n")


def example_filter_matches_by_team():
    """Example: Filter matches by team name"""
    print("Example 4: Filtering matches by team\n")
    
    scraper = VLRScraper()
    all_matches = scraper.get_latest_matches(limit=20)
    
    team_name = "Sentinels"
    filtered_matches = [
        match for match in all_matches
        if team_name.lower() in match.get('team1', '').lower() or
        team_name.lower() in match.get('team2', '').lower()
    ]
    
    print(f"Matches featuring {team_name}:")
    print(json.dumps(filtered_matches, indent=2))
    print(f"\nFound {len(filtered_matches)} matches featuring {team_name}\n")


def example_save_to_json():
    """Example: Save data to JSON file"""
    print("Example 5: Saving data to JSON file\n")
    
    scraper = VLRScraper()
    
    data = {
        'matches': scraper.get_latest_matches(limit=10),
        'live_matches': scraper.get_live_matches(),
        'events': scraper.get_upcoming_events(limit=10)
    }
    
    filename = 'vlr_data.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data saved to {filename}")


if __name__ == "__main__":
    print("=" * 70)
    print("VLR.gg Scraper - Usage Examples")
    print("=" * 70)
    print()
    
    # Run all examples
    examples = [
        example_get_matches,
        example_get_live_matches,
        example_get_events,
        example_filter_matches_by_team,
        example_save_to_json
    ]
    
    for example in examples:
        try:
            example()
            print("-" * 70)
            print()
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
            print("-" * 70)
            print()
