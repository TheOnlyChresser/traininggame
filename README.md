# traininggame
Et laeringsspil hvor man bygger og traener en simpel neural network-model i en Pygame UI.

## Krav før første kørsel
- Python 3.10 eller nyere
- `pip` (foelger normalt med Python)
- Internetforbindelse foerste gang: MNIST data downloades automatisk til `./data`

## Første setup (Windows PowerShell)
Kør kommandoerne fra projektets rodmappe:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Hvis PowerShell blokerer aktivering af venv:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Start spillet
```powershell
python main.py
```

## Kør tests
```powershell
python -m unittest discover -s tests
```

## Projektlinks
- Klasse-diagram: https://lucid.app/lucidchart/b7ea6733-79de-4f6f-9dfb-e04d91a4da64/edit?invitationId=inv_28ca8d4d-f137-4d56-95c0-7b8d77946145
