# t1. Are all pageids in ii.from_id?

t1 = pids.isin(ii.from_id)
t1t = t1.value_counts()

# t2. Are all pageids in pg.id, ns = 0?

t2_pg = pg[pg.ns == 0]
t2 = pids.isin(t2_pg.id)
t2t = t2.value_counts()

# Values not in ii are not there due to not being in cl, which in turn is a result 
# of a bug in sqldump2csv
