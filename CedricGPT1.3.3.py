import pyperclip
import requests
from pynput import keyboard
from openai import OpenAI

GPTmodel = "gpt-4o-mini"

client = OpenAI(
    api_key="", #mettre sa propre clé API ici
)

def get_selected_text():
    return pyperclip.paste()

def correct_text_with_openai(text):
    text_to_correct = "Tu es un outil de correction d'orthographe. Corrige uniquement l'orthographe, ne réponds que le texte corrigé. Certains mots peuvent être en anglais, ou la phrase peut être entièrement en anglais, c'est normal, adapte-toi à la langue :\n\n" + text + "\n"
    print(text_to_correct)  # logs
    
    completion = client.chat.completions.create(
        model= GPTmodel,
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": text_to_correct}
        ],
        max_tokens=1024,
        temperature=0
    )
    print(completion.choices[0].message.content)
    corrected_text = completion.choices[0].message.content.strip()
    return corrected_text

def translate_text_with_openai(text):
    prompt = (
        "traduit le texte en anglais s'il est en français,"
        "ou en français s'il est en anglais. la traduction doit garder le sens de la phrase mais n'est pas forcement litérale, elle est gramaticalment juste:\n\n"
        f"{text}\n"
    )
    print(prompt)  # logs

    completion = client.chat.completions.create(
        model=GPTmodel,
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0
    )
    print(completion.choices[0].message.content)
    translated_text = completion.choices[0].message.content.strip()
    return translated_text

def rephrase_text_with_openai(text):
    prompt = (
        "Reformule les mots et idées suivants en désordre pour créer une phrase ou un texte clair et compréhensible:\n\n"
        f"{text}\n"
    )
    print(prompt)  # logs

    completion = client.chat.completions.create(
        model=GPTmodel,
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0
    )
    print(completion.choices[0].message.content)
    rephrased_text = completion.choices[0].message.content.strip()
    return rephrased_text

def supprimer_guillemets(chaine):
    if chaine.startswith('"') and chaine.endswith('"'):
        return chaine[1:-1]
    else:
        return chaine

def copy_corrected_text_to_clipboard(corrected_text):
    pyperclip.copy(corrected_text)

def on_hotkeyCor():
    print('Global hotkey activated!')
    selected_text = get_selected_text()
    corrected_text = correct_text_with_openai(selected_text)
    corrected_text = supprimer_guillemets(corrected_text)
    copy_corrected_text_to_clipboard(corrected_text)

def on_hotkeyTranslate():
    print('Translation hotkey activated!')
    selected_text = get_selected_text()
    translated_text = translate_text_with_openai(selected_text)
    translated_text = supprimer_guillemets(translated_text)
    copy_corrected_text_to_clipboard(translated_text)

def on_hotkeyRephrase():
    print('Rephrasing hotkey activated!')
    selected_text = get_selected_text()
    rephrased_text = rephrase_text_with_openai(selected_text)
    rephrased_text = supprimer_guillemets(rephrased_text)
    copy_corrected_text_to_clipboard(rephrased_text)


def on_hotkeyKill():
    print('<ctrl>+<alt>+k pressed')
    exit()

with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+q': on_hotkeyCor,
        '<ctrl>+<alt>+k': on_hotkeyKill,
        '<ctrl>+<alt>+d': on_hotkeyTranslate,
        '<ctrl>+<alt>+a': on_hotkeyRephrase}) as h:
    h.join()
