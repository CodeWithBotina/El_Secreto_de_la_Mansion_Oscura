# El Secreto de la Mansión Oscura 🏰

Un juego de misterio y deducción desarrollado en Python usando Pygame y Z3-Solver.

## 📋 Descripción

En una noche tormentosa, el empresario Alexander fue encontrado muerto en su mansión. Como detective principal del caso, deberás:
- Explorar la mansión
- Interrogar a los tres sospechosos principales
- Recolectar pistas
- Resolver el misterio antes de que se agote el tiempo

## 🎮 Características

- **Sistema de exploración**: Múltiples habitaciones y áreas para investigar
- **Personajes interactivos**: Cada sospechoso tiene su propia historia y diálogos
- **Sistema de pistas**: Recolecta información clave para resolver el misterio
- **Temporizador dinámico**: El tiempo es tu enemigo, ¡úsalo sabiamente!
- **Música adaptativa**: La música cambia según la ubicación y situación
- **Múltiples finales**: Tus decisiones afectan el desenlace del caso

## 🔧 Requisitos del Sistema

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- 500MB de espacio libre en disco
- Tarjeta gráfica compatible con Pygame
- Sistema operativo: Windows/Linux/MacOS

## ⚙️ Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/CodeWithBotina/El_Secreto_de_la_Mansion_Oscura.git
cd El_Secreto_de_la_Mansion_Oscura
```

2. **Crear un entorno virtual** (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 🎯 Ejecución

1. **Activar el entorno virtual** (si no está activado)
```bash
# Windows
venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate
```

2. **Ejecutar el juego**
```bash
python src/main.py
```

## 🎮 Controles

- **Flechas**: Mover al detective
- **E**: Interactuar con personajes/objetos
- **ESC**: Pausar juego
- **ESPACIO**: Continuar diálogo

## 🏗️ Estructura del Proyecto

```
El_Secreto_de_la_Mansion_Oscura/
│
├── src/                    # Código fuente
│   ├── assets/            # Recursos del juego
│   │   ├── images/        # Imágenes y sprites
│   │   ├── sounds/        # Música y efectos de sonido
│   │   └── fonts/         # Fuentes tipográficas
│   │
│   ├── game/              # Lógica principal del juego
│   │   ├── __init__.py
│   │   ├── game.py       # Clase principal del juego
│   │   ├── button.py     # Sistema de botones
│   │   ├── character.py  # Lógica de personajes
│   │   └── solver.py     # Sistema de resolución de misterio
│   │
│   └── main.py           # Punto de entrada
│
├── README.md             # Este archivo
├── requirements.txt      # Dependencias del proyecto
└── .gitignore           # Archivos ignorados por git
```

## 🔍 Resolución de Problemas

### Error: No se encuentra Pygame
```bash
pip install pygame
```

### Error: No se encuentra Z3-Solver
```bash
pip install z3-solver
```

### Error: Problemas con el audio
Verifica que tu sistema tenga los drivers de audio actualizados y que no estén muteados.

## 👥 Contribuir

1. Haz un Fork del proyecto
2. Crea una rama para tu función: `git checkout -b feature/NuevaFuncion`
3. Haz commit de tus cambios: `git commit -m 'Añadir nueva función'`
4. Push a la rama: `git push origin feature/NuevaFuncion`
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🎨 Créditos

- Desarrollo: CodeWithBotina
- Música: [Derechos Recervados a Quien Corresponda]
- Sprites y gráficos: [Derechos Recervados a Quien Corresponda]

## 📧 Contacto

- GitHub: [@CodeWithBotina](https://github.com/CodeWithBotina)
- Email: tu@email.com

---
Hecho con ❤️ por CodeWithBotina
