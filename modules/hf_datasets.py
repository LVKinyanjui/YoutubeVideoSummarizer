# bookcorpus_downloader.py

from datasets import load_dataset

def download_single_book():
    """
    Downloads a single book from the BookCorpus dataset.
    
    Returns:
    str: The text content of the downloaded book.
    """
    # Load only one example from the BookCorpus dataset
    dataset = load_dataset("bookcorpus", split="train", streaming=True)
    
    # Get the first book
    for book in dataset:
        return book['text']

def get_book_stats(book_text):
    """
    Calculates basic statistics for the given book text.
    
    Args:
    book_text (str): The text content of the book.
    
    Returns:
    dict: A dictionary containing the book statistics.
    """
    return {
        "total_characters": len(book_text),
        "total_words": len(book_text.split()),
        "preview": book_text[:1000]  # First 1000 characters as preview
    }

if __name__ == "__main__":
    # This block will only run if the script is executed directly
    book = download_single_book()
    stats = get_book_stats(book)
    
    print("Book Preview:")
    print(stats["preview"])
    print(f"\nTotal characters: {stats['total_characters']}")
    print(f"Total words: {stats['total_words']}")