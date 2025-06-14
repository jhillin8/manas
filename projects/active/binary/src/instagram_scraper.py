#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime
import re
from typing import Dict, List, Any

class InstagramScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def scrape_posts(self, username: str, count: int = 100) -> List[Dict[str, Any]]:
        """Scrape Instagram posts using web scraping approach"""
        posts = []
        
        try:
            # Get user page
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url)
            
            if response.status_code != 200:
                print(f"Failed to access Instagram profile: {response.status_code}")
                return posts
            
            # Extract shared data from page
            content = response.text
            shared_data_match = re.search(r'window\._sharedData = ({.*?});', content)
            
            if not shared_data_match:
                print("Could not find shared data in page")
                return posts
            
            shared_data = json.loads(shared_data_match.group(1))
            
            # Navigate to user posts
            user_media = shared_data.get('entry_data', {}).get('ProfilePage', [{}])[0]
            user_data = user_media.get('graphql', {}).get('user', {})
            
            if not user_data:
                print("Could not extract user data")
                return posts
            
            # Extract posts from edge_owner_to_timeline_media
            timeline_media = user_data.get('edge_owner_to_timeline_media', {})
            edges = timeline_media.get('edges', [])
            
            for edge in edges[:count]:
                node = edge.get('node', {})
                
                post_data = {
                    'id': node.get('id'),
                    'shortcode': node.get('shortcode'),
                    'timestamp': node.get('taken_at_timestamp'),
                    'caption': '',
                    'likes': node.get('edge_liked_by', {}).get('count', 0),
                    'comments': node.get('edge_media_to_comment', {}).get('count', 0),
                    'is_video': node.get('is_video', False),
                    'display_url': node.get('display_url'),
                    'accessibility_caption': node.get('accessibility_caption', ''),
                    'hashtags': [],
                    'mentions': []
                }
                
                # Extract caption text
                caption_edges = node.get('edge_media_to_caption', {}).get('edges', [])
                if caption_edges:
                    caption_text = caption_edges[0].get('node', {}).get('text', '')
                    post_data['caption'] = caption_text
                    
                    # Extract hashtags and mentions
                    post_data['hashtags'] = re.findall(r'#(\w+)', caption_text)
                    post_data['mentions'] = re.findall(r'@(\w+)', caption_text)
                
                posts.append(post_data)
                
            print(f"Successfully scraped {len(posts)} posts from @{username}")
            return posts
            
        except Exception as e:
            print(f"Error scraping posts: {str(e)}")
            return posts
    
    def analyze_content_themes(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content themes from scraped posts"""
        
        fashion_keywords = ['outfit', 'style', 'fashion', 'dress', 'shoes', 'bag', 'jewelry', 'designer', 'trend', 'look', 'ootd']
        wellness_keywords = ['workout', 'fitness', 'health', 'wellness', 'meditation', 'yoga', 'skincare', 'beauty', 'selfcare']
        lifestyle_keywords = ['travel', 'vacation', 'restaurant', 'food', 'coffee', 'home', 'decor', 'lifestyle', 'experience']
        
        theme_counts = {
            'fashion': 0,
            'wellness': 0,
            'lifestyle': 0,
            'other': 0
        }
        
        engagement_by_theme = {
            'fashion': [],
            'wellness': [],
            'lifestyle': [],
            'other': []
        }
        
        for post in posts:
            caption = (post.get('caption', '') + ' ' + post.get('accessibility_caption', '')).lower()
            hashtags = ' '.join(post.get('hashtags', [])).lower()
            full_text = caption + ' ' + hashtags
            
            likes = post.get('likes', 0)
            comments = post.get('comments', 0)
            engagement = likes + (comments * 10)  # Weight comments more heavily
            
            # Categorize post
            if any(keyword in full_text for keyword in fashion_keywords):
                theme_counts['fashion'] += 1
                engagement_by_theme['fashion'].append(engagement)
            elif any(keyword in full_text for keyword in wellness_keywords):
                theme_counts['wellness'] += 1
                engagement_by_theme['wellness'].append(engagement)
            elif any(keyword in full_text for keyword in lifestyle_keywords):
                theme_counts['lifestyle'] += 1
                engagement_by_theme['lifestyle'].append(engagement)
            else:
                theme_counts['other'] += 1
                engagement_by_theme['other'].append(engagement)
        
        # Calculate average engagement by theme
        avg_engagement = {}
        for theme, engagements in engagement_by_theme.items():
            if engagements:
                avg_engagement[theme] = sum(engagements) / len(engagements)
            else:
                avg_engagement[theme] = 0
        
        return {
            'theme_distribution': theme_counts,
            'average_engagement_by_theme': avg_engagement,
            'total_posts_analyzed': len(posts)
        }

def main():
    scraper = InstagramScraper()
    
    print("🔍 Scraping Brooks Nader's Instagram posts...")
    posts = scraper.scrape_posts('brooksnader', 100)
    
    if not posts:
        print("❌ No posts scraped. Trying alternative approach...")
        return
    
    print(f"✅ Scraped {len(posts)} posts")
    
    # Analyze themes
    print("📊 Analyzing content themes...")
    analysis = scraper.analyze_content_themes(posts)
    
    # Save results
    results = {
        'scraped_at': datetime.now().isoformat(),
        'username': 'brooksnader',
        'posts': posts,
        'analysis': analysis
    }
    
    with open('/Users/josephhillin/manas/projects/active/binary/brooks_nader_data.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("📈 Analysis Results:")
    print(f"Total posts: {analysis['total_posts_analyzed']}")
    print("\nTheme Distribution:")
    for theme, count in analysis['theme_distribution'].items():
        percentage = (count / analysis['total_posts_analyzed']) * 100
        print(f"  {theme.capitalize()}: {count} posts ({percentage:.1f}%)")
    
    print("\nAverage Engagement by Theme:")
    for theme, engagement in analysis['average_engagement_by_theme'].items():
        print(f"  {theme.capitalize()}: {engagement:.0f}")
    
    print(f"\n💾 Data saved to brooks_nader_data.json")

if __name__ == "__main__":
    main()