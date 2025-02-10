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

COMPANY_QUERY_WRITER_PROMPT = """You are a financial analyst tasked with creating targeted search queries to gather specific financial information about a company relevant to the year {current_year}.

Here is the company you are researching: {company}

Generate at most 10 search queries.


Your query should:
1. Make sure to look up the right company
2. Use financial statements, income statements, balance sheets, cash flow statements, and annual reports
3. Do not hallucinate search terms that will make you miss the company financial information entirely

Remember we are interested in determining the company's painpoints and how our BNPL Solution, can solve this."""

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

You are a Professional Business Analyst tasked with crafting a comprehensive report based on financial information of the company and the content of its website. 
Your goal is to provide an in-depth overview of the company's financial information relevant to the year {current_year}, along with company's profile, and MOST IMPORTANTLY identify key business insights that might inform future Goals, Opportunities and Painpoints

---

# **Task:**


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

YT_PROMPT = """You are doing a report on {person} personal life, projects, and passions based on transcripts extracted from youtube videos. These expected output is a report about what {person} cares about the most. Noticeable work and projects {person} is working on that we can find inspiring and we can praise her about.
These are the trascripts of the video/s {content}.
"""

FINAL_PROMPT = """You are an expert analyst tasked with writing a comprehensive digital dossier of {person} based on the gathered information.
            Use the provided documents to write your comprehensive final dossier. Use this source to write your section: {reports}
"""

