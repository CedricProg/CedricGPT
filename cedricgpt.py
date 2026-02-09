"""CedricGPT - Assistant de correction/traduction/reformulation global pour Windows.

Ce script écoute des raccourcis clavier globaux, récupère le texte sélectionné,
l'envoie à l'API OpenAI, puis remplace automatiquement la sélection par le résultat.

Conçu pour être simple à déployer : un seul fichier runtime + variables d'environnement.
"""

from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass
from typing import Final

import keyboard
import pyperclip
from openai import OpenAI


@dataclass(frozen=True)
class AppConfig:
    """Configuration applicative chargée depuis l'environnement.

    Toutes les valeurs sont surchargables via variables `CEDRICGPT_*`.
    """

    # Modèle récent par défaut (modifiable si votre compte/API expose un autre alias)
    model: str = os.getenv("CEDRICGPT_MODEL", "gpt-5.2")

    # Raccourcis globaux
    hotkey_correct: str = os.getenv("CEDRICGPT_HOTKEY_CORRECT", "ctrl+alt+q")
    hotkey_translate: str = os.getenv("CEDRICGPT_HOTKEY_TRANSLATE", "ctrl+alt+d")
    hotkey_rephrase: str = os.getenv("CEDRICGPT_HOTKEY_REPHRASE", "ctrl+alt+a")
    hotkey_quit: str = os.getenv("CEDRICGPT_HOTKEY_QUIT", "ctrl+alt+k")

    # Contrôle du remplacement automatique dans l'application active
    auto_paste: bool = os.getenv("CEDRICGPT_AUTO_PASTE", "1") == "1"

    # Délai pour laisser Windows alimenter le presse-papiers après Ctrl+C
    copy_wait_seconds: float = float(os.getenv("CEDRICGPT_COPY_WAIT_SECONDS", "0.15"))


PROMPTS: Final[dict[str, str]] = {
    "correct": (
        "Tu es un correcteur de texte. Corrige uniquement les fautes d'orthographe et de "
        "grammaire sans changer le sens. Réponds uniquement avec la version finale."
    ),
    "translate": (
        "Traduis le texte en français s'il est en anglais, sinon traduis-le en anglais. "
        "Conserve le ton, l'intention et le sens. Réponds uniquement avec la traduction finale."
    ),
    "rephrase": (
        "Reformule le texte pour le rendre plus clair, naturel et fluide, sans altérer l'idée "
        "d'origine. Réponds uniquement avec la reformulation finale."
    ),
}


class CedricGPT:
    """Orchestrateur principal.

    Étapes d'un traitement:
    1) Copier la sélection active avec Ctrl+C
    2) Interroger OpenAI (Responses API)
    3) Remplacer la sélection avec Ctrl+V (optionnel)
    4) Restaurer le presse-papiers d'origine
    """

    def __init__(self, config: AppConfig) -> None:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY manquante. Définissez-la dans l'environnement.")

        self.client = OpenAI(api_key=api_key)
        self.config = config

        # Empêche deux traitements simultanés si l'utilisateur spamme les hotkeys
        self._busy = threading.Lock()

    def _grab_selected_text(self) -> tuple[str, str]:
        """Capture la sélection active et retourne (texte_selectionne, ancien_presse_papiers)."""
        previous_clipboard = pyperclip.paste()
        keyboard.send("ctrl+c")
        time.sleep(self.config.copy_wait_seconds)
        selected_text = pyperclip.paste().strip()
        return selected_text, previous_clipboard

    def _replace_selection(self, new_text: str) -> None:
        """Place le résultat dans le presse-papiers puis colle dans la fenêtre active."""
        pyperclip.copy(new_text)
        if self.config.auto_paste:
            keyboard.send("ctrl+v")

    @staticmethod
    def _strip_surrounding_quotes(text: str) -> str:
        """Supprime des guillemets englobants éventuels ajoutés par le modèle."""
        if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
            return text[1:-1]
        return text

    def _call_openai(self, mode: str, source_text: str) -> str:
        """Appelle l'API OpenAI via Responses API (intégration recommandée moderne)."""
        response = self.client.responses.create(
            model=self.config.model,
            instructions=PROMPTS[mode],
            input=source_text,
            temperature=0,
        )

        # output_text est la façon la plus simple de récupérer le texte consolidé.
        text = (response.output_text or "").strip()
        return self._strip_surrounding_quotes(text)

    def _transform(self, mode: str) -> None:
        """Pipeline complet pour un mode donné (correct/translate/rephrase)."""
        if not self._busy.acquire(blocking=False):
            print("CedricGPT est déjà en cours de traitement...")
            return

        previous_clipboard = ""
        try:
            selected_text, previous_clipboard = self._grab_selected_text()
            if not selected_text:
                print("Aucun texte sélectionné.")
                return

            result = self._call_openai(mode, selected_text)
            if not result:
                print(f"Réponse vide pour le mode '{mode}'.")
                return

            self._replace_selection(result)
            print(f"[{mode}] terminé")
        except Exception as exc:
            print(f"Erreur CedricGPT ({mode}): {exc}")
        finally:
            # Toujours restaurer le presse-papiers utilisateur
            if previous_clipboard:
                pyperclip.copy(previous_clipboard)
            self._busy.release()

    def run(self) -> None:
        """Démarre la boucle des hotkeys globales."""
        print("CedricGPT démarré")
        print(f"- Correction: {self.config.hotkey_correct}")
        print(f"- Traduction: {self.config.hotkey_translate}")
        print(f"- Reformulation: {self.config.hotkey_rephrase}")
        print(f"- Quitter: {self.config.hotkey_quit}")

        keyboard.add_hotkey(self.config.hotkey_correct, lambda: self._transform("correct"))
        keyboard.add_hotkey(self.config.hotkey_translate, lambda: self._transform("translate"))
        keyboard.add_hotkey(self.config.hotkey_rephrase, lambda: self._transform("rephrase"))

        # Sortie immédiate du process à la demande utilisateur
        keyboard.add_hotkey(self.config.hotkey_quit, lambda: os._exit(0))
        keyboard.wait()


def main() -> None:
    """Point d'entrée exécutable."""
    app = CedricGPT(AppConfig())
    app.run()


if __name__ == "__main__":
    main()
