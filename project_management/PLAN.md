# Project Plan
---

### 1. Initial Structure

| Objective | Statut |
| :-------: | :----: |
| Create the github repo | ✅ |
| Create the Makefile | ✅ |

### 2. Rules

| Objective | Statut |
| :-------: | :----: |
| Using the model **Qwen/Qwen3-0.6B** | ❌ |
| Provide a CLI using Python Fire | ❌ |
| Implemente a progress bars using `tqdm` | ❌ |

### 3. RAG

#### 3.1 Knowledge Base Ingestion System

| Objective | Statut |
| :-------: | :----: |
| Give the LLM the VLLM repo (all files) | ❌ |
| Implement intelligent chunking for Python code and Markdown documentation | ❌ |
| Create a searchable knowledge index using `TF-IDF` or `BM25` | ❌ |
| Store the index for fast retrieval (max 5 minutes indexing time) | ❌ |

#### 3.2 Retrieval System

| Implement semantic search over the indexed knowledge base | ❌ |
| Return top-k most relevant code snippets for any querry | ❌ |
| Each result must include: file_path, first_character_index, last_character_index | ❌ |
| Support batch processing of multiple questions from JSON datasets | ❌ |
| Achieve at least 80% recall@5 on docs questions and 50% on code questions | ❌ |

#### 3.3 Answer Generation System

| Pass retrieved context to the LLM withing token limits | ❌ |
| Generate answers based on the retrieved code and documentation | ❌ |
| Output structured JSON following the provided pydantic models | ❌ |

##### Good Answer:

| Readable without seeing the original question | ❌ |
| Cites the source(s) it draws from | ❌ |
| Limits itself to source content (no hallucination) | ❌ |
| Directly answers the queston asked | ❌ |

#### 3.4 Evaluation System

| Implement recall@k metric to measure retrieval quality | ❌ |
| Compare retrieved sources against ground truth annotations | ❌ |
| Calculate overlap between retrieved and correct souces (minimum 5% overlap counts as found) | ❌ |
| Provide detailed performance metrics | ❌ |

### 4. Python Application

| Objective | Statut |
| :-------: | :----: |
| | ❌ |

### 2.

| Objective | Statut |
| :-------: | :----: |
| | ❌ |


### . README

| Objective | Statut |
| :-------: | :----: |
| Global structure of the README | ❌ |
| Initial texts | ❌ |
| Additionals Sections | ❌ |