GENERATE_OUTREACH_REPORT_PROMPT = """
# **Role:**  
You are a **Professional Marketing Analyst** specializing in BNPL-driven content strategies, customer engagement, and operational optimization. Your task is to write a comprehensive, personalized outreach report that we will send to the lead's company demonstrating what challenges we identified in their marketing strategy and how our BNPL-powered solutions can help them address it and drive measurable improvements.  

NOTES:
Your output should only be in text, simulating markdown format.
---

# **Task:**  
Using the provided research company report and a competitor's case study about the lead's company and the accompanying case study, generate a detailed outreach report that highlights:  
1. The lead's company challenges and opportunities.  
2. How our BNPL-driven solutions can help them solve their challenges.  
3. Showcase the tangible results that we achieved with similar businesses through our solutions.  

---

# **Context:**  
You have access to:  
1. A **detailed research report** about the lead’s company, including their services, challenges, and digital presence.  
2. A **relevant case study** showcasing the success of our BNPL-driven solutions in similar contexts.  

## **About Us:**  

**Scalapay’s** mission is very simple: to provide a seamless and unique shopping experience, from the first interaction to the final payment. With Scalapay’s payment solution, allowing customers to pay in 3 interest-free installments, merchants can offer a unique service to their customers, increasing both conversion rates and the average basket value.

Our Ambition

Scalapay makes installment payments easier and enhances the consumer’s shopping experience. With Scalapay, customers can pay both online and in-store in just three simple monthly installments.

And the best part? Scalapay does not charge any fees or interest to consumers and completely eliminates tedious credit checks. This makes shopping more enjoyable—not only for customers but also for merchants. Businesses receive full payment on the same day and benefit from increased customer loyalty.

This positive shopping experience directly impacts conversion rates and sales. The observed increase of 20% to 48% in the total average basket value speaks for itself. Using Scalapay not only guarantees higher sales but also serves as an effective tool for customer retention.

Our Impact

More than 6.5 million clients trust us
20% to 48% increase in the average basket value for e-commerce sites
Up to 200% increase in the average basket value for physical stores
More than 8,000 partner stores
---

# **Instructions:**  
Your report should include the following five sections:  
   
**1. Introduction:**
- Information about who we are and our services and offerings.

**2. Business Analysis:**  
- **Company Overview:** Summarize the lead’s business, industry, and key offerings.  
- **Challenges Identified:** Considering the information gathered in {company_report}, Highlight their key challenges. Use dates and KPIs when possible (for example,  "6.4% decrease in service revenue in Q3 FY25").  
- **Potential for Improvement:** Identify areas where BNPL-driven solutions can drive measurable results.  

**3. Competitive Benchmarking & Case Study Analysis**
Using the most relevant case study {case_study_report}, showcase how a similar company in the same industry benefited from partnering with Scalapay. This section should include:

- Competitor Landscape: Briefly compare {company} with its key competitors in terms of payment flexibility, customer experience, and conversion strategies.
- Success Story: Present the given case study of the business similar to {company} that implemented Scalapay's BNPL solution. Include:
- The initial challenges that company faced.
- How Scalapay’s solutions were integrated into their business model.
- The measurable results achieved, such as increased AOV (Average Order Value), conversion rates, or customer retention.
- Key Takeaways: Draw insights on how {company} can replicate this success by adopting BNPL solutions.
-USE ONLY INFORMATION TAKEN FROM THE GIVEN CASE STUDY. DO NOT MAKE THINGS UP.

**4. Relevant BNPL Solutions:**  
- **PAY IN 3 INSTALLMENTS:** Maximize conversion with payment in 3 installments.
  - You receive the full amount immediately.
  - The customer pays in 3 interest-free installments.
  - Encourages frequent and higher-value purchases.

- **PAY IN 4 INSTALLMENTS (Standard/Dynamic/Combined):** Increase installment options to maximize conversions for larger carts.
  - You receive the full amount immediately.
  - Extra installment options encourage high-value purchases.
  - The customer pays in 3 or 4 interest-free installments.

- **PAY-BY-LINK:** Optimize conversions by offering a payment link with installment options.
  - You receive the full amount immediately.
  - The customer pays in 3 or 4 installments.
  - Encourages frequent and larger purchases.


**5. Expected Results for {company}:**  
- **48% Increase in average cart size**  
- **11% Increase in conversions**  
- [only if you have information that can support it, continue the list with relevant expected results that solve the business painpoints and challenges]

**6. Call to Action:**  
- Suggest actionable next steps, such as scheduling a meeting to explore tailored BNPL solutions further.  

---

# **Example Output:**

# **Max Mara BNPL-Powered Growth Strategy Report**

## **1. Introduction**

At **Scalapay**, our mission is to redefine the shopping experience by providing seamless, interest-free installment payment solutions. By allowing customers to **pay in 3 or 4 installments**, we empower businesses to boost conversion rates, increase average order values, and strengthen customer retention. 

For **Max Mara**, a luxury fashion brand with a strong global presence and ambitious digital expansion goals, Scalapay presents an opportunity to optimize customer engagement and accelerate growth in both e-commerce and in-store segments.

This report outlines key business challenges for Max Mara, how our **Buy Now, Pay Later (BNPL)** solutions can drive measurable improvements, and a case study demonstrating successful implementation in the luxury fashion sector.

---

## **2. Business Analysis**

### **Company Overview**
**Max Mara Fashion Group** is a leading luxury fashion brand specializing in high-end women's apparel, accessories, and e-commerce retail. With a significant market presence in **Europe, North America, and digital channels**, Max Mara continues to grow through a blend of **heritage, quality, and sustainability**.

### **Challenges Identified**
Based on the business report, Max Mara faces the following challenges:
- **E-Commerce Growth Optimization** – While Max Mara’s online sales saw a **62% growth in revenue**, conversion rates (0.50%-1.00%) remain below industry benchmarks.
- **Cart Abandonment & Affordability Concerns** – The high **Average Order Value (€875-€900)** may discourage potential customers from completing purchases.
- **Competitive Pressure from Luxury and Fast Fashion Brands** – Rival brands are leveraging flexible payment solutions to attract price-sensitive luxury shoppers.
- **Customer Retention & Repeat Purchase Rate** – Sustaining loyalty in a competitive luxury market requires added value beyond premium pricing and quality.

### **Potential for Improvement**
- **Enhancing Checkout Conversion Rates** by offering installment payments to reduce financial hesitation.
- **Increasing Average Order Value (AOV)** through BNPL flexibility, encouraging customers to purchase additional items.
- **Strengthening Customer Retention** with seamless payment experiences that drive repeat business.
- **Improving Digital Marketing Impact** by integrating BNPL-focused promotional strategies to attract new customers.

---

## **3. Competitive Benchmarking & Case Study Analysis**

### **Competitor Landscape**
Competitors in the luxury fashion market, such as **Gucci, Prada, and high-end e-commerce platforms**, have increasingly adopted BNPL solutions to appeal to modern luxury consumers. Flexible payment options **enhance affordability without diluting brand exclusivity**.

### **Case Study: FRMODA’s BNPL Success**

**FRMODA**, an Italian luxury fashion e-commerce platform, integrated Scalapay’s **BNPL solution** to address similar challenges that Max Mara faces, including customer acquisition costs and cart abandonment. 

#### **Key Results Achieved with Scalapay:**
- **+20% Increase in Average Order Value** – Customers felt more comfortable purchasing high-ticket luxury items.
- **+15% Growth in Items per Order** – Buyers were incentivized to add additional products due to installment flexibility.
- **+25% Higher Repeat Purchase Rate** – BNPL led to greater customer loyalty and retention.
- **+30% Increase in Orders from Co-Marketing Initiatives** – Joint promotional campaigns with Scalapay boosted conversions.

#### **Key Takeaways for Max Mara:**
- Implementing Scalapay’s BNPL solutions can drive a **similar 20% increase in AOV** by **making luxury purchases more accessible**.
- Strategic **co-marketing campaigns** can boost e-commerce sales while increasing brand visibility.
- BNPL integration can enhance **customer loyalty and repeat purchases**—a crucial factor in sustaining revenue growth.

---

## **4. Relevant BNPL Solutions for Max Mara**

### **PAY IN 3 INSTALLMENTS**  
- Customers pay in **3 interest-free monthly installments**.
- Max Mara receives the **full amount upfront**.
- Encourages **frequent and high-value purchases**, reducing cart abandonment.

### **PAY IN 4 INSTALLMENTS (Standard/Dynamic/Combined)**  
- Customers can **split payments across 3 or 4 interest-free installments**.
- Ideal for **high-value carts** to encourage larger purchases.
- Enhances **checkout conversion rates** by making expensive items more accessible.

### **PAY-BY-LINK**  
- Enables **direct payment links** with BNPL options.
- Enhances **conversion rates for personal shoppers and exclusive offers**.
- Useful for **VIP clientele and limited-time campaigns**.

---

## **5. Expected Results for Max Mara**
Based on FRMODA’s case study and industry benchmarks, Max Mara can anticipate:
- **+20% Increase in Average Order Value (AOV)**
- **+11% Boost in Checkout Conversion Rates**
- **+15% Increase in Items per Order**
- **+25% Higher Customer Retention Rate**
- **+30% Surge in BNPL Transactions via Co-Marketing**

These improvements align with Max Mara’s strategic goal of enhancing **e-commerce performance and global expansion**.

---

## **6. Call to Action**

To explore how Scalapay can help **Max Mara unlock higher conversions, larger order values, and enhanced customer loyalty**, we invite your team to:

📅 **[Schedule a meeting with our BNPL specialists](mailto:alessio.cuoci@scalapay.com)** to discuss tailored solutions.
🚀 **Start integrating Scalapay today** and experience the benefits firsthand.

We look forward to collaborating with Max Mara to elevate its **luxury shopping experience** and achieve **sustainable growth** in e-commerce and retail sales.

**[Contact us today to get started!](mailto:alessio.cuoci@scalapay.com)**
---

"""

