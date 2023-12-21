# Projet de Correction Orthographique avec GPT-3.5

Ce projet propose un correcteur orthographique utilisant l'API GPT-3 de OpenAI. Il permet de corriger le texte en cours en utilisant des raccourcis clavier et en exploitant la puissance de GPT-3. Voici comment utiliser ce code et personnaliser votre expérience.

## Configuration

1. **Obtenez une clé API GPT-3 de OpenAI**
   - Accédez à [OpenAI](https://beta.openai.com/signup/).
   - Obtenez une clé API en suivant les instructions fournies.

2. **Remplacez la clé API dans le code**
   - Ouvrez le fichier et trouvez la section du code où la clé API est définie (`api_key = "ma clé"`).
   - Remplacez `"ma clé"` par votre clé API.

## Utilisation

1. **Correction du texte**
   - Appuyez sur `<Ctrl>+<Alt>+w` pour corriger le texte actuellement sélectionné.
   - Le texte corrigé est copié dans le presse-papiers.

2. **Terminer le programme**
   - Appuyez sur `<Ctrl>+<Alt>+q` pour quitter le programme.


## Installation des bibliothèques

1. **Installer Python**
   - Si vous n'avez pas encore installé Python sur votre système, téléchargez et installez la dernière version depuis [le site officiel de Python](https://www.python.org/).
   - Assurez-vous de cocher l'option "Ajouter Python à la variable d'environnement PATH" lors de l'installation.

2. **Installer les dépendances Python**
   - Ouvrez une fenêtre de terminal ou de commande.
   - Exécutez la commande suivante pour installer les dépendances nécessaires :
     ```
     pip install pyperclip requests pynput openai
     ```
Avec ces étapes, vous devriez avoir Python installé, les dépendances requises installées, et votre environnement OpenAI configuré pour utiliser le script de correction orthographique.

## Remarques supplémentaires

- **Limite de tokens**
  - La variable `max_tokens` dans la fonction `correct_text_with_openai` peut être ajustée pour contrôler la longueur du texte envoyé à GPT-3.

- **Température du modèle**
  - La variable `temperature` dans la fonction `correct_text_with_openai` peut être ajustée pour contrôler la créativité de la réponse de GPT-3.

- **Personnalisation des raccourcis clavier**
  - Modifiez les raccourcis clavier dans la section `keyboard.GlobalHotKeys` du code pour correspondre à vos préférences.

- **Sécurité**
  - Assurez-vous de garder votre clé API confidentielle. Ne partagez pas votre clé API dans le code source public.

N'hésitez pas à ajouter d'autres fonctionnalités ou personnaliser le code selon vos besoins spécifiques. Bonne correction orthographique ! 📝✨
