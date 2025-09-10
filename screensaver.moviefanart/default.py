# default.py
import xbmc
import xbmcaddon
import xbmcgui
import json
import random
import time

addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')

class Settings:
    """Centralized settings management with proper defaults."""
    
    def __init__(self, addon):
        self.interval = self._get_int_setting(addon, "movie_interval", 10)
        self.show_title = self._get_bool_setting(addon, "show_title", True)
        self.font_size = self._get_font_setting(addon, "font_size", "FontM")
        self.show_year = self._get_bool_setting(addon, "show_year", True)
        self.fade_delay = self._get_int_setting(addon, "poster_delay", 3)
        self.show_shadow = self._get_bool_setting(addon, "show_shadow", True)
        
    def _get_int_setting(self, addon, setting_name, default):
        """Get integer setting with fallback to default."""
        try:
            return int(addon.getSetting(setting_name)) or default
        except (ValueError, TypeError):
            return default

    def _get_bool_setting(self, addon, setting_name, default_value):
        """Get boolean setting with fallback to default."""
        try:
            setting_value = addon.getSetting(setting_name)
            if setting_value.lower() == "true":
                return True
            elif setting_value.lower() == "false":
                return False
            else:
                return default_value
        except (AttributeError, TypeError):
            return default_value

    def _get_font_setting(self, addon, setting_name, default_value):
        """Get font setting by converting the returned index to a font name."""
        try:
            setting_value = addon.getSetting(setting_name)
            
            # First try as direct string value
            font_options = ["FontS", "FontM", "FontH"]
            if setting_value in font_options:
                return setting_value
            
            # Try as index
            index = int(setting_value)
            if 0 <= index < len(font_options):
                return font_options[index]
                
        except (ValueError, TypeError) as e:
            xbmc.log(f"{addon_name}: Could not read font setting '{setting_name}': {e}, using default.", xbmc.LOGWARNING)
            
        return default_value

class MovieLibrary:
    """Handles movie data retrieval from Kodi."""
    
    @staticmethod
    def get_movies_with_artwork():
        """Get all movies that have both fanart and poster artwork."""
        command = {
            "jsonrpc": "2.0", 
            "method": "VideoLibrary.GetMovies", 
            "params": {"properties": ["title", "art", "year"]}, 
            "id": 1
        }
        
        try:
            result = json.loads(xbmc.executeJSONRPC(json.dumps(command)))
            if 'result' not in result or 'movies' not in result['result']:
                return []
                
            movies = result['result']['movies']
            return [
                movie for movie in movies 
                if (movie.get('art', {}).get('fanart') and 
                    movie.get('art', {}).get('poster'))
            ]
        except (json.JSONDecodeError, KeyError) as e:
            xbmc.log(f"{addon_name}: Error getting movies: {e}", xbmc.LOGERROR)
            return []

class ScreenLayout:
    """Calculates screen layout dimensions and positions."""
    
    def __init__(self, window_width, window_height):
        self.width = window_width
        self.height = window_height
        
    def get_poster_dimensions(self):
        """Calculate poster size and position."""
        width = int(self.width * 0.25)
        height = int(width * 1.5)  # 2:3 aspect ratio
        x = int(self.width * 0.05)
        y = int(self.height * 0.05)
        return x, y, width, height
        
    def get_title_position(self):
        """Calculate title position."""
        y_position = int(self.height * 0.8)  # 80% from top
        
        return (
            int(self.width * 0.1),      # x: 10% from left
            y_position,                 # y: 80% from top
            int(self.width * 0.8),      # width: 80% of screen
            int(self.height * 0.2)      # height: 20% of screen
        )

