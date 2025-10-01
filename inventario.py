import json
import os
import logging
from typing import List, Optional, Dict, Any
from producto import Producto

class SecurityError(Exception):
    """Excepción personalizada para errores de seguridad."""
    pass

class Inventario:
    """
    Clase que gestiona el inventario de productos.
    
    Permite agregar, eliminar, actualizar y buscar productos,
    así como generar reportes y estadísticas.
    """
    
    def __init__(self, archivo_datos: str = "inventario.json"):
        """
        Inicializa el inventario.
        
        Args:
            archivo_datos (str): Nombre del archivo para persistir los datos
        """
        self.productos: Dict[str, Producto] = {}
        self.archivo_datos = archivo_datos
        self.cargar_datos()
    
    def agregar_producto(self, producto: Producto) -> bool:
        """
        Agrega un producto al inventario.
        
        Args:
            producto (Producto): Producto a agregar
            
        Returns:
            bool: True si se agregó exitosamente, False si ya existe
        """
        if producto.id in self.productos:
            return False
        
        self.productos[producto.id] = producto
        self.guardar_datos()
        return True
    
    def eliminar_producto(self, id_producto: str) -> bool:
        """
        Elimina un producto del inventario.
        
        Args:
            id_producto (str): ID del producto a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False si no existe
        """
        if id_producto not in self.productos:
            return False
        
        del self.productos[id_producto]
        self.guardar_datos()
        return True
    
    def obtener_producto(self, id_producto: str) -> Optional[Producto]:
        """
        Obtiene un producto por su ID.
        
        Args:
            id_producto (str): ID del producto
            
        Returns:
            Optional[Producto]: Producto si existe, None si no existe
        """
        return self.productos.get(id_producto)
    
    def actualizar_stock(self, id_producto: str, nueva_cantidad: int) -> bool:
        """
        Actualiza el stock de un producto.
        
        Args:
            id_producto (str): ID del producto
            nueva_cantidad (int): Nueva cantidad en stock
            
        Returns:
            bool: True si se actualizó exitosamente, False si no existe
        """
        producto = self.obtener_producto(id_producto)
        if producto is None:
            return False
        
        producto.actualizar_stock(nueva_cantidad)
        self.guardar_datos()
        return True
    
    def actualizar_precio(self, id_producto: str, nuevo_precio: float) -> bool:
        """
        Actualiza el precio de un producto.
        
        Args:
            id_producto (str): ID del producto
            nuevo_precio (float): Nuevo precio
            
        Returns:
            bool: True si se actualizó exitosamente, False si no existe
        """
        producto = self.obtener_producto(id_producto)
        if producto is None:
            return False
        
        producto.actualizar_precio(nuevo_precio)
        self.guardar_datos()
        return True
    
    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        """
        Busca productos por nombre (búsqueda parcial, insensible a mayúsculas).
        
        Args:
            nombre (str): Nombre o parte del nombre a buscar
            
        Returns:
            List[Producto]: Lista de productos que coinciden
        """
        nombre_lower = nombre.lower()
        return [producto for producto in self.productos.values() 
                if nombre_lower in producto.nombre.lower()]
    
    def buscar_por_categoria(self, categoria: str) -> List[Producto]:
        """
        Busca productos por categoría (búsqueda parcial, insensible a mayúsculas).
        
        Args:
            categoria (str): Categoría o parte de la categoría a buscar
            
        Returns:
            List[Producto]: Lista de productos que coinciden
        """
        categoria_lower = categoria.lower()
        return [producto for producto in self.productos.values() 
                if categoria_lower in producto.categoria.lower()]
    
    def obtener_todos_productos(self) -> List[Producto]:
        """
        Obtiene todos los productos del inventario.
        
        Returns:
            List[Producto]: Lista de todos los productos
        """
        return list(self.productos.values())
    
    def productos_bajo_stock(self, umbral: int = 10) -> List[Producto]:
        """
        Obtiene productos con stock bajo.
        
        Args:
            umbral (int): Cantidad mínima para considerar stock bajo
            
        Returns:
            List[Producto]: Lista de productos con stock bajo
        """
        return [producto for producto in self.productos.values() 
                if producto.cantidad < umbral]
    
    def calcular_valor_total_inventario(self) -> float:
        """
        Calcula el valor total del inventario.
        
        Returns:
            float: Valor total del inventario
        """
        return sum(producto.calcular_valor_total() for producto in self.productos.values())
    
    def obtener_producto_mas_caro(self) -> Optional[Producto]:
        """
        Obtiene el producto más caro del inventario.
        
        Returns:
            Optional[Producto]: Producto más caro o None si no hay productos
        """
        if not self.productos:
            return None
        
        return max(self.productos.values(), key=lambda p: p.precio)
    
    def obtener_producto_mas_barato(self) -> Optional[Producto]:
        """
        Obtiene el producto más barato del inventario.
        
        Returns:
            Optional[Producto]: Producto más barato o None si no hay productos
        """
        if not self.productos:
            return None
        
        return min(self.productos.values(), key=lambda p: p.precio)
    
    def calcular_promedio_precios_por_categoria(self) -> Dict[str, float]:
        """
        Calcula el promedio de precios por categoría.
        
        Returns:
            Dict[str, float]: Diccionario con categoría y promedio de precios
        """
        categorias = {}
        
        for producto in self.productos.values():
            if producto.categoria not in categorias:
                categorias[producto.categoria] = []
            categorias[producto.categoria].append(producto.precio)
        
        promedios = {}
        for categoria, precios in categorias.items():
            promedios[categoria] = sum(precios) / len(precios)
        
        return promedios
    
    def generar_reporte_stock_bajo(self, umbral: int = 10) -> str:
        """
        Genera un reporte de productos con stock bajo.
        
        Args:
            umbral (int): Cantidad mínima para considerar stock bajo
            
        Returns:
            str: Reporte formateado
        """
        productos_bajo = self.productos_bajo_stock(umbral)
        
        if not productos_bajo:
            return f"No hay productos con stock menor a {umbral} unidades."
        
        reporte = f"REPORTE DE PRODUCTOS BAJO STOCK (menor a {umbral} unidades)\n"
        reporte += "=" * 60 + "\n"
        
        for producto in productos_bajo:
            reporte += f"{producto}\n"
        
        return reporte
    
    def generar_reporte_valor_inventario(self) -> str:
        """
        Genera un reporte del valor total del inventario.
        
        Returns:
            str: Reporte formateado
        """
        valor_total = self.calcular_valor_total_inventario()
        total_productos = len(self.productos)
        
        reporte = "REPORTE DE VALOR DEL INVENTARIO\n"
        reporte += "=" * 40 + "\n"
        reporte += f"Total de productos: {total_productos}\n"
        reporte += f"Valor total del inventario: ${valor_total:.2f}\n"
        
        return reporte
    
    def generar_estadisticas(self) -> str:
        """
        Genera un reporte con estadísticas del inventario.
        
        Returns:
            str: Reporte formateado
        """
        if not self.productos:
            return "No hay productos en el inventario."
        
        producto_mas_caro = self.obtener_producto_mas_caro()
        producto_mas_barato = self.obtener_producto_mas_barato()
        promedios_categoria = self.calcular_promedio_precios_por_categoria()
        
        reporte = "ESTADÍSTICAS DEL INVENTARIO\n"
        reporte += "=" * 40 + "\n"
        reporte += f"Total de productos: {len(self.productos)}\n"
        reporte += f"Valor total del inventario: ${self.calcular_valor_total_inventario():.2f}\n\n"
        
        reporte += "PRODUCTO MÁS CARO:\n"
        reporte += f"{producto_mas_caro}\n\n"
        
        reporte += "PRODUCTO MÁS BARATO:\n"
        reporte += f"{producto_mas_barato}\n\n"
        
        reporte += "PROMEDIO DE PRECIOS POR CATEGORÍA:\n"
        for categoria, promedio in promedios_categoria.items():
            reporte += f"{categoria}: ${promedio:.2f}\n"
        
        return reporte
    
    def guardar_datos(self):
        """
        Guarda los datos del inventario en el archivo JSON de forma segura.
        """
        # Validar y sanitizar el nombre del archivo
        archivo_seguro = self._validar_ruta_archivo(self.archivo_datos)
        
        datos = {
            'productos': [producto.to_dict() for producto in self.productos.values()]
        }
        
        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(archivo_seguro)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, mode=0o755, exist_ok=True)
            
            # Escribir archivo con permisos seguros
            with open(archivo_seguro, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
            
            # Establecer permisos seguros
            os.chmod(archivo_seguro, 0o644)
            
        except (OSError, IOError, PermissionError) as e:
            print(f"Error al guardar datos: {e}")
            raise
    
    def cargar_datos(self):
        """
        Carga los datos del inventario desde el archivo JSON de forma segura.
        """
        # Validar y sanitizar el nombre del archivo
        archivo_seguro = self._validar_ruta_archivo(self.archivo_datos)
        
        if not os.path.exists(archivo_seguro):
            return
        
        try:
            # Verificar que el archivo no sea un enlace simbólico malicioso
            if os.path.islink(archivo_seguro):
                raise SecurityError("No se permiten enlaces simbólicos por seguridad")
            
            # Verificar permisos del archivo
            if not os.access(archivo_seguro, os.R_OK):
                raise PermissionError("Sin permisos de lectura para el archivo")
            
            with open(archivo_seguro, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            # Validar estructura de datos
            if not isinstance(datos, dict):
                raise ValueError("Formato de archivo inválido")
            
            self.productos = {}
            productos_data = datos.get('productos', [])
            
            if not isinstance(productos_data, list):
                raise ValueError("Formato de productos inválido")
            
            for producto_data in productos_data:
                if not isinstance(producto_data, dict):
                    continue  # Saltar entradas inválidas
                
                try:
                producto = Producto.from_dict(producto_data)
                self.productos[producto.id] = producto
                except (KeyError, ValueError, TypeError) as e:
                    print(f"Error al cargar producto: {e}")
                    continue  # Continuar con el siguiente producto
                
        except (json.JSONDecodeError, KeyError, ValueError, PermissionError, OSError) as e:
            # Log del error sin exponer información sensible
            self._log_error_seguro("Error al cargar datos del inventario", e)
            print("Error: No se pudieron cargar los datos del inventario. Se iniciará con inventario vacío.")
            self.productos = {}
    
    def _validar_ruta_archivo(self, ruta: str) -> str:
        """
        Valida y sanitiza la ruta del archivo para prevenir path traversal.
        
        Args:
            ruta: Ruta del archivo a validar
        
        Returns:
            str: Ruta sanitizada y segura
            
        Raises:
            SecurityError: Si la ruta es insegura
        """
        if not ruta or not isinstance(ruta, str):
            raise ValueError("Ruta de archivo inválida")
        
        # Normalizar la ruta
        ruta_normalizada = os.path.normpath(ruta)
        
        # Verificar que no contenga secuencias peligrosas
        secuencias_peligrosas = ['..', '~', '//', '\\\\']
        for secuencia in secuencias_peligrosas:
            if secuencia in ruta_normalizada:
                raise SecurityError(f"Ruta insegura detectada: {secuencia}")
        
        # Verificar que la ruta esté dentro del directorio de trabajo
        directorio_actual = os.getcwd()
        ruta_absoluta = os.path.abspath(ruta_normalizada)
        
        if not ruta_absoluta.startswith(directorio_actual):
            raise SecurityError("Ruta fuera del directorio permitido")
        
        return ruta_absoluta
    
    def _log_error_seguro(self, mensaje: str, error: Exception):
        """
        Registra errores de forma segura sin exponer información sensible.
        
        Args:
            mensaje: Mensaje descriptivo del error
            error: Excepción capturada
        """
        # Configurar logging seguro
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('inventario_errors.log'),
                logging.StreamHandler()
            ]
        )
        
        # Log solo información segura
        logging.error(f"{mensaje}: {type(error).__name__}")
    
    def generar_analisis_completo_inventario(self, umbral_precio_alto: float = 100.0, 
                                           umbral_precio_bajo: float = 50.0,
                                           umbral_stock_bajo: int = 10,
                                           umbral_stock_medio: int = 25,
                                           umbral_desviacion: float = 20.0,
                                           umbral_productos_bajo_stock: int = 3,
                                           umbral_precio_competitivo: float = 80.0,
                                           umbral_stock_alto: int = 50):
        """
        Genera un análisis completo del inventario con estadísticas y recomendaciones.
        
        Args:
            umbral_precio_alto: Umbral para considerar precios altos
            umbral_precio_bajo: Umbral para considerar precios bajos
            umbral_stock_bajo: Umbral para stock bajo
            umbral_stock_medio: Umbral para stock medio
            umbral_desviacion: Umbral para desviación estándar
            umbral_productos_bajo_stock: Umbral para productos bajo stock
            umbral_precio_competitivo: Umbral para precios competitivos
            umbral_stock_alto: Umbral para stock alto
        
        Returns:
            dict: Análisis completo del inventario
        """
        # Validar parámetros
        if umbral_precio_alto <= 0 or umbral_precio_bajo <= 0:
            raise ValueError("Los umbrales de precio deben ser positivos")
        if umbral_stock_bajo < 0 or umbral_stock_medio < 0:
            raise ValueError("Los umbrales de stock no pueden ser negativos")
        
        # Procesar datos del inventario
        datos_inventario = self._procesar_datos_inventario()
        estadisticas = self._calcular_estadisticas_por_categoria(datos_inventario)
        analisis_stock = self._analizar_stock_por_categoria(datos_inventario, umbral_stock_bajo, umbral_stock_medio)
        productos_clasificados = self._clasificar_productos_por_precio(umbral_precio_alto, umbral_precio_bajo)
        reportes = self._generar_reportes_por_categoria(estadisticas, analisis_stock)
        optimizaciones = self._calcular_optimizaciones(estadisticas)
        recomendaciones = self._generar_recomendaciones(estadisticas, analisis_stock, 
                                                      umbral_desviacion, umbral_productos_bajo_stock,
                                                      umbral_precio_competitivo, umbral_stock_alto)
        
        return {
            'resumen': {
                'total_productos': len(self.productos),
                'valor_total_inventario': datos_inventario['valor_total'],
                'categorias_unicas': len(estadisticas)
            },
            'estadisticas': estadisticas,
            'analisis_stock': analisis_stock,
            'productos_clasificados': productos_clasificados,
            'reportes': reportes,
            'optimizaciones': optimizaciones,
            'recomendaciones': recomendaciones
        }
    
    def _procesar_datos_inventario(self) -> dict:
        """Procesa los datos básicos del inventario."""
        valor_total = 0
        categorias = set()
        
        for producto in self.productos.values():
            valor_total += producto.calcular_valor_total()
            categorias.add(producto.categoria)
        
        return {
            'valor_total': valor_total,
            'categorias': list(categorias)
        }
    
    def _calcular_estadisticas_por_categoria(self, datos_inventario: dict) -> dict:
        """Calcula estadísticas detalladas por categoría."""
        estadisticas = {}
        
        for categoria in datos_inventario['categorias']:
            productos_categoria = [p for p in self.productos.values() if p.categoria == categoria]
            precios = [p.precio for p in productos_categoria]
            
            if precios:
                estadisticas[categoria] = self._calcular_estadisticas_precios(precios, len(productos_categoria))
        
        return estadisticas
    
    def _calcular_estadisticas_precios(self, precios: list, total_productos: int) -> dict:
        """Calcula estadísticas de precios para una categoría."""
        if not precios:
            return {}
        
        precio_promedio = sum(precios) / len(precios)
        precio_maximo = max(precios)
        precio_minimo = min(precios)
        desviacion_estandar = self._calcular_desviacion_estandar(precios, precio_promedio)
        
        return {
            'precio_promedio': round(precio_promedio, 2),
            'precio_maximo': precio_maximo,
            'precio_minimo': precio_minimo,
            'desviacion_estandar': round(desviacion_estandar, 2),
            'total_productos': total_productos
        }
    
    def _calcular_desviacion_estandar(self, precios: list, promedio: float) -> float:
        """Calcula la desviación estándar de una lista de precios."""
        if len(precios) <= 1:
            return 0.0
        
        suma_cuadrados = sum((precio - promedio) ** 2 for precio in precios)
        return (suma_cuadrados / len(precios)) ** 0.5
    
    def _analizar_stock_por_categoria(self, datos_inventario: dict, umbral_bajo: int, umbral_medio: int) -> dict:
        """Analiza el stock por categoría."""
        analisis = {}
        
        for categoria in datos_inventario['categorias']:
            productos_categoria = [p for p in self.productos.values() if p.categoria == categoria]
            stock_total = sum(p.cantidad for p in productos_categoria)
            stock_promedio = stock_total / len(productos_categoria) if productos_categoria else 0
            
            bajo_stock = sum(1 for p in productos_categoria if p.cantidad < umbral_bajo)
            stock_medio = sum(1 for p in productos_categoria if umbral_bajo <= p.cantidad < umbral_medio)
            stock_alto = sum(1 for p in productos_categoria if p.cantidad >= umbral_medio)
            
            analisis[categoria] = {
                'stock_total': stock_total,
                'stock_promedio': round(stock_promedio, 2),
                'productos_bajo_stock': bajo_stock,
                'productos_stock_medio': stock_medio,
                'productos_stock_alto': stock_alto
            }
        
        return analisis
    
    def _clasificar_productos_por_precio(self, umbral_alto: float, umbral_bajo: float) -> dict:
        """Clasifica productos por rango de precios."""
        especiales = []
        normales = []
        economicos = []
        
        for producto in self.productos.values():
            if producto.precio > umbral_alto:
                especiales.append(producto.id)
            elif producto.precio < umbral_bajo:
                economicos.append(producto.id)
            else:
                normales.append(producto.id)
        
        return {
            'especiales': especiales,
            'normales': normales,
            'economicos': economicos
        }
    
    def _generar_reportes_por_categoria(self, estadisticas: dict, analisis_stock: dict) -> list:
        """Genera reportes detallados por categoría."""
        reportes = []
        
        for categoria in estadisticas.keys():
            reporte = f"Reporte para categoría: {categoria}\n"
            reporte += "=" * 50 + "\n"
            
            # Estadísticas de precios
            stats = estadisticas[categoria]
            reporte += f"Precio promedio: ${stats['precio_promedio']:.2f}\n"
            reporte += f"Precio máximo: ${stats['precio_maximo']:.2f}\n"
            reporte += f"Precio mínimo: ${stats['precio_minimo']:.2f}\n"
            reporte += f"Desviación estándar: ${stats['desviacion_estandar']:.2f}\n"
            reporte += f"Total productos: {stats['total_productos']}\n"
            
            # Análisis de stock
            if categoria in analisis_stock:
                analisis = analisis_stock[categoria]
                reporte += f"Stock total: {analisis['stock_total']}\n"
                reporte += f"Stock promedio: {analisis['stock_promedio']:.2f}\n"
                reporte += f"Productos bajo stock: {analisis['productos_bajo_stock']}\n"
                reporte += f"Productos stock medio: {analisis['productos_stock_medio']}\n"
                reporte += f"Productos stock alto: {analisis['productos_stock_alto']}\n"
            
            reportes.append(reporte)
        
        return reportes
    
    def _calcular_optimizaciones(self, estadisticas: dict) -> dict:
        """Calcula métricas de optimización por categoría."""
        optimizaciones = {}
        
        for categoria, stats in estadisticas.items():
            # Obtener precios de la categoría
            precios = [p.precio for p in self.productos.values() if p.categoria == categoria]
            
            if len(precios) > 0:
                precios_ordenados = sorted(precios)
                n = len(precios_ordenados)
                
                # Calcular percentiles
                percentil_25 = precios_ordenados[int(n * 0.25)] if n > 0 else 0
                percentil_50 = precios_ordenados[int(n * 0.5)] if n > 0 else 0
                percentil_75 = precios_ordenados[int(n * 0.75)] if n > 0 else 0
                percentil_90 = precios_ordenados[int(n * 0.9)] if n > 0 else 0
                
                # Calcular coeficiente de variación
                promedio = stats['precio_promedio']
                desviacion = stats['desviacion_estandar']
                coeficiente_variacion = (desviacion / promedio) if promedio > 0 else 0
                
                optimizaciones[categoria] = {
                    'percentil_25': round(percentil_25, 2),
                    'percentil_50': round(percentil_50, 2),
                    'percentil_75': round(percentil_75, 2),
                    'percentil_90': round(percentil_90, 2),
                    'coeficiente_variacion': round(coeficiente_variacion, 4),
                    'rango_intercuartilico': round(percentil_75 - percentil_25, 2)
                }
        
        return optimizaciones
    
    def _generar_recomendaciones(self, estadisticas: dict, analisis_stock: dict,
                               umbral_desviacion: float, umbral_productos_bajo_stock: int,
                               umbral_precio_competitivo: float, umbral_stock_alto: int) -> list:
        """Genera recomendaciones basadas en el análisis."""
        recomendaciones = []
        
        for categoria in estadisticas.keys():
            stats = estadisticas[categoria]
            analisis = analisis_stock.get(categoria, {})
            
            recomendacion = f"Recomendaciones para {categoria}:\n"
            
            # Recomendaciones basadas en desviación estándar
            if stats['desviacion_estandar'] > umbral_desviacion:
                recomendacion += "- Alta variabilidad en precios, considerar estandarización\n"
            
            # Recomendaciones basadas en stock
            if analisis.get('productos_bajo_stock', 0) > umbral_productos_bajo_stock:
                recomendacion += "- Muchos productos con stock bajo, revisar reabastecimiento\n"
            
            # Recomendaciones basadas en precios
            if stats['precio_promedio'] > umbral_precio_competitivo:
                recomendacion += "- Precios altos, evaluar competitividad\n"
            
            # Recomendaciones basadas en stock alto
            if analisis.get('stock_promedio', 0) > umbral_stock_alto:
                recomendacion += "- Stock alto, considerar promociones\n"
            
            if len(recomendacion.split('\n')) > 1:  # Solo agregar si hay recomendaciones
                recomendaciones.append(recomendacion)
        
        return recomendaciones
    
    def calcular_valor_inventario_con_descuentos(self, umbral_precio: float = 100.0, 
                                                factor_alto: float = 1.1, 
                                                factor_bajo: float = 0.9) -> float:
        """
        Calcula el valor del inventario aplicando descuentos según el precio.
        
        Args:
            umbral_precio: Precio umbral para aplicar diferentes factores
            factor_alto: Factor a aplicar a productos con precio alto
            factor_bajo: Factor a aplicar a productos con precio bajo
            
        Returns:
            float: Valor total del inventario con descuentos aplicados
        """
        if umbral_precio <= 0:
            raise ValueError("El umbral de precio debe ser positivo")
        if factor_alto <= 0 or factor_bajo <= 0:
            raise ValueError("Los factores deben ser positivos")
        
        total = 0
        for producto in self.productos.values():
            if producto.precio > umbral_precio:
                total += producto.precio * factor_alto
            else:
                total += producto.precio * factor_bajo
        return total