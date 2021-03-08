# Test technique Nalia

## Consignes
L'objectif de ce test est de récupérer par API des données sur Intercom et de les stocker dans une base de donnée sur AWS.
Pour ce faire vous devez : 
- [x] Ecrire la fonction python `import_intercom()` dans le fichier `app.py` du dossier `fargate1` pour extraite toutes les données des contacts et des conversations.
- [x] Stocker ces données dans un bucket S3
- [] Ecrire la fonction python `etl_datalake_to_datawarehouse` dans le fichier `app.py` du dossier `fargate2` pour transférer les données de la S3 sur la database
- [x] Déployer les images docker sur AWS
- [] Run les tasks ECS manuellement (sans orchestrateur)
	- pb: je n'ai as les autorisations pour créer une instance fargate

## Info d'environnement

* api intercom : token = `dG9rOjI2N2JmN2VlX2E0MmNfNGFlYl9hZmI4XzRjOGZlYWU0NjMxOToxOjA=`
    * contacts à lire : `tous (9)`
    * conversations à lire : `toutes`
* datalake (bucket S3) : ``nalia-technical-test``
* chemin du fichier à écrire : ``s3://data/users.json`` et ``s3://data/conversations.json``
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

- [x] écrire un script de CD dans github action qui publie les containers docker à chaque commit
	- mise en place d'un workflow:
		- merge dev -> master (après de potentiels tests nont écris pour le script python)
		- build de l'image docker et push sur le registry d'ECS (AWS) (uniquement depuis master)
- [x] remonter les erreurs de vos scripts fargate dans un compte sentry
	- simple implémentation (je n'ai pas encore poussé les tests et erreurs possibles)
- [] brancher datadog (ou un autre) sur le compte AWS que l'on vous a donné
	- pb: je n'ai as les autorisations pour créer une instance (ou tâche) fargate
	- https://docs.datadoghq.com/fr/integrations/ecs_fargate/?tab=fluentbitetfirelens
    
## Hypothèses simplificatrices pour le test

- [x] utiliser des variables en dur dans le code
	- j'ai préféré utiliser des fichiers de configuration
- [] lire seulement l'utilisateur qui est donnée
- [x] vider la table de aurora à chaque exécution du fargate pour etre rempli de nouveau
	- utilisation de `Truncate` en sql
- [x] ré-écrire le fichier dans le datalake à chaque appel sur intercom
	- le fichier est simplement écrasé (le versinning n'est pas activé)


## Support

* https://developers.intercom.com/intercom-api-reference/v2.0/reference -> API de référence Intercom
* Pour toute question, contacter alexis@nalia.io

## Memo

```bash
$ crudini --get fargate1/config.ini AWS access_key
AKIA6F5VT4B2FFBHZTFO
```

* https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action
* https://github.com/pascalgn/automerge-action (When a pull request is merged by this action, the merge will not trigger other GitHub workflows. Similarly, when another GitHub workflow creates a pull request, this action will not be triggered. This is because an action in a workflow run can't trigger a new workflow run. However, the workflow_run event is triggered as expected.)