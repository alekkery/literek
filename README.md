## literek README

___literek___  urządzenia edukacyjnego wspierającego naukę poprzez zabawę z fiszkami. Działanie aplikacji polega na losowym usuwaniu jednej litery ze słów pobranych z bazy danych i wyświetlaniu ich ze znakiem `_` w miejscu luki. Zadaniem użytkownika jest pokazanie odpowiedniej fiszki do kamery urządzenia. System analizuje obraz, rozpoznaje literę i weryfikuje poprawność odpowiedzi – w razie sukcesu przechodzi do kolejnego hasła, a w przypadku błędu pozwala na ponowną próbę.

## Zalecenia
___zalecamy używać___ `UV` https://docs.astral.sh/uv/

Przy uzyciu ___UV___ uruchamiamy przez `uv run main.py`

### Pobranie uv
Windown `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Linux/MacOS `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Dane
Wypakowane pliki z teachable machine idą do `./model_data/`

Pliki ze słowami idą do `./word_data/`

