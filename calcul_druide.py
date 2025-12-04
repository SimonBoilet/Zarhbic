"""
Programme de calculatrice RPN (Calcul Druide).
Version : Corrigée pour analyse statique (Pylint/Embold).

Auteur: Etudiant BUT2
Date: 12/2023
Description: Lit un fichier défini dans une variable et affiche le résultat NPI.
Respecte les normes PEP8 et les bonnes pratiques.
"""

import sys
from pathlib import Path
from typing import List

# --- CONFIGURATION ---
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
    Correction R1705 : Suppression des 'elif' inutiles après return.
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
    Correction W0707 : Ajout de 'from None' lors de la levée d'exception.
    """
    stack: List[int] = []
    tokens = expression.split()

    for token in tokens:
        if token in VALID_OPERATORS:
            if len(stack) < 2:
                raise IndexError(f"Calcul impossible : pile insuffisante pour '{token}'")
            
            op2 = stack.pop()
            op1 = stack.pop()
            
            res = perform_operation(token, op1, op2)
            stack.append(res)
        else:
            try:
                stack.append(int(token))
            except ValueError as e:
                # Correction W0707 : Chainage explicite de l'exception
                raise ValueError(f"Token invalide détecté : '{token}'") from e

    if len(stack) != 1:
        msg = f"Expression incomplète : il reste {len(stack)} nombres."
        raise ValueError(msg)

    return stack[0]


def main() -> int:
    """
    Orchestrateur principal.
    Correction W0703 : Suppression du catch-all 'Exception'.
    """
    input_path = Path(FICHIER_ENTREE)

    # Correction W1309 : Suppression du f-string inutile
    print("--- Démarrage du Calcul Druide ---")
    print(f"Fichier cible : {input_path.absolute()}")

    try:
        expression = input_path.read_text(encoding="utf-8").strip()
        print(f"Expression lue : {expression}")

        result = calculate_rpn(expression)
        
        print(f"Résultat final : {result}")
        return 0

    except FileNotFoundError:
        # Correction C0301 : Coupe de la ligne trop longue
        print(f"Erreur : Le fichier '{FICHIER_ENTREE}' n'existe pas.",
              file=sys.stderr)
        return 1
    except (ValueError, IndexError, ZeroDivisionError) as e:
        print(f"Erreur de calcul : {e}", file=sys.stderr)
        return 2
    # Suppression du bloc 'except Exception' (W0703)


if __name__ == "__main__":
    sys.exit(main())