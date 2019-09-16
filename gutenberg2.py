
#%%
import pandas as pd
import glob
import re
import xml.etree.ElementTree as ET
import requests
import sqlite3


#%%
data_dir = './cache/epub'
epub_path = data_dir + '/{0}/pg{0}.rdf'
TAG = re.compile(r'<[^>]+>')

# Data 

gut_url = 'https://www.gutenberg.org/ebooks/{}'
gut_txt = 'https://www.gutenberg.org/ebooks/{}.txt.utf-8'

ns = dict(base="http://www.gutenberg.org/",
    rdfs="http://www.w3.org/2000/01/rdf-schema#",
    rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    marcrel="http://id.loc.gov/vocabulary/relators/",
    pgterms="http://www.gutenberg.org/2009/pgterms/",
    cc="http://web.resource.org/cc/",
    dcam="http://purl.org/dc/dcam/",
    dcterms="http://purl.org/dc/terms/")

xpaths = dict(
    subjects = ".//dcterms:subject/rdf:Description/rdf:value",
    bookshelves = ".//pgterms:bookshelf/rdf:Description/rdf:value",
    languages = ".//dcterms:language/rdf:Description/rdf:value",
    agents = ".//marcrel:ill/pgterms:agent/pgterms:name",
    rights = ".//dcterms:rights",
    title = ".//dcterms:title",
    types = ".//dcterms:type/rdf:Description/rdf:value",
    creators = ".//dcterms:creator/pgterms:agent/pgterms:name",
    formats = ".//dcterms:hasFormat/pgterms:file/dcterms:format/rdf:Description/rdf:value"
)

default_formats = ["text/plain; charset={}".format(cs) 
                   for cs in ['utf-8', 'ascii', 'iso-8859-1']] + ['text/plain']
default_formats_str = '|'.join(default_formats)

# Functions

def get_gids(data_dir=data_dir):
    gids = [int(path.split('/')[-1])
        for path in glob.glob(data_dir+'/*')
        if not re.search(r'delete', path, re.IGNORECASE)]
    gids = sorted(gids)
    return gids

def get_rdf(gut_id, data_dir=data_dir):
    path = "{0}/{1}/pg{1}.rdf".format(data_dir, gut_id)
    rdf = open(path, 'r', encoding='utf8').read()
    return rdf

def get_text_url(gut_id):
    gut_txt = gut_txt.format(gut_id)
    return gut_txt

def get_text_content(gut_id):
    gut_url = get_text_url(gut_id)
    r = requests.get(gut_url)
    return r.text

def get_items(el, xpath, ns=ns):
    items = [item.text for item in el.findall(xpath, namespaces=ns)]
    return items

def get_rdf_root(gut_id):
    rdf = get_rdf(gut_id)
    root = ET.fromstring(rdf)
    return root 

def get_metadata(gut_id):
    rdf_root = get_rdf_root(gut_id)
    md = {}
    for item in xpaths:
        md[item] = get_items(rdf_root, xpaths[item])
    return md

def get_catalog(gids):
    data = []
    for gid in gids:
        md = get_metadata(gid)
        for key in md.keys():
            for val in md[key]:
                data.append((gid, key, val))
    df = pd.DataFrame(data, columns=['gid','key','val'])
    return df

#%% Get GIDs
gids = get_gids()

#%% 
df = get_catalog(gids)

#%%
df_wide = df.groupby(['gid', 'key']).val.apply(lambda x: '|'.join(x)).unstack()
df_wide = df_wide.loc[df_wide.languages == 'en']
df_wide = df.wide.loc[df_wide.types == 'Text']
df_wide = df.wide.loc[df_wide.rights.str.match('Public')

#%%
TEXT = df_wide.formats.str.contains(r"^\s*({})\s*".format(default_formats_str)).fillna(False)
df_text = df_wide.loc[TEXT]

#%%
catalog = df_text[['title', 'creators', 'subjects']].copy()

#%%
catalog.subjects = catalog.subjects.fillna('None given')
catalog.creators = catalog.creators.fillna('None given')

#%%
db_dir = './'
with sqlite3.connect(db_dir + '/gutenberg.db') as db:
    catalog.to_sql('catalog', db, index=True, if_exists='replace')

#%%
tables = {}
for key in xpaths.keys():
    print(key)
    items = df.loc[df.key==key, ['gid','val']]
    items = items.set_index('gid')
    items = pd.Series(items.val)
    tables[key] = items

UTF = tables['formats'].str.contains('text/plain; charset=utf')

tables['title']

data_dir2 = '/home/rca2t/Public/ETA/data/gutenberg'

import sqlite3

with sqlite3.connect(data_dir2 + '/gutenberg.db') as db:
    for table in tables:
        print(table)
        tables[table].to_sql(table, db, index=True, if_exists='replace')

df.loc[(df.key=='formats') &  (df.val.str.match('text/plain'))].val.value_counts()[:4]

def get_works_by(name_pat):
    creators = pd.DataFrame(tables['creators'])
    titles = pd.DataFrame(tables['title'])
    works = titles.loc[creators.val.str.contains(name_pat)]
    return works

milton = get_works_by('Milton, John')
austen = get_works_by('Austen, Jane')


import requests
download_dir = '/home/rca2t/Public/ETA/data/gutenberg/downloads'
def download_works(works, download_dir=download_dir):
    gids = works.index.tolist()
    for gid in gids:
        print(gid)
        url = 'https://www.gutenberg.org/ebooks/{}.txt.utf-8'.format(gid)
        r = requests.get(url)
        with open(download_dir+"/g{}.txt".format(gid), 'w', encoding='utf8') as out:
            out.write(r.text)

works = download_works(austen)
milton.groupby('title').count()
