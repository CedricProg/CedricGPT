# Version ""stable""" de ce code 

import pyperclip
from pynput import keyboard
from openai import OpenAI

# Initialize OpenAI client with API key
client = OpenAI(
    api_key = "ma clé",
)

# Function to get currently selected text from clipboard
def get_selected_text():
    return pyperclip.paste()

# Function to correct text using GPT
def correct_text_with_openai(text):
    text_to_correct = "corrige uniquement l'orthographe, ne répond que le texte corriger : \n'\n "+text+"\n'"
    print(text_to_correct)  # logs #
    
    # Call the OpenAI API to get the corrected text
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
          {"role": "system", "content": ""},
          {"role": "user", "content": text_to_correct}
        ],
        max_tokens=512,
        temperature=0
    )
    corrected_text = completion.choices[0].message.content

    # Log the corrected text received from GPT
    print(corrected_text)
    return corrected_text

# Function to remove surrounding quotes from a string
def supprimer_guillemets(chaine):
    if chaine.startswith('"') and chaine.endswith('"'):
        return chaine[1:-1]
    else:
        return chaine


# Function to copy corrected text to clipboard
def copy_corrected_text_to_clipboard(corrected_text):
    pyperclip.copy(corrected_text)

# Callback function for the hotkey to correct text
def on_hotkeyCorrect():
    print('Global hotkey activated!')
    selected_text = get_selected_text()
    corrected_text = supprimer_guillemets(correct_text_with_openai(selected_text))
    copy_corrected_text_to_clipboard(corrected_text)

# Callback function for the hotkey to terminate the program
def on_hotkeyKill():
    print('<ctrl>+<alt>+q pressed')
    exit()

# Set up global hotkeys
with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+w': on_hotkeyCorrect,
        '<ctrl>+<alt>+q': on_hotkeyKill}) as h:
    h.join()


#   Explications et Commentaires:
# - Le script utilise la bibliothèque `pyperclip` pour accéder au contenu du presse-papiers.
# - La fonction `correct_text_with_openai` prépare et envoie une requête à l'API GPT-3 pour corriger le texte.
# - Le script utilise la bibliothèque `pynput` pour gérer les raccourcis clavier globaux.
# - La fonction `supprimer_guillemets` retire les guillemets entourant une chaîne.
# - Les fonctions `on_hotkeyCor`, `on_hotkeyKill`, et `on_activate_i` sont des rappels (callbacks) déclenchés par les raccourcis clavier.
# - Le bloc `with keyboard.GlobalHotKeys(...)` configure les raccourcis clavier globaux et associe les callbacks correspondants.