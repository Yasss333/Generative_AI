documents = [
    "Exercise improves brain memory" ,
    "Sleep helps memory retention" ,
    "Reading boosts knowledge" ,
    "Meditation improves focus and recall" ,
    "Eating healthy improves brain function"
]


def simple_search(query, docs):
    results = []
    for doc in docs:
        if query.lower() in doc.lower():
            results.append(doc)
    return results

def set_back_query(user_query):
    mapping = {
        "memory": "how human memory works",
        "brain": "brain function and cognition",
        "recall": "information retrieval in humans"
    }
    for key in mapping:
        if key in user_query.lower():
            return mapping[key]
    
    return "General concept of"+user_query

def rrf_fusion(results_list, k=60):
    scores={}
    for result in results_list:
        for rank, doc in enumerate(result):
            if doc not in scores:
                scores[doc]=0
            scores[doc]=+1/(k+rank+1)
    return  sorted(scores.items(),key=lambda x:x[1],reverse=True)

def step_back_rag(user_query):
    step_query=set_back_query(user_query)
    queries=[
        user_query,
        step_query
    ]

    all_results=[]

    for q in queries:
        res=simple_search(q,documents)
        all_results.append(res)

    ranked=rrf_fusion(all_results)

    return ranked


def fan_out_rrf(user_query):
    queries = [
        user_query,
        'memory improvement',
        'brain health',
        'recall techniques'
    ]

    all_results = []

    for q in queries:
        res = simple_search(q, documents)
        all_results.append(res)   # ⚠️ append (important here)

    ranked = rrf_fusion(all_results)

    return ranked

def rag_with_cot(user_query):
    results=step_back_rag(user_query)

    context=" ".join([doc for doc, _ in results[:5]])

    prompt=f"""
    Context:
    {context}
    Question:
    {user_query}

    lets think step by step
    """
    return prompt
results = rag_with_cot("brain")
print(results)