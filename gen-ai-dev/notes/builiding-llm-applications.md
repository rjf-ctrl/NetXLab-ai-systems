# FUNDAMENTALS

## EMBEDDINGS
- turning text into vdectors while considering semnatic relationships
- ![alt text](images/image.png)

### VECTOR DATABASE
- Audio -> audio model -> audio vector embeddings -> eg.RedisSearch Vector Similarity Search
- Text -> text vector embeddings, etc.
- Vector databases are optimised storing, indexing and retrieving unstructured data
- When a new object (say, word) is inserted, the semantically similar set of objets is found using various indeixing techniques
- ![alt text](images/image-1.png)

Vector Similarity: (common measures) 1. Cosine Similarity 2. Euclidian Distance
![alt text](images/image-2.png)

- FOUNDATIONAL MODEL: llms trained on massive amounts of public data eg: ChatGPT

### CONTEXT WINDOW AND TOKEN LIMITS
- token = unit of text read by model
- context window ~ RAM for LLM
- when context window exceeded it cannot work on previously mentioned content
- Input tokens->Predict next token->Add it to context->Predict another

## CUSTOMIZING LLMs
![alt text](images/image-3.png)
![alt text](images/image-4.png)
![alt text](images/image-5.png)
- ![alt text](images/image-6.png)
- ![alt text](images/image-7.png)
- llms have cache to answer re-questions
### INTEGRATION
- ![alt text](images/image-8.png)