import os
import shutil
import openai
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import (LangchainEmbedding, LLMPredictor, ServiceContext,
                         SimpleDirectoryReader, StorageContext,
                         VectorStoreIndex)
from llama_index.vector_stores import RedisVectorStore
from llama_index.storage.storage_context import StorageContext


class ChatDataLoader:

    def __init__(self, nome_collection: str = "default", index_document: str = None, openai_api_key: str = None):
        self.path = "./storage/vector_storage/chromadb/"
        self.__openai_api_key = openai_api_key
        self.index_document = index_document
        self.nome_collection = nome_collection
        self.__create_db()
        self.chat = None

    def __create_db(self):
        vector_store = RedisVectorStore(
            index_name=self.index_document, index_prefix="gptvector_", redis_url="redis://201.87.244.247:6379", overwrite=True)
        self.redis = vector_store

    def save_request(self):
        openai.api_key = self.__openai_api_key
        os.environ.clear()
        os.environ.setdefault("OPENAI_API_KEY", self.__openai_api_key)

    def __create_storage_context(self) -> StorageContext:
        storage_context = StorageContext.from_defaults(vector_store=self.redis)
        return storage_context

    def create_service_context(self) -> ServiceContext:
        llm_predictor = LLMPredictor(llm=ChatOpenAI(
            temperature=0.9, max_tokens=512, model_name='gpt-3.5-turbo', openai_api_key=self.__openai_api_key))
        service_context = ServiceContext.from_defaults(
            llm_predictor=llm_predictor,
            embed_model=LangchainEmbedding(HuggingFaceEmbeddings(model_name='./modelo_embeddings')))
        return service_context

    def add_document_llama(self, documents: list | None = None):
        # load document
        documents_ = SimpleDirectoryReader(input_files=[os.path.join(os.getcwd(), 'filesdata', x) for x in documents]) if documents is not None else SimpleDirectoryReader(
            input_dir=os.path.join(os.getcwd(), "filesdata"))
        VectorStoreIndex.from_documents(
            documents=documents_.load_data(),
            service_context=self.create_service_context(),
            storage_context=self.__create_storage_context(),
            show_progress=True
        )
        # move document to dump
        self.move_document_to_dump(documents=documents)

    @staticmethod
    def move_document_to_dump(documents: list | None = None):
        if not os.path.exists(os.path.join(os.getcwd(), "dumps")):
            os.mkdir(os.path.join(os.getcwd(), "dumps"))
        if documents is None:
            lista_documentos = os.listdir(
                os.path.join(os.getcwd(), "filesdata"))
            for arquivo in lista_documentos:
                shutil.move(os.path.join(os.getcwd(), "filesdata", arquivo),
                            os.path.join(os.getcwd(), "dumps", arquivo))
        else:
            for arquivo in documents:
                shutil.move(os.path.join(os.getcwd(), "filesdata", arquivo),
                            os.path.join(os.getcwd(), "dumps", arquivo))

    def load_index_storage(self):
        load_index = VectorStoreIndex.from_vector_store(
            vector_store=self.redis, service_context=self.create_service_context())
        print(
            f"Index loaded: {load_index.index_id}\n Name: {self.index_document}")
        return load_index.as_chat_engine(chat_mode='context')

    def chat_bot(self, message: str):
        if self.chat is None:
            self.chat = self.load_index_storage()
        return self.chat.chat(message).response


if __name__ == "__main__":
    chat = ChatDataLoader(openai_api_key="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",
                          index_document="cadastro", nome_collection="cadastro")
    # chat.add_document_llama(['cadastro.pdf'])
    while True:
        mensagem = input("Usuario: ")
        if mensagem == "sair":
            break
        print(f"Bot: {chat.chat_bot(mensagem)}\n")
