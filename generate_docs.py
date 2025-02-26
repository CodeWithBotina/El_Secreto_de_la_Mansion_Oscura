# Archivo: generate_docs.py
import os
import sys

def generate_docs():
    """
    Genera la documentación del proyecto usando Sphinx.
    """
    try:
        # Generar archivos .rst automáticamente
        print("Generando archivos .rst...")
        os.system("sphinx-apidoc -o docs/source src")

        # Construir la documentación en HTML
        print("Generando documentación en HTML...")
        os.system("sphinx-build -b html docs/source docs/_build/html")

        print("Documentación generada en docs/_build/html/")
    except Exception as e:
        print(f"Error al generar la documentación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_docs()