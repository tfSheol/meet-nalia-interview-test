# Test technique Nalia

## Info d'environnement

* api intercom : token = `dG9rOmVkNGViN2IxX2RmY2NfNDlkMV9hM2E4XzcxNDIxMDQ1ZmNiYzoxOjA=`
    * users à lire : `tous (9)`
    * conversations à lire : `toutes`
* datalake (bucket S3) : ``nalia-technical-test``
* chemin du fichier à écrire : ``s3://data/users.json``
* datawarehouse (aurora) :
	* `mdp : Pb81F7RFQaPHKWGnLk5q`
	* `user : admin`
	* `port : 3306`
	* `host : database-2.cgvivklne8l4.eu-west-3.rds.amazonaws.com`
	* `db : naliatest`
	* Tables :
		* `conversation`
		* `users`
* endpoint de ECR pour déployer les images : 
	* Scrapping image : `974801592436.dkr.ecr.eu-west-3.amazonaws.com/scrapping`
	* Push db image : `974801592436.dkr.ecr.eu-west-3.amazonaws.com/database`

* Connection console AWS
    * `ID Organisation : 974801592436`
    * `user : test`
    * `password : test-technique1`

* Accès AWS par programmation
    * `Acces key : AKIA6F5VT4B2FFBHZTFO`
    * `Secret key : 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`
    
## Optionnels

* limiter l'accès du user test à un seul bucket S3 en écriture et lecture à partir d'IAM
* écrire un script de CD dans github action qui publie les containers docker à chaque commit
* remonter les erreurs de vos scripts fargate dans un compte sentry
* brancher datadog (ou un autre) sur le compte AWS que l'on vous a donné
    
## Hypothèses simplificatrices pour le test

* utiliser des variables en dur dans le code
* lire seulement l'utilisateur qui est donnée
* vider la table de aurora à chaque exécution du fargate pour etre rempli de nouveau
* ré*écrire le fichier dans le datalake à chaque appel sur intercom
