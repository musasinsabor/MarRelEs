library(ggplot2)
#df creation
economy = read.csv("n_annotated_economy_annotation_file.csv", header=TRUE, encoding = "UTF-8", stringsAsFactors=TRUE)
med = read.csv("n_annotated_medicine_annotation_file.csv", header=TRUE, encoding = "UTF-8", stringsAsFactors=TRUE)
all = read.csv("all_data_annotation_file.csv", header=TRUE, encoding = "UTF-8", stringsAsFactors=TRUE)
original_med = read.csv("medicine_annotation_file.csv", header=TRUE, encoding = "UTF-8", stringsAsFactors=TRUE)
original_economy = read.csv("economy_annotation_file.csv", header=TRUE, encoding = "UTF-8", stringsAsFactors=TRUE)
full = read.csv("full_data_annotation_file.csv", header=TRUE, encoding = "UTF-8", stringsAsFactors=TRUE)
etape4 = read.csv("hyperonym_patterns/Hyp/etape4/sample_data_economy_annotated.csv", header=TRUE, encoding = "UTF-8", stringsAsFactors=TRUE)


## descripción de variables

summary(all)

# Mezclar los dataframes original_economy y original_medicine
mezcla <- rbind(original_economy, original_med)

#

summary(economy$annotation)
summary(med$id)
t = table(economy$annotation)
sort(table(med$id), decreasing = TRUE)

sort(table(economy$annotation), decreasing = TRUE)
prop.table(sort(table(economy$annotation), decreasing = TRUE)) * 100

## TYPE ALL DATA 

summary(full$topic)
summary(economy$id)
summary(med$topic)
## relational semantic
t1 = sort(table(subset1$relational_semantic_type), decreasing = TRUE)
table(subset1$relational_semantic_type)
t1
t2 = sort(table(subset2$relational_semantic_type), decreasing = TRUE)

prop.table(t1) * 100
prop.table(t2) * 100

# ids

t1 = sort(table(subset1$id), decreasing = TRUE)
id1 = data.frame(table(subset1$id))
id2 = data.frame(table(subset2$id))
t2 = sort(table(subset2$id), decreasing = TRUE)

prop.table(t1) * 100
prop.table(t2) * 100
t2 = sort(table(subset2$id), decreasing = TRUE)

r = ftable(all$topic, all$annotation, all$id)
prop.table(table(all$topic,all$annotation), 1) * 100

summary(subset1$relational_semantic_type)
summary(subset2$relational_semantic_type)
summary(subset2$id)

# Crear un subset para cada valor único de "topic"
subset1 <- subset(full, topic == "economy")
subset2 <- subset(full, topic == "medicine")
subset3 <- subset(all, annotation == "« OUI »")
subset3 <- subset(all, topic == "economy" & annotation == "« OUI »")
subset4 <- subset(all, topic == "medicine" & annotation == "« OUI »")
subset5 <- subset(all, relational_semantic_type == "hyp_coordonné" & annotation == "« OUI »")

## 
p = data.frame(summary(subset3$id))

table(subset5$id)
# Combinar los subsets en un solo dataframe
combined2 <- rbind(subset3, subset4)


## annotation
t2 = sort(table(combined$annotation), decreasing = TRUE)
t2

## annotation non

# Crear el gráfico
ggplot(combined2, aes(x = topic, fill = justification)) +
  geom_bar(position = "fill") +
  labs(title = "Répartition des valeurs selon justification", fill = "justification",
       x = "Candidats-marqueurs valides", y = "Proportion") +
  theme_bw()


# Combinar los subsets en un solo dataframe
combined <- rbind(subset1, subset2)

# Crear el gráfico
ggplot(combined, aes(x = topic, fill = relational_semantic_type)) +
  geom_bar(position = "fill") +
  labs(title = "Répartition des valeurs obtenues selon leur type", fill = "Type de candidat-marqueur",
       x = "Candidats-marqueurs", y = "Proportion") +
  theme_bw()


##anotation

h1 <- barplot(sort(table(economy$annotation), decreasing = TRUE), main="Distribution de l'annotation (economie)", xlab = "Annotation", ylab = "Frecuence")
h2 <- barplot(sort(table(med$annotation), decreasing = TRUE), main="Distribution de l'annotation (medicine)", xlab = "Annotation", ylab = "Frecuence")
new_h <- rbind(h1,h2)
barplot(new_h, beside=TRUE, main="Histogram", xlab="Age")

# Crear un subset para cada valor único de "topic"
subset1 <- subset(all, topic == "economy")
subset2 <- subset(all, topic == "medicine")

# Combinar los subsets en un solo dataframe
combined <- rbind(subset1, subset2)

# Crear el gráfico
ggplot(combined, aes(x = topic, fill = annotation)) +
  geom_bar(position = "fill") +
  labs(title = "Répartition des valeurs d'annotation",
       x = "Topic", y = "Proportion") +
  scale_fill_manual(values = c("« NON »" = "turquoise", "« OUI »" = "green", "« INCERTAINE »" = "grey")) +  # Personalizar colores si es necesario+
  theme_bw()

## CM

subset5 <- subset(all, annotation == "« OUI »")
summary(subset5$annotation)
subset_all <- all[all$global_freq_oui > all$global_freq_non, ]
summary(subset_all$tag)

table(subset5$relational_semantic_type)

## etape 4
prop.table(table(etape4$annotation, etape4$id), 2)* 100

# Crear un subset filtrado
subset_df <- all[all$id %in% c("H01", "H34"), ]
# Crear la nueva variable 'presence_bool' en el subset 'etape4'
etape4$presence_bool <- ifelse(etape4$presence == 'none', FALSE, TRUE)
summary(etape4$presence_bool)
V1
table(etape4$presence_bool, etape4$annotation)
chisq.test(etape4$presence_bool, etape4$annotation)
assocplot(table(etape4$presence_bool,etape4$annotation))
assocplot(table(etape4$presence,etape4$annotation), main = 'Croisement des variables: annotation et presence des CT', xlab = 'presence des CT', ylab = 'annotation')
assocplot(table(all$presence,all$annotation), main = 'Croisement des variables: annotation et presence des CT', xlab = 'presence des CT', ylab = 'annotation')
mosaicplot(table(all$presence,all$annotation), shade=T)

table(all$presence, all$annotation)
table(all$presence)
prop.table(table(all$presence, all$annotation), 2)* 100
chisq.test(all$presence, all$annotation)
prop.table(table(all$presence), 1)* 100
table(subset_df$annotation, subset_df$id)
prop.table(table(subset_df$annotation, subset_df$id), 2)* 100

