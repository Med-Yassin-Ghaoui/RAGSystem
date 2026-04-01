import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
from inngest.experimental import ai
from dotenv import load_dotenv
import uuid
import os
import datetime
from data_loader import load_and_chunk_pdf, embed_texts
from custom_types import RAGChunkAndSrc, RAGQueryResult,RAGSearchResult,RAGUpsertResult
from vector_db import QdrantStorage
import google.genai as genai
#load dotenv loads the enviroment variables inside of the .env file
load_dotenv()

inngest_client = inngest.Inngest(
    app_id='rag_app',
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer()


)

#the decorator
@inngest_client.create_function(
    fn_id="RAG: Ingest PDF",
    trigger=inngest.TriggerEvent(event="rag/ingest_pdf")
)
async def rag_ingest_pdf(ctx: inngest.Context):
    #we're going to have two individual steps happening in this function, loading then embedding and add to vector database
 
    def _load(ctx: inngest.Context) -> RAGChunkAndSrc :
        pdf_path= ctx.event.data["pdf_path"]
        source_id = ctx.event.data.get("source_id", pdf_path)
        chunks= load_and_chunk_pdf(pdf_path)
        return RAGChunkAndSrc(chunks=chunks, source_id=source_id)

    def _upsert(chunks_and_src: RAGChunkAndSrc) -> RAGUpsertResult : 
        chunks = chunks_and_src.chunks
        source_id=chunks_and_src.source_id
        vecs = embed_texts(chunks)
        ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_id}:{i}")) for i in range (len(chunks))]
        payloads = [{"source": source_id, "text": chunks[i]} for i in range (len(chunks))]
        QdrantStorage().upsert(ids, vecs, payloads)
        return RAGUpsertResult(ingested= len(chunks))
    
    #this is how to call the functions
    chunks_and_src = await ctx.step.run("load-and-chunk", lambda: _load(ctx),output_type=RAGChunkAndSrc)
    ingested = await ctx.step.run ("embed-and-upsert", lambda : _upsert(chunks_and_src), output_type = RAGUpsertResult)
    return ingested.model_dump()

@inngest_client.create_function(
    fn_id="RAG: Query PDF",
    trigger=inngest.TriggerEvent(event="rag/query_pdf_ai")
)

async def rag_query_pdf_ai (ctx: inngest.Context):
    def _search(question: str, top_k: int = 5)-> RAGSearchResult : 
        query_vec = embed_texts([question])[0]
        store = QdrantStorage()
        found = store.search(query_vec, top_k)
        return RAGSearchResult(contexts=found["contexts"], sources=found["sources"])
    
    question= ctx.event.data["question"]
    top_k = int(ctx.event.data.get("top_k",5))

    found=await ctx.step.run("embed-and-search", lambda: _search(question, top_k), output_type = RAGSearchResult)


    context_block = "\n\n".join(f"- {c}" for c in found.contexts)

    user_content = (
        "You answer questions using only the provided context.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Answer concisely using the context above."
    )

    def _generate_answer(prompt: str) -> str:
        client = genai.Client(api_key=os.getenv("GOOGLE_API"))

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config={
            "max_output_tokens": 1024,
            "temperature": 0.2,
            }
        )

        return response.text.strip()

    answer = await ctx.step.run(
        "llm-answer",
        lambda: _generate_answer(user_content)
    )

    return {
        "answer": answer,
        "sources": found.sources,
        "num_contexts": len(found.contexts)
    }

app=FastAPI()

inngest.fast_api.serve(app, inngest_client, [rag_ingest_pdf, rag_query_pdf_ai])
