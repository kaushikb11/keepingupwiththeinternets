from operator import add
from typing import Annotated, Dict, List, TypedDict


class PostContent(TypedDict):
    title: str
    selftext: str
    url: str
    comments: List[Dict]
    extracted_urls: List[str]
    url_content: Dict[str, str]
    summary: str


class Section(TypedDict):
    title: str
    points: List[str]


class ProcessingState(TypedDict):
    subreddit: str
    posts: List[Dict]
    processed_posts: Annotated[List[PostContent], add]
    script_plan: str
    sections: List[Section]
    introduction: str
    dialogues: Annotated[List[Dict[str, str]], add]
    final_script: str
    audio_path: str
