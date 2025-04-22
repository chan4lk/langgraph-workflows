"""
Tools for the bookstore workflow.
This module provides tools for the bookstore agents to interact with the system.
"""

from langchain_core.tools import Tool
from typing import Dict, Any, List, Optional

# Simulated database of books
BOOK_CATALOG = [
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Classic Fiction",
        "age_limit": 14,
        "id": "book-001",
        "in_stock": True,
        "price": 12.99,
        "description": "A portrait of the Jazz Age in all of its decadence and excess."
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": "Fiction",
        "age_limit": 12,
        "id": "book-002",
        "in_stock": True,
        "price": 11.50,
        "description": "The unforgettable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it."
    },
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "age_limit": 10,
        "id": "book-003",
        "in_stock": True,
        "price": 14.99,
        "description": "The first novel in the Harry Potter series, featuring a young wizard's adventures at Hogwarts School of Witchcraft and Wizardry."
    }
]

def search_book_catalog(
    query: str = None,
    genre: str = None,
    age_group: int = None
) -> List[Dict[str, Any]]:
    """
    Search the book catalog for books matching the search criteria.
    
    Args:
        query: General search query (title, author, etc.)
        genre: Genre to filter by
        age_group: Maximum age limit to filter by
        
    Returns:
        List of books matching the criteria
    """
    results = []
    
    for book in BOOK_CATALOG:
        # Check for query match
        query_match = not query or (
            query.lower() in book["title"].lower() or 
            query.lower() in book["author"].lower() or
            query.lower() in book["genre"].lower() or
            query.lower() in book["description"].lower()
        )
        
        # Check for genre match
        genre_match = not genre or genre.lower() in book["genre"].lower()
        
        # Check for age limit match
        age_match = not age_group or book["age_limit"] <= age_group
        
        if query_match and genre_match and age_match:
            results.append(book)
    
    return results

def add_book_to_catalog(
    title: str,
    author: str,
    genre: str,
    age_limit: int,
    price: float = 9.99,
    description: str = ""
) -> Dict[str, Any]:
    """
    Add a new book to the catalog.
    
    Args:
        title: Book title
        author: Book author
        genre: Book genre
        age_limit: Minimum recommended age
        price: Book price (default: 9.99)
        description: Book description (optional)
        
    Returns:
        Newly added book entry
    """
    # Generate a new book ID
    new_id = f"book-{len(BOOK_CATALOG) + 1:03d}"
    
    # Create new book entry
    new_book = {
        "title": title,
        "author": author,
        "genre": genre,
        "age_limit": age_limit,
        "id": new_id,
        "in_stock": True,
        "price": price,
        "description": description
    }
    
    # Add to catalog
    BOOK_CATALOG.append(new_book)
    
    return new_book

def get_book_details(book_id: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific book.
    
    Args:
        book_id: ID of the book to retrieve
        
    Returns:
        Book details or None if not found
    """
    for book in BOOK_CATALOG:
        if book["id"] == book_id:
            return book
    return None

# Define the tools
search_catalog_tool = Tool(
    name="search_book_catalog",
    description="Search for books in the catalog by query, genre, or age group",
    func=search_book_catalog
)

add_book_tool = Tool(
    name="add_book_to_catalog",
    description="Add a new book to the catalog with title, author, genre, and age limit",
    func=add_book_to_catalog
)

get_book_tool = Tool(
    name="get_book_details",
    description="Get detailed information about a specific book by its ID",
    func=get_book_details
)
