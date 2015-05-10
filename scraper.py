import cPickle as pickle
from urllib2 import urlopen
from bs4 import BeautifulSoup
import time
from multiprocessing.dummy import Pool
from sh import curl

def get_search_terms():
    html = urlopen("http://icml.cc/2015/?page_id=710")
    soup = BeautifulSoup(html)
    papers = soup.findAll("tr", "ro2")
    titles = map(lambda x: x.find("td").text, papers)
    terms = map(lambda x: x.replace(' ', '+').encode('utf-8').strip(), titles)
    return terms

def search_single(term):
    UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36" 
    base = "https://www.google.com/search?q="
    query = base + term 
    res = curl(query, A=UA)
    soup = BeautifulSoup(res.stdout)
    return soup

def GrabLinkWithAnchor(single_res):
    return [single_res.text, single_res['href']]

def parse_single(soup_res):
    links = map(lambda x: x.find("a"), soup_res.findAll("div", "rc"))
    AnchorsLinks = map(lambda x: GrabLinkWithAnchor(x), links)
    arxivs = filter(lambda x: x[1].startswith("http://arxiv.org/abs"), AnchorsLinks)
    return arxivs

def single_wrapper(term):
    sp = search_single(term)
    print "grabbed %s now sleeping 2 seconds" % term
    time.sleep(2)
    return parse_single(sp)

def parallel_wrapper(term_list):
    p = Pool(3)
    res = p.map(single_wrapper, term_list)
    p.close()
    p.join()
    return res

if __name__ == '__main__':
    terms = get_search_terms()
    arxiv_results = parallel_wrapper(terms)
    pickle.dump(arxiv_results, open('arxivLinksTitles.pkl', 'wb'))
