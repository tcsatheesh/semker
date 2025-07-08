"""
Billing tools for MCP server.

This module contains the MCP tools for retrieving billing data.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="FaqTool",
    stateless_http=True,
)


@mcp.tool(description="A tool to retrieve frequently asked questions (FAQ) data.")
async def get_faq_data() -> str:
   
   # using requests to fetch data from the FAQ endpoint
    import requests
    
    try:
        response = requests.get("https://www.vodafone.co.uk/mobile/global-roaming?icmp=uk~1_consumer~topnav~3_help~1_costs_and_charges~3_travelling_abroad&linkpos=topnav~1~3~1~3")
        response.raise_for_status()  # Raise an error for bad responses
        # The response is in text format
        faq_data = response.text
        # load this into beautifulsoup to parse the HTML
        from bs4 import BeautifulSoup   
        soup = BeautifulSoup(faq_data, 'html.parser')
        # Get the body of the HTML
        faq_data = soup.body.get_text(separator="\n").strip()         
        return faq_data
    except requests.RequestException as e:
        return f"Error fetching FAQ data: {str(e)}"
