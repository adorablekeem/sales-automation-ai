import sys
import os

import asyncio
from typing import cast, Any, Literal
import json

from tools.tools import get_transcript
from tools.tools import extract_youtube_id
from tools.tools import get_youtube_interview_urls
from tools.proxycurl.linkedin import scrape_linkedin_profile
from linkedin_lookup_agent import lookup as linkedin_lookup_agent
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from tavily import AsyncTavilyClient
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel, Field

from agent.configuration import Configuration
from agent.state import InputState, OutputState, OverallState
from agent.utils import deduplicate_and_format_sources, format_all_notes
from agent.prompts import (
    EXTRACTION_PROMPT,
    REFLECTION_PROMPT,
    INFO_PROMPT,
    YT_PROMPT,
    QUERY_WRITER_PROMPT,
    FINAL_PROMPT
)

# LLMs

class ResearchGraphState(TypedDict):
    linkedin_content: str # LinkedIn search results
    completed_notes: str # Completed notes
    final_report: str # Final report
    reports: list # Reports

    async def generate_queries(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
        """Generate search queries based on the user input and extraction schema."""
        # Get configuration
        configurable = Configuration.from_runnable_config(config)
        max_search_queries = configurable.max_search_queries

        # Generate search queries
        structured_llm = openai4o.with_structured_output(Queries)

        # Format system instructions
        person_str = f"Email: {state.person['email']}"
        if "name" in state.person:
            person_str += f" Name: {state.person['name']}"
        if "linkedin" in state.person:
            person_str += f" LinkedIn URL: {state.person['linkedin']}"
        if "role" in state.person:
            person_str += f" Role: {state.person['role']}"
        if "company" in state.person:
            person_str += f" Company: {state.person['company']}"

        query_instructions = QUERY_WRITER_PROMPT.format(
            person=person_str,
            info=json.dumps(state.extraction_schema, indent=2),
            user_notes=state.user_notes,
            max_search_queries=max_search_queries,
        )

        print(query_instructions)
        
        # Generate queries
        results = cast(
            Queries,
            structured_llm.invoke(
                [
                    {"role": "system", "content": query_instructions},
                    {
                        "role": "user",
                        "content": query_instructions,
                    },
                ]
            ),
        )

        # Queries
        query_list = [query for query in results.queries]
        return {"search_queries": query_list}

    @staticmethod
    def collect_person_info(state: OverallState):
        return {"reports": []}

    async def research_person(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
        """Execute a multi-step web search and information extraction process.

        This function performs the following steps:
        1. Executes concurrent web searches using the Tavily API
        2. Deduplicates and formats the search results
        """

        # Get configuration
        configurable = Configuration.from_runnable_config(config)
        max_search_results = configurable.max_search_results

        # Web search
        search_tasks = []
        for query in state.search_queries:
            search_tasks.append(
                tavily_async_client.search(
                    query,
                    search_depth="advanced",
                    max_results=max_search_results,
                    include_raw_content=True,
                    topic="general",
                )
            )

        # Execute all searches concurrently
        search_docs = await asyncio.gather(*search_tasks)

        # Deduplicate and format sources
        source_str = deduplicate_and_format_sources(
            search_docs, max_tokens_per_source=1000, include_raw_content=True
        )

        print(source_str)
        
        # Generate structured notes relevant to the extraction schema
        p = INFO_PROMPT.format(
            info=json.dumps(state.extraction_schema, indent=2),
            content=source_str,
            people=state.person,
            user_notes=state.user_notes,
        )
        result = await openai4o.ainvoke(p)
        return {"reports": [result.content]}


    async def linkedin_search(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
        """Search LinkedIn for the person's profile and extract relevant information."""

        linkedin_profile_url = linkedin_lookup_agent(state.person['name'])

        # Scrape the LinkedIn profile data
        linkedin_data = str(scrape_linkedin_profile(linkedin_profile_url))
        system_message = (
            "parse all this information and write a comprehensive report on the person's LinkedIn profile."
        )
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Use this source to write your section: {linkedin_data}"},
        ]
        # Extract LinkedIn content
        linkedin_content = await openai4o.ainvoke(messages)

    
        return {"reports": [linkedin_content]}
    
    async def youtube_interviews(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
        """Execute a multi-step web search and information extraction process.

        This function performs the following steps:
        1. Executes concurrent web searches using the Tavily API
        2. Deduplicates and formats the search results
        """

        # Web search
        youtube_url = get_youtube_interview_urls(state.person['name'], max_results=3)
        video_ids = [extract_youtube_id(url) for url in youtube_url]

        video_transcripts = await asyncio.gather(
        *[get_transcript(video_id, languages=["it", "en"]) for video_id in video_ids]
        )
                
        # Filter out None or exceptions
        video_transcripts = [transcript for transcript in video_transcripts if transcript]
        if not video_transcripts:
            print("No valid transcripts found!")  # Debug
            return {"reports": []}
        
        source_str = str(video_transcripts)
        # Generate structured notes relevant to the extraction schema
        p = YT_PROMPT.format(
            person=state.person,
            info=json.dumps(state.extraction_schema, indent=2),
            content=source_str,
        )
        interviews = await openai4o.ainvoke(p)
        return {"reports": [interviews.content]}

    async def finalize_report(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
        """Node to write a section."""
        
        # Access 'reports' correctly based on the structure of `state`
        try:
            reports = state.reports  # Use this if `reports` is an attribute of the `OverallState` object
        except AttributeError:
            reports = state.get("reports", [])  # Use this if `state` is a dictionary or supports `.get()`

        # If `reports` is still empty or None, raise an error or handle the missing value gracefully
        if not reports:
            raise ValueError("Reports are missing or not populated in the state.")

        # Write section using the gathered source docs from the interview

        l = FINAL_PROMPT.format(
            person=state.person,
            info=json.dumps(state.extraction_schema, indent=2),
            reports=reports,
        )

        # Invoke the model
        final_report = await openai4o.ainvoke(l)

        # Access the content of the response
        return {"final_report": final_report.content}


    def gather_notes_extract_schema(state: OverallState) -> dict[str, Any]:
        """Gather notes from the web search and extract the schema fields."""

        # Format all notes
        notes = format_all_notes(state.completed_notes)

        # Extract schema fields
        system_prompt = EXTRACTION_PROMPT.format(
            info=json.dumps(state.extraction_schema, indent=2), notes=notes
        )
        structured_llm = openai4o.with_structured_output(state.extraction_schema)
        result = structured_llm.invoke(
            [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": "Produce a structured output from these notes.",
                },
            ]
        )
        return {"info": result}


    def reflection(state: OverallState) -> dict[str, Any]:
        """Reflect on the extracted information and generate search queries to find missing information."""
        structured_llm = openai4o.with_structured_output(ReflectionOutput)

        # Format reflection prompt
        system_prompt = REFLECTION_PROMPT.format(
            schema=json.dumps(state.extraction_schema, indent=2),
            info=state.info,
        )

        # Invoke
        result = cast(
            ReflectionOutput,
            structured_llm.invoke(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Produce a structured reflection output."},
                ]
            ),
        )

        if result.is_satisfactory:
            return {"is_satisfactory": result.is_satisfactory}
        else:
            return {
                "is_satisfactory": result.is_satisfactory,
                "search_queries": result.search_queries,
                "reflection_steps_taken": state.reflection_steps_taken + 1,
            }

class OutputState(BaseModel):
    final_report: str

# Add nodes and edges
builder = StateGraph(
    OverallState,
    input=InputState,
    output=OutputState,
    config_schema=Configuration,
)


rate_limiter = InMemoryRateLimiter(
    requests_per_second=4,
    check_every_n_seconds=0.1,
    max_bucket_size=10,  # Controls the maximum burst size.
)
openai4o = ChatOpenAI(model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,)

# Search

tavily_async_client = AsyncTavilyClient()


class Queries(BaseModel):
    queries: list[str] = Field(
        description="List of search queries.",
    )


class ReflectionOutput(BaseModel):
    is_satisfactory: bool = Field(
        description="True if all required fields are well populated, False otherwise"
    )
    missing_fields: list[str] = Field(
        description="List of field names that are missing or incomplete"
    )
    search_queries: list[str] = Field(
        description="If is_satisfactory is False, provide 1-3 targeted search queries to find the missing information"
    )
    reasoning: str = Field(description="Brief explanation of the assessment")

builder.add_node("collect_person_info", ResearchGraphState.collect_person_info)
builder.add_node("generate_queries", ResearchGraphState.generate_queries)
builder.add_node("research_person", ResearchGraphState.research_person)
builder.add_node("linkedin_search", ResearchGraphState.linkedin_search)
builder.add_node("finalize_report", ResearchGraphState.finalize_report)
builder.add_node("youtube_interviews", ResearchGraphState.youtube_interviews)

builder.add_edge(START, "collect_person_info")
builder.add_edge("collect_person_info", "generate_queries")
builder.add_edge("collect_person_info", "linkedin_search")
builder.add_edge("collect_person_info", "youtube_interviews")
builder.add_edge("generate_queries", "research_person")
builder.add_edge(["research_person", "linkedin_search", "youtube_interviews"], "finalize_report")
builder.add_edge("finalize_report", END)

# Compile
graph = builder.compile()
