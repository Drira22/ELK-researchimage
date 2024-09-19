import streamlit as st
from elasticsearch import Elasticsearch

# Establish a connection to Elasticsearch
es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200, "scheme": "http"}])

def search_images(keyword):
    """Search Elasticsearch for images based on the keyword."""
    query = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["tags", "title"]
            }
        },
        "size": 10  # Number of results to return
    }
    results = es.search(index="flickrphotos", body=query)
    return results

def display_results(results):
    """Display the image and its title without extra details."""
    for hit in results['hits']['hits']:
        # Extract the relevant fields
        title = hit["_source"]["title"]
        image_id = hit["_source"]["id"]
        flickr_secret = hit["_source"]["flickr_secret"]
        flickr_server = hit["_source"]["flickr_server"]
        flickr_farm = hit["_source"]["flickr_farm"]

        # Construct the image URL
        image_url = f"http://farm{flickr_farm}.staticflickr.com/{flickr_server}/{image_id}_{flickr_secret}.jpg"
        
        # Display the image and its title
        st.image(image_url, caption=title, width=300)

# Streamlit interface
st.title("Flickr Image Search")
keyword = st.text_input("Enter a keyword:")
if st.button("Search"):
    if keyword:
        try:
            results = search_images(keyword)
            if results['hits']['total']['value'] > 0:
                display_results(results)
            else:
                st.write("No results found")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.write("Please enter a keyword to search.")
