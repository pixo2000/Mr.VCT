"""
VLR.gg Scraper - Fetch latest matches and events from vlr.gg
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime


class VLRScraper:
    """Scraper for vlr.gg to fetch Valorant esports matches and events"""
    
    BASE_URL = "https://www.vlr.gg"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_latest_matches(self, limit: int = 10) -> List[Dict]:
        """
        Fetch the latest matches from vlr.gg
        
        Args:
            limit: Maximum number of matches to return
            
        Returns:
            List of match dictionaries containing match information
        """
        try:
            url = f"{self.BASE_URL}/matches"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            matches = []
            
            # Find all match cards on the page
            match_cards = soup.find_all('a', class_='wf-module-item', limit=limit)
            
            for card in match_cards:
                match_data = self._parse_match_card(card)
                if match_data:
                    matches.append(match_data)
            
            return matches
            
        except requests.RequestException as e:
            print(f"Error fetching matches: {e}")
            return []
    
    def _parse_match_card(self, card) -> Optional[Dict]:
        """Parse a match card element to extract match information"""
        try:
            match_info = {}
            
            # Get match URL
            match_info['url'] = self.BASE_URL + card.get('href', '')
            
            # Get team names
            teams = card.find_all('div', class_='text-of')
            if len(teams) >= 2:
                match_info['team1'] = teams[0].get_text(strip=True)
                match_info['team2'] = teams[1].get_text(strip=True)
            
            # Get match score
            scores = card.find_all('div', class_='match-item-vs-team-score')
            if len(scores) >= 2:
                match_info['score1'] = scores[0].get_text(strip=True)
                match_info['score2'] = scores[1].get_text(strip=True)
            
            # Get match time/status
            time_elem = card.find('div', class_='ml-status')
            if time_elem:
                match_info['status'] = time_elem.get_text(strip=True)
            
            # Get tournament/event name
            event_elem = card.find('div', class_='match-item-event')
            if event_elem:
                event_series = event_elem.find('div', class_='match-item-event-series')
                if event_series:
                    match_info['event'] = event_series.get_text(strip=True)
            
            # Get match format (BO3, BO5, etc.)
            eta_elem = card.find('div', class_='ml-eta')
            if eta_elem:
                match_info['format'] = eta_elem.get_text(strip=True)
            
            return match_info if match_info else None
            
        except Exception as e:
            print(f"Error parsing match card: {e}")
            return None
    
    def get_upcoming_events(self, limit: int = 10) -> List[Dict]:
        """
        Fetch upcoming events from vlr.gg
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List of event dictionaries containing event information
        """
        try:
            url = f"{self.BASE_URL}/events"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            events = []
            
            # Find event cards
            event_cards = soup.find_all('a', class_='wf-card', limit=limit)
            
            for card in event_cards:
                event_data = self._parse_event_card(card)
                if event_data:
                    events.append(event_data)
            
            return events
            
        except requests.RequestException as e:
            print(f"Error fetching events: {e}")
            return []
    
    def _parse_event_card(self, card) -> Optional[Dict]:
        """Parse an event card element to extract event information"""
        try:
            event_info = {}
            
            # Get event URL
            event_info['url'] = self.BASE_URL + card.get('href', '')
            
            # Get event name
            title_elem = card.find('div', class_='event-item-title')
            if title_elem:
                event_info['name'] = title_elem.get_text(strip=True)
            
            # Get event dates
            dates_elem = card.find('div', class_='event-item-desc-item-value')
            if dates_elem:
                event_info['dates'] = dates_elem.get_text(strip=True)
            
            # Get prize pool
            prize_elems = card.find_all('div', class_='event-item-desc-item-value')
            if len(prize_elems) > 1:
                event_info['prize'] = prize_elems[1].get_text(strip=True)
            
            # Get location/region
            location_elem = card.find('div', class_='event-item-desc-item')
            if location_elem:
                location_icon = location_elem.find('i', class_='fa-location-dot')
                if location_icon and location_icon.parent:
                    event_info['location'] = location_icon.parent.find('div', class_='event-item-desc-item-value')
                    if event_info['location']:
                        event_info['location'] = event_info['location'].get_text(strip=True)
            
            # Get event status
            status_elem = card.find('div', class_='event-item-status')
            if status_elem:
                event_info['status'] = status_elem.get_text(strip=True)
            
            return event_info if event_info else None
            
        except Exception as e:
            print(f"Error parsing event card: {e}")
            return None
    
    def get_live_matches(self) -> List[Dict]:
        """
        Fetch currently live matches from vlr.gg
        
        Returns:
            List of live match dictionaries
        """
        try:
            url = f"{self.BASE_URL}/matches"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            live_matches = []
            
            # Find match cards with "LIVE" status
            match_cards = soup.find_all('a', class_='wf-module-item')
            
            for card in match_cards:
                status_elem = card.find('div', class_='ml-status')
                if status_elem and 'LIVE' in status_elem.get_text(strip=True).upper():
                    match_data = self._parse_match_card(card)
                    if match_data:
                        live_matches.append(match_data)
            
            return live_matches
            
        except requests.RequestException as e:
            print(f"Error fetching live matches: {e}")
            return []


def main():
    """Example usage of VLRScraper"""
    scraper = VLRScraper()
    
    print("=" * 60)
    print("VLR.gg Scraper - Latest Valorant Esports Data")
    print("=" * 60)
    
    # Get latest matches
    print("\n📋 LATEST MATCHES:")
    print("-" * 60)
    matches = scraper.get_latest_matches(limit=5)
    
    if matches:
        for i, match in enumerate(matches, 1):
            print(f"\n{i}. {match.get('team1', 'TBD')} vs {match.get('team2', 'TBD')}")
            if 'score1' in match and 'score2' in match:
                print(f"   Score: {match['score1']} - {match['score2']}")
            if 'status' in match:
                print(f"   Status: {match['status']}")
            if 'event' in match:
                print(f"   Event: {match['event']}")
            if 'format' in match:
                print(f"   Format: {match['format']}")
            if 'url' in match:
                print(f"   URL: {match['url']}")
    else:
        print("No matches found.")
    
    # Get live matches
    print("\n\n🔴 LIVE MATCHES:")
    print("-" * 60)
    live_matches = scraper.get_live_matches()
    
    if live_matches:
        for i, match in enumerate(live_matches, 1):
            print(f"\n{i}. {match.get('team1', 'TBD')} vs {match.get('team2', 'TBD')}")
            if 'score1' in match and 'score2' in match:
                print(f"   Score: {match['score1']} - {match['score2']}")
            if 'event' in match:
                print(f"   Event: {match['event']}")
            if 'url' in match:
                print(f"   URL: {match['url']}")
    else:
        print("No live matches at the moment.")
    
    # Get upcoming events
    print("\n\n📅 UPCOMING EVENTS:")
    print("-" * 60)
    events = scraper.get_upcoming_events(limit=5)
    
    if events:
        for i, event in enumerate(events, 1):
            print(f"\n{i}. {event.get('name', 'Unknown Event')}")
            if 'dates' in event:
                print(f"   Dates: {event['dates']}")
            if 'prize' in event:
                print(f"   Prize: {event['prize']}")
            if 'location' in event:
                print(f"   Location: {event['location']}")
            if 'status' in event:
                print(f"   Status: {event['status']}")
            if 'url' in event:
                print(f"   URL: {event['url']}")
    else:
        print("No upcoming events found.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
