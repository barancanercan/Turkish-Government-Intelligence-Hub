"""
Vector Store Updater
Incremental update for vector database
"""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


class VectorUpdater:
    """
    Handles incremental updates to the vector store.
    """
    
    def __init__(self, vectorstore=None, embeddings=None):
        self.vectorstore = vectorstore
        self.embeddings = embeddings
        self.metadata_store = {}
    
    def set_vectorstore(self, vectorstore, embeddings):
        """
        Set vector store and embeddings.
        
        Args:
            vectorstore: Chroma vector store
            embeddings: Embedding model
        """
        self.vectorstore = vectorstore
        self.embeddings = embeddings
    
    def compute_content_hash(self, content: str) -> str:
        """
        Compute hash of content for change detection.
        
        Args:
            content: Content to hash
            
        Returns:
            Hash string
        """
        return hashlib.md5(content.encode()).hexdigest()
    
    async def add_documents(
        self,
        documents: List[Dict[str, Any]],
        collection_name: str = "news",
    ) -> Dict[str, Any]:
        """
        Add documents to vector store.
        
        Args:
            documents: List of document dictionaries
            collection_name: Collection name
            
        Returns:
            Result statistics
        """
        if not self.vectorstore or not self.embeddings:
            logger.warning("Vector store not initialized")
            return {"added": 0, "errors": 0}
        
        from langchain_core.documents import Document
        
        docs_to_add = []
        ids_to_add = []
        
        for doc in documents:
            try:
                content = doc.get("content", "")
                if not content or len(content) < 20:
                    continue
                
                content_hash = self.compute_content_hash(content)
                
                if self._is_duplicate(content_hash, collection_name):
                    continue
                
                metadata = {
                    "id": doc.get("id", ""),
                    "source": doc.get("source", ""),
                    "url": doc.get("url", ""),
                    "title": doc.get("title", ""),
                    "party": doc.get("party", ""),
                    "content_hash": content_hash,
                    "created_at": datetime.now().isoformat(),
                    "collection": collection_name,
                }
                
                langchain_doc = Document(
                    page_content=content,
                    metadata=metadata,
                )
                
                doc_id = doc.get("id", content_hash[:16])
                docs_to_add.append(langchain_doc)
                ids_to_add.append(doc_id)
                
                self._store_metadata(doc_id, content_hash, collection_name)
                
            except Exception as e:
                logger.error(f"Error preparing document: {e}")
        
        if docs_to_add:
            try:
                self.vectorstore.add_documents(docs_to_add, ids=ids_to_add)
                logger.info(f"Added {len(docs_to_add)} documents to {collection_name}")
            except Exception as e:
                logger.error(f"Error adding documents: {e}")
                return {"added": 0, "errors": len(docs_to_add)}
        
        return {
            "added": len(docs_to_add),
            "skipped": len(documents) - len(docs_to_add),
            "errors": 0,
        }
    
    def _is_duplicate(self, content_hash: str, collection: str) -> bool:
        """
        Check if content already exists.
        
        Args:
            content_hash: Hash of content
            collection: Collection name
            
        Returns:
            True if duplicate
        """
        key = f"{collection}:{content_hash}"
        return key in self.metadata_store
    
    def _store_metadata(self, doc_id: str, content_hash: str, collection: str):
        """
        Store metadata for change detection.
        
        Args:
            doc_id: Document ID
            content_hash: Content hash
            collection: Collection name
        """
        key = f"{collection}:{content_hash}"
        self.metadata_store[key] = {
            "doc_id": doc_id,
            "content_hash": content_hash,
            "collection": collection,
            "stored_at": datetime.now().isoformat(),
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get update statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            "total_stored": len(self.metadata_store),
            "collections": list(set(
                v["collection"] for v in self.metadata_store.values()
            )),
        }


async def update_vector_store(
    documents: List[Dict[str, Any]],
    vectorstore=None,
    embeddings=None,
    collection_name: str = "news",
) -> Dict[str, Any]:
    """
    Convenience function to update vector store.
    
    Args:
        documents: Documents to add
        vectorstore: Vector store
        embeddings: Embeddings
        collection_name: Collection name
        
    Returns:
        Update result
    """
    updater = VectorUpdater(vectorstore, embeddings)
    return await updater.add_documents(documents, collection_name)
