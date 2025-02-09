from tools.my_tools import get_profile_url

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0125")

    template = """given the full name and company {name_of_person} I want you to get it me a link to their Linkedin profile page.
                      Your answer should contain only a URL.
                      For example, if the person is Nicola Olivetto at Scalapay and you find the URL https://www.linkedin.com/posts/nicola-olivetto-73968692_scalapay-buys-an-italian-payment-institute-activity-7038422608941359104-5mPT, your answer should be https://www.linkedin.com/posts/nicola-olivetto-73968692/recent-activity/reactions/'
                      Here below is an example of your reasoning and answer:
                      'To find the LinkedIn profile page for Nicola Olivetto at Scalapay, I will perform a search to locate the correct URL.
                      Make sure that the profile is relevant and specific of the person.

This is an example:
Action: Crawl Google 4 linkedin profile page
Action Input: "Nicola Olivetto Scalapay LinkedIn"
Observation: https://www.linkedin.com/posts/nicola-olivetto-73968692_scalapay-buys-an-italian-payment-institute-activity-7038422608941359104-5mPT
Thought:The URL provided is a LinkedIn post, not the profile page. I will continue searching for other LinkedIn profile URLs in order to be sure when generating the final answer.

Action: Crawl Google 4 linkedin profile page
Action Input: "Nicola Olivetto Scalapay LinkedIn profile"
Observation: https://www.linkedin.com/posts/nicola-olivetto-73968692_scalapay-buys-an-italian-payment-institute-activity-7038422608941359104-5mPT
Thought:It seems that the search is repeatedly returning a LinkedIn post URL rather than the profile page. I will attempt another search to find the correct LinkedIn profile URL.

Action: Crawl Google 4 linkedin profile page
Action Input: "Nicola Olivetto LinkedIn profile Scalapay"
Observation: https://www.linkedin.com/posts/nicola-olivetto-73968692_scalapay-buys-an-italian-payment-institute-activity-7038422608941359104-5mPT
Thought:It appears that the search is consistently returning a LinkedIn post URL rather than the profile page. This might indicate that the profile page is not easily accessible or indexed. However, based on the pattern of LinkedIn URLs, I can deduce the likely profile URL from the post URL.

Final Answer: https://www.linkedin.com/in/nicola-olivetto-73968692/'

If you can't infert the correct profile page URL from the searches that you did, because the URLs do not correctly match the format "https://www.linkedin.com/in/nicola-olivetto-73968692/", generate the URL based on the URLs you have found the most.
For example, if in three searches you found: https://it.linkedin.com/in/david-capuano-, https://www.linkedin.com/pub/dir/+/Capuano/it-0-Italy, https://it.linkedin.com/in/david-capuano-;
The final answer will be "https://it.linkedin.com/in/david-capuano-"
                      
                      """

    tools_for_agent1 = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="useful for when you need get the Linkedin Page URL",
        ),
    ]


    agent = initialize_agent(
        tools_for_agent1, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )

    linkedin_username = agent.run(prompt_template.format_prompt(name_of_person=name))
    
    return linkedin_username
