import json
from atlassian import Confluence
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get("CONFLUENCE_API_KEY")

# Confluence Cloud credentials
CONFLUENCE_URL = "https://wzha8255.atlassian.net"
EMAIL = "zhangwen08@gmail.com"

def get_confluence_client():
    """Create and return a Confluence client."""
    confluence = Confluence(
        url=CONFLUENCE_URL,
        username=EMAIL,
        password=API_TOKEN
    )
    return confluence


def fetch_pages(space_key: str = "~71202036c2aa3a2bad44639186484e3a5a1d54", limit: int = 50):
    """Fetch pages from a Confluence space."""
    confluence = get_confluence_client()
    
    pages = []
    
    try:
        # Get all pages in the space
        cql = f'space = "{space_key}" AND type = page'
        ## CQL = Confluence Query Language, it's like SQL but for Confluence, e.g. space = "XYZ" and type = page
        results = confluence.cql(cql, limit=limit)
        
        # loop through results, 
        for result in results.get("results", []):
            
            page_id = result.get("content", {}).get("id") ## using get() instead of referring to the key directly which will crash if key doesn't exit. get() return None if the key is missing.
            if not page_id:
                page_id = result.get("id")
            
            # Get full page content. The second api call. The first api call get page IDs. The second api call to get the actual content (HTML)
            full_page = confluence.get_page_by_id(
                page_id,
                expand="body.storage"
            )
            
            pages.append({
                "id": page_id,
                "title": full_page.get("title", ""),
                "content": (
                    full_page.get("body", {})
                    .get("storage", {})
                    .get("value", "")
                )
            })
    
    except Exception as e:
        print(f"Error fetching pages: {e}")
        raise
    
    return pages


if __name__ == "__main__":
    pages = fetch_pages(space_key="~71202036c2aa3a2bad44639186484e3a5a1d54")
    print(json.dumps(pages, indent=2))
