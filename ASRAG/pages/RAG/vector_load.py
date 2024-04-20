from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex,SummaryIndex,SimpleKeywordTableIndex,StorageContext, load_index_from_storage
from llama_index.embeddings.openai import OpenAIEmbedding


def vector_load(db_path,embedding_model,collection_name,mode):
    storage_context = StorageContext.from_defaults(persist_dir=db_path)
    db = chromadb.PersistentClient(path=db_path)
    embed_model = OpenAIEmbedding(model=embedding_model)
    chroma_collection = db.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    # storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # index = eval(mode+".from_vector_store(vector_store, embed_model=embed_model)")
    if mode =='VectorStoreIndex':
        index = VectorStoreIndex.from_vector_store(
            vector_store,  embed_model=embed_model
        )
    elif mode =='SummaryIndex':
        # index = SummaryIndex.from_vector_store(
        #     vector_store,  embed_model=embed_model
        # )
        index = load_index_from_storage(storage_context)
    elif mode =='SimpleKeywordTableIndex':
        index = load_index_from_storage(storage_context)

    return index