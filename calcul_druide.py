"""
Programme de calculatrice RPN (Calcul Druide).

Auteur: Etudiant BUT2
Date: 12/2023
Description: Lit un fichier contenant une expression NPI et affiche le résultat.
Respecte les normes PEP8 et les bonnes pratiques de développement efficace.
"""

import sys
from pathlib import Path
from typing import List, Union

# [cite_start]Constantes pour éviter les "Magic Strings" [cite: 242]
OP_ADD = "+"
OP_SUB = "-"
OP_MUL = "*"
OP_DIV = "/"
VALID_OPERATORS = {OP_ADD, OP_SUB, OP_MUL, OP_DIV}


def perform_operation(op: str, val1: int, val2: int) -> int:
    """
    Exécute une opération dyadique entre deux entiers.

    :param op: L'opérateur (+, -, *, /)
    :param val1: Le premier opérande (celui dépilé en second)
    :param val2: Le second opérande (celui dépilé en premier)
    :return: Le résultat entier de l'opération
    :raises ZeroDivisionError: Si division par zéro
    :raises ValueError: Si l'opérateur est inconnu
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
        return int(val1 / val2)  # Division entière demandée implicitement
    else:
        raise ValueError(f"Opérateur inconnu : {op}")


def calculate_rpn(expression: str) -> int:
    """
    Calcule le résultat d'une expression en notation polonaise inverse.

    :param expression: Chaîne de caractères (ex: "3 5 +")
    :return: Résultat du calcul
    :raises IndexError: Si l'expression est mal formée (pas assez d'opérandes)
    :raises ValueError: Si un token est invalide
    """
    stack: List[int] = []
    tokens = expression.split()

    for token in tokens:
        if token in VALID_OPERATORS:
            # [cite_start]Vérification de la contrainte dyadique [cite: 11]
            if len(stack) < 2:
                raise IndexError(f"Calcul impossible : pile insuffisante pour '{token}'")
            
            # Attention : l'ordre est important pour -, /. 
            # Le dernier empilé est le 2ème opérande.
            op2 = stack.pop()
            op1 = stack.pop()
            
            res = perform_operation(token, op1, op2)
            stack.append(res)
        else:
            try:
                # Tente de convertir en entier
                stack.append(int(token))
            except ValueError:
                raise ValueError(f"Token invalide détecté : '{token}'")

    if len(stack) != 1:
        raise ValueError("Expression incomplète : il reste plusieurs nombres dans la pile.")

    return stack[0]


def get_expression_from_file(file_path: Path) -> str:
    """
    Lit le contenu d'un fichier texte de manière sûre.

    [cite_start]Utilise read_text avec encodage explicite[cite: 145, 372].
    :param file_path: Chemin vers le fichier
    :return: Le contenu du fichier sous forme de chaîne
    """
    return file_path.read_text(encoding="utf-8").strip()


def main() -> int:
    """
    Point d'entrée principal du programme.
    Gère les arguments CLI et les exceptions de haut niveau.
    """
    # Gestion des arguments (nom de fichier attendu)
    if len(sys.argv) != 2:
        print("Usage: python calcul_druide.py <fichier_calcul.txt>", file=sys.stderr)
        return 1

    input_file = Path(sys.argv[1])

    try:
        # [cite_start]1. Lecture [cite: 372]
        expression = get_expression_from_file(input_file)
        print(f"Expression lue : {expression}")

        # 2. Calcul
        result = calculate_rpn(expression)
        
        # 3. Affichage
        print(f"Résultat : {result}")
        return 0

    except FileNotFoundError:
        # [cite_start]Gestion spécifique erreur fichier [cite: 208]
        print(f"Erreur : Le fichier '{input_file}' est introuvable.", file=sys.stderr)
        return 2
    except (ValueError, IndexError, ZeroDivisionError) as e:
        # Gestion des erreurs de logique métier
        print(f"Erreur de calcul : {e}", file=sys.stderr)
        return 3
    except Exception as e:
        # Filet de sécurité global (logging recommandé en prod)
        print(f"Erreur inattendue : {e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    # [cite_start]Point d'entrée protégé [cite: 318]
    sys.exit(main())