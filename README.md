---

# El Secreto de la Mansión Oscura 🏰

Un emocionante juego de misterio y deducción desarrollado en Python utilizando **Pygame** para la interfaz gráfica y **Z3-Solver** para la lógica de resolución de acertijos. Sumérgete en una historia llena de intriga, pistas y múltiples finales.

---

## 📋 Descripción del Juego

En una noche tormentosa, el empresario **Alexander** fue encontrado muerto en su mansión. Como detective principal del caso, tendrás que:

- **Explorar la mansión**: Recorre múltiples habitaciones y áreas para descubrir pistas.
- **Interrogar a los sospechosos**: Tres personajes con sus propias historias y secretos.
- **Recolectar pistas**: Encuentra objetos y detalles clave para resolver el misterio.
- **Resolver el enigma**: Usa tu lógica y las pistas recolectadas para descubrir al culpable antes de que se agote el tiempo.

---

## 🎮 Características Principales

- **Sistema de exploración**: Navega por diferentes áreas de la mansión, cada una con su propio diseño y desafíos.
- **Personajes interactivos**: Cada sospechoso tiene diálogos únicos y comportamientos que cambian según tu progreso.
- **Sistema de pistas**: Recolecta y combina pistas para avanzar en la investigación.
- **Temporizador dinámico**: El tiempo corre en contra tuya, ¡debes ser rápido y eficiente!
- **Música adaptativa**: La banda sonora cambia según la situación y la ubicación en la mansión.
- **Múltiples finales**: Tus decisiones y descubrimientos afectan el desenlace de la historia.

---

## 🔧 Requisitos del Sistema

- **Python**: Versión 3.12.x
- **Pip**: Gestor de paquetes de Python
- **Espacio en disco**: 500MB libres
- **Tarjeta gráfica**: Compatible con Pygame
- **Sistema operativo**: Windows 10/11 (también compatible con Linux y macOS con configuraciones adicionales)

---

## ⚙️ Instalación

Sigue estos pasos para configurar y ejecutar el juego:

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/CodeWithBotina/El_Secreto_de_la_Mansion_Oscura.git
   cd El_Secreto_de_la_Mansion_Oscura
   ```

2. **Crear un entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**:
   - Para instalar solo las dependencias principales:
     ```bash
     pip install .
     ```
   - Para instalar dependencias de desarrollo, pruebas y documentación:
     ```bash
     pip install .[dev,test,docs]
     ```

---

## 🎯 Ejecución del Juego

1. **Activar el entorno virtual**:
   ```bash
   venv\Scripts\activate
   ```

2. **Ejecutar el juego**:
   ```bash
   python main.py
   ```

---

## 🎮 Controles

- **Flechas (↑ ↓ ← →)**: Mover al detective.
- **E**: Interactuar con personajes u objetos.
- **ESC**: Pausar el juego.
- **ESPACIO**: Continuar diálogos.

---

## 🏗️ Estructura del Proyecto

```
El_Secreto_de_la_Mansion_Oscura/
│
├── assets/                       # Recursos del juego
│   ├── images/                   # Imágenes y sprites
│   └── sounds/                   # Música y efectos de sonido
│
├── src/                          # Código fuente
│   ├── game/                     # Lógica principal del juego
│   │    ├── __init__.py
│   │    ├── game.py              # Clase principal del juego
│   │    ├── game_constants.py    # Constantes del juego
│   │    ├── game_maps.py         # Mapeo de las habitaciones
│   │    └── game_state.py        # Estados del juego
│   │
│   ├── ui/                       # Interfaz de usuario
│   │    ├── __init__.py
│   │    └── button.py            # Sistema de botones
│   │
│   └── utils/                    # Utilidades del juego
│        ├── __init__.py
│        ├── logger.py            # Registro del juego
│        ├── path_manager.py      # Administrador de rutas
│        └── resource_manager.py  # Administrador de recursos
│
├── docs/                         # Documentación
│   └── source/                   # Archivos .rst
│
├── test/                         # Pruebas del proyecto
│   ├── __init__.py
│   ├── test_game.py              # Pruebas del juego
│   └── test_resource_manager.py  # Pruebas del administrador de recursos
│
├── main.py                       # Punto de entrada del juego
├── README.md                     # Este archivo
├── LICENSE                       # Licencia del proyecto
├── pyproject.toml                # Configuración del proyecto y dependencias
├── .gitignore                    # Archivos ignorados por Git
├── game.spec                     # Configuración para empaquetar el juego
├── libz3.dll                     # Biblioteca Z3 para Windows
└── generate_docs.py              # Script para generar documentación
```

---

## 🔍 Resolución de Problemas

### 1. **Problemas con Z3-Solver**
Si encuentras errores relacionados con Z3-Solver, sigue estos pasos:
```bash
pip uninstall z3-solver
pip install importlib_resources>=5.0.0
pip install z3-solver==4.12.3.0
```

### 2. **Problemas con Pygame**
Si Pygame no funciona correctamente, reinstálalo con:
```bash
pip uninstall pygame
pip install pygame==2.6.1
```

### 3. **Problemas con el audio**
- Asegúrate de que los drivers de audio estén actualizados.
- Verifica que el volumen no esté muteado en el sistema.

### 4. **Problemas con importlib_resources**
Si falta `importlib_resources`, instálalo con:
```bash
pip install importlib_resources>=5.0.0
```

---

## 👥 Contribuir

¡Tu ayuda es bienvenida! Sigue estos pasos para contribuir:

1. Haz un **Fork** del proyecto.
2. Crea una rama para tu función: `git checkout -b feature/NuevaFuncion`.
3. Haz commit de tus cambios: `git commit -m 'Añadir nueva función'`.
4. Sube la rama: `git push origin feature/NuevaFuncion`.
5. Abre un **Pull Request** para revisar tus cambios.

---

## 📝 Licencia

Este proyecto está bajo la **Licencia MIT**. Para más detalles, consulta el archivo [LICENSE](LICENSE).

---

## 🎨 Créditos

- **Desarrollo**: CodeWithBotina
- **Música**: [Derechos Reservados a Quien Corresponda]
- **Sprites y gráficos**: [Derechos Reservados a Quien Corresponda]

---

## 📧 Contacto

- **GitHub**: [@CodeWithBotina](https://github.com/CodeWithBotina)
- **Email**: CodeWithBotina.team@outlook.com

---

Hecho con ❤️ por **CodeWithBotina**. ¡Diviértete resolviendo el misterio! 🕵️‍♂️

---
