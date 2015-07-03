"""
add popups and image links to timeseries_analyses.html

requires two javascript libraries in the same directory:
https://raw.github.com/nhoening/popup.js/master/dist/nhpup_1.1.js

"""

import os

basedir=os.environ['MYCONNECTOME_DIR']

def add_timeseries_links():
    infile=os.path.join(basedir,'timeseries/timeseries_analyses.html')
    outfile=os.path.join(basedir,'timeseries/timeseries_analyses_annot.html')
    
    # multiple entries for some networks because of divergent naming across
    # within- and between- network analyses
    
    netnames={'Default':['1','Default mode network'],
              'DMN':['1','Default mode network'],
              'Visual_2':['2','Secondary visual network'],
              'Frontoparietal_1':['3','Frontoparietal network'],
              'Fronto_parietal':['3','Frontoparietal network'],
              'Visual_1':['4.5','Primary visual network'],
              'Dorsal_Attention':['5','Dorsal attention network'],
              'Ventral_Attention':['7','Ventral attention network'],
              'Salience':['8','Salience network'],
              'Cingulo_Opercular':['9','Cingulo-opercular network'],
              'Cingulo_opercular':['9','Cingulo-opercular network'],
              'Somatomotor':['10','Somatomotor network'],
              'Frontoparietal_2':['11.5','Secondary fronto-parietal network'],
              'Medial_Parietal':['15','Medial parietal network'],
              'Parieto_occipital':['16','Parieto-occipital network'],
              'Parieto_Occipital':['16','Parieto-occipital network']}
              
    lines=open(infile).readlines()
    f=open(outfile,'w')
    reps={'panas.positive':'PANAS positive mood scale (after scan)',
          'afterscan.diastolic':'Diastolic blood pressure (after scan)',
          'afterscan.systolic':'Systolic blood pressure (after scan)',
          'afterscan.pulse':'Pulse (after scan)',
          'temp.mean':'Mean outdoor temperature (day of scan)',
          'email.LIWCnegemo':'LIWC Negative emotion scale on sent emails (day of scan)',
          'email.LIWCposemo':'LIWC Positive emotion scale on sent emails (day of scan)',
          'panas.fatigue':'PANAS fatigue scale (after scan)',
          'prevevening.Guthealth':'Self-rated gut health (previous evening)',
          'prevevening.Stress':'Self-rated psychological stress (previous evening)',
          'prevevening.Alcohol':'Amount of alcohol consumed (previous evening)',
          'prevevening.Psoriasisseverity':'Self-rated psoriasis severity (previous evening)',
          'TuesThurs':'Tuesdays (fasted/no caffeine) vs. Thursdays (fed/caffeinated)',
          'zeo.zq':'Overall sleep quality measured using Zeo sleep monitor (morning before scan)',
          'morning.Sleepquality':'Self-rated sleep quality (morning before scan)',
          'panas.negative':'PANAS negative mood scale (after scan)'}
    
    for l in lines:
        if l.find('</style>')>-1:
            l="""#pup {
      position:absolute;
      z-index:200; /* aaaalways on top*/
      padding: 3px;
      margin-left: 10px;
      margin-top: 5px;
      width: 250px;
      border: 1px solid black;
      background-color: #777;
      color: white;
      font-size: 0.95em;
      top: 200px;
      left:200px;

    }
    
    
    </style>
    """
    
        if l.find('<title>')>-1:
            l+="""<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
    <script type="text/javascript" src="nhpup_1.1.js"></script>
    """
        for r in reps.keys():
            if l.find(r)>-1:
                l=l.replace(r,
            "<a onmouseover=\"nhpup.popup('%s');\">%s</a>"%(reps[r],r))
            
        for r in netnames:
               if l.find(r)>-1:
                   img='network_plots/network%s.png'%netnames[r][0]
                   l=l.replace(r,
          "<a onmouseover=\"nhpup.popup('%s: <br/><br/> <img src=&quot;%s&quot;/>', {'width': 250});\">%s</a>"%(netnames[r][1],img,r))
        if l.find('<h3>Behavioral variables vs. each other:</h3>')>-1:
            l="""<p>Mouse over behavioral variables for a more detailed description, and over network names for an image of the network.</p>
            """+l
        f.write(l)
        
    
        
    f.close()
    
if __name__ == "__main__":
    add_timeseries_links()
