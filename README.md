# Projet de Correction Orthographique, Traduction et Reformulation avec GPT

Ce projet propose un correcteur orthographique, un outil de traduction et de reformulation utilisant l'API GPT d'OpenAI. Il permet d'effectuer ces actions via des raccourcis clavier, en exploitant la puissance du modèle GPT-4 pour améliorer et manipuler du texte sélectionné.

## Configuration

1. **Obtenez une clé API OpenAI**
   - Accédez à [OpenAI](https://beta.openai.com/signup/).
   - Obtenez une clé API en suivant les instructions fournies.

2. **Remplacez la clé API dans le code**
   - Ouvrez le fichier et trouvez la section du code où la clé API est définie (`api_key = ""`).
   - Remplacez `""` par votre clé API.

## Utilisation

1. **Correction du texte**
   - Appuyez sur `<Ctrl>+<Alt>+q` pour corriger le texte actuellement sélectionné.
   - Le texte corrigé est copié dans le presse-papiers.

2. **Traduction du texte**
   - Appuyez sur `<Ctrl>+<Alt>+d` pour traduire le texte sélectionné du français vers l'anglais ou inversement.
   - Le texte traduit est copié dans le presse-papiers.

3. **Reformulation du texte**
   - Appuyez sur `<Ctrl>+<Alt>+a` pour reformuler le texte sélectionné.
   - Le texte reformulé est copié dans le presse-papiers.

4. **Terminer le programme**
   - Appuyez sur `<Ctrl>+<Alt>+k` pour quitter le programme.

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

## Remarques supplémentaires

- **Limite de tokens**
  - La variable `max_tokens` dans les fonctions utilisant OpenAI peut être ajustée pour contrôler la longueur du texte envoyé à GPT-4.

- **Température du modèle**
  - La variable `temperature` peut être ajustée pour contrôler la créativité de la réponse. Pour la correction orthographique, elle est réglée sur 0 pour obtenir des réponses plus strictes.

- **Personnalisation des raccourcis clavier**
  - Modifiez les raccourcis clavier dans la section `keyboard.GlobalHotKeys` du code pour correspondre à vos préférences.

- **Sécurité**
  - Assurez-vous de garder votre clé API confidentielle. Ne partagez pas votre clé API dans le code source public.

N'hésitez pas à ajouter d'autres fonctionnalités ou personnaliser le code selon vos besoins spécifiques. Bonne utilisation de GPT pour vos corrections, traductions et reformulations ! 📝✨
