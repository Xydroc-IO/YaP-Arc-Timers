#!/usr/bin/env python3
"""
ARC Raiders Event Timer Display
Fetches and displays event timers from MetaForge
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import re
import threading
import time
import json
import os
from PIL import Image, ImageTk

# Debug mode - set to True to save HTML/JSON responses
DEBUG_MODE = True


class EventTimer:
    def __init__(self, name, status, locations, time_info, countdown_seconds, upcoming_windows):
        self.name = name
        self.status = status  # "Active" or "Upcoming"
        self.locations = locations
        self.time_info = time_info  # e.g., "1:00 AM - 2:00 AM"
        self.countdown_seconds = countdown_seconds
        self.upcoming_windows = upcoming_windows  # List of upcoming time windows


class ArcTimersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ARC Raiders Event Timers")
        self.root.geometry("1600x900")
        self.root.minsize(1200, 700)  # Set minimum window size
        self.root.configure(bg="#1a1a1a")
        
        # Set window icon (look in parent directory)
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            icon_path = os.path.join(parent_dir, 'timers250.png')
            if os.path.exists(icon_path):
                icon_image = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon_image)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        self.events = []
        self.update_thread = None
        self.running = True
        self.refresh_triggered = False  # Prevent multiple refreshes
        self.last_refresh_time = 0
        
        # Get user's local timezone
        self.local_tz = self.get_local_timezone()
        print(f"User timezone: {self.local_tz}")
        
        self.setup_ui()
        self.fetch_and_display_events()
        
    def setup_ui(self):
        # Header - more compact to give grid more space
        header_frame = tk.Frame(self.root, bg="#2d2d2d", height=65)
        header_frame.pack(fill=tk.X, padx=8, pady=8)
        header_frame.pack_propagate(False)
        
        # Logo and title container
        title_container = tk.Frame(header_frame, bg="#2d2d2d")
        title_container.pack(side=tk.LEFT, padx=16, pady=10)
        
        # Load and display logo (look in parent directory)
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            logo_path = os.path.join(parent_dir, 'timers250.png')
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                # Resize logo to fit header (maintain aspect ratio)
                logo_image = logo_image.resize((45, 45), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(
                    title_container,
                    image=self.logo_photo,
                    bg="#2d2d2d"
                )
                logo_label.pack(side=tk.LEFT, padx=(0, 12))
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        # Title with timezone info
        tz_name = datetime.now().astimezone().tzname() if self.local_tz else "Local"
        title_label = tk.Label(
            title_container,
            text=f"ARC Raiders Event Timers ({tz_name})",
            font=("Arial", 18, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        title_label.pack(side=tk.LEFT)
        
        self.refresh_btn = tk.Button(
            header_frame,
            text="⟳ Refresh",
            command=self.fetch_and_display_events,
            bg="#4a9eff",
            fg="#ffffff",
            font=("Arial", 10, "bold"),
            padx=16,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.refresh_btn.pack(side=tk.RIGHT, padx=16, pady=10)
        
        self.status_label = tk.Label(
            header_frame,
            text="Loading...",
            font=("Arial", 9),
            bg="#2d2d2d",
            fg="#888888"
        )
        self.status_label.pack(side=tk.RIGHT, padx=16)
        
        # Scrollable frame for events - fully expandable
        container = tk.Frame(self.root, bg="#1a1a1a")
        container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        canvas = tk.Canvas(container, bg="#1a1a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")
        
        # Configure the scrollable frame to expand
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Make canvas window expand with canvas
        self.canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind canvas resize to update window width
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(self.canvas_window, width=e.width))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mouse wheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
    def parse_countdown(self, countdown_text):
        """Parse countdown text like '3h 42m 26s' or '42m 26s' to seconds"""
        if not countdown_text:
            return 0
            
        hours = 0
        minutes = 0
        seconds = 0
        
        h_match = re.search(r'(\d+)h', countdown_text.lower())
        m_match = re.search(r'(\d+)m', countdown_text.lower())
        s_match = re.search(r'(\d+)s', countdown_text.lower())
        
        if h_match:
            hours = int(h_match.group(1))
        if m_match:
            minutes = int(m_match.group(1))
        if s_match:
            seconds = int(s_match.group(1))
            
        return hours * 3600 + minutes * 60 + seconds
    
    def get_local_timezone(self):
        """Get the user's local timezone"""
        try:
            # Try to get local timezone
            local_tz_name = datetime.now(timezone.utc).astimezone().tzname()
            # Get the timezone object
            return datetime.now().astimezone().tzinfo
        except Exception as e:
            print(f"Could not detect timezone: {e}, using system local time")
            return None
    
    def convert_utc_time_to_local(self, time_str):
        """Convert UTC time string like '5:00 AM' to local timezone"""
        try:
            # Parse the UTC time
            utc_time = datetime.strptime(time_str.strip(), "%I:%M %p")
            
            # Get current date in UTC
            now_utc = datetime.now(timezone.utc)
            
            # Combine with today's date in UTC
            utc_datetime = datetime(
                now_utc.year, now_utc.month, now_utc.day,
                utc_time.hour, utc_time.minute,
                tzinfo=timezone.utc
            )
            
            # Convert to local timezone
            if self.local_tz:
                local_datetime = utc_datetime.astimezone(self.local_tz)
            else:
                local_datetime = utc_datetime.astimezone()
            
            # Return formatted local time
            return local_datetime.strftime("%I:%M %p")
        except Exception as e:
            print(f"Error converting time {time_str}: {e}")
            return time_str
    
    def convert_time_range_to_local(self, time_range):
        """Convert UTC time range like '5:00 AM - 6:00 AM' to local timezone"""
        try:
            if not time_range or '-' not in time_range:
                return time_range
            
            parts = time_range.split('-')
            if len(parts) != 2:
                return time_range
            
            start_time = self.convert_utc_time_to_local(parts[0])
            end_time = self.convert_utc_time_to_local(parts[1])
            
            return f"{start_time} - {end_time}"
        except Exception as e:
            print(f"Error converting time range {time_range}: {e}")
            return time_range
    
    def format_countdown(self, seconds):
        """Format seconds to '3h 42m 26s' format"""
        if seconds <= 0:
            return "0s"
            
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0 or not parts:
            parts.append(f"{secs}s")
            
        return " ".join(parts)
    
    def fetch_events_from_api(self):
        """Try to fetch events from MetaForge API"""
        try:
            # Try potential API endpoints
            api_urls = [
                "https://metaforge.app/api/arc-raiders/event-timers",
                "https://metaforge.app/api/events/arc-raiders",
                "https://api.metaforge.app/arc-raiders/event-timers",
            ]
            
            headers = {
                'User-Agent': 'ArcTimersApp/1.0',
                'Accept': 'application/json',
            }
            
            for api_url in api_urls:
                try:
                    response = requests.get(api_url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"Successfully fetched from API: {api_url}")
                        # Parse JSON data here
                        return self.parse_api_data(data)
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"API fetch failed: {e}")
            return None
    
    def parse_api_data(self, data):
        """Parse event data from API response"""
        events = []
        # This will need to be adjusted based on actual API structure
        if isinstance(data, dict) and 'events' in data:
            for event_data in data.get('events', []):
                event = EventTimer(
                    name=event_data.get('name', ''),
                    status=event_data.get('status', 'Upcoming'),
                    locations=event_data.get('locations', []),
                    time_info=event_data.get('time', ''),
                    countdown_seconds=event_data.get('countdown', 0),
                    upcoming_windows=event_data.get('windows', [])
                )
                events.append(event)
        return events if events else None
    
    def fetch_events(self):
        """Fetch events from the MetaForge website"""
        # First try API
        api_events = self.fetch_events_from_api()
        if api_events:
            return api_events
        
        # Fall back to web scraping
        try:
            url = "https://metaforge.app/arc-raiders/event-timers"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            print("Fetching events from MetaForge website...")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            html_content = response.text
            
            # Save HTML for debugging (save in parent directory)
            if DEBUG_MODE:
                try:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    parent_dir = os.path.dirname(script_dir)
                    debug_file = os.path.join(parent_dir, 'debug_response.html')
                    with open(debug_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"Debug: Saved HTML response to {debug_file}")
                except:
                    pass
            
            soup = BeautifulSoup(html_content, 'lxml')
            events = []
            
            print("Parsing event cards from HTML...")
            
            # Find all event cards - they have specific class patterns
            # Look for divs that contain event information
            event_cards = soup.find_all('div', class_=lambda x: x and 'bg-secondary/70' in x)
            
            print(f"Found {len(event_cards)} event cards")
            
            for card in event_cards:
                try:
                    # Extract event name from h4
                    name_elem = card.find('h4', class_=lambda x: x and 'text-foreground' in x and 'font-semibold' in x)
                    if not name_elem:
                        continue
                    
                    event_name = name_elem.get_text(strip=True)
                    
                    # Extract status from badge
                    status = "Upcoming"
                    status_badge = card.find('span', class_=lambda x: x and ('text-green-400' in x or 'text-blue-400' in x))
                    if status_badge:
                        badge_text = status_badge.get_text(strip=True)
                        if 'Active' in badge_text:
                            status = "Active"
                    
                    # Extract locations
                    locations = []
                    location_elem = card.find('div', class_=lambda x: x and 'text-muted-foreground' in x and 'text-xs' in x and 'uppercase' in x)
                    if location_elem:
                        location_text = location_elem.get_text(strip=True)
                        for loc in ["Dam", "Spaceport", "Buried City", "Blue Gate"]:
                            if loc in location_text:
                                locations.append(loc)
                    
                    # Extract countdown
                    countdown_seconds = 0
                    countdown_elem = card.find('span', class_=lambda x: x and 'text-lg' in x and 'font-semibold' in x and 'text-white' in x)
                    if countdown_elem:
                        countdown_text = countdown_elem.get_text(strip=True)
                        countdown_seconds = self.parse_countdown(countdown_text)
                    
                    # Extract time range and convert to local timezone
                    time_info = ""
                    time_elem = card.find('div', class_=lambda x: x and 'text-foreground/90' in x and 'text-sm' in x and 'font-medium' in x)
                    if time_elem:
                        utc_time_info = time_elem.get_text(strip=True)
                        time_info = self.convert_time_range_to_local(utc_time_info)
                    
                    # Extract upcoming windows and convert times to local timezone
                    upcoming_windows = []
                    windows_container = card.find('div', class_=lambda x: x and 'divide-border' in x)
                    if windows_container:
                        window_divs = windows_container.find_all('div', class_=lambda x: x and 'py-1.5' in x)
                        for window_div in window_divs[:5]:  # Limit to 5
                            window_text = window_div.get_text(separator=' ', strip=True)
                            # Convert time range in window text
                            # Format is like "5:00 AM - 6:00 AM Dam in 3h 38m 42s"
                            time_range_match = re.search(r'(\d{1,2}:\d{2}\s*[AP]M)\s*-\s*(\d{1,2}:\d{2}\s*[AP]M)', window_text)
                            if time_range_match:
                                utc_range = f"{time_range_match.group(1)} - {time_range_match.group(2)}"
                                local_range = self.convert_time_range_to_local(utc_range)
                                window_text = window_text.replace(utc_range, local_range)
                            upcoming_windows.append(window_text)
                    
                    if event_name and (countdown_seconds > 0 or locations):
                        event = EventTimer(
                            name=event_name,
                            status=status,
                            locations=locations if locations else ["Multiple Locations"],
                            time_info=time_info,
                            countdown_seconds=countdown_seconds,
                            upcoming_windows=upcoming_windows
                        )
                        events.append(event)
                        print(f"✓ Parsed: {event_name} - {status} - {self.format_countdown(countdown_seconds)}")
                        
                except Exception as e:
                    print(f"Error parsing card: {e}")
                    continue
            
            if events:
                print(f"\n✓ Successfully parsed {len(events)} events from website")
                return events
            else:
                print("ERROR: No events parsed from website")
                return self.create_error_placeholder()
            
        except Exception as e:
            print(f"ERROR fetching events: {e}")
            import traceback
            traceback.print_exc()
            return self.create_error_placeholder()
    
    def create_error_placeholder(self):
        """Create an error placeholder to indicate fetch failed"""
        return []
    
    def fetch_and_display_events(self):
        """Fetch events in a separate thread and display them"""
        self.status_label.config(text="Loading...")
        self.refresh_btn.config(state=tk.DISABLED)
        
        def fetch_thread():
            self.events = self.fetch_events()
            event_count = len(self.events)
            
            status_text = f"Last updated: {datetime.now().strftime('%I:%M:%S %p')}"
            
            if event_count == 0:
                status_text = "ERROR: Failed to fetch events from website"
            else:
                status_text += f" ({event_count} events loaded)"
            
            self.root.after(0, self.display_events)
            self.root.after(0, lambda: self.status_label.config(text=status_text))
            self.root.after(0, lambda: self.refresh_btn.config(state=tk.NORMAL))
            
        thread = threading.Thread(target=fetch_thread, daemon=True)
        thread.start()
    
    def display_events(self):
        """Display events in the GUI"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Check if we have events
        if not self.events:
            # Display error message - compact version
            error_frame = tk.Frame(self.scrollable_frame, bg="#2d2d2d", relief=tk.RAISED, borderwidth=2)
            error_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=15, pady=15)
            self.scrollable_frame.grid_rowconfigure(0, weight=1)
            self.scrollable_frame.grid_columnconfigure(0, weight=1)
            
            error_icon = tk.Label(
                error_frame,
                text="⚠",
                font=("Arial", 36),
                bg="#2d2d2d",
                fg="#ef4444"
            )
            error_icon.pack(pady=(30, 15))
            
            error_title = tk.Label(
                error_frame,
                text="Unable to Fetch Events",
                font=("Arial", 16, "bold"),
                bg="#2d2d2d",
                fg="#ffffff"
            )
            error_title.pack(pady=8)
            
            error_msg = tk.Label(
                error_frame,
                text="Could not retrieve event data from MetaForge website.\n\n"
                     "Possible causes:\n"
                     "• Website structure may have changed\n"
                     "• Network connection issues\n"
                     "• Website is temporarily unavailable\n\n"
                     "Try clicking the Refresh button or check test_fetch.py for debugging.",
                font=("Arial", 10),
                bg="#2d2d2d",
                fg="#aaaaaa",
                justify=tk.CENTER
            )
            error_msg.pack(pady=15, padx=30)
            
            # Add helpful commands - more compact
            help_frame = tk.Frame(error_frame, bg="#1a1a1a")
            help_frame.pack(pady=15, padx=30, fill=tk.X)
            
            help_label = tk.Label(
                help_frame,
                text="Debug Commands:",
                font=("Arial", 9, "bold"),
                bg="#1a1a1a",
                fg="#888888",
                anchor="w"
            )
            help_label.pack(anchor="w", pady=(8, 4))
            
            cmd_label = tk.Label(
                help_frame,
                text="python3 test_fetch.py    # Test website connection\n"
                     "cat debug_response.html  # View fetched HTML",
                font=("Courier", 8),
                bg="#1a1a1a",
                fg="#4a9eff",
                anchor="w",
                justify=tk.LEFT
            )
            cmd_label.pack(anchor="w", padx=8)
            
            return
        
        # Sort events: Active first, then by countdown
        active_events = [e for e in self.events if e.status == "Active"]
        upcoming_events = sorted([e for e in self.events if e.status == "Upcoming"],
                                key=lambda x: x.countdown_seconds)
        
        all_events = active_events + upcoming_events
        
        # Display events in a 3x3 grid with proper expansion
        row = 0
        col = 0
        max_cols = 3
        
        # Configure all columns to expand equally (horizontal resizing)
        for i in range(max_cols):
            self.scrollable_frame.grid_columnconfigure(i, weight=1, minsize=300)
        
        # Calculate number of rows needed and set them to expand (vertical resizing)
        num_rows = (len(all_events) + max_cols - 1) // max_cols
        for i in range(num_rows):
            self.scrollable_frame.grid_rowconfigure(i, weight=1, minsize=200)
        
        for event in all_events:
            self.create_event_card(self.scrollable_frame, event, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Start countdown update
        self.update_countdowns()
    
    def create_event_card(self, parent, event, row, col):
        """Create a card widget for an event"""
        # Card frame - compact but readable, expands in all directions
        card = tk.Frame(parent, bg="#2d2d2d", relief=tk.RAISED, borderwidth=2)
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        
        # Status badge - more compact
        status_color = "#22c55e" if event.status == "Active" else "#3b82f6"
        status_badge = tk.Label(
            card,
            text=event.status.upper(),
            bg=status_color,
            fg="#ffffff",
            font=("Arial", 9, "bold"),
            padx=8,
            pady=2
        )
        status_badge.pack(anchor="nw", padx=10, pady=8)
        
        # Event name
        name_label = tk.Label(
            card,
            text=event.name,
            font=("Arial", 14, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            anchor="w",
            wraplength=350
        )
        name_label.pack(fill=tk.X, padx=10, pady=(0, 4))
        
        # Locations - compact
        locations_text = ", ".join(event.locations)
        if len(locations_text) > 35:
            locations_text = locations_text[:32] + "..."
        locations_label = tk.Label(
            card,
            text=locations_text.upper(),
            font=("Arial", 9),
            bg="#2d2d2d",
            fg="#888888",
            anchor="w"
        )
        locations_label.pack(fill=tk.X, padx=10, pady=(0, 6))
        
        # Time info - compact
        if event.time_info:
            time_label = tk.Label(
                card,
                text=event.time_info,
                font=("Arial", 11, "bold"),
                bg="#2d2d2d",
                fg="#ffffff",
                anchor="w"
            )
            time_label.pack(fill=tk.X, padx=10, pady=(0, 4))
        
        # Countdown
        countdown_text = "ENDS IN" if event.status == "Active" else "STARTS IN"
        countdown_label = tk.Label(
            card,
            text=countdown_text,
            font=("Arial", 9),
            bg="#2d2d2d",
            fg="#888888",
            anchor="w"
        )
        countdown_label.pack(fill=tk.X, padx=10, pady=(2, 0))
        
        countdown_value = tk.Label(
            card,
            text=self.format_countdown(event.countdown_seconds),
            font=("Arial", 20, "bold"),
            bg="#2d2d2d",
            fg="#4a9eff",
            anchor="w"
        )
        countdown_value.pack(fill=tk.X, padx=10, pady=(1, 6))
        
        # Store reference for updates
        countdown_value.event = event
        
        # Upcoming windows - show first 2, more compact
        if event.upcoming_windows:
            windows_label = tk.Label(
                card,
                text="UPCOMING",
                font=("Arial", 8, "bold"),
                bg="#2d2d2d",
                fg="#888888",
                anchor="w"
            )
            windows_label.pack(fill=tk.X, padx=10, pady=(4, 2))
            
            for window in event.upcoming_windows[:2]:  # Show first 2
                # Truncate long window text
                window_text = window if len(window) <= 38 else window[:35] + "..."
                window_label = tk.Label(
                    card,
                    text=window_text,
                    font=("Arial", 8),
                    bg="#2d2d2d",
                    fg="#aaaaaa",
                    anchor="w"
                )
                window_label.pack(fill=tk.X, padx=10, pady=1)
        
        # Add small bottom padding
        tk.Label(card, bg="#2d2d2d").pack(pady=4)
    
    def update_countdowns(self):
        """Update all countdown timers"""
        if not self.running:
            return
            
        try:
            has_zero_countdown = False
            
            # Find all countdown labels and update them
            for widget in self.scrollable_frame.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and hasattr(child, 'event'):
                        event = child.event
                        if event.countdown_seconds > 0:
                            event.countdown_seconds -= 1
                            child.config(text=self.format_countdown(event.countdown_seconds))
                        
                        if event.countdown_seconds == 0:
                            has_zero_countdown = True
            
            # Only trigger refresh once when countdown hits 0, with a cooldown
            current_time = time.time()
            if has_zero_countdown and not self.refresh_triggered:
                if current_time - self.last_refresh_time > 60:  # 60 second cooldown
                    self.refresh_triggered = True
                    self.last_refresh_time = current_time
                    print("Event countdown reached 0, refreshing data...")
                    self.root.after(100, self.auto_refresh)
                    return
            
            # Schedule next update
            self.root.after(1000, self.update_countdowns)
            
        except Exception as e:
            print(f"Error updating countdowns: {e}")
            self.root.after(1000, self.update_countdowns)
    
    def auto_refresh(self):
        """Auto refresh after countdown expires"""
        self.fetch_and_display_events()
        self.refresh_triggered = False
    
    def on_closing(self):
        """Handle window closing"""
        self.running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    app = ArcTimersGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

