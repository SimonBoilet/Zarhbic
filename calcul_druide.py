"""
Programme de calculatrice RPN (Calcul Druide).
Version : Fichier d'entrée défini par variable.

Auteur: Etudiant BUT2
Date: 12/2023
Description: Lit un fichier défini dans une variable et affiche le résultat NPI.
Respecte les normes PEP8 et les bonnes pratiques (Pathlib, Typage).
"""

import sys
from pathlib import Path
from typing import List

# --- CONFIGURATION ---
# Nom du fichier à lire (à modifier ici)
FICHIER_ENTREE = "calcul.txt"

# --- CONSTANTES ---
OP_ADD = "+"
OP_SUB = "-"
OP_MUL = "*"
OP_DIV = "/"
VALID_OPERATORS = {OP_ADD, OP_SUB, OP_MUL, OP_DIV}


def perform_operation(op: str, val1: int, val2: int) -> int:
    """
    Exécute une opération dyadique entre deux entiers.
    """
    if op == OP_ADD:
        return val1 + val2
    elif op == OP_SUB:
        return val1 - val2
    elif op == OP_MUL:
        return val1 * val2
    elif op == OP_DIV:
        if val2 == 0:
            raise ZeroDivisionError("Division par zéro impossible.")
        return int(val1 / val2)
    else:
        raise ValueError(f"Opérateur inconnu : {op}")


def calculate_rpn(expression: str) -> int:
    """
    Calcule le résultat d'une expression en notation polonaise inverse.
    """
    stack: List[int] = []
    tokens = expression.split()

    for token in tokens:
        if token in VALID_OPERATORS:
            if len(stack) < 2:
                raise IndexError(f"Calcul impossible : pile insuffisante pour '{token}'")
            
            # L'ordre de dépilement est crucial pour la soustraction et la division
            op2 = stack.pop()  # Le dernier élément empilé (2ème opérande)
            op1 = stack.pop()  # L'avant-dernier élément empilé (1er opérande)
            
            res = perform_operation(token, op1, op2)
            stack.append(res)
        else:
            try:
                stack.append(int(token))
            except ValueError:
                raise ValueError(f"Token invalide détecté : '{token}'")

    if len(stack) != 1:
        raise ValueError(f"Expression incomplète : il reste {len(stack)} nombres dans la pile.")

    return stack[0]


def main() -> int:
    """
    Orchestrateur principal.
    Utilise la constante FICHIER_ENTREE au lieu des arguments système.
    """
    # Utilisation de Pathlib pour gérer le chemin du fichier [cite: 119]
    input_path = Path(FICHIER_ENTREE)

    print(f"--- Démarrage du Calcul Druide ---")
    print(f"Fichier cible : {input_path.absolute()}")

    try:
        # Lecture avec encodage explicite [cite: 119, 346]
        # read_text() ouvre, lit et ferme le fichier proprement
        expression = input_path.read_text(encoding="utf-8").strip()
        
        print(f"Expression lue : {expression}")

        # Calcul
        result = calculate_rpn(expression)
        
        print(f"Résultat final : {result}")
        return 0

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{FICHIER_ENTREE}' n'existe pas.", file=sys.stderr)
        print("Veuillez vérifier le nom du fichier dans la variable 'FICHIER_ENTREE'.", file=sys.stderr)
        return 1
    except (ValueError, IndexError, ZeroDivisionError) as e:
        print(f"Erreur de calcul : {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Erreur inattendue : {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    # Appel de main
    main()