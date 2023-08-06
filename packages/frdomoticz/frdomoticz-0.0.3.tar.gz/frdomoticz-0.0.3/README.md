<p align="center">
  <h3 align="center">FRDomoticz</h3>

  <p align="center">
    Le package pour simplifier le contrôle de la Freebox Révolution avec Domoticz
    <br />
    <br />
    <a href="https://github.com/MatthieuF44/frdomoticz/tree/main/examples">Exemples</a>
    -
    <a href="https://github.com/MatthieuF44/frdomoticz/issues">Reporter un bug</a>
  </p>
</p>

<details open="open">
  <summary>TABLE DES MATIÈRES</summary>
  <ol>
    <li>
      <a href="#a-propos-du-projet">A propos du projet</a>
    </li>
    <li>
      <a href="#commencer">Commencer</a>
      <ul>
        <li><a href="#prérequis">Prérequis</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
        <a href="#utilisation">Utilisation</a>
        <ul>
            <li><a href="#code-télécommande">Code télécommande</a></li>
            <li><a href="#préparation-du-script-shell">Préparation du script shell</a></li>
            <li><a href="#script-python">Script python</a></li>
            <li><a href="#domoticz">Domoticz</a></li>
      </ul>
    </li>
    <li><a href="#contribuer">Contribuer</a></li>
    <li><a href="#licence">Licence</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## A propos du projet

Tout d'abord, mon souhait était de faire de domoticz une télécommande personnalisée pour mon freebox player. J'avais envie d'appuyer sur un seul bouton pour lancer ma station radio préférée, ma série en replay, etc...

Après s'être rendu compte que la tâche de programmation était rébarbative, mais que le résultat était à la hauteur de mes attentes. J'ai décidé de simplifier mon code afin de faire une "librairie".

C'est ainsi que de fil en aiguille, j'ai créé ce package qui, pourquoi pas, pourrait intéresser l'un d'entre vous.

Ce projet est en constante évolution, n'hésitez pas à me faire part de vos remarques afin d'améliorer le code.

## Commencer

L'installation du package est très simple, il suffit de bien suivre les instructions ci-dessous. Si vous rencontrer un problème, n'hésitez pas à créer un ticket.

### Prérequis

Afin d'installer le package, il est nécessaire de vérifier que Python et PIP soit bien installé.
* Python > 3.0
  ```sh
  python --version
  ```
* PIP
  ```sh
  pip --version
  ```
* Package "time"
* Package "requests"

### Installation

Une fois les prérequis respectés, il suffit de lancer la commande suivante :
  ```sh
  pip install frdomoticz
  ```

## Utilisation

Afin d'utiliser au mieux le package, merci de suivre les instructions ci-dessous. Si vous le souhaitez, vous pouvez également utiliser les exemples du repo.

### Code télécommande

Afin d'obtenir le code télécommande nécessaire dans le script, il faut suivre les étapes ci-dessous :

1. Avec la télécommande de votre Freebox révolution, allez dans "Réglages" puis "Système" puis "Informations Freebox Player et Server" et pour terminer "Player"

2. Récupérez le code télécommande réseau qui se trouve dans les lignes de droite. Ce dernier sera à intégrer dans vos futurs scripts.

### Préparation du script shell

1. Dans le dossier ci-dessous, créez un nouveau script shell "exec.sh".
   ```sh
   /domoticz/scripts/exec.sh
   ```
   Ce dernier permettra de lancer nos divers scripts python sans interrompre domoticz.

2. Dans ce fichier, placez les lignes de code suivantes :
   ```sh
    #! /bin/sh
    /usr/bin/python /home/pi/domoticz/scripts/$1.py $2 $3 > /dev/null 2>&1 &
   ```

### Script python

1. Toujours dans le dossier "script" de domoticz, créez un nouveau script python.
   ```sh
   /domoticz/scripts/nom_du_script.py
   ```
2. Ensuite, importez la librairie dans votre script avec la ligne suivante :
   ```Python
    from frdomoticz import lib
   ```
3. Puis, renseignez le code de votre télécommande :
   ```Python
     code = 123456789 
   ```
4. Pour terminer, insérez les différentes ligne de code correspondantes à votre demande :
   ```Python
     lib.init(code) # Initialise le player sur la page d'accueil
     lib.radio(code) # Sélectionne le menu Radio du player
     lib.down(code)  # Simule un appui sur la touche bas de la télécommande.
   ```

<!--  _Pour plus de renseignement, suivez la [documentation complète](https://example.com)_ -->

### Domoticz

1. Dans l'onglet "Configuration" puis dans "Matériel", créer un nouveau matériel de type "Dummy" ayant le nom que vous souhaitez (par ex. "Télécommande freebox")

2. Ensuite, créer cliquer sur "Créer un capteur virtuel" et vous sélectionnerez le type "Interrupteur".

3. Retrouvez l'interrupteur que vous venez de créer dans l'onglet "Interrupteurs" puis sélectionnez "Modifier".

4. Configurez le type de l'interrupteur en "Push On Button" puis dans "Action On" renseignez le nom de votre script python :

   ```Python
     script://exec.sh nom_du_script.py
   ```

5. Domoticz est maintenant configuré pour éxécuter le script python à chaque fois que vous appuyerez sur l'interrupteur.

## Contribuer

Les contributions sont ce qui fait de la communauté open source un endroit incroyable pour apprendre, inspirer et créer. Toutes les contributions que vous apportez sont **très appréciées**.

1. "Forker" le projet
2. Créer une nouvelle "Branch" (`git checkout -b feature/AmazingFeature`)
3. Validez vos modifications (`git commit -m 'Add some AmazingFeature'`)
4. "Push" la nouvelle "Branch" (`git push origin feature/AmazingFeature`)
5. Ouvrir une "Pull Request"

## Licence

Distribué sous la licence "GNU General Public License v3 (GPLv3)". Voir [Licence](https://github.com/MatthieuF44/frdomoticz/license) pour plus d'informations.

## Contact

MatthieuF44 - mattdevue[at]gmail.com

Lien du projet : [https://github.com/MatthieuF44/frdomoticz/](https://github.com/MatthieuF44/frdomoticz/)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png