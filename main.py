"""
El Secreto de la Mansión Oscura - Punto de entrada principal
"""
import sys
import os
import traceback
import pygame

def setup_environment():
    """Configure environment for the game"""
    # Agregar la ruta del proyecto al PYTHONPATH
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)
    
    # Configurar codificación para la consola
    if sys.platform.startswith('win'):
        os.system('chcp 65001')

def main():
    """Main entry point"""
    try:
        setup_environment()
        
        # Importar después de configurar el environment
        from src.game.game import Game
        
        # Inicializar Pygame
        pygame.init()
        
        # Crear y ejecutar el juego
        game = Game()
        game.run()
        
    except Exception as e:
        # Mostrar error detallado
        print("\nError durante la ejecución del juego:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Descripción: {str(e)}")
        print("\nTraceback completo:")
        traceback.print_exc()
        
        # Mantener la ventana abierta para ver el error
        input("\nPresiona Enter para cerrar...")
        
    finally:
        # Limpiar recursos
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
