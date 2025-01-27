EXTRACTION_PROMPT = """Your task is to take notes gathered from web research and extract them into the following schema.

<schema>
{info}
</schema>

Here are all the notes from research:

<web_research_notes>
{notes}
</web_research_notes>
"""

QUERY_WRITER_PROMPT = """You are a search query generator tasked with creating targeted search queries to gather specific information about a person.

Here is the person you are researching: {person}

Generate at most {max_search_queries} search queries.


Your query should:
1. Make sure to look up the right name
2. Use context clues as to the company the person works at (if it isn't concretely provided)
3. Do not hallucinate search terms that will make you miss the persons profile entirely
4. Use ONLY the full name extracted from the email. If the input email is "alessio.cuoci@scalapay.com", an example query would be "Alessio Cuoci Scalapay Interviews" or "Alessio Cuoci Scalapay Articles"
9. Use always interviews and articles
10. Use instagram
11. Never use information related to the LinkedIn profile

Create a focused query that will maximize the chances of finding information about the person.
Remember we are interested in determining the person's interests and hobbies mainly."""

INFO_PROMPT = """You are doing web research on people, {people}.

You have just scraped website content. Your task is to take clear, organized notes about a person, focusing on topics relevant to our interests.

<Website contents>
{content}
</Website contents>

Here are any additional notes from the user:
<user_notes>
{user_notes}
</user_notes>

Please provide detailed research notes that:
1. Are well-organized and easy to read
2. Focus on topics mentioned in the schema
3. Include specific facts, dates, and figures when available
4. Maintain accuracy of the original content
5. Note when important information appears to be missing or unclear
6. Provide the URLs of the sources you used, these urls should be written right after the sentence. For example "Beyond his professional life, Alessio Cuoci is known for his passion for Italian music and football (https://www.instagram.com/ale_qoc/.)."
'


The 'References' section should ALWAYS include the sources you used to gather information, and the related urls. DO NOT MAKE UP ANY RESOURCE USED. IF YOU DIDN'T USE THAT SPECIFIC URL, DO NOT REPORT IT.
Remember: Don't try to format the output to match the schema - just take clear notes that capture all relevant information."""

YT_PROMPT = """You are doing reports on youtube video transcripts.
    Do a profile report on the youtube video transcript of the person {person}, based on the trascripts {content}.
"""

FINAL_PROMPT = """You are an expert analyst tasked with writing a comprehensive digital dossier of {person} based on the gathered information.
            Use the provided documents to write your comprehensive final dossier. Use this source to write your section: {reports}
"""

REFLECTION_PROMPT = """You are a research analyst tasked with reviewing the quality and completeness of extracted person information.

Compare the extracted information with the required schema:

<Schema>
{schema}
</Schema>

Here is the extracted information:
<extracted_info>
{info}
</extracted_info>

Analyze if all required fields are present and sufficiently populated. Consider:
1. Are any required fields missing?
2. Are any fields incomplete or containing uncertain information?
3. Are there fields with placeholder values or "unknown" markers?
"""