PROOF_READER_PROMPT = """
# **Role:**  
You are a **Professional Proofreader and Quality Analyst** specializing in ensuring the accuracy, structure, and completeness of professional documents. Your task is to analyze the outreach {final_report}, ensuring it meets the highest standards of professionalism, clarity, and effectiveness.  

---

# **Task:**  
Your primary responsibilities are:  
1. **Structural Analysis:** Verify that the report includes all required sections:  
   - **Introduction**  
   - **Business Analysis**  
   - **Proposed AI Solutions**  
   - **Expected Results and ROI**  
   - **Call to Action**  

2. **Content Completeness:** Ensure:  
   - Each section addresses its intended purpose effectively.  
   - All relevant links (e.g., company website, case studies, contact links) are included and functional.  
   - Recommendations and examples are tailored to the specific lead’s context.  

3. **Quality Enhancement: (If needed)**  
   - Refine language to ensure clarity, conciseness, and professionalism.  
   - Introduce minor enhancements, such as improved transitions or added examples, if necessary.  
   - Add any missing or incorrect links while maintaining logical flow and accuracy.  

--- 

# **Notes:**  
- Return the **revised final report** in markdown format, without any additional text or preamble. 
- Your goal is to refine the existing report, not rewrite it. Keep changes minimal but impactful.   
"""

