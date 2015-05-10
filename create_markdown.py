import cPickle as pickle
import operator
def readResults():
    l = pickle.load(open("arxivLinksTitles.pkl", 'rb'))
    arxivs = reduce(operator.add, filter(lambda x: len(x) > 0, l))
    return arxivs

def toLinks(arxivs):
    return map(lambda x: '[' + x[0]  +']' + '(' + x[1] + ')', arxivs)

def toNumberedList(links):
    return '\n'.join(map(lambda x,y: str(1 + x) + '.' + ' ' + y, range(len(links)), links))

def write_markdown(file_name, links):
    f=open(file_name, 'wb')
    f.write(links)
    f.close()

def wrapper():
    arxs = readResults()
    lxs = toLinks(arxs)
    nums = toNumberedList(lxs)
    write_markdown('icml2015_arxiv.md', nums)

if __name__ == '__main__':
    wrapper()

