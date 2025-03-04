# LangGraph Agent

This repository contains a **LangGraph** workflow (or “agent”) designed to orchestrate a multi-step lead processing and outreach flow. The diagram below outlines how the agent nodes connect and process information.

<img width="1263" alt="sales-ai-graph" src="https://github.com/user-attachments/assets/9b82d1ba-f320-47ed-a48f-b3a39db6e54f" />


## Overview

The agent uses [LangGraph](https://github.com/hwchase17/langchain) or a similar library to define **nodes** (i.e., tasks/functions) and **edges** (i.e., transitions/flow) to:

1. **Fetch leads** from a CRM.  
2. **Check** if there are remaining leads to process.  
3. **Collect person & company info** from multiple data sources:
   - **Generate queries** for web searches
   - **Research person** (web or LinkedIn)
   - **Research company** (company data & news)
   - **YouTube interviews**  
4. **Compile** a final report.  
5. **Generate** a custom outreach report.  
6. **Send** an outreach email.  
7. **Loop** back until no leads remain.

## Requirements

- **Python 3.9+** (or the version compatible with your environment)
- Package dependencies for:
  - [LangGraph or LangChain](https://github.com/hwchase17/langchain)
  - [OpenAI / LLMs](https://platform.openai.com/docs/introduction)
  - [Requests](https://pypi.org/project/requests/) (for HTTP calls)
  - [Pydantic](https://docs.pydantic.dev/) (for data models)
  - [Any additional tooling**: e.g., `google-docs-tools`, custom tools, or `slack_bolt` if integrated with Slack]

Install the necessary packages via:

```bash
pip install -r requirements.txt
