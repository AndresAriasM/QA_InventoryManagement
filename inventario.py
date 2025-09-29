import json
import os
from typing import List, Optional, Dict, Any
from producto import Producto
import sys  # Import no utilizado
import datetime  # Import no utilizado

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
        # Variables sin usar para generar New Issues
        variable_inutil = "no se usa"
        numero_sin_proposito = 999
    
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
        Guarda los datos del inventario en el archivo JSON.
        """
        datos = {
            'productos': [producto.to_dict() for producto in self.productos.values()]
        }
        
        with open(self.archivo_datos, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
    
    def cargar_datos(self):
        """
        Carga los datos del inventario desde el archivo JSON.
        """
        if not os.path.exists(self.archivo_datos):
            return
        
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            self.productos = {}
            for producto_data in datos.get('productos', []):
                producto = Producto.from_dict(producto_data)
                self.productos[producto.id] = producto
                
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error al cargar los datos: {e}")
            self.productos = {}
    
    # MÉTODOS DUPLICADOS PARA GENERAR DUPLICATIONS
    def calcular_valor_total_inventario_duplicado(self) -> float:
        """
        Calcula el valor total del inventario.
        
        Returns:
            float: Valor total del inventario
        """
        return sum(producto.calcular_valor_total() for producto in self.productos.values())
    
    def calcular_valor_total_inventario_otro(self) -> float:
        """
        Calcula el valor total del inventario.
        
        Returns:
            float: Valor total del inventario
        """
        return sum(producto.calcular_valor_total() for producto in self.productos.values())
    
    # FUNCIÓN MUY LARGA Y MAL NOMBRADA PARA MAINTAINABILITY
    def funcion_muy_larga_y_mal_nombrada_que_hace_muchas_cosas_diferentes_y_es_dificil_de_mantener(self, param1, param2, param3, param4, param5):
        """
        Esta función es muy larga y hace muchas cosas diferentes.
        """
        # Variables sin usar
        var1 = "no se usa"
        var2 = 123
        var3 = []
        
        # Lógica compleja y repetitiva
        resultado = 0
        for i in range(100):
            if i % 2 == 0:
                resultado += i * 2
            else:
                resultado += i * 3
        
        # Más lógica innecesaria
        lista_temporal = []
        for j in range(50):
            if j > 25:
                lista_temporal.append(j * 2)
            else:
                lista_temporal.append(j * 3)
        
        # Procesamiento adicional
        suma_total = 0
        for k in range(len(lista_temporal)):
            if k % 2 == 0:
                suma_total += lista_temporal[k] * 2
            else:
                suma_total += lista_temporal[k] * 3
        
        # Más código innecesario
        diccionario_temporal = {}
        for l in range(30):
            if l % 3 == 0:
                diccionario_temporal[f"key_{l}"] = l * 4
            elif l % 3 == 1:
                diccionario_temporal[f"key_{l}"] = l * 5
            else:
                diccionario_temporal[f"key_{l}"] = l * 6
        
        # Procesamiento final
        valor_final = 0
        for m in range(20):
            if m % 4 == 0:
                valor_final += m * 7
            elif m % 4 == 1:
                valor_final += m * 8
            elif m % 4 == 2:
                valor_final += m * 9
            else:
                valor_final += m * 10
        
        # Retorno complejo
        return {
            'resultado': resultado,
            'suma_total': suma_total,
            'valor_final': valor_final,
            'diccionario': diccionario_temporal,
            'param1': param1,
            'param2': param2,
            'param3': param3,
            'param4': param4,
            'param5': param5
        }
    
    def obtener_total_productos_version1(self):
        """Calcula total de productos"""
        return len(self.productos)

    def obtener_total_productos_version2(self):
        """Calcula total de productos"""  
        return len(self.productos)

    def get_cantidad_productos(self):
        """Calcula total de productos"""
        return len(self.productos)

    def contar_productos_inventario(self):
        """Calcula total de productos"""
        return len(self.productos)

    def procesar_inventario_metodo_1(self):
        total = 0
        for producto in self.productos.values():
            if producto.precio > 100:
                total += producto.precio * 1.1
            else:
                total += producto.precio * 0.9
        return total

    def procesar_inventario_metodo_2(self):
        total = 0
        for producto in self.productos.values():
            if producto.precio > 100:
                total += producto.precio * 1.1
            else:
                total += producto.precio * 0.9
        return total

    def funcion_extremadamente_larga_y_compleja_que_procesa_todo_el_inventario_con_multiples_validaciones_calculos_estadisticos_y_generacion_de_reportes_detallados(
        self, parametro1, parametro2, parametro3, parametro4, parametro5, parametro6, parametro7, parametro8, parametro9, parametro10):
        """
        Esta función es extremadamente larga y hace demasiadas cosas diferentes.
        Procesa inventario, calcula estadísticas, genera reportes y hace validaciones.
        """
        # Variables temporales innecesarias
        var_temp_1 = "variable temporal 1"
        var_temp_2 = 12345
        var_temp_3 = []
        var_temp_4 = {}
        var_temp_5 = None
        var_temp_6 = True
        var_temp_7 = 3.14159
        var_temp_8 = "otra variable"
        var_temp_9 = [1, 2, 3, 4, 5]
        var_temp_10 = {"key": "value"}
        
        # Procesamiento inicial del inventario
        total_productos = len(self.productos)
        valor_total_inventario = 0
        productos_por_categoria = {}
        precios_por_categoria = {}
        stock_por_categoria = {}
        
        # Primer bucle: procesar todos los productos
        for producto in self.productos.values():
            valor_total_inventario += producto.calcular_valor_total()
            
            if producto.categoria not in productos_por_categoria:
                productos_por_categoria[producto.categoria] = 0
                precios_por_categoria[producto.categoria] = []
                stock_por_categoria[producto.categoria] = 0
            
            productos_por_categoria[producto.categoria] += 1
            precios_por_categoria[producto.categoria].append(producto.precio)
            stock_por_categoria[producto.categoria] += producto.cantidad
        
        # Segundo bucle: cálculos complejos
        estadisticas_detalladas = {}
        for categoria, precios in precios_por_categoria.items():
            if len(precios) > 0:
                precio_promedio = sum(precios) / len(precios)
                precio_maximo = max(precios)
                precio_minimo = min(precios)
                desviacion_estandar = 0
                
                # Calcular desviación estándar
                for precio in precios:
                    desviacion_estandar += (precio - precio_promedio) ** 2
                desviacion_estandar = (desviacion_estandar / len(precios)) ** 0.5
                
                estadisticas_detalladas[categoria] = {
                    'precio_promedio': precio_promedio,
                    'precio_maximo': precio_maximo,
                    'precio_minimo': precio_minimo,
                    'desviacion_estandar': desviacion_estandar,
                    'total_productos': productos_por_categoria[categoria],
                    'stock_total': stock_por_categoria[categoria]
                }
        
        # Tercer bucle: procesamiento adicional
        productos_especiales = []
        productos_normales = []
        productos_economicos = []
        
        for producto in self.productos.values():
            if producto.precio > parametro1 * parametro2:
                productos_especiales.append(producto)
            elif producto.precio < parametro3 * parametro4:
                productos_economicos.append(producto)
            else:
                productos_normales.append(producto)
        
        # Cuarto bucle: cálculos de tendencias
        tendencias_precio = {}
        for categoria in precios_por_categoria.keys():
            precios = precios_por_categoria[categoria]
            if len(precios) > 1:
                tendencia = 0
                for i in range(1, len(precios)):
                    if precios[i] > precios[i-1]:
                        tendencia += 1
                    elif precios[i] < precios[i-1]:
                        tendencia -= 1
                tendencias_precio[categoria] = tendencia / (len(precios) - 1)
            else:
                tendencias_precio[categoria] = 0
        
        # Quinto bucle: análisis de stock
        analisis_stock = {}
        for categoria in stock_por_categoria.keys():
            stock_total = stock_por_categoria[categoria]
            productos_categoria = productos_por_categoria[categoria]
            stock_promedio = stock_total / productos_categoria if productos_categoria > 0 else 0
            
            productos_bajo_stock = 0
            productos_stock_medio = 0
            productos_stock_alto = 0
            
            for producto in self.productos.values():
                if producto.categoria == categoria:
                    if producto.cantidad < parametro5:
                        productos_bajo_stock += 1
                    elif producto.cantidad < parametro6:
                        productos_stock_medio += 1
                    else:
                        productos_stock_alto += 1
            
            analisis_stock[categoria] = {
                'stock_total': stock_total,
                'stock_promedio': stock_promedio,
                'productos_bajo_stock': productos_bajo_stock,
                'productos_stock_medio': productos_stock_medio,
                'productos_stock_alto': productos_stock_alto
            }
        
        # Sexto bucle: generación de reportes
        reportes_generados = []
        for categoria in self.productos.keys():
            reporte_categoria = f"Reporte para categoría: {categoria}\n"
            reporte_categoria += "=" * 50 + "\n"
            
            if categoria in estadisticas_detalladas:
                stats = estadisticas_detalladas[categoria]
                reporte_categoria += f"Precio promedio: ${stats['precio_promedio']:.2f}\n"
                reporte_categoria += f"Precio máximo: ${stats['precio_maximo']:.2f}\n"
                reporte_categoria += f"Precio mínimo: ${stats['precio_minimo']:.2f}\n"
                reporte_categoria += f"Desviación estándar: ${stats['desviacion_estandar']:.2f}\n"
                reporte_categoria += f"Total productos: {stats['total_productos']}\n"
                reporte_categoria += f"Stock total: {stats['stock_total']}\n"
            
            if categoria in analisis_stock:
                analisis = analisis_stock[categoria]
                reporte_categoria += f"Stock promedio: {analisis['stock_promedio']:.2f}\n"
                reporte_categoria += f"Productos bajo stock: {analisis['productos_bajo_stock']}\n"
                reporte_categoria += f"Productos stock medio: {analisis['productos_stock_medio']}\n"
                reporte_categoria += f"Productos stock alto: {analisis['productos_stock_alto']}\n"
            
            reportes_generados.append(reporte_categoria)
        
        # Séptimo bucle: cálculos de optimización
        optimizaciones = {}
        for categoria in precios_por_categoria.keys():
            precios = precios_por_categoria[categoria]
            if len(precios) > 0:
                # Calcular percentiles
                precios_ordenados = sorted(precios)
                n = len(precios_ordenados)
                percentil_25 = precios_ordenados[int(n * 0.25)] if n > 0 else 0
                percentil_50 = precios_ordenados[int(n * 0.5)] if n > 0 else 0
                percentil_75 = precios_ordenados[int(n * 0.75)] if n > 0 else 0
                percentil_90 = precios_ordenados[int(n * 0.9)] if n > 0 else 0
                
                # Calcular coeficiente de variación
                precio_promedio = sum(precios) / len(precios)
                desviacion = (sum((p - precio_promedio) ** 2 for p in precios) / len(precios)) ** 0.5
                coeficiente_variacion = desviacion / precio_promedio if precio_promedio > 0 else 0
                
                # Calcular rango intercuartílico
                rango_intercuartilico = percentil_75 - percentil_25
                
                optimizaciones[categoria] = {
                    'percentil_25': percentil_25,
                    'percentil_50': percentil_50,
                    'percentil_75': percentil_75,
                    'percentil_90': percentil_90,
                    'coeficiente_variacion': coeficiente_variacion,
                    'rango_intercuartilico': rango_intercuartilico
                }
        
        # Octavo bucle: análisis de correlaciones
        correlaciones = {}
        for categoria1 in precios_por_categoria.keys():
            for categoria2 in precios_por_categoria.keys():
                if categoria1 != categoria2:
                    precios1 = precios_por_categoria[categoria1]
                    precios2 = precios_por_categoria[categoria2]
                    
                    if len(precios1) > 1 and len(precios2) > 1:
                        # Calcular correlación de Pearson
                        n = min(len(precios1), len(precios2))
                        suma1 = sum(precios1[:n])
                        suma2 = sum(precios2[:n])
                        suma_productos = sum(precios1[i] * precios2[i] for i in range(n))
                        suma_cuadrados1 = sum(p ** 2 for p in precios1[:n])
                        suma_cuadrados2 = sum(p ** 2 for p in precios2[:n])
                        
                        numerador = n * suma_productos - suma1 * suma2
                        denominador = ((n * suma_cuadrados1 - suma1 ** 2) * (n * suma_cuadrados2 - suma2 ** 2)) ** 0.5
                        
                        correlacion = numerador / denominador if denominador != 0 else 0
                        correlaciones[f"{categoria1}-{categoria2}"] = correlacion
        
        # Noveno bucle: generación de recomendaciones
        recomendaciones = []
        for categoria in estadisticas_detalladas.keys():
            stats = estadisticas_detalladas[categoria]
            analisis = analisis_stock.get(categoria, {})
            
            recomendacion = f"Recomendaciones para {categoria}:\n"
            
            if stats['desviacion_estandar'] > parametro7:
                recomendacion += "- Alta variabilidad en precios, considerar estandarización\n"
            
            if analisis.get('productos_bajo_stock', 0) > parametro8:
                recomendacion += "- Muchos productos con stock bajo, revisar reabastecimiento\n"
            
            if stats['precio_promedio'] > parametro9:
                recomendacion += "- Precios altos, evaluar competitividad\n"
            
            if analisis.get('stock_promedio', 0) > parametro10:
                recomendacion += "- Stock alto, considerar promociones\n"
            
            recomendaciones.append(recomendacion)
        
        # Décimo bucle: cálculos finales
        metricas_finales = {}
        for categoria in precios_por_categoria.keys():
            precios = precios_por_categoria[categoria]
            if len(precios) > 0:
                # Calcular moda
                frecuencias = {}
                for precio in precios:
                    precio_redondeado = round(precio, 2)
                    frecuencias[precio_redondeado] = frecuencias.get(precio_redondeado, 0) + 1
                
                moda = max(frecuencias, key=frecuencias.get) if frecuencias else 0
                
                # Calcular asimetría
                precio_promedio = sum(precios) / len(precios)
                desviacion = (sum((p - precio_promedio) ** 2 for p in precios) / len(precios)) ** 0.5
                asimetria = sum(((p - precio_promedio) / desviacion) ** 3 for p in precios) / len(precios) if desviacion > 0 else 0
                
                # Calcular curtosis
                curtosis = sum(((p - precio_promedio) / desviacion) ** 4 for p in precios) / len(precios) - 3 if desviacion > 0 else 0
                
                metricas_finales[categoria] = {
                    'moda': moda,
                    'asimetria': asimetria,
                    'curtosis': curtosis
                }
        
        # Retorno extremadamente complejo
        return {
            'total_productos': total_productos,
            'valor_total_inventario': valor_total_inventario,
            'estadisticas_detalladas': estadisticas_detalladas,
            'tendencias_precio': tendencias_precio,
            'analisis_stock': analisis_stock,
            'reportes_generados': reportes_generados,
            'optimizaciones': optimizaciones,
            'correlaciones': correlaciones,
            'recomendaciones': recomendaciones,
            'metricas_finales': metricas_finales,
            'productos_especiales': len(productos_especiales),
            'productos_normales': len(productos_normales),
            'productos_economicos': len(productos_economicos),
            'parametros_utilizados': {
                'param1': parametro1, 'param2': parametro2, 'param3': parametro3,
                'param4': parametro4, 'param5': parametro5, 'param6': parametro6,
                'param7': parametro7, 'param8': parametro8, 'param9': parametro9,
                'param10': parametro10
            },
            'variables_temporales': {
                'var1': var_temp_1, 'var2': var_temp_2, 'var3': var_temp_3,
                'var4': var_temp_4, 'var5': var_temp_5, 'var6': var_temp_6,
                'var7': var_temp_7, 'var8': var_temp_8, 'var9': var_temp_9,
                'var10': var_temp_10
            }
        }
    
    # FUNCIONES DUPLICADAS PARA GENERAR DUPLICATIONS
    def buscar_productos_por_nombre_alternativo(self, nombre: str) -> List[Producto]:
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
    
    def encontrar_productos_por_nombre(self, nombre: str) -> List[Producto]:
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
    
    def localizar_productos_por_nombre(self, nombre: str) -> List[Producto]:
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
    
    def buscar_productos_por_categoria_alternativo(self, categoria: str) -> List[Producto]:
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
    
    def encontrar_productos_por_categoria(self, categoria: str) -> List[Producto]:
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
    
    def localizar_productos_por_categoria(self, categoria: str) -> List[Producto]:
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
    
    def obtener_todos_los_productos(self) -> List[Producto]:
        """
        Obtiene todos los productos del inventario.
        
        Returns:
            List[Producto]: Lista de todos los productos
        """
        return list(self.productos.values())
    
    def listar_todos_productos(self) -> List[Producto]:
        """
        Obtiene todos los productos del inventario.
        
        Returns:
            List[Producto]: Lista de todos los productos
        """
        return list(self.productos.values())
    
    def devolver_todos_productos(self) -> List[Producto]:
        """
        Obtiene todos los productos del inventario.
        
        Returns:
            List[Producto]: Lista de todos los productos
        """
        return list(self.productos.values())
    
    def calcular_valor_inventario_total(self) -> float:
        """
        Calcula el valor total del inventario.
        
        Returns:
            float: Valor total del inventario
        """
        return sum(producto.calcular_valor_total() for producto in self.productos.values())
    
    def obtener_valor_total_inventario(self) -> float:
        """
        Calcula el valor total del inventario.
        
        Returns:
            float: Valor total del inventario
        """
        return sum(producto.calcular_valor_total() for producto in self.productos.values())
    
    def sumar_valor_inventario(self) -> float:
        """
        Calcula el valor total del inventario.
        
        Returns:
            float: Valor total del inventario
        """
        return sum(producto.calcular_valor_total() for producto in self.productos.values())
    
    def procesar_inventario_metodo_3(self):
        total = 0
        for producto in self.productos.values():
            if producto.precio > 100:
                total += producto.precio * 1.1
            else:
                total += producto.precio * 0.9
        return total
    
    def procesar_inventario_metodo_4(self):
        total = 0
        for producto in self.productos.values():
            if producto.precio > 100:
                total += producto.precio * 1.1
            else:
                total += producto.precio * 0.9
        return total
    
    def procesar_inventario_metodo_5(self):
        total = 0
        for producto in self.productos.values():
            if producto.precio > 100:
                total += producto.precio * 1.1
            else:
                total += producto.precio * 0.9
        return total
    
    # VULNERABILIDADES DE SEGURIDAD INTENCIONALES
    def ejecutar_comando_sistema(self, comando_usuario):
        """
        VULNERABILIDAD: Ejecuta comandos del sistema sin validación
        """
        import os
        import subprocess
        
        # VULNERABILIDAD CRÍTICA: Ejecución de comandos sin sanitización
        resultado = os.system(comando_usuario)
        return resultado
    
    def ejecutar_comando_subprocess(self, comando_usuario):
        """
        VULNERABILIDAD: Ejecuta comandos con subprocess sin validación
        """
        import subprocess
        
        # VULNERABILIDAD CRÍTICA: Shell injection
        resultado = subprocess.run(comando_usuario, shell=True, capture_output=True, text=True)
        return resultado.stdout
    
    def evaluar_codigo_dinamico(self, codigo_usuario):
        """
        VULNERABILIDAD: Ejecuta código Python dinámicamente
        """
        # VULNERABILIDAD CRÍTICA: Code injection
        resultado = eval(codigo_usuario)
        return resultado
    
    def ejecutar_codigo_dinamico(self, codigo_usuario):
        """
        VULNERABILIDAD: Ejecuta código Python dinámicamente
        """
        # VULNERABILIDAD CRÍTICA: Code injection
        resultado = exec(codigo_usuario)
        return resultado
    
    def cargar_archivo_json_inseguro(self, ruta_archivo):
        """
        VULNERABILIDAD: Carga archivos JSON sin validación
        """
        import json
        
        # VULNERABILIDAD: Path traversal y carga sin validación
        with open(ruta_archivo, 'r') as archivo:
            datos = json.load(archivo)
        return datos
    
    def guardar_datos_inseguro(self, datos_usuario, ruta_archivo):
        """
        VULNERABILIDAD: Guarda datos sin validación
        """
        import json
        
        # VULNERABILIDAD: Path traversal y escritura sin validación
        with open(ruta_archivo, 'w') as archivo:
            json.dump(datos_usuario, archivo)
    
    def procesar_entrada_usuario_insegura(self, entrada_usuario):
        """
        VULNERABILIDAD: Procesa entrada de usuario sin sanitización
        """
        # VULNERABILIDAD: SQL injection simulation
        query = f"SELECT * FROM productos WHERE nombre = '{entrada_usuario}'"
        
        # VULNERABILIDAD: XSS simulation
        html_response = f"<div>Resultado: {entrada_usuario}</div>"
        
        # VULNERABILIDAD: Command injection simulation
        comando = f"ls -la {entrada_usuario}"
        
        return {
            'query': query,
            'html': html_response,
            'comando': comando
        }
    
    def autenticacion_insegura(self, usuario, password):
        """
        VULNERABILIDAD: Autenticación insegura
        """
        # VULNERABILIDAD: Password en texto plano
        usuarios = {
            'admin': 'admin123',
            'user': 'password',
            'test': 'test123'
        }
        
        # VULNERABILIDAD: Comparación insegura
        if usuarios.get(usuario) == password:
            return True
        return False
    
    def generar_token_inseguro(self, usuario):
        """
        VULNERABILIDAD: Generación de token insegura
        """
        import base64
        import hashlib
        
        # VULNERABILIDAD: Token predecible
        token_simple = base64.b64encode(f"{usuario}:{hashlib.md5(usuario.encode()).hexdigest()}".encode()).decode()
        
        # VULNERABILIDAD: Hash débil (MD5)
        token_md5 = hashlib.md5(f"{usuario}secret".encode()).hexdigest()
        
        return {
            'token_simple': token_simple,
            'token_md5': token_md5
        }
    
    def validar_entrada_insegura(self, entrada):
        """
        VULNERABILIDAD: Validación insegura de entrada
        """
        # VULNERABILIDAD: No hay validación de entrada
        # VULNERABILIDAD: Permite caracteres peligrosos
        resultado = entrada
        
        # VULNERABILIDAD: Concatenación directa sin escape
        mensaje = f"Procesando: {resultado}"
        
        # VULNERABILIDAD: Uso de pickle sin validación
        import pickle
        datos_serializados = pickle.dumps(resultado)
        
        return {
            'mensaje': mensaje,
            'datos_serializados': datos_serializados
        }
    
    def acceso_archivo_inseguro(self, nombre_archivo):
        """
        VULNERABILIDAD: Acceso a archivos sin validación
        """
        # VULNERABILIDAD: Path traversal
        ruta_completa = f"/tmp/{nombre_archivo}"
        
        # VULNERABILIDAD: Lectura sin validación de permisos
        with open(ruta_completa, 'r') as archivo:
            contenido = archivo.read()
        
        return contenido
    
    def conexion_base_datos_insegura(self, query_usuario):
        """
        VULNERABILIDAD: Conexión a base de datos insegura
        """
        import sqlite3
        
        # VULNERABILIDAD: Credenciales hardcodeadas
        usuario_db = "admin"
        password_db = "admin123"
        host_db = "localhost"
        
        # VULNERABILIDAD: SQL injection
        query_completa = f"SELECT * FROM productos WHERE nombre LIKE '%{query_usuario}%'"
        
        # VULNERABILIDAD: Conexión sin validación
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        
        # VULNERABILIDAD: Ejecución directa de query
        cursor.execute(query_completa)
        resultados = cursor.fetchall()
        
        conn.close()
        
        return {
            'credenciales': {'usuario': usuario_db, 'password': password_db, 'host': host_db},
            'query': query_completa,
            'resultados': resultados
        }