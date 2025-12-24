
from qa import llm
from vector import directory_ingest
from vector import chroma_store
# -------------------------------------------------
# CONFIG
# -------------------------------------------------
DOCUMENT_PATH = "resource"
COLLECTION_NAME = "documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama3"

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    print("🚀 Starting Document Understanding Pipeline")

    directory_ingest.ingest_directory(DOCUMENT_PATH)

    # Ask question
    while True:
        question = input("\n❓ Ask a question (or type 'exit'): ")
        if question.lower() == "exit":
            break

        context = chroma_store.retrieve_context(question)
        answer = llm.ask_llm(context, question)

        print("\n🧠 Answer:")
        print(answer)

# -------------------------------------------------
if __name__ == "__main__":
    main()
