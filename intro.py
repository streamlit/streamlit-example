import streamlit as st
import pandas as pd


def intro():
    st.markdown("""
    # 1. Introduction
    ## 1.1 Contexte
    Rakuten, crééen 1997 au Japon et àl'origine du concept de marketplace, est devenu l'une des plus grandes plateformes 
    de e-commerce au monde avec une communauté de plus de 1,3 milliard de membres.

    Rakuten Institute of Technology (RIT) est le département de recherche et d'innovation de Rakuten. RIT fait de la 
    recherche appliquée dans les domaines de la vision par ordinateur, du traitement du langage naturel, de l'apprentissage 
    machine/profond et de l'interaction homme-machine. Le 6 janvier 2020, RIT propose le challenge suivant : Rakuten France 
    Multimodal Product Data Classification.

    Ce défi porte sur le thème de la classification multimodale (texte et image) des codes types de produits à grande échelle
    où l'objectif est de prédire le code type de chaque produit tel que défini dans le catalogue de Rakuten France.

    Le catalogage des produits via la catégorisation des titres et des images est un problème fondamental 
    pour tout marché de e-commerce, 
    avec des applications allant de la recherche et des recommandations personnalisées à la compréhension des requêtes. 
    Les approches manuelles basées sur des règles de catégorisation ne sont pas évolutives puisque les produits commerciaux 
    sont organisés en plusieurs classes. Le déploiement d'approches multimodales serait une technique utile pour les 
    entreprises de e-commerce car elles ont du mal àcatégoriser les produits en fonction des images et des labels des marchands 
    et àéviter les doublons, en particulier lors de la vente de produits neufs et d'occasion de marchands professionnels et
    non professionnels.

    Les progrès dans ce domaine de recherche ont été limités par le manque de données réelles provenant de catalogues 
    commerciaux réels. Ce projet présente plusieurs aspects de recherche intéressants en raison de la nature 
    intrinsèquement bruyante des labels et des images des produits, de la taille des catalogues de e-commerce et de 
    la distribution déséquilibrée typique des données.
    ## 1.2 Description du problème
    L'objectif de ce défi des données est la classification à grande échelle des données produit multimodales (texte et image) 
    en codes de type de produit.

    Par exemple, dans le catalogue Rakuten France, un produit avec une désignation ou un titre français "Klarstein Présentoir 
    2 Montres Optique Fibre" associé à une image et parfois à une description complémentaire.
    Ce produit est classé sous le code de type de produit 1500. Il existe d'autres produits avec des titres, 
    des images et des descriptions possibles différents, qui se trouvent sous le même code de type de produit. 
    Compte tenu de ces informations sur les produits, comme l'exemple ci- dessus, ce défi propose de modéliser un 
    classificateur pour classer les produits dans son code de type de produit correspondant.
        
    """)


def conclusion():
        st.markdown("""
    # 7.Conclusion
    L'objectif de ce projet est la classification des produits e-commerce àgrande échelle en 27 classes de codes de type de 
    produit. Les données sont multimodales et contiennent notamment des textes et des images de produit.

    Pour atteindre l’objectif, nous avons d’abord entraîné des modèles unimodaux sur des données de textes et des images 
    respectivement. Ensuite, les meilleurs modèles des textes et des images ont étéchoisis pour former le modèle multimodal. 
    Les meilleurs modèles choisis dans ce projet sont le modèle Word2Vec avec skip gram pour la partie texte et le modèle 
    EfficientNetB1 pour la partie image. Finalement, le modèle multimodal a étéconstruit par une fusion au niveau de la 
    décision qui permet d’augmenter la performance de prédiction d'environ 7% par rapport au modèle unimodal de texte, 
    avec un score «accuracy »de 86.1%.

    Les difficultés de ce projet sont la taille des données importante etle manque de ressources de calcul. 
    Nous avons pris beaucoup de temps sur l'entraînement des modèles de Deep learning notamment pour tester les différents 
    modèles de transfert learning des images.
        """)


def perspective():
        st.markdown("""
    # 8. Perspective
    Plusieurs pistes d’amélioration peuvent être envisagé pour augmenter la performance du modèle multimodal :

    - Plusieurs groupes participés àce Data Challenge ont utilisé CamemBERT comme le modèle de texte [2], qui peut donner un score de 89.9% [3]. L'application de ce modèle de texte va très probablement augmenter le score du modèle de texte et du modèle multimodal final.

    - Le choix du modèle d’image dans notre projet est dûàla contrainte de temps. Il reste sûrement d’autres configurations et/ou modèles plus prometteurs. Ainsi, les modèles dans la bibliothèque Pytorch sont à tester.

    - Un nettoyage préalable des images pourrait être réalisé afin de réduire les bruits lors d’entrainement des modèles des images. Bi et al. [3] a trouvé des erreurs de labels dans les images brutes et utilisé un outil open source  cleanlab (https://github.com/cleanlab/cleanlab) pour nettoyer les images avant la modélisation.

    - Une stratégie du modèle d’ensemble pourrait être appliquée auprès des modèles de fusion de configurations différentes. Bi et al. [3] a appliqué une classification de voting sur l’ensemble de 12 modèles de fusion au niveau de décision  avec différentes configurations et réussi à améliorer le score final de 90.17% à 91.44%.
            """)
        
def donnees():
       
        st.markdown("""
    # 2. Description des données
    Pour ce challenge, Rakuten France met à disposition env. 99 000 listes de produits au format CSV, y compris le train (84 916)
    et l'ensemble de test (13 812). L'ensemble de données se compose de désignations de produits, de descriptions de produits, 
    d'images de produits et de leur code de type de produit correspondant.

    Les données sont réparties selon deux critères, formant quatre ensembles distincts : entraînement ou test, entrée ou sortie.

    - X_train.csv : fichier d'entrée d'entraînement

    - Y_train.csv : fichier de sortie d'entraînement

    - X_test.csv : fichier d'entrée de test

    De plus, le fichier images.zip est fourni contenant toutes les images. La décompression de ce fichier fournira un dossier 
    nommé images avec deux sous-dossiers nommés image_train et image_test, contenant respectivement des images d'entraînement 
    et de test.
       
       """)