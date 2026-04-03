documents = [
    "Exercise improves brain memory",
    "Sleep helps memory retention",
    "Reading boosts knowledge",
    "Meditation improves focus and recall",
    "Eating healthy improves brain function"
]

def simple_search(query, docs):
    results = []
    for doc in docs:
        if query.lower() in doc.lower():
            results.append(doc)
    return results

def fan_out_search(user_query):
    queries = [
        user_query,
        'memory improvement',
        'brain health',
        'recall teachniques'
    ]

    all_results = []
    for q in queries:
        res = simple_search(q, documents)
        all_results.extend(res)

    return list(set(all_results))

results = fan_out_search("memory")
print(results)