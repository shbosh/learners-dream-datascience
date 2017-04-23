! pip install pandas
! pip install numpy
! pip install guess_language_spirit

# Import packages
import numpy as np
import pandas as pd
from guess_language import guess_language
import json
from pandas.io.json import json_normalize
import re



def openjson(fname):
    with open(fname, encoding='utf-8') as data_file:
        data = json.load(data_file)
    return data

def normalize_to_df(course_list):
    course_df = json_normalize(course_list)
    return course_df
    

## Read json and convert to dataframe
coursera = openjson('courserav1.json')
edx = openjson('edx.json')
udacity = openjson('udacity.json')
# khanacademy = openjson('khanacademy.json')
futurelearn = openjson('futurelearn.json')
goodreads = openjson('goodreads-cs.json')

# strip down to level of courses 
coursera = coursera["elements"]
edx = edx["items"]
udacity = udacity["courses"]
goodreads = goodreads['GoodreadsResponse']['search']['results']['work']

# json normalize list
coursera_df = normalize_to_df(coursera)
edx_df = normalize_to_df(edx)
udacity_df = normalize_to_df(udacity)
futurelearn_df = normalize_to_df(futurelearn)
goodreads_df = normalize_to_df(goodreads)


### Functions to use 
# Enter a dataframe with the col name to check and returns only the english entries 
def extract_eng(dataframe, colname):
    try:
        dataframe['language'] = dataframe[colname].apply(guess_language)
    except: 
        pass
    return dataframe[dataframe['language'] == "en"]

def get_category_coursera(row):
    domain_col = row[2]
    num_domains = len(domain_col)
    if num_domains == 1:
        row['categoryone'] = domain_col[0]['domainId']
        row['categoryonesub'] = domain_col[0]['subdomainId']
    elif num_domains == 2:
        row['categoryone'] = domain_col[0]['domainId']
        row['categorytwo'] = domain_col[1]['domainId']
        row['categoryonesub'] = domain_col[0]['subdomainId']
        row['categorytwosub'] = domain_col[1]['subdomainId']
    return row
    
    
def get_category_edx(row):
    if row is None: 
        return row
    domain_col = row[75]
    num_domains = len(domain_col)
    row['maxtitles'] = num_domains
    if num_domains > 7:
        num_domains = 7
    for i in range(0, num_domains):
        row['subject' + str(i)] = domain_col[i]["title"]
    return row
    # check row num: for a,b in enumerate(edx_df.columns): print(a,b)
    
    #check max number of topics
    # if num_domains == 1:
    #     row['categoryone'] = domain_col[0]['domainId']
    #     row['categoryonesub'] = domain_col[0]['subdomainId']
    # elif num_domains == 2:
    #     row['categoryone'] = domain_col[0]['domainId']
    #     row['categorytwo'] = domain_col[1]['domainId']
    #     row['categoryonesub'] = domain_col[0]['subdomainId']
    #     row['categorytwosub'] = domain_col[1]['subdomainId']
    # return row
    
def get_category_udacity(row):
    if row is None: 
        return row
    domain_col = row[27]
    num_domains = len(domain_col)
    row['maxtitles'] = num_domains
    if num_domains > 7:
        num_domains = 7
    for i in range(0, num_domains):
        row['subject' + str(i)] = domain_col[i]
    return row

# futurelearn has its categories in futurelearn_df['categories']
# udacity['tracks']



    
    
    
def search(text,n, target):
    # word = r"\W*([\w]+)"
    # groups = re.search(r'{}\W*{}{}'.format(word*n,target,word*n), text).groups()
    try:
        words = re.findall(r'\w+', text)
        index = words.index(target)
        print(words[index - n: index])
    except ValueError:
        return
    return words[index - n: index]




# Assessing goodreads api 
# goodreads['GoodreadsResponse']['search']['results']['work'][1]['average_rating']
# goodreads['GoodreadsResponse']['search']['results']['work'][1]['best_book']['title']

## Data Cleaning 
# Remove non english entries 
coursera_df = extract_eng(coursera_df, 'description')
edx_df = extract_eng(edx_df, 'description')
udacity_df = extract_eng(udacity_df, 'required_knowledge')

## Data Augmentation 

# Coursera 
coursera_df = coursera_df.apply(get_category_coursera, axis=1)
# Use coursera_categoryonesub as the main category 
coursera_df = coursera_df[['name','categoryonesub','description','workload','slug']]
# Change workload to common unit of weeks
searchpartial = partial(search, n = 1, target = 'hours')
coursera['Hours'] = coursera_df['workload'].apply(searchpartial)

# EDX
edx_df = edx_df.apply(get_category_edx, axis = 1)

# Udacity
a = udacity_df.apply(get_category_udacity, axis = 1)




## Combine all to one big dataframe 
# Since Coursera is the limiting dataframe, the columns would be:
## Name, category/domainTypes, description, course_length, workload, slug 






# Functions 

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
  # Parse the feed
  d=feedparser.parse(url)
  wc={}

  # Loop over all the entries
  for e in d.entries:
    if 'summary' in e: summary=e.summary
    else: summary=e.description

    # Extract a list of words
    words=getwords(e.title+' '+summary)
    for word in words:
      wc.setdefault(word,0)
      wc[word]+=1
  return d.feed.title,wc
  
 
def getwords(html):
  # Remove all the HTML tags
  txt=re.compile(r'<[^>]+>').sub('',html)

  # Split words by all non-alpha characters
  words=re.compile(r'[^A-Z^a-z]+').split(txt)

  # Convert to lowercase
  return [word.lower(  ) for word in words if word!='']
  
apcount={}
wordcounts={}
feedlist=[]
for feedurl in file('feedlist.txt'):
  feedlist.add(feedurl)
  title,wc=getwordcounts(feedurl)
  wordcounts[title]=wc
  for word,count in wc.items(  ):
    apcount.setdefault(word,0)
    if count>1:
      apcount[word]+=1
      
wordlist=[]
for w,bc in apcount.items(  ):
  frac=float(bc)/len(feedlist)
  if frac>0.1 and frac<0.5: wordlist.append(w)
  
out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
  #deal with unicode outside the ascii range
  blog = blog.encode('ascii','ignore)
  out.write(blog)
  for word in wordlist:
    if word in wc: out.write('\t%d' % wc[word])
    else: out.write('\t0')
  out.write('\n')







