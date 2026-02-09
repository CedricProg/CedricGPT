# CedricGPT (Windows 11, from scratch)

CedricGPT est un agent local minimaliste :
1. vous sélectionnez un texte dans n'importe quelle application,
2. vous appuyez sur un raccourci,
3. le texte est corrigé / traduit / reformulé puis remplacé directement.

Le projet est reparti de zéro, **sans compatibilité avec l'ancien code**.

## Philosophie technique

- **Simple à maintenir** : un runtime principal `cedricgpt.py`.
- **Peu de dépendances** : `openai`, `keyboard`, `pyperclip`.
- **Déploiement facile** : exécution Python ou binaire `.exe` avec PyInstaller.
- **Intégration OS transparente** : hotkeys globaux + copier/coller simulé.

## Architecture

### 1) Hotkeys globales
Le module `keyboard` écoute des raccourcis système Windows.

### 2) Capture de la sélection
Le script envoie `Ctrl+C`, attend un court délai, puis lit le presse-papiers.

### 3) Appel OpenAI (Responses API)
Le texte est envoyé à OpenAI via l'intégration moderne `client.responses.create(...)`.

### 4) Remplacement dans l'app active
Le résultat est copié dans le presse-papiers puis collé avec `Ctrl+V`.
Le presse-papiers d'origine est ensuite restauré.

## Configuration

Variables d'environnement (voir `.env.example`) :

- `OPENAI_API_KEY` : clé API OpenAI
- `CEDRICGPT_MODEL` : modèle (défaut: `gpt-5.2`)
- `CEDRICGPT_HOTKEY_*` : raccourcis globaux
- `CEDRICGPT_AUTO_PASTE` : `1` (colle auto) ou `0`
- `CEDRICGPT_COPY_WAIT_SECONDS` : délai après `Ctrl+C`

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

PowerShell (clé API) :

```powershell
setx OPENAI_API_KEY "sk-..."
```

## Lancer CedricGPT

```bash
python cedricgpt.py
```

Raccourcis par défaut :
- `Ctrl+Alt+Q` : correction
- `Ctrl+Alt+D` : traduction FR ↔ EN
- `Ctrl+Alt+A` : reformulation
- `Ctrl+Alt+K` : quitter

## Générer un exécutable (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --name CedricGPT cedricgpt.py
```

Binaire de sortie : `dist/CedricGPT.exe`

## Notes pratiques

- Sur certains environnements Windows, les hooks clavier globaux peuvent nécessiter des droits élevés.
- Certaines applications sécurisées peuvent bloquer la simulation `Ctrl+C` / `Ctrl+V`.
- Si `gpt-5.2` n'est pas disponible sur votre compte, surchargez `CEDRICGPT_MODEL`.
