from langchain.utilities import SerpAPIWrapper
from tavily import TavilyClient
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from typing import List, Optional
import asyncio

tavily_client = TavilyClient(api_key="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")

class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__(serpapi_api_key="1b4378b230dc7a198363f0be289d5d342e9924a303c18b35c49463cea71bb0ee")

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
            "answer_box" in res.keys()
            and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
            "sports_results" in res.keys()
            and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
            "knowledge_graph" in res.keys()
            and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["link"]

        else:
            toret = "No good search result found"
        return toret

def get_profile_url(name: str) -> str:
    """Searches for an individual's LinkedIn profile URL using Tavily."""
    query = f"{name} LinkedIn"
    response = tavily_client.search(query=query, max_results=3)
    if response and response['results']:
        return response['results'][0]['url']
    else:
        return "LinkedIn profile not found."
    
def get_youtube_interview_urls(name: str, max_results: int = 3) -> List[str]:
    """
    Search for multiple YouTube interview URLs related to a given person's name.
    Returns a list of unique YouTube URLs. If none found, returns an empty list.
    """
    query = f"{name} youtube interview"
    response = tavily_client.search(query=query, max_results=max_results)
    print(response)
    if not response or "results" not in response or not response["results"]:
        return []  # No results from Tavily or error in response

    seen_urls = set()
    interview_urls = []

    for item in response["results"]:
        url = item.get("url", "")
        title = item.get("title", "").lower()
        description = item.get("content", "").lower()  # or whatever field Tavily uses

        # Check if it's a YouTube link
        if "youtube.com" in url or "youtu.be" in url:
            # Optionally filter to ensure it looks like an interview for this person
            # For instance, check if "interview" is in the title or snippet
            # and the person's name is likely in the content.
            
            # You could also check if person's name is in the title:
            if name.lower() in title or name.lower() in description:
                if url not in seen_urls:
                    seen_urls.add(url)
                    interview_urls.append(url)

    return interview_urls

async def get_transcript(video_id, languages=['it','en']):
    """
    Fetch the transcript for a given YouTube video ID.
    By default, tries English transcripts first.
    """
    try:
        # This returns a list of dictionaries, where each dict contains
        # {'text': "...", 'start': ..., 'duration': ...}
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)

        # Join all the "text" entries together into a single string
        transcript_text = "\n".join([entry['text'] for entry in transcript_list])
        return transcript_text

    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None


def extract_youtube_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a given URL if possible.
    Returns the ID as a string, or None if it can't be parsed.
    """
    try:
        parsed_url = urlparse(url)

        # Example: https://www.youtube.com/watch?v=VIDEO_ID
        if "youtube.com" in parsed_url.netloc:
            # Check if it's a standard watch URL
            if parsed_url.path == "/watch":
                # The video ID should be in the 'v' query parameter
                query_params = parse_qs(parsed_url.query)
                if "v" in query_params:
                    return query_params["v"][0]

            # Example: https://www.youtube.com/embed/VIDEO_ID
            # The path is "/embed/VIDEO_ID"
            if parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]

        # Example: https://youtu.be/VIDEO_ID
        if "youtu.be" in parsed_url.netloc:
            # The path will be "/VIDEO_ID"
            return parsed_url.path.strip("/")

        # If the link structure doesn’t match known patterns, return None
        return None

    except Exception:
        return None