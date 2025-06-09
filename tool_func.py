from langchain_core.tools import tool
import json

@tool
def property_search(query: str = "") -> str:
    """Search for properties based on user criteria. Input should be the search query."""
    try:
        with open('conventional_properties.json', 'r') as file:
            property_data = json.load(file)
        
        properties = property_data.get("data", [])
        
        # Format the properties data for better readability
        formatted_properties = []
        for prop in properties:
            formatted_prop = f"""
               Property ID: {prop.get('id', 'N/A')}
               Name: {prop.get('name', 'N/A')}
               Location: {prop.get('full_address', 'N/A')}
               Area Available: {prop.get('area_available', 'N/A')} square ft
               Rent per sq ft: ₹{prop.get('quoted_rent_per_sqft', 'N/A')}
            """
            formatted_properties.append(formatted_prop.strip())
        
        return "\n" + "="*50 + "\n".join(formatted_properties) + "\n" + "="*50
        
    except FileNotFoundError:
        return "Property database file not found."
    except json.JSONDecodeError:
        return "Error reading property database."
    except Exception as e:
        return f"Error accessing property data: {str(e)}"