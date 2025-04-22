# Dottify

Dottify est une bibliothèque Python simple qui permet de convertir des dictionnaires en objets accessibles par attributs. Au lieu d'utiliser la syntaxe classique dict["key"], vous pouvez accéder aux valeurs d'un dictionnaire en utilisant la notation par points dict.key après avoir appliqué la transformation.

## Installation

Vous pouvez installer Dottify via pip :
```bash
pip install dottify
```
## Utilisation

Voici un exemple d'utilisation de Dottify :
```python
from dottify import Dottify
           
persons = {
    "Alice": {
        "age": 30,
        "city": "Paris",
        "profession": "Engineer"
    },
    "Charlie": {
        "age": 35,
        "city": "Marseille",
        "profession": "Doctor"
    }
}

persons = Dottify(persons)

print(persons.Alice.age)             # 30
print(persons.Charlie.city)          # Marseille
print(persons.Charlie.age)           # 35
print(persons.Alice.profession)      # Engineer
```
## Fonctionnalités

- Conversion facile de dictionnaires en objets accessibles par attributs.
- Prise en charge des dictionnaires imbriqués.

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à soumettre des demandes de tirage (pull requests) ou à ouvrir des problèmes (issues) sur le dépôt GitHub.

## License

Distribué sous la licence MIT. Voir [LICENSE](LICENSE) pour plus d'informations.

