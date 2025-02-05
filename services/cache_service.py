from datetime import datetime, timedelta
import json
import os
from typing import Dict, Any, Optional
import logging

class CacheService:
    def __init__(self, cache_dir: str = "cache", ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _get_cache_path(self, key: str) -> str:
        """Get file path for cache key"""
        safe_key = "".join(c for c in key if c.isalnum())
        return os.path.join(self.cache_dir, f"{safe_key}.json")

    def get(self, key: str) -> Optional[str]:
        """Get cached content if it exists and is not expired"""
        try:
            cache_path = self._get_cache_path(key)
            if not os.path.exists(cache_path):
                return None

            with open(cache_path, 'r') as f:
                cached_data = json.load(f)

            # Check if cache is expired
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - cached_time > self.ttl:
                os.remove(cache_path)  # Clean up expired cache
                return None

            return cached_data['content']

        except Exception as e:
            logging.error(f"Cache read error for {key}: {e}")
            return None

    def set(self, key: str, content: str):
        """Cache content with timestamp"""
        try:
            cache_data = {
                'content': content,
                'timestamp': datetime.now().isoformat(),
            }
            
            cache_path = self._get_cache_path(key)
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)

        except Exception as e:
            logging.error(f"Cache write error for {key}: {e}")

    def clear(self, key: str = None):
        """Clear specific cache entry or all cache"""
        try:
            if key:
                cache_path = self._get_cache_path(key)
                if os.path.exists(cache_path):
                    os.remove(cache_path)
            else:
                # Clear all cache files
                for cache_file in os.listdir(self.cache_dir):
                    os.remove(os.path.join(self.cache_dir, cache_file))

        except Exception as e:
            logging.error(f"Cache clear error: {e}")

    def cleanup_expired(self):
        """Remove all expired cache entries"""
        try:
            for cache_file in os.listdir(self.cache_dir):
                cache_path = os.path.join(self.cache_dir, cache_file)
                try:
                    with open(cache_path, 'r') as f:
                        cached_data = json.load(f)
                    
                    cached_time = datetime.fromisoformat(cached_data['timestamp'])
                    if datetime.now() - cached_time > self.ttl:
                        os.remove(cache_path)
                        
                except Exception as e:
                    logging.error(f"Error processing cache file {cache_file}: {e}")
                    os.remove(cache_path)  # Remove corrupted cache file

        except Exception as e:
            logging.error(f"Cache cleanup error: {e}") 