import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    PayloadSchemaType
)
from app.core.logger import logger
from app.core.config import settings
from qdrant_client.models import Filter, FieldCondition, MatchValue

class QdrantVectorStore:

    def __init__(self):

        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )

        self.collection_name = settings.QDRANT_COLLECTION

        self._ensure_collection()

    def _ensure_collection(self):

        try:

            if not self.client.collection_exists(self.collection_name):

                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=384,
                        distance=Distance.COSINE
                    )
                )

                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="user_id",
                    field_schema=PayloadSchemaType.KEYWORD
                )

                logger.info(f"Created collection: {self.collection_name}")

            else:
                logger.info(f"Collection exists: {self.collection_name}")

        except Exception as e:
            logger.error(f"Collection setup error: {e}")

    def add_embeddings(
        self,
        embeddings,
        chunks,
        document_id,
        user_id
    ):

        try:

            user_id = str(user_id)

            points = []

            for emb, chunk in zip(embeddings, chunks):

                # convert numpy/tensor -> plain python list
                vector = emb.tolist() if hasattr(emb, "tolist") else emb

                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={
                            "document_id": str(document_id),
                            "user_id": user_id,
                            "text": chunk,
                            "embedding": vector
                        }
                    )
                )

            logger.info(f"Uploading {len(points)} points")

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info("Qdrant upsert successful")

        except Exception as e:
            logger.error(f"Add embeddings error: {e}")
            raise

    def search(
        self,
        query_embedding,
        user_id,
        k=20
    ):

        try:

            user_id = str(user_id)

            # convert numpy/tensor -> plain python list
            query_vector = (
                query_embedding.tolist()
                if hasattr(query_embedding, "tolist")
                else query_embedding
            )

            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=k,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=user_id)
                        )
                    ]
                )
            )

            results = response.points

            logger.info(f"Retrieved {len(results)} results")

            formatted = []

            for r in results:

                formatted.append({
                    "document_id": r.payload.get("document_id") if r.payload else None,
                    "text": r.payload.get("text") if r.payload else None,
                    "embedding": r.payload.get("embedding") if r.payload else None,
                    "score": r.score
                })
            return formatted

        except Exception as e:
            logger.error(f"Search error: {e}")
            raise


    def delete_document_vectors( self, document_id: str ):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(
                            value=document_id
                        )
                    )
                ]
            )
        )


qdrant_store = QdrantVectorStore()