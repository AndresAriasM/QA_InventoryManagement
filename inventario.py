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