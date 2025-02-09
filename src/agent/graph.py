import sys
import os

import asyncio
from typing import cast, Any, Literal
import json

from tools.rag_tool import fetch_similar_case_study
from tools.my_tools import get_transcript
from tools.my_tools import extract_youtube_id
from tools.my_tools import get_youtube_interview_urls
from tools.proxycurl.linkedin import scrape_linkedin_profile
from linkedin_lookup_agent import lookup as linkedin_lookup_agent
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from tavily import AsyncTavilyClient
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel, Field

from agent.utils import get_report, save_reports_locally
from tools.google_docs_tools import GoogleDocsManager
from tools.gmail_tools import GmailTools
from tools.structured_outputs import EmailResponse
from langsmith import traceable

from agent.configuration import Configuration
from agent.state import InputState, OutputState, OverallState
from agent.utils import deduplicate_and_format_sources, format_all_notes
from datetime import datetime
from agent.prompts import (
    EXTRACTION_PROMPT,
    REFLECTION_PROMPT,
    INFO_PROMPT,
    COMPANY_INFO_PROMPT,
    YT_PROMPT,
    QUERY_WRITER_PROMPT,
    FINAL_PROMPT,
    COMPANY_QUERY_WRITER_PROMPT,
    OUTREACH_PROMPT,
    GENERATE_OUTREACH_REPORT_PROMPT,
    PROOF_READER_PROMPT
)


SEND_EMAIL_DIRECTLY = True

