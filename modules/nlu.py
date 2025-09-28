
import spacy
import re

# load the small English model for spaCy
nlp = spacy.load("en_core_web_sm")

KNOWN_BRANDS = ["innovate ai co.", "connective living", "datacorp", "audiophonic"]
KNOWN_CATEGORIES = ["software", "electronics"]

def parse_query(user_query: str) -> dict:
    """
    Parses a natural language query to extract structured entities for database querying.
    
    Args:
        user_query: The user's question in plain English.

    Returns:
        A dictionary containing the extracted entities.
    """

    query_lower = user_query.lower()
    doc = nlp(query_lower)
    
    entities = {}
    

    for brand in KNOWN_BRANDS:
        if brand in query_lower:
            entities['brand'] = brand.title() 
            
    for category in KNOWN_CATEGORIES:
        if category in query_lower:
            entities['category'] = category.title()

 
    price_conditions = {}
    
 
    numbers = [token.text for token in doc if token.like_num]
    
    if numbers:
   
        numeric_values = [float(n) for n in numbers]
        
        if "between" in query_lower and len(numeric_values) == 2:
            price_conditions['$gte'] = min(numeric_values)
            price_conditions['$lte'] = max(numeric_values)
        elif "less than" in query_lower or "under" in query_lower:
            price_conditions['$lt'] = numeric_values[0]
        elif "more than" in query_lower or "over" in query_lower or "above" in query_lower:
            price_conditions['$gt'] = numeric_values[0]

    if price_conditions:
        entities['price'] = price_conditions

    rating_conditions = {}
    if "rating" in query_lower:
        rating_numbers = [float(token.text) for token in doc if token.like_num and token.i > doc.text.find("rating")]
        if rating_numbers:
            if "above" in query_lower or "over" in query_lower:
                rating_conditions['$gt'] = rating_numbers[0]
            elif "below" in query_lower or "under" in query_lower:
                rating_conditions['$lt'] = rating_numbers[0]

    if rating_conditions:
        entities['ratings.average'] = rating_conditions
        
    return entities

if __name__ == '__main__':
    test_queries = [
        "show me electronics",
        "find software from Innovate AI Co.",
        "show me products with a price under 500",
        "find products with a price between 100 and 300",
        "show me electronics from audiophonic with a price over 200",
        "find products with a rating above 4.6"
    ]
    
    for query in test_queries:
        parsed_entities = parse_query(query)
        print(f"Query: '{query}'")
        print(f"Parsed: {parsed_entities}\n")