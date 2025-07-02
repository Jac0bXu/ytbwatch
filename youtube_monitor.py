"""
YouTube Channel Monitor

This script monitors YouTube channels for new videos and downloads them automatically.
Configuration (including API keys) should be stored in config.yaml - see config.example.yaml.

Security Note: Never commit config.yaml to version control as it contains sensitive API keys.
"""

import asyncio
import time
import yaml
import os
import ytb_list

# Get the parent directory path
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METADATA_DIR = os.path.join(PARENT_DIR, "metadata")
os.makedirs(METADATA_DIR, exist_ok=True)

def save_video_metadata(video_id, snippet, video_url):
    """Save essential video metadata to a YAML file."""
    metadata = {
        'video_id': video_id,
        'title': snippet.get('title', ''),
        'description': snippet.get('description', ''),
        'channel_id': snippet.get('channelId', ''),
        'channel_title': snippet.get('channelTitle', ''),
        'published_at': snippet.get('publishedAt', ''),
        'video_url': video_url,
        'thumbnail_url': snippet.get('thumbnails', {}).get('maxres', {}).get('url', '') or snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
        'tags': snippet.get('tags', []),
        'category_id': snippet.get('categoryId', ''),
        'duration': snippet.get('duration', ''),
        'view_count': snippet.get('viewCount', ''),
        'like_count': snippet.get('likeCount', ''),
        'comment_count': snippet.get('commentCount', ''),
        'live_broadcast_content': snippet.get('liveBroadcastContent', ''),
        'privacy_status': snippet.get('privacyStatus', ''),
        'made_for_kids': snippet.get('madeForKids', False),
        'downloaded': True  # Mark as downloaded
    }
    
    metadata_file = os.path.join(METADATA_DIR, f"{video_id}.yaml")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"📄 Metadata saved to: {metadata_file}")

def get_video_status(video_id):
    """Get the status of a video from its metadata file."""
    metadata_file = os.path.join(METADATA_DIR, f"{video_id}.yaml")
    if not os.path.exists(metadata_file):
        return None
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)
    
    return {
        'downloaded': metadata.get('downloaded', False)
    }

def update_video_status(video_id, **status_updates):
    """Update the status of a video in its metadata file."""
    metadata_file = os.path.join(METADATA_DIR, f"{video_id}.yaml")
    if not os.path.exists(metadata_file):
        print(f"⚠️ Metadata file not found for video {video_id}")
        return
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)
    
    # Update the metadata with new status
    metadata.update(status_updates)
    
    with open(metadata_file, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"📄 Updated status for video {video_id}: {status_updates}")

def load_downloaded_videos():
    """Load the set of already downloaded video IDs from metadata files."""
    downloaded_videos = set()
    
    if not os.path.exists(METADATA_DIR):
        return downloaded_videos
    
    for filename in os.listdir(METADATA_DIR):
        if filename.endswith('.yaml'):
            video_id = filename[:-5]  # Remove .yaml extension
            status = get_video_status(video_id)
            if status and status['downloaded']:
                downloaded_videos.add(video_id)
    
    return downloaded_videos

def save_downloaded_video(video_id):
    """Mark a video as downloaded in its metadata (deprecated - kept for compatibility)."""
    # This function is now handled by save_video_metadata, but kept for compatibility
    pass

async def monitor_channels():
    """Monitor YouTube channels for new videos and download them."""
    # Load configuration from config.yaml (contains sensitive API keys)
    # Make sure config.yaml is in .gitignore and never committed to version control
    config = ytb_list.load_config()
    downloaded_videos = load_downloaded_videos()  # Now loads from metadata files
    
    for channel_id, channel_config in config['youtube_channels'].items():
        print(f"\nChecking channel: {channel_id}")
        try:
            latest_videos = ytb_list.get_latest_youtube_videos(config['youtube_api_key'], channel_id)
            for item in latest_videos:
                video_id = item['id']['videoId']
                snippet = item['snippet']
                video_title = snippet['title']
                
                if video_id not in downloaded_videos:
                    print(f"✨ New video found: {video_title}")
                    video_file, thumb_file, video_url = ytb_list.download_media(video_id, snippet)
                    
                    # Save metadata to YAML file (includes downloaded=True status)
                    save_video_metadata(video_id, snippet, video_url)
                    
                    print(f"✅ Downloaded: {video_title}")
                else:
                    print(f"Video '{video_title}' already processed. Skipping.")
        except Exception as e:
            print(f"An unexpected error occurred while processing channel {channel_id}: {e}")

async def main():
    """Main monitoring loop."""
    config = ytb_list.load_config()
    interval_seconds = config.get("check_interval_minutes", 60) * 60
    
    print("🎬 YouTube Monitor Started")
    print(f"📅 Checking every {interval_seconds / 60} minutes")
    
    while True:
        await monitor_channels()
        print(f"\n--- YouTube check complete. Waiting for {interval_seconds / 60} minutes before next check. ---")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n📺 YouTube Monitor stopped by user.")