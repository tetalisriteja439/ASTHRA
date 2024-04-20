from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex,SummaryIndex,StorageContext,SimpleKeywordTableIndex
from llama_index.embeddings.openai import OpenAIEmbedding



def vector_storing(db_path,embedding_model,collection_name,nodes,mode):
    db = chromadb.PersistentClient(path=db_path)
    embed_model = OpenAIEmbedding(model=embedding_model)
    chroma_collection = db.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    if mode =='VectorStoreIndex':
        index = VectorStoreIndex(
            nodes = nodes , embed_model=embed_model
        )
    elif mode =='SummaryIndex':
        index = SummaryIndex(
            nodes = nodes , embed_model=embed_model
        )
    elif mode =='SimpleKeywordTableIndex':
        index = SimpleKeywordTableIndex(
            nodes = nodes , embed_model=embed_model
        )
    index.storage_context.persist(persist_dir=db_path)
    return index