__author__ = 'kault'

import urllib2

### This is a simple Internet search engine created with the Intro to CS course
### on udacity.com. Still in alpha, still buggy, still working on it. Future
### revisions will rank and list results. 


### INDEX: [[keyword1, [url1,1 , url1,2 , ...]],
###         [keyword2, [url2,1 , ...]] ...]


# From urllib2, gets page source code
# Would like to investigate how this works
def get_page(url):
    return urllib2.urlopen(url).read()


# Finds the next 'target' link in a source code page
def get_next_target(page):
    start_link = page.find('<a href=')

    if start_link == -1:
        return None, 0
    else:
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote + 1:end_quote]
        return url, end_quote


# Extracts all links from a source code page. Currently buggy
def get_all_links(page):
    links = []
    while page:
        url, end_pos = get_next_target(page)
        if url:
            links.append(url)
            page = page[end_pos:]
        else:
            break
    return links


# Appends elements in second list to first list unless they are already there
def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)


#how do we change this so that rather than have a list of URLs, we're
#building up our index
def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        page = tocrawl.pop()            # URL
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
    return index


# If keyword is in index, add url to the list of assoc. URLs
# If keyword is not in index, add an entry [keyword, [url]]
def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    index.append([keyword, [url]])


# Looks in index to see if word is in it. Returns [] if it isn't there,
# returns list of a list of keywords if it is.
def lookup(index, word):
    for entry in index:
        if entry[0] == word:
            return entry[1]
    return []


# Uses .split() on the source page, garnering keywords. These keywords are
# then added to the index
def add_page_to_index(index, url, content):
    list_of_words = content.split()
    for word in list_of_words:
        add_to_index(index, word, url)


## Takes a seed page, crawls to specified max_depth
## Max depth of 0 returns page, 1 returns page + its links
#def crawl_web(seed, max_depth):
#    tocrawl = [seed]
#    crawled = []
#    next_depth = []
#    depth = 0
#    while tocrawl and depth <= max_depth:
#        page = tocrawl.pop()
#        if page not in crawled:
#            union(tocrawl, get_all_links(get_page(page)))
#            crawled.append(page)
#        if not tocrawl:
#            tocrawl, next_depth = next_depth, []
#            depth += 1
#    return crawled