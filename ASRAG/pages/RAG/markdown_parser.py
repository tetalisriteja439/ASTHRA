from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core.node_parser import MarkdownElementNodeParser


def markdown_parser(documents):

    # for the purpose of this example, we will use the small model embedding and gpt3.5
    # embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    llm = OpenAI(model="gpt-3.5-turbo-0125")

    Settings.llm = llm

    node_parser = MarkdownElementNodeParser(
        llm=OpenAI(model="gpt-3.5-turbo-0125"), num_workers=8
    )

    nodes = node_parser.get_nodes_from_documents(documents)

    base_nodes, objects = node_parser.get_nodes_and_objects(nodes)

    return base_nodes, objects