#! /usr/bin/env python

#%% Import libraries

import glob
import os
import subprocess
import re
import pandas as pd
import xml.etree.ElementTree as ET
import requests
import sqlite3
import fire

#%% Definitions

rdf_dir = './cache/epub'
rdf_path = rdf_dir + '/{0}/pg{0}.rdf'

db_dir = './'
db_name = db_dir + '/gutenberg.db'

pg_rdf_url = "https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.zip"
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
default_formats_str = '^\s*' + '|'.join(default_formats) + '\s*'
default_formats_rgx =  re.compile(default_formats_str)

#%% Core Functions

def get_gids():
    gids = [path.split('/')[-1]
        for path in glob.glob(rdf_dir + '/*')]
    gids = [int(gid) for gid in gids
        if not re.search(r'[^0-9]+', gid)]
    gids = sorted(gids)
    return gids

def get_rdf(gid):
    path = rdf_path.format(gid)
    rdf = open(path, 'r', encoding='utf8').read()
    return rdf

def get_text_url(gid):
    return gut_txt.format(gid)

def get_text_content(gid):
    gut_url = get_text_url(gid)
    r = requests.get(gut_url)
    return r.text

def get_items(el, xpath, ns=ns):
    items = [item.text for item in el.findall(xpath, namespaces=ns)]
    return items

def get_rdf_root(gid):
    rdf = get_rdf(gid)
    root = ET.fromstring(rdf)
    return root 

def get_metadata(gid):
    root = get_rdf_root(gid)
    md = {item:get_items(root, xpaths[item]) for item in xpaths}
    return md

def get_catalog(gids):
    data = []
    for gid in gids:
        md = get_metadata(gid)
        for key in md.keys():
            if key == 'formats':
                vals = sorted(md[key])
            else:
                vals = md[key]
            for val in vals:
                val = val.upper()
                data.append((gid, key, val))
    df = pd.DataFrame(data, columns=['gid','key','val'])
    return df

def get_catalog_wide(df):
    print(df.head())
    df_wide = df.groupby(['gid', 'key']).val.apply(lambda x: '\n'.join(x))\
        .unstack().fillna('NONE GIVEN')
    return df_wide

def get_reduced_wide(df, cols=['title', 'creators', 'formats', 'languages', 'types']):
    return df[cols]

def get_catalog_text(df_wide):
    df_wide = df_wide.loc[df_wide.languages == 'en']
    df_wide = df_wide.loc[df_wide.types == 'Text']
    df_wide = df_wide.loc[df_wide.rights.str.match('Public')]
    txtidx = df_wide.formats.str.contains(default_formats_rgx).fillna(False)
    df_text = df_wide.loc[txtidx, ['title', 'creators', 'subjects']]
    df_text.subjects = df_text.subjects.fillna('None given')
    df_text.creators = df_text.creators.fillna('None given')
    return df_text
    
def save_catalog_to_db(catalog):
    with sqlite3.connect(db_name) as db:
        catalog.to_sql('catalog', db, index=True, if_exists='replace')

def get_catalog_from_db():
    with sqlite3.connect(db_name) as db:
        catalog = pd.read_sql('select * from catalog', db, index_col='gid')
        return catalog
    
def get_gids_for_pat_from_db(catalog, name_pat, key='creators'):
    sql  = "SELECT gid FROM catalog WHERE creators LIKE ?"
    with sqlite3.connect(db_name) as db:
        df = pd.read_sql(sql, db, params=(name_pat,))
        return df.gid.tolist()

#%% Commands

def download_cache(overwrite=True):
    """Download RDF catalog from Project Gutenburg"""
    if overwrite == False or not os.path.exists('./cache/epub'):
        print("Downloading RDF data")
        rdf_zip = pg_rdf_url.split('/')[-1]
        rdf_tar =  rdf_zip.replace('.zip', '')
        subprocess.call(['wget', pg_rdf_url])
        subprocess.call(['unzip', rdf_zip])
        subprocess.call(['tar', '-xf', rdf_tar])
        subprocess.call(['rm', rdf_zip])
        subprocess.call(['rm', rdf_tar])
    else:
        print("RDF files exist on system. Set overwrite = True to overwrite.")

def populate_database(replace=True):
    """Create db with downloaded RDF data"""
    print("Creating database of RDF data")
    # Check to see if RDF data is there ...
    gids = get_gids()
    df = get_catalog(gids)
    df_wide = get_catalog_wide(df)
    save_catalog_to_db(df_wide)

def remove_cache():
    """Remove RDF cache from file system"""
    print("Removing cache")
    subprocess.call(['rm', '-rf', './cache'])

#%% Run
if __name__ == '__main__':
    
    commands = {
        'download-cache': download_cache,
        'dc': download_cache,
        'populate-database': populate_database,
        'pd': populate_database,
        'remove-cache': remove_cache,
        'rc': remove_cache
    }
    fire.Fire(commands)
    
    # catalog = get_catalog_from_db()
    # pat = 'AUSTEN, JANE'
    # austen_gids = get_gids_for_pat_from_db(catalog, pat)