class MovieFanartScreensaver(xbmcgui.Window):
    SHADOW_OFFSET = 3
    SHADOW_COLOR = '0x88000000'
    TEXT_COLOR = '0xFFFFFFFF'
    
    def __init__(self):
        super().__init__()
        self.settings = Settings(addon)
        self.movies = []
        self.monitor = xbmc.Monitor()
        self.closed = False
        
        self.width = self.getWidth()
        self.height = self.getHeight()
        self.layout = ScreenLayout(self.width, self.height)
        
    def initialize(self):
        """Load movies and create UI controls."""
        self.movies = MovieLibrary.get_movies_with_artwork()
        if not self.movies:
            return False
            
        self._create_controls()
        return True
        
    def _create_controls(self):
        """Create and add all UI controls using settings."""
        # Background
        self.background = xbmcgui.ControlImage(
            0, 0, self.width, self.height, '', 
            colorDiffuse='0xFF000000'
        )
        
        # Fanart (fills entire screen)
        self.fanart_image = xbmcgui.ControlImage(0, 0, self.width, self.height, '')
        
        # Poster
        poster_x, poster_y, poster_w, poster_h = self.layout.get_poster_dimensions()
        self.poster_image = xbmcgui.ControlImage(
            poster_x, poster_y, poster_w, poster_h, '', aspectRatio=2
        )
        
        # Title labels using settings
        title_x, title_y, title_w, title_h = self.layout.get_title_position()
        title_font = self.settings.font_size
        
        # Create shadow label (only if enabled)
        if self.settings.show_shadow:
            self.title_shadow = xbmcgui.ControlLabel(
                title_x + self.SHADOW_OFFSET, 
                title_y + self.SHADOW_OFFSET,
                title_w, title_h, '', title_font, self.SHADOW_COLOR
            )
        else:
            self.title_shadow = None
        
        # Create main title label
        self.title_label = xbmcgui.ControlLabel(
            title_x, title_y, title_w, title_h, '', 
            title_font, self.TEXT_COLOR
        )
           
        # Add controls in proper order
        controls_to_add = [self.background, self.fanart_image, self.poster_image]
        
        if self.title_shadow:
            controls_to_add.append(self.title_shadow)
            
        controls_to_add.append(self.title_label)
        
        for control in controls_to_add:
            self.addControl(control)
            
        # Initially hide poster
        self.poster_image.setVisible(False)
        
    def display_random_movie(self):
        """Display a random movie with fanart, poster, and title."""
        if not self.movies or self.closed:
            return
            
        movie = random.choice(self.movies)
        
        # Set fanart immediately with error handling
        try:
            fanart_path = movie['art']['fanart']
            self.fanart_image.setImage(fanart_path, useCache=False)
        except (KeyError, TypeError) as e:
            xbmc.log(f"{addon_name}: Error setting fanart: {e}", xbmc.LOGWARNING)
            
        # Prepare poster (hidden initially) with error handling
        try:
            poster_path = movie['art']['poster'] 
            self.poster_image.setImage(poster_path, useCache=False)
            self.poster_image.setVisible(False)
        except (KeyError, TypeError) as e:
            xbmc.log(f"{addon_name}: Error setting poster: {e}", xbmc.LOGWARNING)
        
        # Set title
        self._update_title(movie)
        
        # Wait with delayed poster reveal
        self._wait_with_poster_reveal()
        
    def _update_title(self, movie):
        """Update title labels based on settings."""
        if not self.settings.show_title:
            if self.title_shadow:
                self.title_shadow.setLabel('')
            self.title_label.setLabel('')
            return
            
        title = movie['title']
        if self.settings.show_year and movie.get('year', 0) > 0:
            title = f"{title} ({movie['year']})"
            
        if self.title_shadow:
            self.title_shadow.setLabel(title)
        self.title_label.setLabel(title)
        
    def _wait_with_poster_reveal(self):
        """Wait for interval duration, showing poster after fade delay."""
        start_time = time.time()
        poster_shown = False
        
        while (time.time() - start_time < self.settings.interval and 
               not self.monitor.abortRequested() and not self.closed):
            
            # Show poster after fade delay
            if (not poster_shown and 
                time.time() - start_time >= self.settings.fade_delay):
                self.poster_image.setVisible(True)
                poster_shown = True
                
            xbmc.sleep(100)
            
    def run_slideshow(self):
        """Main slideshow loop."""
        while not self.monitor.abortRequested() and not self.closed:
            self.display_random_movie()
            
    def onAction(self, action):
        """Handle user input - close screensaver on any action."""
        self.closed = True
        self.close()

def run():
    """Main entry point."""
    screensaver = MovieFanartScreensaver()
    
    try:
        if screensaver.initialize():
            screensaver.show()
            screensaver.run_slideshow()
    finally:
        screensaver.close()
        del screensaver

if __name__ == '__main__':
    run()