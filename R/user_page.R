source('settings.R')

up = read.csv(ps(data$dumps, 'de_pmh_sample_filtered.csv'), sep = ';', header = FALSE)
names(up) = log_header

up = up[,c('userid','pageid','diff')]
up$edits = rep(1, nrow(up))
up$diff = abs(up$diff)

user_page = aggregate(up[,c('diff','edits')], 
                      by = list(up$userid, up$pageid), 
                      function(x) sum(as.numeric(x)))
names(user_page)[1:2] = c('userid', 'pageid')

write.table(user_page, ps(data$trans, 'de_user_page.csv'), row.names = FALSE, sep = ';')
