import os
import requests

def scrape_linkedin_profile(linkedin_profile_url:str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    api_key = 'BJ_R64t-wrBf4TPTdQ4LAg'
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=headers
    )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
            
    return data



    
