import sys
sys.path.append('../')

import logging
import traceback as tb
import suds.metrics as metrics
from tests import *
from suds import *
from suds.client import Client
from datetime import datetime
import mygene

from get_entrez_dict import *

def get_DAVID_annotation(infile='',genes=[],outfile='',fdr_thresh=0.1,thd=0.1,count = 2,
                         cats='GENETIC_ASSOCIATION_DB_DISEASE,KEGG_PATHWAY,REACTOME_PATHWAY,GOTERM_BP_FAT'):
    """
    get david annotation for a list of gene symbols
    two modes of use:
    - specify infile, will write results to outfile with DAVID_ prepended
    - specify gene list, will not write results unless outfile is also specified
    in each case, return the chart report list
    """
    
    if len(infile)>0:
        assert os.path.exists(infile)
        f=open(infile)
        genes=[i.strip() for i in f.readlines()]
        f.close()
    
    assert len(genes)>0
    
    g2e,e2g=get_entrez_dict()
    all_genes=g2e.keys()
    all_genes.sort()
    
    
    
    errors = 0
    setup_logging()
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    url = 'http://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl'  
    print 'url=%s' % url
    
    #
    # create a service client using the wsdl.
    #
    client = Client(url)
    
    #
    # print the service (introspection)
    #
    print client
    
    #authenticate user email 
    print client.service.authenticate('poldrack@utexas.edu')
    
    
    
    
    idType = 'ENTREZ_GENE_ID'
    listName = 'test'
    listType = 0
    entrez_list=[]
    update_dict=False
    
    for g in genes:
        try:
            entrez_list.append(g2e[g])
        except:
            print g,'not in dictionary, trying mygene'
            mg=mygene.MyGeneInfo()
            entrez=[]
            result=mg.query(g,species='human')
            for h in result['hits']:
                    if h.has_key('entrezgene'):
                        updateDict=True
                        g2e[g]='%d'%h['entrezgene']
                        e2g['%d'%h['entrezgene']]=g
                        entrez_list.append('%d'%h['entrezgene'])
                        break
    
    if update_dict:
        print 'updating entrez dict'
        save_entrez_dict(g2e)
    
    inputIds=','.join(entrez_list)
    
    print client.service.addList(inputIds, idType, listName, listType)
    client.service.setCategories(cats)
    #client.service.setCurrentSpecies(1)
    
    chartReport= client.service.getChartReport(thd, count)
    
    if len(infile)>0:
        outfile=os.path.join(os.path.dirname(infile),'DAVID_'+os.path.basename(infile))
    
    if len(outfile)>0:
        f_gc=open(outfile,'w')
        for gc in range(len(chartReport)):
            clust=chartReport[gc]
            if clust.benjamini<fdr_thresh:
                genesyms=[e2g[x] for x in clust.geneIds.replace(' ','').split(',')]
                f_gc.write('%s\t%f\t%f\t%s\n'%(clust.termName,clust.benjamini,clust.foldEnrichment,','.join(genesyms)))
        
        f_gc.close()
    
    return chartReport
