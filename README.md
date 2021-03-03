# Test technique Nalia

## Info d'environnement

* api intercom : ``...``
    * user à lire : ``...``
* datalake (bucket S3) : ``...``
* chemin du fichier à écrire : ``s3://.../users/{user_id}.json``
* datawarehouse (aurora) : ``[connection string]``
* endpoint de ECR pour déployer les images : ``...``

* optionnels

    * role pré-crée pour exécuter le code fargate : ``...``
    * table aurora sur laquelle mettre les données : ``...``
    
## Optionnels

* limiter l'accès du role ``...`` à un seul bucket S3 en écriture et lecture à partir d'IAM
* écrire un script de CD dans github action qui publie les containers docker à chaque commit
* remonter les erreurs de vos scripts fargate dans un compte sentry
* brancher datadog (ou un autre) sur le compte AWS que l'on vous a donné
    
## Hypothèses simplificatrices pour le test

* utiliser des variables en dur dans le code
* lire seulement l'utilisateur qui est donnée
* vider la table de aurora à chaque exécution du fargate pour etre rempli de nouveau
* ré-écrire le fichier dans le datalake à chaque appel sur intercom