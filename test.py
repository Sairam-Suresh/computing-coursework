from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define two sentences
sentence1 = "I do not want engineering. Engineering."
sentence2 = "I do not want engineering. Engineering."
#sentence2 = "The SAF Engineering Scholarship is for military engineers-to-be, who are ready to serve the nation and be groomed as leaders with specific deep specialisation in engineering. The scholarship equips you with a world-class education and training to spearhead in-depth engineering studies, as well as design and operationalise high-end technological capabilities for the SAF."

# Create CountVectorizer object
vectorizer = CountVectorizer()

# Fit and transform the sentences
vectorized_sentences = vectorizer.fit_transform([sentence1, sentence2])

# Calculate cosine similarity
cosine_sim = cosine_similarity(vectorized_sentences)

print("Cosine similarity between the two sentences:", cosine_sim[0][1])