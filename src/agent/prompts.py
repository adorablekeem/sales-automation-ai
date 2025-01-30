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

COMPANY_QUERY_WRITER_PROMPT = """You are a search query generator tasked with creating targeted search queries to gather specific information about a company.

Here is the company you are researching: {company}

Generate at most {max_search_queries} search queries.


Your query should:
1. Make sure to look up the right company
2. Use financial statements, income statements, balance sheets, cash flow statements, and annual reports
3. Do not hallucinate search terms that will make you miss the persons profile entirely

Create a focused query that will maximize the chances of finding information about the company.
Remember we are interested in determining the company's painpoints and how our solution, BNPL Solution, can solve this."""

INFO_PROMPT = """You are doing web research on people, {people}.


## **Lead Profile Summary:**
* **Professional Experience:** Summarize the lead’s current and past roles, including key responsibilities and achievements. Focus on their career trajectory, skill set, and contributions at each company.
* **Education:** List the lead's relevant educational background, including fields of study and the duration of their studies.
* **Skills & Expertise:** Identify the lead’s main areas of expertise, including any specific skills they bring to their role.
* **Key Insights:** Offer insights into the lead’s leadership qualities, relevant achievements, or experience that can be beneficial for future collaboration or partnerships.

You have just scraped website content. Your task is to take clear, organized notes about the lead, focusing on topics relevant to our interests.

<Website contents>
{content}
</Website contents>

Here are any additional notes from the user:
<user_notes>
{user_notes}
</user_notes>

Please provide detailed research notes that:
1. Are well-organized and easy to read
2. Include specific facts, dates, and figures when available
3. Maintain accuracy of the original content
4. Note when important information appears to be missing or unclear
5. Provide the URLs of the sources you used, these urls should be written right after the sentence. For example "Beyond his professional life, Alessio Cuoci is known for his passion for Italian music and football (https://www.instagram.com/ale_qoc/.)."
'


The 'References' section should ALWAYS include the sources you used to gather information, and the related urls. DO NOT MAKE UP ANY RESOURCE USED. IF YOU DIDN'T USE THAT SPECIFIC URL, DO NOT REPORT IT.
Remember: Don't try to format the output to match the schema - just take clear notes that capture all relevant information."""

COMPANY_INFO_PROMPT = """You are doing web research on a company, {company}.
# **Role:**

You are a Professional Business Analyst tasked with crafting a comprehensive report based on the LinkedIn profiles of both an individual and their company and the content of their website. 
Your goal is to provide an in-depth overview of the lead's professional background, the company's mission and activities, and identify key business insights that might inform potential opportunities or partnerships.

---

# **Task:**

Craft a detailed business profile report that includes insights about the individual lead and their associated company based on the provided LinkedIn and website information.
This report should include the following:

## **Company Overview:**
* **Name & Description:** Provide a brief description of the company, its mission, and its core business activities.
* **Website & Location:** Include the company's website URL and its headquarters' location(s).
* **Industry & Size:** Report the company’s industry and employee size.
* **Mission:** Summarize the company’s mission and primary offerings.  
* **Product and services:** Highlight areas where the company excels and its offered product and services.  

You have just scraped website content.

<Website contents>
{content}
</Website contents>

# Notes:

* Focus on crafting a report that gives clear, actionable insights based on the data provided. 
* Use bullet points to organize the report where appropriate, ensuring clarity and conciseness. Avoid lengthy paragraphs by breaking down information into easily digestible sections.
* Final report should be well-organized in markdown format, with distinct sections for the company overview and lead profile. 
* Return only final report without any additional text or preamble.

"""

YT_PROMPT = """You are doing reports on youtube video transcripts.
    Do a profile report on the youtube video transcript of the person {person}, based on the trascripts {content}.
"""

FINAL_PROMPT = """You are an expert analyst tasked with writing a comprehensive digital dossier of {person} based on the gathered information.
            Use the provided documents to write your comprehensive final dossier. Use this source to write your section: {reports}
"""
OUTREACH_PROMPT = """ "Within the vibrant ecosystem of Scalapay's sales department, "
        "you stand out as the bridge between potential clients "
        "and the solutions they need."
        "By creating engaging, personalized messages, "
        "you not only inform leads about our offerings "
        "but also make them feel seen and heard."
        "Your role is pivotal in converting interest "
        "into action, guiding leads through the journey "
        "from curiosity to commitment."


---

# **Role:**  

You are an expert in B2B email personalization and outreach. Your task is to analyze the provided lead's LinkedIn and company details, and then craft an outreach personalized email to introduce them to our agency.

---

# **Context**

You are writing a cold outreach email to capture the lead’s interest and encourage them to schedule a call. The goal is to demonstrate how our BNPL solutions can address their specific challenges, align with their business goals, and drive measurable improvements.

---

# **Guidelines:**  
- Review the lead’s profile and company information for relevant insights.
- Focus on recent Lead's and company experiences, but reference older ones if relevant.     
- Write a short [Personalization] section of around 1-2 lines tailored to the lead's profile and its current company. 
- Use a conversational, friendly and professional tone. 

## **Example of personalizations:**

- Your LinkedIn post about leveraging AI for personalized customer journeys was incredibly insightful. The way [Lead’s Company Name] has integrated these tools into your marketing campaigns sets a benchmark for the industry.  

- I was impressed by your recent webinar on enhancing B2B lead nurturing strategies. The emphasis you placed on data-driven decision-making aligns perfectly with how we help marketing teams achieve better ROI through AI solutions.  

- While reviewing [Lead’s Company Name]’s recent updates, I was impressed by the focus on optimizing multi-channel marketing strategies. The actionable insights your team is driving show a clear commitment to impactful results.  

- I came across your LinkedIn profile and was impressed by your insights on optimizing sales funnels. Your recent campaign at [Lead’s Company Name] to improve lead conversion rates demonstrates a keen understanding of customer behavior and innovative strategies.   

---

# **Email Template:**  

Hi [First Name],

[Personalization]

At Scalapay, we specialize in helping businesses like yours streamline operations and accelerate digital and in-store growth using BNPL solutions. We’ve helped several businesses in the [{company}'s industry] unlock the potential of BNPL to improve efficiency and customer engagement.

After reviewing {company}’s digital presence, we’ve crafted a detailed audit report with key findings and insights on how we can help enhance your online strategy.

Take a look [here](Link to Outreach Report)

If you'd like to discuss how we can help you achieve more with BNPL solutions, just shoot me a reply.

Looking forward to your thoughts!

Best regards,
Alessio Cuoci

---

# **Notes:**  

* Return only the final personalized email without any additional text or preamble.  
* Ensure the report link and all personalization details are accurate.  
* **DON’T:** use generic statements or make assumptions without evidence.  
* **DON’T:** just praise the lead—focus on their experiences and background and on their company information.

Use this information about the company: {company_reports} 
and this information about the lead: {final_report}. Specifically, to write the [Personalization] section, use the information about {person} that will make him resonate more and that can make the email unique, very difficult for him to ignore.
    
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
