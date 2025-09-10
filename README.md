# Kodi Movie Fanart Screensaver

A Kodi screensaver addon that displays your movie library's beautiful fanart with poster overlays and customizable titles using custom font definitions (SEE BELOW).

## Features

- **Full-screen fanart display** - Shows high-quality fanart from your movie collection as the background
- **Delayed poster overlay** - Movie posters fade in after a configurable delay for a cinematic effect
- **Customizable titles** - Display movie titles and years with multiple font sizes and shadow effects
- **Smart filtering** - Only displays movies that have both fanart and poster artwork
- **Responsive layout** - Automatically adapts to different screen resolutions
- **User interaction** - Press any key or button to exit the screensaver

## How It Works

The screensaver randomly selects movies from your Kodi library that have both fanart and poster artwork available. It displays the fanart as a full-screen background, then after a configurable delay, overlays the movie poster in the bottom-left corner along with the movie title and year (if enabled).

## Configuration Options

The screensaver includes several customizable settings accessible through Kodi's addon settings:

- **Font Size** (`font_size`) - Choose between Small (FontS), Medium (FontM), or Large (FontH) title text
- **Poster Delay** (`poster_delay`) - Delay in seconds before the poster overlay appears (0-10 seconds, default: 3)
- **Movie Interval** (`movie_interval`) - How long to display each movie before switching (5-60 seconds, default: 10)
- **Show Shadow** (`show_shadow`) - Enable/disable drop shadow effect on titles (default: enabled)
- **Show Title** (`show_title`) - Enable/disable movie title display (default: enabled)  
- **Show Year** (`show_year`) - Enable/disable movie year display alongside title (default: enabled)

## Installation Requirements

### Font Configuration

**IMPORTANT:** This screensaver requires custom font definitions to display titles properly. You must add the following font entries to your skin's `Font.xml` file
Your custom font must be located at `<kodi_userdata>/media/fonts/<font_file>`.  The following uses `helvetica.ttf` as an EXAMPLE only, replace with your font's filename:

```xml
<font>
    <name>FontH</name>
    <filename>helvetica.ttf</filename>
    <size>127</size>
    <style>normal</style>	
</font>			
<font>
    <name>FontS</name>
    <filename>helvetica.ttf</filename>
    <size>24</size>
    <style>bold</style>	
</font>		
<font>
    <name>FontM</name>
    <filename>helvetica.ttf</filename>
    <size>72</size>
    <style>bold</style>	
</font>
```

### Locating Font.xml

The `Font.xml` file is typically located in:
- **Default skin:** `<kodi_installation>/addons/skin.estuary/xml/Font.xml`
- **Custom skins:** `<kodi_installation>/addons/<skin_name>/xml/Font.xml`
- **User data:** `<kodi_userdata>/addons/<skin_name>/xml/Font.xml`

Add the font definitions within the existing `<fonts>` section of the file.

### Movie Library Requirements

- Your Kodi movie library must be properly scraped with artwork
- Movies need both **fanart** and **poster** images to appear in the screensaver
- Use a metadata scraper like The Movie Database (TMDB) to ensure complete artwork

## Technical Details

- **Language:** Python 3
- **Kodi API:** Uses JSON-RPC for movie library access
- **UI Framework:** xbmcgui Window and Control classes
- **Aspect Ratios:** Maintains proper poster aspect ratio (2:3)
- **Performance:** Efficient random selection and memory management

## Layout

- **Fanart:** Full-screen background
- **Poster:** Bottom-left corner (25% screen width, 2:3 aspect ratio)
- **Title:** Bottom area (80% from top, 80% screen width)
- **Positioning:** Responsive to different screen resolutions

## Troubleshooting

### Titles Not Displaying
- **Check font file location:** Ensure your custom font file is located at `<kodi_userdata>/media/fonts/<font_file>`
- **Verify font definitions:** Confirm the font definitions are added to your skin's `Font.xml`
- **Match filenames:** Ensure the font filename in Font.xml matches the actual font file name
- **Restart Kodi:** Restart Kodi after modifying `Font.xml` 
- **Alternative:** Consider using built-in fonts like `"font_MainMenu"` by modifying the screensaver code

### No Movies Showing
- Ensure your movie library is properly scraped
- Verify movies have both fanart and poster artwork
- Check Kodi logs for any error messages

### Screensaver Not Activating
- Set the screensaver in Kodi Settings → Interface → Screensaver
- Adjust screensaver delay time as needed
- Ensure the addon is properly installed and enabled

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this screensaver addon.

## License

This project is open source. Please check the license file for specific terms and conditions.
