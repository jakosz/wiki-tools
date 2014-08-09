source('settings.R')

LANG = 'de'

up = read.csv(ps(data$trans, LANG, '_user_page.csv'), sep = ';')
upp = read.csv(ps(data$trans, LANG, '_user_page_profiles.csv'), sep = ';')

upp = cbind(up, upp[,2:ncol(upp)])

# -- variables for per-user aggregation:

# distribute diff among categories

ctg = upp[,7:ncol(upp)]
upp[,7:ncol(upp)] = ctg * (upp$diff / rowSums(ctg))

# number of pages

upp$pages = rep(1, nrow(upp))

# input to good articles

upp$good_diff = upp$diff * upp$good

# input to featured

upp$featured_diff = upp$diff * upp$featured

# -- aggregate

bad = apply(upp, 1, function(x) any(any(is.na(x)), any(is.nan(x))))
upp = upp[!bad, ]

user_profile = aggregate(upp[,-c(1:2)], by = list(upp$userid), FUN = function(x) sum(as.numeric(x)))
names(user_profile)[1] = 'userid'

iCat = which(names(user_profile) %in% data$meta$namec[[LANG]])
user_profile$entropy = apply(user_profile[,iCat], 1, function(x) entropy(x, unit='log2'))

write.table(user_profile, ps(data$trans, LANG, '_user_profiles.csv'), sep = ';', row.names = FALSE)
