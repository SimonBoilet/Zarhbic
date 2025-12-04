"""
Programme : "Calcul Druide"
Python version : 3.10+

Auteur: Simon Boilet
Date: 04/12/2025
"""

import sys
from pathlib import Path
from typing import List

FICHIER_ENTREE = "calcul.txt"

OP_ADD = "+"
OP_SUB = "-"
OP_MUL = "*"
OP_DIV = "/"
VALID_OPERATORS = {OP_ADD, OP_SUB, OP_MUL, OP_DIV}


def perform_operation(op: str, val1: int, val2: int) -> int:
    """
    Exécute une opération entre deux entiers.
    """
    if op == OP_ADD:
        return val1 + val2
    if op == OP_SUB:
        return val1 - val2
    if op == OP_MUL:
        return val1 * val2
    if op == OP_DIV:
        if val2 == 0:
            raise ZeroDivisionError("Division par zéro impossible.")
        return int(val1 / val2)
    
    raise ValueError(f"Opérateur inconnu : {op}")


def calculate_rpn(expression: str) -> int:
    """
    Calcule le résultat d'une expression en notation polonaise inverse.
    """
    stack: List[int] = []
    items = expression.split()

    for item in items:
        if item in VALID_OPERATORS:
            if len(stack) < 2:
                raise IndexError(f"Calcul impossible : pile insuffisante pour '{item}'")
            
            op2 = stack.pop()
            op1 = stack.pop()
            
            res = perform_operation(item, op1, op2)
            stack.append(res)
        else:
            try:
                stack.append(int(item))
            except ValueError as e:
                raise ValueError(f"item invalide détecté : '{item}'") from e

    if len(stack) != 1:
        msg = f"Expression incomplète : il reste {len(stack)} nombres."
        raise ValueError(msg)

    return stack[0]


def main() -> int:
    """
    Programme principal.
    """
    file_path = Path(FICHIER_ENTREE)

    print("--- Démarrage du Calcul Druide ---")
    print(f"Fichier cible : {file_path.absolute()}")

    try:
        expression = file_path.read_text(encoding="utf-8").strip()
        print(f"Expression lue : {expression}")

        result = calculate_rpn(expression)
        
        print(f"Résultat final : {result}")
        return 0

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{FICHIER_ENTREE}' n'existe pas.",
              file=sys.stderr)
        return 1
    except (ValueError, IndexError, ZeroDivisionError) as e:
        print(f"Erreur de calcul : {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())