"""
Web Tools - Search and data fetching with Tavily Integration
"""
from typing import Dict, Any, List, Optional
import requests
from utils.logger import logger
from config import settings

# Robustly try to import Tavily (support multiple package layouts)
import importlib

TAVILY_AVAILABLE = False
TavilySearchResults = None

_candidates = [
    'langchain_community.tools.tavily_search.TavilySearchResults',
    'langchain_tavily.TavilySearchResults',
    'langchain_tavily.client.TavilySearchResults',
    'langchain_tavily.tool.TavilySearchResults',
    'langchain_community.tools.tavily.TavilySearchResults'
]

for candidate in _candidates:
    module_name, _, attr = candidate.rpartition('.')
    try:
        mod = importlib.import_module(module_name)
        if hasattr(mod, attr):
            TavilySearchResults = getattr(mod, attr)
            TAVILY_AVAILABLE = True
            logger.info(f"✅ Found Tavily import: {candidate}")
            break
    except Exception:
        continue

if not TAVILY_AVAILABLE:
    logger.warning("⚠️  Tavily import not found. Ensure langchain-tavily is installed and the package layout matches expectations.")


class TavilySearchTool:
    """Tavily Web Search Tool - Optimized for AI Agents"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Tavily search tool"""
        self.api_key = api_key or getattr(settings, 'tavily_api_key', '')
        
        if not self.api_key:
            logger.warning("⚠️  Tavily API key not found in settings")
            self.available = False
        else:
            # Try different constructor signatures used across versions
            initialized = False
            for kwargs in ("api_key", "tavily_api_key", "key"): 
                try:
                    # some wrappers accept api_key, others tavily_api_key
                    self.tool = TavilySearchResults(**{kwargs: self.api_key, 'max_results': 5})
                    self.available = TAVILY_AVAILABLE
                    logger.info(f"✅ Tavily search tool initialized (param='{kwargs}')")
                    initialized = True
                    break
                except TypeError:
                    continue
                except Exception as e:
                    logger.error(f"❌ Failed to initialize Tavily with param '{kwargs}': {e}")
            if not initialized:
                logger.error("❌ Failed to initialize Tavily with any known constructor signature")
                self.available = False
    
    def search(self, query: str, max_results: int = 5, 
              include_answer: bool = True) -> Dict[str, Any]:
        """
        Search using Tavily API
        
        Args:
            query: Search query
            max_results: Maximum results to return
            include_answer: Include Tavily's answer in response
        
        Returns:
            Dict with search results
        """
        if not self.available:
            logger.error("❌ Tavily search tool not available")
            return {
                "status": "error",
                "error": "Tavily tool not initialized",
                "results": []
            }
        
        logger.info(f"🔍 Searching with Tavily: {query}")
        
        try:
            # Use Tavily's search
            results = self.tool.invoke(query)
            
            # Parse results
            parsed_results = self._parse_tavily_results(results)
            
            return {
                "status": "success",
                "query": query,
                "results_count": len(parsed_results),
                "results": parsed_results,
                "raw_response": results
            }
        
        except Exception as e:
            logger.error(f"❌ Tavily search error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "results": []
            }
    
    def search_with_context(self, query: str, context: str = "") -> Dict[str, Any]:
        """
        Search with contextual information
        
        Args:
            query: Search query
            context: Additional context for the search
        
        Returns:
            Search results with context
        """
        full_query = f"{context}\n{query}" if context else query
        return self.search(full_query)
    
    def _parse_tavily_results(self, results: Any) -> List[Dict[str, Any]]:
        """Parse Tavily results into structured format"""
        parsed = []
        
        # Handle string results (Tavily returns formatted string)
        if isinstance(results, str):
            # Parse the formatted string response
            lines = results.split('\n')
            for line in lines:
                if line.strip():
                    parsed.append({
                        "content": line.strip(),
                        "type": "result"
                    })
        
        # Handle dict results
        elif isinstance(results, dict):
            if 'results' in results:
                for result in results.get('results', []):
                    parsed.append({
                        "title": result.get('title', ''),
                        "url": result.get('url', ''),
                        "content": result.get('content', ''),
                        "score": result.get('score', 0)
                    })
            
            if 'answer' in results:
                parsed.insert(0, {
                    "content": results['answer'],
                    "type": "answer"
                })
        
        # Handle list results
        elif isinstance(results, list):
            for item in results:
                if isinstance(item, dict):
                    parsed.append(item)
                else:
                    parsed.append({"content": str(item)})
        
        return parsed


class DataFetchTool:
    """Data fetching tool for APIs and endpoints"""
    
    @staticmethod
    def fetch(url: str, params: Dict[str, Any] = None, 
             headers: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Fetch data from API endpoint
        
        Args:
            url: API endpoint URL
            params: Query parameters
            headers: HTTP headers
        
        Returns:
            API response data
        """
        logger.info(f"📊 Fetching data from: {url}")
        
        try:
            response = requests.get(
                url,
                params=params or {},
                headers=headers or {},
                timeout=10
            )
            response.raise_for_status()
            
            return {
                "status": "success",
                "data": response.json() if response.text else {},
                "status_code": response.status_code,
                "url": url
            }
        
        except requests.exceptions.Timeout:
            logger.error(f"❌ Request timeout: {url}")
            return {
                "status": "error",
                "error": "Request timeout",
                "error_type": "TimeoutError",
                "url": url
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__,
                "url": url
            }
    
    @staticmethod
    def post_data(url: str, data: Dict[str, Any] = None,
                 headers: Dict[str, str] = None) -> Dict[str, Any]:
        """
        POST data to API endpoint
        
        Args:
            url: API endpoint URL
            data: Data to POST
            headers: HTTP headers
        
        Returns:
            API response
        """
        logger.info(f"📤 POSTing data to: {url}")
        
        try:
            response = requests.post(
                url,
                json=data or {},
                headers=headers or {"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            
            return {
                "status": "success",
                "data": response.json() if response.text else {},
                "status_code": response.status_code
            }
        
        except Exception as e:
            logger.error(f"❌ POST error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__
            }


class WebScraperTool:
    """Web scraping tool"""
    
    @staticmethod
    def scrape(url: str, timeout: int = 10) -> Dict[str, Any]:
        """
        Scrape webpage content
        
        Args:
            url: Website URL
            timeout: Request timeout
        
        Returns:
            Scraped content
        """
        logger.info(f"🕷️  Scraping: {url}")
        
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            # Extract title from HTML
            title = "Scraped Content"
            if "<title>" in response.text:
                start = response.text.find("<title>") + 7
                end = response.text.find("</title>")
                title = response.text[start:end]
            
            return {
                "status": "success",
                "url": url,
                "title": title,
                "content_length": len(response.text),
                "content_preview": response.text[:500],
                "headers": dict(response.headers)
            }
        
        except Exception as e:
            logger.error(f"❌ Scraping error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "url": url
            }


# Create tool instances
tavily_search = TavilySearchTool()
data_fetch = DataFetchTool()
web_scraper = WebScraperTool()