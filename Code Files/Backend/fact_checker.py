import wikipedia

def verify_topic(topic: str):
    """Wikipedia Search + Summary"""
    try:
        # Step 1: Search for closest matching pages
        search_results = wikipedia.search(topic, results=3)
        
        if not search_results:
            return {
                "verified": False,
                "summary": f"No Wikipedia page found for '{topic}'",
                "url": ""
            }
        
        # Step 2: Take the first best match and get summary
        best_match = search_results[0]
        summary = wikipedia.summary(best_match, sentences=2)
        page = wikipedia.page(best_match)
        
        return {
            "verified": True,
            "summary": f"Related to: {best_match}\n\n{summary}",
            "url": page.url
        }
    except wikipedia.DisambiguationError as e:
        # If multiple options
        options = ", ".join(e.options[:3])
        return {
            "verified": False,
            "summary": f"Multiple results found. Try: {options}",
            "url": ""
        }
    except:
        return {
            "verified": False,
            "summary": f"No wikipedia page found for '{topic}'.",
            "url": ""
        }
        