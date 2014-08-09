library(jap)

data = list(dumps = '/home/y/proj/wiki/data/dumps/', 
            trans = '/home/y/proj/wiki/data/trans/', 
            meta = list(
              mainc = list(
                de = c(236366, 224908, 691624, 8132391, 235991, 235635, 242544, 242681), 
                fr = vector()),
              namec = list(
                de = c('Geographie', 'Geschichte', 'Gesellschaft', 'Kunst_und_Kultur', 'Religion', 'Sport', 'Technik', 'Wissenschaft'), 
                fr = vector())
              )
            )

log_header = c('pageid','ns','revid','parentid','userid','timestamp','size','diff','line')
