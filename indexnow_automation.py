#!/usr/bin/env python3
"""
TicketShield IndexNow Automation
Automatically submits all site URLs to IndexNow daily
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json

# Configuration
INDEXNOW_KEY = "0a2c34a96894d84f848a58ea92fb2985"
KEY_LOCATION = f"https://ticketshield.com/.well-known/{INDEXNOW_KEY}.txt"
SITE_URL = "https://ticketshield.com"
def fetch_all_urls():
    """Fetch all URLs from the sitemap"""
    print(f"[{datetime.now()}] Fetching sitemap from {SITEMAP_URL}...")
    
    try:
        response = requests.get(SITEMAP_URL, timeout=30)
        response.raise_for_status()
        
        # Parse the XML sitemap
        root = ET.fromstring(response.content)
        
        # Handle sitemap namespace
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        print(f"✓ Found {len(urls)} URLs in sitemap")
        return urls
        
    except Exception as e:
        print(f"✗ Error fetching sitemap: {e}")
        # Fallback to known important pages
        return [
            f"{SITE_URL}/",
            f"{SITE_URL}/about",
            f"{SITE_URL}/services",
            f"{SITE_URL}/traffic-tickets",
            f"{SITE_URL}/dui",
            f"{SITE_URL}/traffic-criminal",
            f"{SITE_URL}/faqs",
            f"{SITE_URL}/blog",
            f"{SITE_URL}/insights",
            f"{SITE_URL}/contact",
        ]

def submit_to_indexnow(urls):
    """Submit URLs to IndexNow"""
    if not urls:
        print("No URLs to submit")
        return False
    
    # IndexNow has a 10,000 URL limit per request
    batch_size = 10000
    total_batches = (len(urls) + batch_size - 1) // batch_size
    
    print(f"\n[{datetime.now()}] Submitting {len(urls)} URLs in {total_batches} batch(es)...")
    
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        payload = {
            "host": "ticketshield.com",
            "key": INDEXNOW_KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": batch
        }
        
        try:
            response = requests.post(
                "https://www.bing.com/indexnow",
                headers={"Content-Type": "application/json; charset=utf-8"},
                data=json.dumps(payload),
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✓ Batch {batch_num}/{total_batches}: Successfully submitted {len(batch)} URLs")
            elif response.status_code == 202:
                print(f"✓ Batch {batch_num}/{total_batches}: URLs accepted and queued for processing")
            else:
                print(f"✗ Batch {batch_num}/{total_batches}: HTTP {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"✗ Batch {batch_num}/{total_batches}: Error - {e}")
            continue
    
    return True

def generate_llms_txt(urls):
    """Generate llms.txt file for AI assistant discoverability"""
    print(f"\n[{datetime.now()}] Generating llms.txt file...")
    
    # Filter for important content
    blog_urls = [url for url in urls if '/blog/' in url or '/insights/' in url]
    
    # Build llms.txt content
    content = f"""# TicketShield - Traffic Ticket Defense

> {SITE_URL}

## About

TicketShield helps drivers fight traffic tickets across the United States. We connect drivers with experienced traffic attorneys who specialize in ticket defense, license protection, and traffic [...]  

## Key Services

- Traffic Ticket Defense
- DUI/DWI Defense  
- License Suspension Help
- Traffic Criminal Offenses
- Insurance Points Reduction

## Blog & Resources ({len(blog_urls)} articles)\n
"""
    
    # Add recent blog posts
    for url in blog_urls[:20]:  # Limit to 20 most recent
        content += f"- {url}\n"
    
    content += f"\n## Important Pages\n\n"
    important_pages = [
        f"{SITE_URL}/about",
        f"{SITE_URL}/services",
        f"{SITE_URL}/traffic-tickets",
        f"{SITE_URL}/dui",
        f"{SITE_URL}/faqs",
        f"{SITE_URL}/contact"
    ]
    
    for page in important_pages:
        if page in urls:
            content += f"- {page}\n"
    
    # Save to file
    try:
        with open('llms.txt', 'w') as f:
            f.write(content)
        print(f"✓ llms.txt generated with {len(blog_urls)} blog posts")
        return True
    except Exception as e:
        print(f"✗ Error generating llms.txt: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 60)
    print("TicketShield IndexNow Automation")
    print("=" * 60)
    print(f"Started: {datetime.now()}")
    print()
    
    # Fetch all URLs
    urls = fetch_all_urls()
    
    # Submit to IndexNow
    if urls:
        submit_to_indexnow(urls)
        generate_llms_txt(urls)
    
    print()
    print(f"Completed: {datetime.now()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
