# El Secreto de la Mansión Oscura

# ...existing code...

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/CodeWithBotina/El_Secreto_de_la_Mansion_Oscura.git
cd El_Secreto_de_la_Mansion_Oscura
```

2. Crea un entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta el juego:
```bash
python main.py
```

## 📦 Ejecutable

El ejecutable compilado se encuentra en:
```
dist/El_Secreto_de_la_Mansion_Oscura/El_Secreto_de_la_Mansion_Oscura.exe
```

Para crear el ejecutable:
```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear el ejecutable
python -m PyInstaller game.spec
```

## 🎯 Cómo Jugar

1. **Objetivo**: Descubre quién asesinó a Alexander antes de que se acabe el tiempo
2. **Controles**:
   - Flechas: Mover al personaje
   - E: Interactuar con personajes/objetos
   - ESC: Pausar/Menú
   - ESPACIO: Continuar diálogo

3. **Mecánicas**:
   - Habla con los sospechosos
   - Recolecta pistas
   - Analiza las declaraciones
   - Deduce quién miente

## 🛠️ Tecnologías

- Python 3.7+
- Pygame 2.6.1
- Z3 Solver

## 📁 Estructura del Proyecto

```
El_Secreto_de_la_Mansion_Oscura/
├── src/               # Código fuente
│   ├── game/         # Lógica del juego
│   ├── ui/           # Interfaz de usuario
│   └── utils/        # Utilidades
├── assets/           # Recursos
│   ├── images/       # Gráficos
│   └── sounds/       # Audio
├── docs/            # Documentación
└── tests/           # Pruebas unitarias
```

## 🤝 Contribuir

1. Haz fork del proyecto
2. Crea una rama para tu feature:
```bash
git checkout -b feature/nueva-caracteristica
```
3. Sigue las guías de estilo en docs/development.md
4. Envía un pull request

## 🧪 Tests

Ejecutar las pruebas:
```bash
python -m unittest discover tests
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles

## ✨ Créditos

Desarrollado por CodeWithBotina

## 🐛 Reporte de Bugs

Si encuentras algún bug, por favor crea un issue en el repositorio con:
- Descripción del problema
- Pasos para reproducirlo
- Comportamiento esperado
- Screenshots (si aplica)
