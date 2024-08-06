from openai import OpenAI
import networkx as nx
from cdlib import algorithms
import os
from dotenv import load_dotenv
import json
from bs4 import BeautifulSoup
from LLMmodule import get_llm_response


input_file_path = "../MLModelTraining/covenants.json"

# 1. Source Documents → Text Chunks
def split_documents_into_chunks(documents, chunk_size=600, overlap_size=100):
    chunks = []
    for document in documents:
        for i in range(0, len(document), chunk_size - overlap_size):
            chunk = document[i:i + chunk_size]
            chunks.append(chunk)
    return chunks


# 2. Text Chunks → Element Instances
def extract_elements_from_chunks(chunks):
    elements = []
    for index, chunk in enumerate(chunks):
        print(f"Chunk index {index} of {len(chunks)}:")
        llm_response = get_llm_response("Extract entities and relationships from the following text.", chunk)
        print(llm_response)
        entities_and_relations = llm_response
        elements.append(entities_and_relations)

    return elements


# 3. Element Instances → Element Summaries
def summarize_elements(elements):
    summaries = []
    for index, element in enumerate(elements):
        print(f"Element index {index} of {len(elements)}:")
        llm_response = get_llm_response("Summarize the following entities and relationships in a structured format. Use \"->\" to represent relationships, after the \"Relationships:\" word.", element)
        print("Element summary:", llm_response)
        summary = llm_response
        summaries.append(summary)
    return summaries


# 4. Element Summaries → Graph Communities
def build_graph_from_summaries(summaries):
    G = nx.Graph()
    for index, summary in enumerate(summaries):
        print(f"Summary index {index} of {len(summaries)}:")
        lines = summary.split("\n")
        entities_section = False
        relationships_section = False
        entities = []
        for line in lines:
            if line.startswith("### Entities:") or line.startswith("**Entities:**"):
                entities_section = True
                relationships_section = False
                continue
            elif line.startswith("### Relationships:") or line.startswith("**Relationships:**"):
                entities_section = False
                relationships_section = True
                continue
            if entities_section and line.strip():
                if line[0].isdigit() and line[1] == ".":
                    line = line.split(".", 1)[1].strip()
                entity = line.strip()
                entity = entity.replace("**", "")
                entities.append(entity)
                G.add_node(entity)
            elif relationships_section and line.strip():
                parts = line.split("->")
                if len(parts) >= 2:
                    source = parts[0].strip()
                    target = parts[-1].strip()
                    relation = " -> ".join(parts[1:-1]).strip()
                    G.add_edge(source, target, label=relation)
    return G


# 5. Graph Communities → Community Summaries
def detect_communities(graph):
    communities = []
    index = 0
    for component in nx.connected_components(graph):
        print(
            f"Component index {index} of {len(list(nx.connected_components(graph)))}:")
        subgraph = graph.subgraph(component)
        if len(subgraph.nodes) > 1:  # Leiden algorithm requires at least 2 nodes
            try:
                sub_communities = algorithms.leiden(subgraph)
                for community in sub_communities.communities:
                    communities.append(list(community))
            except Exception as e:
                print(f"Error processing community {index}: {e}")
        else:
            communities.append(list(subgraph.nodes))
        index += 1
    print("Communities from detect_communities:", communities)
    return communities


def summarize_communities(communities, graph):
    community_summaries = []
    for index, community in enumerate(communities):
        print(f"Summarize Community index {index} of {len(communities)}:")
        subgraph = graph.subgraph(community)
        nodes = list(subgraph.nodes)
        edges = list(subgraph.edges(data=True))
        description = "Entities: " + ", ".join(nodes) + "\nRelationships: "
        relationships = []
        for edge in edges:
            relationships.append(
                f"{edge[0]} -> {edge[2]['label']} -> {edge[1]}")
        description += ", ".join(relationships)

        llm_response = get_llm_response("Summarize the following community of entities and relationships.", description)
        summary = llm_response.strip()
        community_summaries.append(summary)
    return community_summaries


# 6. Community Summaries → Community Answers → Global Answer
def generate_answers_from_communities(community_summaries, query):
    intermediate_answers = []
    for index, summary in enumerate(community_summaries):
        print(f"Summary index {index} of {len(community_summaries)}:")
        llm_response = get_llm_response("Answer the following query based on the provided summary.", f"Query: {query} Summary: {summary}")
        print("Intermediate answer:", llm_response)
        intermediate_answers.append(llm_response)

    final_response = get_llm_response("Combine these answers into a final, concise response.", f"Intermediate answers: {intermediate_answers}")

    return final_response


# Putting It All Together
def graph_rag_pipeline(documents, query, chunk_size=600, overlap_size=100):

    # Step 1: Split documents into chunks
    chunks = split_documents_into_chunks(
        documents, chunk_size, overlap_size)

    # Step 2: Extract elements from chunks
    elements = extract_elements_from_chunks(chunks)

    # Step 3: Summarize elements
    summaries = summarize_elements(elements)

    # Step 4: Build graph and detect communities
    graph = build_graph_from_summaries(summaries)
    print("graph:", graph)
    communities = detect_communities(graph)

    print("communities:", communities[0])
    # Step 5: Summarize communities
    community_summaries = summarize_communities(communities, graph)

    # Step 6: Generate answers from community summaries
    final_answer = generate_answers_from_communities(
        community_summaries, query)

    return final_answer


with open(input_file_path, 'r') as file:
    data = json.load(file)

for document in data:
    html_content = document['data']['html']
    soup = BeautifulSoup(html_content, 'html.parser')
    full_text = soup.get_text()

    query = ("Please find and annotate a paragraph in the following document that defines any of the following types of covenants. Use **[COVENANT DEFINITION]** to mark the beginning of the paragraph. The types of covenant definitions to look for include:"
             "- Leverage"
             "- ICR (Interest Coverage Ratio))"
             "- FCCR (Fixed Charge Coverage Ratio)"
             "- DtE (Debt-to-EBITDA)"
             "- Networth"
             "- Tan Networth (Tangible Networth)"
             "- CR (Current Ratio)"
             "- QR (Quick Ratio)"
             "- CAPEX (CapEx or Investment)"
             "- Dividend (Dividend and Other Payment Restriction)"
             "- Other"
             "Please note that not all types may be present in the document, so provide any one that you find. For example:"
             "'**[Leverage Covenant Definition]**: As of the last day of any fiscal quarter, permit the Consolidated Total Leverage Ratio to be greater than 2.50 to 1.00.'")

    print('Query:', query)
    answer = graph_rag_pipeline(full_text, query)
    print('Answer:', answer)

    break