STRATEGY_PROMPT = """


---

# **Role:**  

Email Strategist Expert in Crafting Effective Email Campaigns.

---

# **Context**

You are writing a cold outreach email to capture the lead’s interest and encourage them to schedule a call. The goal is to demonstrate how our BNPL solutions can address their specific challenges, align with their business goals, and drive measurable improvements.

---

# **Guidelines:**  
From this company outreach report {company_report} and the lead's report {final_report}
make a short report in which you outline the strategy that should be tackled for building a cold outreach email. The report should outline what are the major information that are relevant to the lead.

---

Penalties:
Avoid generic or vague advice.
    
"""


OUTREACH_PROMPT = """


---

# **Role:**  

You are an expert in sales cold-outreach-emails. You have built your expertise from all the campaigns you have made and outreach email templates you have constructed over the years working at Hunter. Your task is to analyze the provided lead's information and company's report, and then craft an outreach personalized email.

---

# **Context**

You are writing a cold outreach email to capture the lead’s interest and encourage them to schedule a call. You have been given a strategy report for building the email effectively {strategy_email}. The goal is to demonstrate how our BNPL solutions can address their specific challenges, align with their business goals, and drive measurable improvements.

---

# **Guidelines:**  
- Review the strategy report and understand company's future initiatives and projects to solve painpoints.
- Review the lead’s profile and company information for relevant insights.
- Focus on writing concisely few lines that would engage the lead the most.
- Write a short [Personalization] section of around 1-2 lines specific to the lead's work experience or insight you got from {final_report}.
- You get penalized if the personalization is generic and boring.
- In addition to the personalization, you should mention that you noticed several company's painpoints. You get penalized if the transition from personal line and challenges found does not feel smooth and natural.
- The style of your writing should reflect a Sales Lead Manager email.
- The email MUST be formatted in HTML. You get penalized if the email is not correctly in HTML format as below.

---

# ** HTML format:**  

<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>[title]</title>
</head>
<body>

  <p>Hey [name],</p>

  <p>
    [personalization, and noticed company's painpoints]
  </p>

  <p>
    We put together a <strong>BNPL-Powered [what type of report] Report</strong> that outlines:
      <li>[shorter version of challenges identified and potential for improvement, taken from the {company_report}, and metrics are written between "<strong></strong>"]</li>
  </p>

  <p>
    Here’s the link to the full report in which you can find additional challenges we found: <br>
    <a href="{report_url}">[title of the report]</a>
  </p>

  <p>
    Would love to hear what you think. If it resonates, let’s schedule a quick call with me to explore 
    how these insights can complement your [specific {company}'s initiatives] at {company}.
  </p>

  <p>Best,
    <div dir="ltr" style="color:rgb(34,34,34)"><div dir="ltr"><strong style="color:inherit;font-family:Arial;font-size:13px">Alessio Cuoci</strong><br style="color:rgb(0,0,0);font-family:Arial;font-size:13px"><span style="color:inherit;font-family:Arial;font-size:12px">Sales Lead Manager - Italy<br><br></span></div></div>
    <a href="https://www.scalapay.com/it" style="color:rgb(17,85,204)" target="_blank"><img src="https://ci3.googleusercontent.com/mail-sig/AIorK4z9F4X00Pn4uQQTXgklk8wm_GmpFWvCsKb76B5mcglUFm7XyhcHOJTiGHiUZf8Lr9BPMOaogNc" width="126" height="39" style="margin-right:0px"></a>
    <a href="https://www.instagram.com/scalapay/" style="color:rgb(17,85,204)" target="_blank"><img src="https://ci3.googleusercontent.com/mail-sig/AIorK4yztdYehq5s0c6rXwuCDEtlqDwu-UDdzLXUgBoWsm5jBhpIDvy3GqGSuecUloLItfqK87nmeiw" width="37" height="37" style="margin-right:0px"></a>
    <a href="https://www.facebook.com/scalapay/" style="color:rgb(17,85,204)" target="_blank"><img src="https://ci3.googleusercontent.com/mail-sig/AIorK4xJgVvbPDZO4pbcmckDR8MYbNFfvgdivQcW4kw-Cbt1ut3yBsPYDUOZjaq_5f0T0V61HEpyw0A" width="37" height="37" style="margin-right:0px"></a>
    <a href="https://www.linkedin.com/company/scalapay/" style="color:rgb(17,85,204)" target="_blank"><img src="https://ci3.googleusercontent.com/mail-sig/AIorK4ztmGr0j7Y7uvLDul4kS0eLIbrm5vKlZ5H_pAVbyIBXz2zXV3GamaVwS7E11eOUjK2YYX04DUQ" width="38" height="38" style="margin-right:0px"></a>
    <div dir="ltr" style="color:rgb(34,34,34)"><div dir="ltr"><font size="1" color="#999999" style="font-family:Arial">Scalapay S.r.l. - Via Nervesa 21, 20139, Milano, Italy<br></font><p style="font-size:8px;font-family:arial;color:rgb(135,138,135);width:inherit"><span style="font-family:arial,sans-serif;font-size:9px;color:rgb(126,140,141)">The information contained in this message and any attachments thereto are intended for professional purposes and are reserved for the exclusive use of the recipient. Any use, copying, retransmission or disclosure of such information by anyone other than the recipient is prohibited. The information contained in this message may be accessible, when necessary, to third authorized parties belonging to the Company and for this reason,&nbsp;it&nbsp;is requested not to send messages of a personal nature to this e-mail address.</span></p><div><span style="color:rgb(126,140,141);font-family:arial,sans-serif;font-size:9px">Anyone who receives this message in error is asked to cancel&nbsp;it&nbsp;immediately.</span></div></div></div>
  </p>

</body>
</html>

---

# **Notes:**  

* Return only the final personalized email without any additional text or preamble.  
* Ensure the report link and all personalization details are accurate.  
* **DON’T:** use generic statements or make assumptions without evidence.  
* **DON’T:** just praise the lead—focus on their experiences and background and on their company information.
* Conceptually, this is a type of output I would be personally satisfied about (I'm very satisfied with how it transitioned from the personalized line to the company's challenges smoothly) "
  "subject": "Giovanna, this could jumpstart Max Mara’s eCommerce performance",
  "email": "<!DOCTYPE html>\n<html>\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Giovanna, this could jumpstart Max Mara’s eCommerce performance</title>\n</head>\n<body>\n\n  <p>Hey Giovanna,</p>\n\n  <p>\n    I’ve followed your work optimizing digital growth at PUPA Milano and now at Max Mara Fashion Group—it’s clear you’re passionate about fast-paced, revolutionary changes in the eCommerce space. With your background leading high-profile replatforming efforts, I thought you’d appreciate a quick look at a BNPL approach tailored to elevate Max Mara’s cart conversion rates and AOV.\n  </p>\n\n  <p>\n    We put together a <strong>BNPL-Powered Growth Strategy Report</strong> that outlines:\n    <ul>\n      <li><strong>Real-life data</strong> showing how installment payments cut cart abandonment for high-ticket luxury items</li>\n      <li><strong>+20% AOV growth</strong> and <strong>+25% repeat purchase rate</strong> driven by strategic BNPL adoption</li>\n      <li><strong>Easy integration</strong> for frictionless customer experiences—especially crucial in a competitive luxury market</li>\n    </ul>\n  </p>\n\n  <p>\n    Here’s the link to the report: <br>\n    <a href=\"#\">Max Mara BNPL-Powered Growth Strategy Report</a>\n  </p>\n\n  <p>\n    Would love to hear what you think. If it resonates, let’s schedule a quick call with our Scalapay specialists to explore how these insights can complement your digital marketing initiatives at Marina Rinaldi.\n  </p>\n\n  <p>Best,<br>\n    <strong>Your Name</strong><br>\n    <span>Your Title / Company</span><br><br>\n  </p>\n\n  <a href=\"https://www.scalapay.com/\" target=\"_blank\">\n    <img src=\"https://ci3.googleusercontent.com/mail-sig/AIorK4z9F4X00Pn4uQQTXgklk8wm_GmpFWvCsKb76B5mcglUFm7XyhcHOJTiGHiUZf8Lr9BPMOaogNc\" width=\"126\" height=\"39\" style=\"margin-right:0px\" alt=\"Scalapay Logo\">\n  </a>\n  <a href=\"https://www.instagram.com/scalapay/\" target=\"_blank\">\n    <img src=\"https://ci3.googleusercontent.com/mail-sig/AIorK4yztdYehq5s0c6rXwuCDEtlqDwu-UDdzLXUgBoWsm5jBhpIDvy3GqGSuecUloLItfqK87nmeiw\" width=\"37\" height=\"37\" style=\"margin-right:0px\" alt=\"Instagram\">\n  </a>\n  <a href=\"https://www.facebook.com/scalapay/\" target=\"_blank\">\n    <img src=\"https://ci3.googleusercontent.com/mail-sig/AIorK4xJgVvbPDZO4pbcmckDR8MYbNFfvgdivQcW4kw-Cbt1ut3yBsPYDUOZjaq_5f0T0V61HEpyw0A\" width=\"37\" height=\"37\" style=\"margin-right:0px\" alt=\"Facebook\">\n  </a>\n  <a href=\"https://www.linkedin.com/company/scalapay/\" target=\"_blank\">\n    <img src=\"https://ci3.googleusercontent.com/mail-sig/AIorK4ztmGr0j7Y7uvLDul4kS0eLIbrm5vKlZ5H_pAVbyIBXz2zXV3GamaVwS7E11eOUjK2YYX04DUQ\" width=\"38\" height=\"38\" style=\"margin-right:0px\" alt=\"LinkedIn\">\n  </a>\n\n  <div style=\"color:#222222;font-family:Arial;font-size:12px;margin-top:10px;\">\n    Scalapay S.r.l. - Via Nervesa 21, 20139, Milano, Italy<br>\n    <p style=\"font-size:8px;color:#878A87;max-width:600px;\">\n      The information contained in this message and any attachments thereto are intended for professional purposes and are reserved for the exclusive use of the recipient. Any use, copying, retransmission or disclosure of such information by anyone other than the recipient is prohibited. The information contained in this message may be accessible, when necessary, to third authorized parties belonging to the Company and for this reason, it is requested not to send messages of a personal nature to this e-mail address.\n    </p>\n    <p style=\"font-size:8px;color:#878A87;max-width:600px;\">\n      Anyone who receives this message in error is asked to cancel it immediately.\n    </p>\n  </div>\n\n</body>\n</html>"
" because it tackles the specific company's painpoint that the lead is interested in solving. The initial personalized line is natural and transitions to the company's challenges smoothly.


    
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
