def build_query(entities: dict) -> dict:
    """
    Builds a MongoDB query document from a dictionary of parsed entities.

    Args:
        entities: A dictionary of entities extracted from the NLU module.
                  Example: {'category': 'Electronics', 'price': {'$gt': 200.0}}

    Returns:
        A dictionary representing a valid MongoDB query.
    """
    if not entities:
        return {} 

    conditions = []
    

    for key, value in entities.items():
  
        if key in ['brand', 'category']:
             conditions.append({key: {"$regex": f"^{value}$", "$options": "i"}})
        else:
        
            conditions.append({key: value})


    if len(conditions) > 1:
        return {"$and": conditions}

    elif conditions:
        return conditions[0]

    else:
        return {}


if __name__ == '__main__':

    test_entities = [
        {'category': 'Electronics'},
        {'brand': 'Innovate Ai Co.', 'category': 'Software'},
        {'price': {'$lt': 500.0}},
        {'price': {'$gte': 100.0, '$lte': 300.0}},
        {'brand': 'Audiophonic', 'category': 'Electronics', 'price': {'$gt': 200.0}},
        {'ratings.average': {'$gt': 4.6}}
    ]

    for i, entities in enumerate(test_entities):
        mongo_query = build_query(entities)
        print(f"--- Test Case {i+1} ---")
        print(f"Input Entities: {entities}")
        print(f"Generated Query: {mongo_query}\n")