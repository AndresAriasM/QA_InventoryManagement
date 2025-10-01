# Sistema de Gestión de Inventarios

## 📋 Descripción

Sistema de gestión de inventarios desarrollado en Python que permite administrar productos, controlar stock, generar reportes y realizar análisis estadísticos del inventario.

## 🚀 Características

- **Gestión de Productos**: Agregar, eliminar, actualizar productos
- **Control de Stock**: Monitoreo y actualización de inventario
- **Búsqueda Avanzada**: Por nombre y categoría
- **Reportes**: Stock bajo, valor del inventario, estadísticas
- **Análisis Completo**: Estadísticas detalladas y recomendaciones
- **Persistencia**: Almacenamiento en formato JSON
- **Validaciones**: Entrada de datos segura y validada

## 🛠️ Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd QA_InventoryManagement
```

2. Instalar dependencias (opcional):
```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Ejecutar el sistema:
```bash
python main.py
```

### Ejecutar tests:
```bash
python test_inventario.py
```

## 📁 Estructura del Proyecto

```
QA_InventoryManagement/
├── main.py                    # Interfaz de usuario principal
├── inventario.py              # Lógica de gestión del inventario
├── producto.py                # Modelo de datos del producto
├── test_inventario.py         # Tests unitarios completos
├── requirements.txt           # Dependencias del proyecto
├── sonar-project.properties   # Configuración SonarQube
└── README.md                  # Documentación del proyecto
```

## 🔧 Funcionalidades Principales

### Gestión de Productos
- Agregar productos con validación completa
- Eliminar productos del inventario
- Actualizar información de productos
- Búsqueda por nombre y categoría

### Control de Inventario
- Monitoreo de stock en tiempo real
- Alertas de stock bajo
- Cálculo de valor total del inventario
- Análisis estadístico completo

### Reportes y Análisis
- Reporte de productos con stock bajo
- Valor total del inventario
- Estadísticas por categoría
- Recomendaciones automáticas

## 🧪 Testing

El proyecto incluye una suite completa de tests unitarios que cubren:

- **Tests de Producto**: Creación, actualización, cálculos
- **Tests de Inventario**: Operaciones CRUD, búsquedas, reportes
- **Tests de Integración**: Flujos completos del sistema
- **Tests de Validación**: Manejo de errores y casos límite

### Ejecutar tests:
```bash
python -m unittest test_inventario.py -v
```

## 📊 Análisis de Calidad

El proyecto está configurado para análisis con SonarQube:

- **Métricas de Código**: Complejidad, duplicación, mantenibilidad
- **Cobertura de Tests**: Análisis de cobertura de código
- **Code Smells**: Detección de problemas de calidad
- **Seguridad**: Análisis de vulnerabilidades

## 🔒 Validaciones y Seguridad

- **Validación de Entrada**: Todos los datos de usuario son validados
- **Manejo de Errores**: Gestión robusta de excepciones
- **Tipos de Datos**: Validación de tipos y rangos
- **Límites de Datos**: Restricciones de longitud y valores

## 📈 Mejoras Implementadas

### Refactorización
- ✅ Función extremadamente larga dividida en métodos específicos
- ✅ Eliminación de código duplicado
- ✅ Mejora de la legibilidad y mantenibilidad

### Confiabilidad
- ✅ Validaciones robustas de entrada
- ✅ Manejo seguro de errores
- ✅ Prevención de divisiones por cero
- ✅ Validación de índices de arrays

### Testing
- ✅ Suite completa de tests unitarios
- ✅ Tests de integración
- ✅ Cobertura de casos límite
- ✅ Tests de validación de errores

### Calidad de Código
- ✅ Eliminación de imports no utilizados
- ✅ Eliminación de variables sin usar
- ✅ Nombres de funciones descriptivos
- ✅ Documentación completa

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para la nueva funcionalidad
3. Commit los cambios
4. Push a la rama
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 👥 Autores

- **Sistema de Gestión de Inventarios** - Desarrollo inicial
- **Equipo de QA** - Mejoras de calidad y testing

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto, contactar al equipo de desarrollo.