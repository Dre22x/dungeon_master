import os
import google.auth
from google.cloud import firestore
from google.oauth2 import service_account

# Set up Google Cloud credentials using service account key
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "service-account-key.json")

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_PATH

# ==============================================================================
#  DATABASE INITIALIZATION
# ==============================================================================


def get_db_client():
    """Initializes and returns a Firestore client."""
    try:
        # Use service account credentials
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH)
        db = firestore.Client(credentials=credentials)
        print("[DatabaseManager] Firestore client initialized successfully.")
        return db
    except Exception as e:
        print(f"[DatabaseManager] FATAL: Could not initialize Firestore client: {e}")
        print(f"[DatabaseManager] Please ensure the service account key file exists at: {SERVICE_ACCOUNT_PATH}")
        return None

db = get_db_client()

# ==============================================================================
#  DATABASE TOOL FUNCTIONS
# ==============================================================================

# --- Database Management Tools ---

def clear_database():
    """
    Completely clears all data from the Firestore database.
    WARNING: This will delete ALL documents in ALL collections!
    """
    if not db:
        return "Error: Database client is not available."
    
    try:
        # Get all collections
        collections = db.collections()
        deleted_count = 0
        
        for collection in collections:
            collection_name = collection.id
            print(f"[DatabaseManager] Clearing collection: {collection_name}")
            
            # Get all documents in the collection
            docs = collection.stream()
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
                print(f"[DatabaseManager] Deleted document: {doc.id}")
        
        print(f"[DatabaseManager] Database cleared successfully. Deleted {deleted_count} documents.")
        return f"Database cleared successfully. Deleted {deleted_count} documents."
        
    except Exception as e:
        return f"Error clearing database: {e}"

def list_all_collections():
    """
    Lists all collections in the database.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        collections = list(db.collections())
        collection_names = [col.id for col in collections]
        print(f"[DatabaseManager] Found {len(collection_names)} collections: {collection_names}")
        return {
            "collections": collection_names,
            "count": len(collection_names)
        }
    except Exception as e:
        return {"error": f"Error listing collections: {e}"}

def list_documents_in_collection(collection_name: str):
    """
    Lists all documents in a specific collection.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.stream()
        
        documents = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['_id'] = doc.id
            documents.append(doc_data)
        
        print(f"[DatabaseManager] Found {len(documents)} documents in collection '{collection_name}'")
        return {
            "collection": collection_name,
            "documents": documents,
            "count": len(documents)
        }
    except Exception as e:
        return {"error": f"Error listing documents in collection '{collection_name}': {e}"}

def get_database_stats():
    """
    Gets statistics about the database including collection counts and document counts.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        collections = list(db.collections())
        stats = {
            "total_collections": len(collections),
            "collections": {}
        }
        
        total_documents = 0
        
        for collection in collections:
            collection_name = collection.id
            docs = list(collection.stream())
            doc_count = len(docs)
            total_documents += doc_count
            
            stats["collections"][collection_name] = {
                "document_count": doc_count,
                "documents": [doc.id for doc in docs]
            }
        
        stats["total_documents"] = total_documents
        
        print(f"[DatabaseManager] Database stats: {stats['total_collections']} collections, {total_documents} total documents")
        return stats
        
    except Exception as e:
        return {"error": f"Error getting database stats: {e}"}

def search_documents(collection_name: str, field_name: str, field_value):
    """
    Searches for documents in a collection where a specific field matches a value.
    """
    if not db:
        return {"error": "Database client is not available."}
    
    try:
        collection_ref = db.collection(collection_name)
        query = collection_ref.where(field_name, "==", field_value)
        docs = query.stream()
        
        results = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['_id'] = doc.id
            results.append(doc_data)
        
        print(f"[DatabaseManager] Found {len(results)} documents in '{collection_name}' where {field_name} == {field_value}")
        return {
            "collection": collection_name,
            "search_field": field_name,
            "search_value": field_value,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        return {"error": f"Error searching documents: {e}"}
    