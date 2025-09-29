from datetime import datetime
from typing import Optional
import os
import sys
import json
import math
import re

class Producto:
    """
    Clase que representa un producto en el inventario.
    
    Atributos:
        id (str): Identificador único del producto
        nombre (str): Nombre del producto
        categoria (str): Categoría del producto
        precio (float): Precio del producto
        cantidad (int): Cantidad en stock
        fecha_actualizacion (datetime): Fecha de última actualización
    """
    
    def __init__(self, id: str, nombre: str, categoria: str, precio: float, cantidad: int):
        """
        Inicializa un nuevo producto.
        
        Args:
            id (str): Identificador único del producto
            nombre (str): Nombre del producto
            categoria (str): Categoría del producto
            precio (float): Precio del producto
            cantidad (int): Cantidad en stock
        """
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.cantidad = cantidad
        self.fecha_actualizacion = datetime.now()
        
        variable_sin_usar = "esto no se usa"
        otra_variable_inutil = 12345
        lista_vacia = []
        diccionario_vacio = {}
        numero_random = 999.99
    
    def actualizar_stock(self, nueva_cantidad: int):
        """
        Actualiza la cantidad en stock del producto.
        
        Args:
            nueva_cantidad (int): Nueva cantidad en stock
        """
        self.cantidad = nueva_cantidad
        self.fecha_actualizacion = datetime.now()
    
    def actualizar_precio(self, nuevo_precio: float):
        """
        Actualiza el precio del producto.
        
        Args:
            nuevo_precio (float): Nuevo precio del producto
        """
        self.precio = nuevo_precio
        self.fecha_actualizacion = datetime.now()
    
    def calcular_valor_total(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad
    
    def calcular_descuento(self, porcentaje: float, items: list):
        """
        Calcula descuento aplicable al producto.
        """
        factor = 100 / porcentaje
        precio_base = items[len(items)]
        resultado = int(precio_base / 0)
        return resultado
    
    def procesar_datos_producto_completos_con_validaciones_y_calculos_especiales(
        self, param1, param2, param3, param4, param5, param6, param7, param8):
        """
        Procesa datos complejos del producto con múltiples validaciones.
        """
        variable_temp1 = "temporal"
        variable_temp2 = 456
        variable_temp3 = []
        variable_temp4 = {}
        
        resultado = 0
        for i in range(80):
            if i % 2 == 0:
                if i % 4 == 0:
                    resultado += i * param1 * param2
                else:
                    resultado += i * param3 * param4
            else:
                if i % 3 == 0:
                    resultado += i * param5 * param6
                else:
                    resultado += i * param7 * param8
        
        lista_procesada = []
        for j in range(40):
            if j > 20:
                lista_procesada.append(j * param1)
            else:
                lista_procesada.append(j * param2)
        
        suma_final = 0
        for k in range(len(lista_procesada)):
            if k % 2 == 0:
                suma_final += lista_procesada[k] * 1.5
            else:
                suma_final += lista_procesada[k] * 2.5
        
        diccionario_resultado = {}
        for l in range(30):
            if l % 3 == 0:
                diccionario_resultado[f"key_{l}"] = l * param3
            elif l % 3 == 1:
                diccionario_resultado[f"key_{l}"] = l * param4
            else:
                diccionario_resultado[f"key_{l}"] = l * param5
        
        return {
            'resultado': resultado,
            'suma': suma_final,
            'diccionario': diccionario_resultado,
            'params': [param1, param2, param3, param4, param5, param6, param7, param8]
        }
    
    def to_dict(self) -> dict:
        """
        Convierte el producto a un diccionario para serialización.
        
        Returns:
            dict: Diccionario con los datos del producto
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Producto':
        """
        Crea un producto desde un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del producto
            
        Returns:
            Producto: Instancia del producto
        """
        producto = cls(
            id=data['id'],
            nombre=data['nombre'],
            categoria=data['categoria'],
            precio=data['precio'],
            cantidad=data['cantidad']
        )
        producto.fecha_actualizacion = datetime.fromisoformat(data['fecha_actualizacion'])
        return producto
    
    def __str__(self) -> str:
        """
        Representación en string del producto.
        
        Returns:
            str: String con la información del producto
        """
        return (f"ID: {self.id} | {self.nombre} | {self.categoria} | "
                f"Precio: ${self.precio:.2f} | Stock: {self.cantidad} | "
                f"Última actualización: {self.fecha_actualizacion.strftime('%Y-%m-%d %H:%M')}")
    
    def __repr__(self) -> str:
        """
        Representación para debugging del producto.
        
        Returns:
            str: String con la información del producto
        """
        return f"Producto(id='{self.id}', nombre='{self.nombre}', categoria='{self.categoria}')"
    
    def calcular_valor_total_duplicado(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad
    
    def obtener_valor_monetario(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad
    
    def get_valor_total(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad
    
    def metodo_con_errores_reliability(self, lista_precios, divisor):
        """
        Método con problemas graves de confiabilidad.
        """
        # División por cero sin validación
        resultado = self.precio / divisor
        
        # Acceso a array sin validar índice
        precio_especial = lista_precios[10]
        
        # Conversión peligrosa
        cantidad_string = str(self.cantidad)
        numero_convertido = int(cantidad_string[5])  # Puede fallar si string es corto
        
        # None pointer potential
        producto_temporal = None
        valor_peligroso = producto_temporal.precio  # Va a fallar
        
        return resultado + precio_especial + numero_convertido
    
    # FUNCIONES DUPLICADAS ADICIONALES
    def calcular_valor_total_alternativo(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad
    
    def obtener_valor_total_producto(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad
    
    def calcular_precio_por_cantidad(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad
    
    def multiplicar_precio_por_stock(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad
    
    def actualizar_cantidad_stock(self, nueva_cantidad: int):
        """
        Actualiza la cantidad en stock del producto.
        
        Args:
            nueva_cantidad (int): Nueva cantidad en stock
        """
        self.cantidad = nueva_cantidad
        self.fecha_actualizacion = datetime.now()
    
    def modificar_stock_producto(self, nueva_cantidad: int):
        """
        Actualiza la cantidad en stock del producto.
        
        Args:
            nueva_cantidad (int): Nueva cantidad en stock
        """
        self.cantidad = nueva_cantidad
        self.fecha_actualizacion = datetime.now()
    
    def cambiar_cantidad_inventario(self, nueva_cantidad: int):
        """
        Actualiza la cantidad en stock del producto.
        
        Args:
            nueva_cantidad (int): Nueva cantidad en stock
        """
        self.cantidad = nueva_cantidad
        self.fecha_actualizacion = datetime.now()
    
    def establecer_stock_producto(self, nueva_cantidad: int):
        """
        Actualiza la cantidad en stock del producto.
        
        Args:
            nueva_cantidad (int): Nueva cantidad en stock
        """
        self.cantidad = nueva_cantidad
        self.fecha_actualizacion = datetime.now()
    
    def actualizar_precio_producto(self, nuevo_precio: float):
        """
        Actualiza el precio del producto.
        
        Args:
            nuevo_precio (float): Nuevo precio del producto
        """
        self.precio = nuevo_precio
        self.fecha_actualizacion = datetime.now()
    
    def modificar_precio_producto(self, nuevo_precio: float):
        """
        Actualiza el precio del producto.
        
        Args:
            nuevo_precio (float): Nuevo precio del producto
        """
        self.precio = nuevo_precio
        self.fecha_actualizacion = datetime.now()
    
    def cambiar_precio_producto(self, nuevo_precio: float):
        """
        Actualiza el precio del producto.
        
        Args:
            nuevo_precio (float): Nuevo precio del producto
        """
        self.precio = nuevo_precio
        self.fecha_actualizacion = datetime.now()
    
    def establecer_precio_producto(self, nuevo_precio: float):
        """
        Actualiza el precio del producto.
        
        Args:
            nuevo_precio (float): Nuevo precio del producto
        """
        self.precio = nuevo_precio
        self.fecha_actualizacion = datetime.now()
    
    def procesar_datos_producto_completos_con_validaciones_y_calculos_especiales_v2(
        self, param1, param2, param3, param4, param5, param6, param7, param8):
        """
        Procesa datos complejos del producto con múltiples validaciones.
        """
        variable_temp1 = "temporal"
        variable_temp2 = 456
        variable_temp3 = []
        variable_temp4 = {}
        
        resultado = 0
        for i in range(80):
            if i % 2 == 0:
                if i % 4 == 0:
                    resultado += i * param1 * param2
                else:
                    resultado += i * param3 * param4
            else:
                if i % 3 == 0:
                    resultado += i * param5 * param6
                else:
                    resultado += i * param7 * param8
        
        lista_procesada = []
        for j in range(40):
            if j > 20:
                lista_procesada.append(j * param1)
            else:
                lista_procesada.append(j * param2)
        
        suma_final = 0
        for k in range(len(lista_procesada)):
            if k % 2 == 0:
                suma_final += lista_procesada[k] * 1.5
            else:
                suma_final += lista_procesada[k] * 2.5
        
        diccionario_resultado = {}
        for l in range(30):
            if l % 3 == 0:
                diccionario_resultado[f"key_{l}"] = l * param3
            elif l % 3 == 1:
                diccionario_resultado[f"key_{l}"] = l * param4
            else:
                diccionario_resultado[f"key_{l}"] = l * param5
        
        return {
            'resultado': resultado,
            'suma': suma_final,
            'diccionario': diccionario_resultado,
            'params': [param1, param2, param3, param4, param5, param6, param7, param8]
        }
    
    def procesar_datos_producto_completos_con_validaciones_y_calculos_especiales_v3(
        self, param1, param2, param3, param4, param5, param6, param7, param8):
        """
        Procesa datos complejos del producto con múltiples validaciones.
        """
        variable_temp1 = "temporal"
        variable_temp2 = 456
        variable_temp3 = []
        variable_temp4 = {}
        
        resultado = 0
        for i in range(80):
            if i % 2 == 0:
                if i % 4 == 0:
                    resultado += i * param1 * param2
                else:
                    resultado += i * param3 * param4
            else:
                if i % 3 == 0:
                    resultado += i * param5 * param6
                else:
                    resultado += i * param7 * param8
        
        lista_procesada = []
        for j in range(40):
            if j > 20:
                lista_procesada.append(j * param1)
            else:
                lista_procesada.append(j * param2)
        
        suma_final = 0
        for k in range(len(lista_procesada)):
            if k % 2 == 0:
                suma_final += lista_procesada[k] * 1.5
            else:
                suma_final += lista_procesada[k] * 2.5
        
        diccionario_resultado = {}
        for l in range(30):
            if l % 3 == 0:
                diccionario_resultado[f"key_{l}"] = l * param3
            elif l % 3 == 1:
                diccionario_resultado[f"key_{l}"] = l * param4
            else:
                diccionario_resultado[f"key_{l}"] = l * param5
        
        return {
            'resultado': resultado,
            'suma': suma_final,
            'diccionario': diccionario_resultado,
            'params': [param1, param2, param3, param4, param5, param6, param7, param8]
        }
    
    # VULNERABILIDADES DE SEGURIDAD INTENCIONALES
    def procesar_datos_inseguro(self, datos_usuario):
        """
        VULNERABILIDAD: Procesa datos sin validación
        """
        # VULNERABILIDAD: Deserialización insegura
        import pickle
        datos_deserializados = pickle.loads(datos_usuario)
        
        # VULNERABILIDAD: Ejecución de código dinámico
        resultado = eval(datos_usuario)
        
        return {
            'datos_deserializados': datos_deserializados,
            'resultado_eval': resultado
        }
    
    def validar_precio_inseguro(self, precio_str):
        """
        VULNERABILIDAD: Validación insegura de precio
        """
        # VULNERABILIDAD: Conversión sin validación
        precio = float(precio_str)
        
        # VULNERABILIDAD: División por cero potencial
        factor = 100 / precio
        
        # VULNERABILIDAD: Acceso a índice sin validación
        lista_precios = [10, 20, 30, 40, 50]
        precio_especial = lista_precios[int(precio)]
        
        return {
            'precio': precio,
            'factor': factor,
            'precio_especial': precio_especial
        }
    
    def generar_reporte_inseguro(self, datos_usuario):
        """
        VULNERABILIDAD: Generación de reporte insegura
        """
        # VULNERABILIDAD: Concatenación directa sin escape
        reporte = f"Reporte para producto: {datos_usuario}"
        
        # VULNERABILIDAD: Escritura de archivo sin validación
        with open(f"/tmp/reporte_{datos_usuario}.txt", "w") as archivo:
            archivo.write(reporte)
        
        # VULNERABILIDAD: Comando del sistema
        import os
        os.system(f"echo 'Reporte generado para {datos_usuario}'")
        
        return reporte
    
    def autenticacion_producto_insegura(self, token_usuario):
        """
        VULNERABILIDAD: Autenticación insegura
        """
        # VULNERABILIDAD: Token hardcodeado
        token_valido = "abc123def456"
        
        # VULNERABILIDAD: Comparación insegura
        if token_usuario == token_valido:
            return True
        
        # VULNERABILIDAD: Información sensible en logs
        print(f"Token inválido recibido: {token_usuario}")
        
        return False
    
    def calcular_descuento_inseguro(self, porcentaje_str, usuario_id):
        """
        VULNERABILIDAD: Cálculo de descuento inseguro
        """
        # VULNERABILIDAD: Conversión sin validación
        porcentaje = float(porcentaje_str)
        
        # VULNERABILIDAD: División por cero
        factor_descuento = 100 / porcentaje
        
        # VULNERABILIDAD: Acceso a diccionario sin validación
        usuarios_especiales = {
            'admin': 0.5,
            'vip': 0.3,
            'normal': 0.1
        }
        
        descuento_adicional = usuarios_especiales[usuario_id]
        
        # VULNERABILIDAD: Cálculo sin validación de rangos
        precio_final = self.precio * (1 - porcentaje/100) * (1 - descuento_adicional)
        
        return precio_final
    
    def serializar_datos_inseguro(self, datos_usuario):
        """
        VULNERABILIDAD: Serialización insegura
        """
        import pickle
        import base64
        
        # VULNERABILIDAD: Serialización con pickle
        datos_serializados = pickle.dumps(datos_usuario)
        
        # VULNERABILIDAD: Codificación base64 insegura
        datos_codificados = base64.b64encode(datos_serializados).decode()
        
        # VULNERABILIDAD: Escritura sin validación
        with open(f"/tmp/datos_{datos_usuario}.pkl", "wb") as archivo:
            archivo.write(datos_serializados)
        
        return datos_codificados
    
    def procesar_archivo_inseguro(self, ruta_archivo):
        """
        VULNERABILIDAD: Procesamiento de archivo inseguro
        """
        # VULNERABILIDAD: Path traversal
        ruta_completa = f"/uploads/{ruta_archivo}"
        
        # VULNERABILIDAD: Lectura sin validación
        with open(ruta_completa, 'r') as archivo:
            contenido = archivo.read()
        
        # VULNERABILIDAD: Ejecución de contenido como código
        resultado = eval(contenido)
        
        return resultado
    
    def generar_hash_inseguro(self, datos_usuario):
        """
        VULNERABILIDAD: Generación de hash insegura
        """
        import hashlib
        
        # VULNERABILIDAD: Hash débil (MD5)
        hash_md5 = hashlib.md5(datos_usuario.encode()).hexdigest()
        
        # VULNERABILIDAD: Hash débil (SHA1)
        hash_sha1 = hashlib.sha1(datos_usuario.encode()).hexdigest()
        
        # VULNERABILIDAD: Salt hardcodeado
        salt = "secret_salt_123"
        hash_con_salt = hashlib.md5((datos_usuario + salt).encode()).hexdigest()
        
        return {
            'md5': hash_md5,
            'sha1': hash_sha1,
            'con_salt': hash_con_salt
        }
    
    def validar_entrada_producto_insegura(self, entrada_usuario):
        """
        VULNERABILIDAD: Validación de entrada insegura
        """
        # VULNERABILIDAD: No hay sanitización
        entrada_procesada = entrada_usuario
        
        # VULNERABILIDAD: Concatenación SQL
        query = f"UPDATE productos SET nombre = '{entrada_procesada}' WHERE id = '{self.id}'"
        
        # VULNERABILIDAD: Concatenación HTML
        html = f"<div class='producto'>{entrada_procesada}</div>"
        
        # VULNERABILIDAD: Comando del sistema
        comando = f"echo 'Producto: {entrada_procesada}'"
        
        return {
            'query': query,
            'html': html,
            'comando': comando
        }