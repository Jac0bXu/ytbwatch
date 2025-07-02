# YouTube Monitor

A Python script that monitors YouTube channels for new videos and downloads them automatically.

## Setup

### Prerequisites

- Python 3.7+
- YouTube Data API v3 key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ytbwatch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create configuration file:
```bash
cp config.example.yaml config.yaml
```

4. Edit `config.yaml` and add your credentials:
   - Add your YouTube API key
   - Configure the channels you want to monitor

### Configuration

The `config.yaml` file should contain:

```yaml
# YouTube API Configuration
youtube_api_key: "YOUR_YOUTUBE_API_KEY_HERE"

# Check interval in minutes
check_interval_minutes: 60

# YouTube channels to monitor
youtube_channels:
  "CHANNEL_ID_1":
    name: "Channel Name 1"
  "CHANNEL_ID_2": 
    name: "Channel Name 2"
```

### Getting YouTube API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API Key)
5. Copy the API key to your `config.yaml`

### Getting Channel IDs

To find a YouTube channel ID:
1. Go to the channel's page
2. Look at the URL - it will contain the channel ID
3. Or use online tools to extract channel ID from channel name/URL

## Usage

Run the monitor:
```bash
python youtube_monitor.py
```

The script will:
- Check configured channels for new videos
- Download new videos automatically
- Save metadata for each video
- Run continuously with the configured interval

## File Structure

- `youtube_monitor.py` - Main monitoring script
- `config.yaml` - Configuration file (not tracked in git)
- `metadata/` - Directory containing video metadata files
- `ytb_list.py` - YouTube API and download functions

## Security Notes

- Never commit `config.yaml` to git (it's in .gitignore)
- Keep your API key secure and don't share it
- Use environment variables for sensitive data in production

## License

[Your chosen license]