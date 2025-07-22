import os
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class SimpleRAG:
    def __init__(self, documents_path="docs/policies/"):
        self.documents_path = documents_path
        self.documents = {}
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.doc_vectors = None
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        self._load_documents()
        self._create_vectors()
    
    def _load_documents(self):
        """Load all policy documents from the directory"""
        if not os.path.exists(self.documents_path):
            print(f"Documents path {self.documents_path} not found")
            return
        
        for filename in os.listdir(self.documents_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.documents_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.documents[filename] = {
                            'content': content,
                            'title': filename.replace('.txt', '').replace('_', ' ').title()
                        }
                        print(f"Loaded document: {filename}")
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
    
    def _create_vectors(self):
        """Create TF-IDF vectors for all documents"""
        if not self.documents:
            print("No documents loaded for vectorization")
            return
        
        doc_contents = [doc['content'] for doc in self.documents.values()]
        self.doc_vectors = self.vectorizer.fit_transform(doc_contents)
        print(f"Created vectors for {len(self.documents)} documents")
    
    def search_documents(self, query, top_k=3):
        """Search documents using TF-IDF similarity"""
        if self.doc_vectors is None:
            return []
        
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.doc_vectors)[0]
        
        # Get top-k most similar documents
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                doc_key = list(self.documents.keys())[idx]
                results.append({
                    'document': doc_key,
                    'title': self.documents[doc_key]['title'],
                    'content': self.documents[doc_key]['content'],
                    'similarity': similarities[idx]
                })
        
        return results
    
    def generate_response(self, query, max_tokens=500):
        """Generate response using retrieved documents and OpenAI"""
        # Search for relevant documents
        relevant_docs = self.search_documents(query, top_k=3)
        
        if not relevant_docs:
            return {
                'response': "I couldn't find relevant policy documents to answer your question.",
                'sources': []
            }
        
        # Create context from relevant documents
        context = "Based on the following policy documents:\n\n"
        sources = []
        
        for i, doc in enumerate(relevant_docs, 1):
            context += f"Document {i}: {doc['title']}\n"
            context += f"{doc['content'][:800]}...\n\n"  # First 800 chars
            sources.append(doc['title'])
        
        # Create prompt for OpenAI
        prompt = f"""You are a policy expert analyzing regional economic resilience. 
        
{context}

Question: {query}

Please provide a comprehensive answer based on the policy documents above. Focus on practical recommendations and cite specific policies or strategies mentioned in the documents. Keep your response concise but informative."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in regional economic policy and development."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return {
                'response': response.choices[0].message.content.strip(),
                'sources': sources
            }
        
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return {
                'response': "I encountered an error while generating a response. Please try again.",
                'sources': sources
            }
    
    def get_sample_queries(self):
        """Return sample queries for testing"""
        return [
            "What strategies promote economic diversification in regions?",
            "How can manufacturing contribute to regional resilience?",
            "What are the main challenges for rural economic development?",
            "How do urban areas build economic resilience?",
            "What role does workforce development play in regional resilience?",
            "How can regions improve access to capital for small businesses?",
            "What infrastructure investments support economic competitiveness?"
        ]

if __name__ == "__main__":
    # Test the RAG system
    rag = SimpleRAG()
    
    print("Testing RAG System with Sample Queries:")
    print("=" * 50)
    
    sample_queries = rag.get_sample_queries()
    
    for i, query in enumerate(sample_queries[:2], 1):  # Test first 2 queries
        print(f"\nQuery {i}: {query}")
        print("-" * 40)
        
        result = rag.generate_response(query)
        print("Response:")
        print(result['response'])
        print(f"\nSources: {', '.join(result['sources'])}")
        print("=" * 50)