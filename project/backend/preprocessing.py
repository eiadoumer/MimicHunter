import re   # regex for word checking and replacement



stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                      'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were',
                      'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
                      'does', 'did', 'doing', 'i', 'you', 'he', 'she', 'it', 'we',
                      'they', 'my', 'your', 'his', 'her', 'its', 'our', 'their']


def clean_text(text):
    
    text= text.lower()  # turn to lower-case  O(n) -> iterating through the whole string
    
    
    #Remove punctuation and digits (replace with space to keep words separate)
    # Regex explained: Keep only letters a-z and whitespace.
    text = re.sub(r'[^a-z\s]', ' ', text)  # O(n)
    
    
    tokens= text.split()   # O(n)
    tokens
    return tokens  # total complexity is O(n) 



def stop_words_removal(tokens):
	filtered_tokens = [word for word in tokens if word not in stop_words]  # O(n) where n is the number of tokens
	return filtered_tokens



def preprocess_text(text):
    cleaned_tokens = clean_text(text)  # O(n)
    filtered_tokens = stop_words_removal(cleaned_tokens)  # O(n)
    return filtered_tokens  # Overall complexity is O(n) where n is the length of the input text





# total complexity of the preprocessing is O(n)





    