import logging  # ✅ Correct import

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ResearchGraphState(TypedDict):
    linkedin_content: str # LinkedIn search results
    completed_notes: str # Completed notes
    final_report: str # Final report
    reports: list # Reports
    company_reports: list # Reports
    outreach_email: str
    reports_folder_link: str
    custom_outreach_report_link: str

    def __init__(self, loader):
        self.lead_loader = loader
        self.docs_manager = GoogleDocsManager()
        self.drive_folder_name = ""

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
    
    async def company_generate_queries(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
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

        query_instructions = COMPANY_QUERY_WRITER_PROMPT.format(
            person=person_str,
            company=state.person['company'],
            current_year = datetime.now().year,
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
                    search_depth="basic",
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

        state.reports = []

        return {"reports": [result.content]}
    
    async def research_company(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
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
                    search_depth="basic",
                    max_results=max_search_results,
                    include_raw_content=True,
                    topic="general",
                )
            )

        # Execute all searches concurrently
        search_docs = await asyncio.gather(*search_tasks)

        # Deduplicate and format sources
        source_str = deduplicate_and_format_sources(
            search_docs, max_tokens_per_source=1300, include_raw_content=True
        )

        # Generate structured notes relevant to the extraction schema
        p = COMPANY_INFO_PROMPT.format(
            info=json.dumps(state.extraction_schema, indent=2),
            content=source_str,
            people=state.person,
            company=state.person['company'],
            current_year = datetime.now().year,
            user_notes=state.user_notes,
        )
        result = await openai4o_long_content.ainvoke(p)
        # TO-DO: Generate multiple reports for different sources
        return {"company_reports": result.content}
    
    async def research_company_news(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
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
                    search_depth="basic",
                    max_results=max_search_results,
                    include_raw_content=True,
                    topic="news",
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
        p = COMPANY_INFO_PROMPT.format(
            info=json.dumps(state.extraction_schema, indent=2),
            content=source_str,
            people=state.person,
            company=state.person['company'],
            user_notes=state.user_notes,
        )
        result = await openai4o.ainvoke(p)
    
        # TO-DO: Generate multiple reports for different sources
        return {"company_reports": [result.content]}


    async def linkedin_search(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
        """Search LinkedIn for the person's profile and extract relevant information."""

        linkedin_profile_url = linkedin_lookup_agent(state.person['name'] + ' ' + state.person['company'])

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
        state.reports = []
    
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

    @traceable
    async def generate_custom_outreach_report(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
        logger.info("Starting LangGraph execution tracing...")

        # Initialize GoogleDocsManager here
        docs_manager = GoogleDocsManager()

        # Load reports
        company_report = state.company_reports
        
        # TODO Create better description to fetch accurate similar case study using RAG
        # get relevant case study
        case_study_report = fetch_similar_case_study(company_report)
    
        
        a = GENERATE_OUTREACH_REPORT_PROMPT.format(
            company_report=company_report,
            case_study_report=case_study_report,
            company=state.person["company"]
        )
        
        openai4o = ChatOpenAI(model="gpt-4o-mini",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,)

        final_outreach_report = await openai4o.ainvoke(a)
        final_outreach_report = final_outreach_report.content

        # TODO Find better way to include correct links into the final report
        # Proof read generated report
        inputs = f"""
        {final_outreach_report}

        ---

        **Correct Links:**

        ** Our website link**: https://elevateAI.com
        ** Case study link**: https://elevateAI.com/case-studies/A
        """
        
        # Call our editor/proof-reader agent
        b = PROOF_READER_PROMPT.format(
            final_report=final_outreach_report
        )

        revised_outreach_report = await openai4o_long_content.ainvoke(b)
        revised_outreach_report = revised_outreach_report.content

        # Make sure revised_outreach_report.content is accessed if it's a response object
        report_content = revised_outreach_report.content if hasattr(revised_outreach_report, 'content') else revised_outreach_report
        
        # Create a folder name based on relevant info
        folder_name = f"Outreach Reports {datetime.now().strftime('%Y-%m-%d')}"
        
        try:
            # Store report into google docs and get shareable link
            new_doc = await docs_manager.add_document(
                content=report_content,
                doc_title=f"Business Report - {state.person['company']}",
                folder_name=folder_name,
                make_shareable=True,
                folder_shareable=True,
                markdown=True,
            )
            

            logger.info(f"Successfully created Google Doc with URL: {new_doc['folder_url']}")
            logger.info(f"Successfully created Google Sheet with URL: {new_doc['shareable_url']}")
            
            return {
                "custom_outreach_report_link": new_doc["shareable_url"],
                "reports_folder_link": new_doc["folder_url"]
            }
        except Exception as e:
            logger.error(f"Failed to create Google Doc: {str(e)}")
            raise
    
    
    async def outreach_email(state: OverallState, config: RunnableConfig) -> dict[str, Any]:
        """Node to write a section."""
        
        # Access 'reports' correctly based on the structure of `state`
        try:
            company_reports = state.company_reports  # Use this if `reports` is an attribute of the `OverallState` object
            final_report = state.final_report
        except AttributeError:
            company_reports = state.get("company_reports", [])  # Use this if `state` is a dictionary or supports `.get()`
            final_report = state.get("final_report", [])
        # If `reports` is still empty or None, raise an error or handle the missing value gracefully
        if not company_reports:
            raise ValueError("Reports are missing or not populated in the state.")
        if not final_report:
            raise ValueError("Reports are missing or not populated in the state.")

        # Write section using the gathered source docs from the interview

        l = OUTREACH_PROMPT.format(
            person=state.person,
            company=state.person['company'],
            info=json.dumps(state.extraction_schema, indent=2),
            company_reports=company_reports, 
            final_report=final_report,
            report_url=state.custom_outreach_report_link
        )

        openai4o = ChatOpenAI(model="gpt-4o-mini",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,)

        structured_llm = openai4o.with_structured_output(EmailResponse)
        # Invoke the model
        outreach_email_result = await structured_llm.ainvoke(l)

        # Get relevant fields
        subject = outreach_email_result.subject
        personalized_email = outreach_email_result.email
        
        # Get lead email
        email = 'keem.adorable@scalapay.com'
        
        # Create draft email
        gmail = GmailTools()
        gmail.create_draft_email(
            recipient=email,
            subject=subject,
            html_email_content=personalized_email
        )
        
        # Send email directly
        if SEND_EMAIL_DIRECTLY:
            gmail.send_email(
                recipient=email,
                subject=subject,
                html_email_content=personalized_email
            )

        
        # Access the content of the response
        return {"outreach_email_result": outreach_email_result.email}





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
    outreach_email_result: str

# Add nodes and edges
builder = StateGraph(
    OverallState,
    input=InputState,
    output=OverallState,
    config_schema=Configuration,
)


rate_limiter = InMemoryRateLimiter(
    requests_per_second=4,
    check_every_n_seconds=0.1,
    max_bucket_size=10,  # Controls the maximum burst size.
)
openai4o = ChatOpenAI(model="gpt-3.5-turbo-0125",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,)

openai4o_long_content = ChatOpenAI(model="o1-mini",
    temperature=1,
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
builder.add_node("company_generate_queries", ResearchGraphState.company_generate_queries)
builder.add_node("research_person", ResearchGraphState.research_person)
builder.add_node("linkedin_search", ResearchGraphState.linkedin_search)
builder.add_node("finalize_report", ResearchGraphState.finalize_report)
builder.add_node("youtube_interviews", ResearchGraphState.youtube_interviews)
builder.add_node("research_company", ResearchGraphState.research_company)
builder.add_node("generate_custom_outreach_report", ResearchGraphState.generate_custom_outreach_report)
builder.add_node("outreach_email", ResearchGraphState.outreach_email)

builder.add_edge(START, "collect_person_info")
builder.add_edge("collect_person_info", "generate_queries")
builder.add_edge("collect_person_info", "linkedin_search")
builder.add_edge("collect_person_info", "youtube_interviews")
builder.add_edge("generate_queries", "research_person")
builder.add_edge(["research_person", "linkedin_search", "youtube_interviews"], "finalize_report")
builder.add_edge(START, "company_generate_queries")
builder.add_edge("company_generate_queries", "research_company")
builder.add_edge(["finalize_report", "research_company"], "generate_custom_outreach_report")
builder.add_edge("generate_custom_outreach_report", "outreach_email")
builder.add_edge("outreach_email", END)

# Compile
graph = builder.compile()
