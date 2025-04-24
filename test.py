from serpapi import GoogleSearch

params = {
  "engine": "google",
  "q": "Coffee",
  "api_key": "e7fc3656a8e82b062a50c7e63f54c74531e9b7e3bb759d24bb28b04eddf1395a"
}

search = GoogleSearch(params)
results = search.get_dict()
organic_results = results["organic_results"]

for results in organic_results:
    titles = results["title"]
    links = results["link"]
    redirect_links = results["redirect_link"]
    displayed_links = results["displayed_link"]
    snippets = results["snippet"]

    print(f"Title: {titles}")
    print(f"Link: {links}")
    print(f"Redirect Link: {redirect_links}")
    print(f"Displayed Link: {displayed_links}")
    print(f"Snippet: {snippets}")