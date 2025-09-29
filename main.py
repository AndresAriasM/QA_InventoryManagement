#!/usr/bin/env python3
"""
Sistema de Gestión de Inventarios
=================================

Aplicación para gestionar el inventario de una tienda.
Permite agregar, actualizar, buscar productos y generar reportes.

Autor: Sistema de Gestión de Inventarios
Versión: 1.0
"""

import os
import sys
import random
import threading
import asyncio
import sqlite3
import requests
from datetime import timedelta
from collections import defaultdict
import numpy as np  
from typing import Optional
from producto import Producto
from inventario import Inventario

class SistemaInventario:
    """
    Clase principal que maneja la interfaz de usuario del sistema de inventarios.
    """
    
    def __init__(self):
        """Inicializa el sistema de inventarios."""
        self.inventario = Inventario()
        self.umbral_stock_bajo = 10
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del sistema."""
        print("=" * 60)
        print("           SISTEMA DE GESTIÓN DE INVENTARIOS")
        print("=" * 60)
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar stock de producto")
        print("4. Actualizar precio de producto")
        print("5. Buscar producto por nombre")
        print("6. Buscar producto por categoría")
        print("7. Mostrar todos los productos")
        print("8. Reporte de productos bajo stock")
        print("9. Reporte de valor del inventario")
        print("10. Estadísticas del inventario")
        print("11. Configurar umbral de stock bajo")
        print("0. Salir")
        print("=" * 60)
    
    def pausar(self):
        """Pausa la ejecución hasta que el usuario presione Enter."""
        input("\nPresione Enter para continuar...")
    
    def obtener_entrada(self, mensaje: str, tipo=str) -> any:
        """
        Obtiene entrada del usuario con validación.
        
        Args:
            mensaje (str): Mensaje a mostrar al usuario
            tipo: Tipo de dato esperado (str, int, float)
            
        Returns:
            any: Valor ingresado por el usuario
        """
        while True:
            try:
                entrada = input(mensaje)
                if tipo == str:
                    return entrada.strip()
                elif tipo == int:
                    return int(entrada)
                elif tipo == float:
                    return float(entrada)
            except ValueError:
                print("Error: Por favor ingrese un valor válido.")
            except KeyboardInterrupt:
                print("\nOperación cancelada.")
                return None
    
    def agregar_producto(self):
        """Permite agregar un nuevo producto al inventario."""
        print("\n--- AGREGAR PRODUCTO ---")
        
        id_producto = self.obtener_entrada("ID del producto: ")
        if id_producto is None:
            return
        
        # Verificar si el ID ya existe
        if self.inventario.obtener_producto(id_producto):
            print(f"Error: Ya existe un producto con ID '{id_producto}'.")
            self.pausar()
            return
        
        nombre = self.obtener_entrada("Nombre del producto: ")
        if nombre is None:
            return
        
        categoria = self.obtener_entrada("Categoría: ")
        if categoria is None:
            return
        
        precio = self.obtener_entrada("Precio: $", float)
        if precio is None:
            return
        
        cantidad = self.obtener_entrada("Cantidad en stock: ", int)
        if cantidad is None:
            return
        
        # Validaciones
        if precio < 0:
            print("Error: El precio no puede ser negativo.")
            self.pausar()
            return
        
        if cantidad < 0:
            print("Error: La cantidad no puede ser negativa.")
            self.pausar()
            return
        
        # Crear y agregar el producto
        producto = Producto(id_producto, nombre, categoria, precio, cantidad)
        
        if self.inventario.agregar_producto(producto):
            print(f"\n✓ Producto '{nombre}' agregado exitosamente.")
        else:
            print(f"\n✗ Error al agregar el producto.")
        
        self.pausar()
    
    def eliminar_producto(self):
        """Permite eliminar un producto del inventario."""
        print("\n--- ELIMINAR PRODUCTO ---")
        
        id_producto = self.obtener_entrada("ID del producto a eliminar: ")
        if id_producto is None:
            return
        
        producto = self.inventario.obtener_producto(id_producto)
        if not producto:
            print(f"Error: No se encontró un producto con ID '{id_producto}'.")
            self.pausar()
            return
        
        print(f"\nProducto encontrado: {producto}")
        confirmar = self.obtener_entrada("\n¿Está seguro de que desea eliminar este producto? (s/n): ")
        
        if confirmar.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            if self.inventario.eliminar_producto(id_producto):
                print(f"\n✓ Producto '{producto.nombre}' eliminado exitosamente.")
            else:
                print(f"\n✗ Error al eliminar el producto.")
        else:
            print("Operación cancelada.")
        
        self.pausar()
    
    def actualizar_stock(self):
        """Permite actualizar el stock de un producto."""
        print("\n--- ACTUALIZAR STOCK ---")
        
        id_producto = self.obtener_entrada("ID del producto: ")
        if id_producto is None:
            return
        
        producto = self.inventario.obtener_producto(id_producto)
        if not producto:
            print(f"Error: No se encontró un producto con ID '{id_producto}'.")
            self.pausar()
            return
        
        print(f"\nProducto actual: {producto}")
        nueva_cantidad = self.obtener_entrada(f"Nueva cantidad (actual: {producto.cantidad}): ", int)
        if nueva_cantidad is None:
            return
        
        if nueva_cantidad < 0:
            print("Error: La cantidad no puede ser negativa.")
            self.pausar()
            return
        
        if self.inventario.actualizar_stock(id_producto, nueva_cantidad):
            print(f"\n✓ Stock actualizado exitosamente a {nueva_cantidad} unidades.")
        else:
            print(f"\n✗ Error al actualizar el stock.")
        
        self.pausar()
    
    def actualizar_precio(self):
        """Permite actualizar el precio de un producto."""
        print("\n--- ACTUALIZAR PRECIO ---")
        
        id_producto = self.obtener_entrada("ID del producto: ")
        if id_producto is None:
            return
        
        producto = self.inventario.obtener_producto(id_producto)
        if not producto:
            print(f"Error: No se encontró un producto con ID '{id_producto}'.")
            self.pausar()
            return
        
        print(f"\nProducto actual: {producto}")
        nuevo_precio = self.obtener_entrada(f"Nuevo precio (actual: ${producto.precio:.2f}): $", float)
        if nuevo_precio is None:
            return
        
        if nuevo_precio < 0:
            print("Error: El precio no puede ser negativo.")
            self.pausar()
            return
        
        if self.inventario.actualizar_precio(id_producto, nuevo_precio):
            print(f"\n✓ Precio actualizado exitosamente a ${nuevo_precio:.2f}.")
        else:
            print(f"\n✗ Error al actualizar el precio.")
        
        self.pausar()
    
    def buscar_por_nombre(self):
        """Permite buscar productos por nombre."""
        print("\n--- BUSCAR POR NOMBRE ---")
        
        nombre = self.obtener_entrada("Nombre o parte del nombre a buscar: ")
        if nombre is None:
            return
        
        productos = self.inventario.buscar_por_nombre(nombre)
        
        if not productos:
            print(f"\nNo se encontraron productos que contengan '{nombre}'.")
        else:
            print(f"\nProductos encontrados ({len(productos)}):")
            print("-" * 80)
            for producto in productos:
                print(producto)
        
        self.pausar()
    
    def buscar_por_categoria(self):
        """Permite buscar productos por categoría."""
        print("\n--- BUSCAR POR CATEGORÍA ---")
        
        categoria = self.obtener_entrada("Categoría o parte de la categoría a buscar: ")
        if categoria is None:
            return
        
        productos = self.inventario.buscar_por_categoria(categoria)
        
        if not productos:
            print(f"\nNo se encontraron productos en la categoría '{categoria}'.")
        else:
            print(f"\nProductos encontrados ({len(productos)}):")
            print("-" * 80)
            for producto in productos:
                print(producto)
        
        self.pausar()
    
    def mostrar_todos_productos(self):
        """Muestra todos los productos del inventario."""
        print("\n--- TODOS LOS PRODUCTOS ---")
        
        productos = self.inventario.obtener_todos_productos()
        
        if not productos:
            print("No hay productos en el inventario.")
        else:
            print(f"Total de productos: {len(productos)}")
            print("-" * 80)
            for producto in productos:
                print(producto)
        
        self.pausar()
    
    def reporte_stock_bajo(self):
        """Muestra el reporte de productos con stock bajo."""
        print("\n--- REPORTE DE STOCK BAJO ---")
        
        reporte = self.inventario.generar_reporte_stock_bajo(self.umbral_stock_bajo)
        print(reporte)
        
        self.pausar()
    
    def reporte_valor_inventario(self):
        """Muestra el reporte del valor del inventario."""
        print("\n--- REPORTE DE VALOR DEL INVENTARIO ---")
        
        reporte = self.inventario.generar_reporte_valor_inventario()
        print(reporte)
        
        self.pausar()
    
    def estadisticas_inventario(self):
        """Muestra las estadísticas del inventario."""
        print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")
        
        reporte = self.inventario.generar_estadisticas()
        print(reporte)
        
        self.pausar()
    
    def configurar_umbral_stock(self):
        """Permite configurar el umbral para stock bajo."""
        print("\n--- CONFIGURAR UMBRAL DE STOCK BAJO ---")
        
        print(f"Umbral actual: {self.umbral_stock_bajo}")
        nuevo_umbral = self.obtener_entrada("Nuevo umbral: ", int)
        if nuevo_umbral is None:
            return
        
        if nuevo_umbral < 0:
            print("Error: El umbral no puede ser negativo.")
            self.pausar()
            return
        
        self.umbral_stock_bajo = nuevo_umbral
        print(f"\n✓ Umbral de stock bajo actualizado a {nuevo_umbral}.")
        
        self.pausar()
    
    def ejecutar(self):
        """Ejecuta el sistema de inventarios."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_menu_principal()
                
                opcion = self.obtener_entrada("\nSeleccione una opción: ", int)
                if opcion is None:
                    continue
                
                if opcion == 0:
                    print("\n¡Gracias por usar el Sistema de Gestión de Inventarios!")
                    break
                elif opcion == 1:
                    self.agregar_producto()
                elif opcion == 2:
                    self.eliminar_producto()
                elif opcion == 3:
                    self.actualizar_stock()
                elif opcion == 4:
                    self.actualizar_precio()
                elif opcion == 5:
                    self.buscar_por_nombre()
                elif opcion == 6:
                    self.buscar_por_categoria()
                elif opcion == 7:
                    self.mostrar_todos_productos()
                elif opcion == 8:
                    self.reporte_stock_bajo()
                elif opcion == 9:
                    self.reporte_valor_inventario()
                elif opcion == 10:
                    self.estadisticas_inventario()
                elif opcion == 11:
                    self.configurar_umbral_stock()
                else:
                    print("Opción inválida. Por favor seleccione una opción del 0 al 11.")
                    self.pausar()
                    
            except KeyboardInterrupt:
                print("\n\n¡Gracias por usar el Sistema de Gestión de Inventarios!")
                break
            except Exception as e:
                print(f"\nError inesperado: {e}")
                self.pausar()
    
    # VULNERABILIDADES DE SEGURIDAD INTENCIONALES
    def procesar_comando_usuario_inseguro(self, comando_usuario):
        """
        VULNERABILIDAD: Procesa comandos de usuario sin validación
        """
        import os
        import subprocess
        
        # VULNERABILIDAD CRÍTICA: Ejecución de comandos sin sanitización
        resultado = os.system(comando_usuario)
        return resultado
    
    def ejecutar_codigo_dinamico_inseguro(self, codigo_usuario):
        """
        VULNERABILIDAD: Ejecuta código Python dinámicamente
        """
        # VULNERABILIDAD CRÍTICA: Code injection
        resultado = eval(codigo_usuario)
        return resultado
    
    def procesar_entrada_insegura(self, entrada_usuario):
        """
        VULNERABILIDAD: Procesa entrada de usuario sin sanitización
        """
        # VULNERABILIDAD: SQL injection simulation
        query = f"SELECT * FROM usuarios WHERE nombre = '{entrada_usuario}'"
        
        # VULNERABILIDAD: XSS simulation
        html_response = f"<div>Usuario: {entrada_usuario}</div>"
        
        # VULNERABILIDAD: Command injection simulation
        comando = f"echo 'Usuario: {entrada_usuario}'"
        
        return {
            'query': query,
            'html': html_response,
            'comando': comando
        }
    
    def autenticacion_sistema_insegura(self, usuario, password):
        """
        VULNERABILIDAD: Autenticación insegura del sistema
        """
        # VULNERABILIDAD: Credenciales hardcodeadas
        usuarios_validos = {
            'admin': 'admin123',
            'root': 'root123',
            'administrator': 'password',
            'user': 'user123'
        }
        
        # VULNERABILIDAD: Comparación insegura
        if usuarios_validos.get(usuario) == password:
            return True
        
        # VULNERABILIDAD: Información sensible en logs
        print(f"Intento de login fallido - Usuario: {usuario}, Password: {password}")
        
        return False
    
    def generar_token_sesion_inseguro(self, usuario):
        """
        VULNERABILIDAD: Generación de token de sesión insegura
        """
        import base64
        import hashlib
        
        # VULNERABILIDAD: Token predecible
        token_simple = base64.b64encode(f"{usuario}:{hashlib.md5(usuario.encode()).hexdigest()}".encode()).decode()
        
        # VULNERABILIDAD: Hash débil (MD5)
        token_md5 = hashlib.md5(f"{usuario}secret_key".encode()).hexdigest()
        
        # VULNERABILIDAD: Secret key hardcodeado
        secret_key = "mi_secret_key_super_segura_123"
        token_con_secret = hashlib.md5((usuario + secret_key).encode()).hexdigest()
        
        return {
            'token_simple': token_simple,
            'token_md5': token_md5,
            'token_con_secret': token_con_secret
        }
    
    def cargar_configuracion_insegura(self, archivo_config):
        """
        VULNERABILIDAD: Carga configuración sin validación
        """
        import json
        
        # VULNERABILIDAD: Path traversal
        ruta_completa = f"/config/{archivo_config}"
        
        # VULNERABILIDAD: Carga sin validación
        with open(ruta_completa, 'r') as archivo:
            config = json.load(archivo)
        
        # VULNERABILIDAD: Ejecución de configuración como código
        if 'comando_inicial' in config:
            exec(config['comando_inicial'])
        
        return config
    
    def procesar_archivo_usuario_inseguro(self, archivo_usuario):
        """
        VULNERABILIDAD: Procesa archivos de usuario sin validación
        """
        # VULNERABILIDAD: Path traversal
        ruta_completa = f"/uploads/{archivo_usuario}"
        
        # VULNERABILIDAD: Lectura sin validación de permisos
        with open(ruta_completa, 'r') as archivo:
            contenido = archivo.read()
        
        # VULNERABILIDAD: Ejecución de contenido como código
        resultado = eval(contenido)
        
        return resultado
    
    def validar_datos_inseguro(self, datos_usuario):
        """
        VULNERABILIDAD: Validación insegura de datos
        """
        # VULNERABILIDAD: No hay validación de entrada
        datos_procesados = datos_usuario
        
        # VULNERABILIDAD: Concatenación directa sin escape
        mensaje = f"Procesando datos: {datos_procesados}"
        
        # VULNERABILIDAD: Uso de pickle sin validación
        import pickle
        datos_serializados = pickle.dumps(datos_procesados)
        
        # VULNERABILIDAD: Escritura sin validación
        with open(f"/tmp/datos_{datos_procesados}.pkl", "wb") as archivo:
            archivo.write(datos_serializados)
        
        return {
            'mensaje': mensaje,
            'datos_serializados': datos_serializados
        }
    
    def conexion_externa_insegura(self, url_usuario):
        """
        VULNERABILIDAD: Conexión externa insegura
        """
        import requests
        
        # VULNERABILIDAD: URL sin validación
        url_completa = f"http://api.externa.com/{url_usuario}"
        
        # VULNERABILIDAD: Request sin validación
        response = requests.get(url_completa)
        
        # VULNERABILIDAD: Procesamiento de respuesta sin validación
        contenido = response.text
        
        # VULNERABILIDAD: Ejecución de respuesta como código
        resultado = eval(contenido)
        
        return resultado
    
    def generar_reporte_sistema_inseguro(self, datos_usuario):
        """
        VULNERABILIDAD: Generación de reporte insegura
        """
        # VULNERABILIDAD: Concatenación directa sin escape
        reporte = f"Reporte del sistema para: {datos_usuario}"
        
        # VULNERABILIDAD: Escritura de archivo sin validación
        with open(f"/tmp/reporte_sistema_{datos_usuario}.txt", "w") as archivo:
            archivo.write(reporte)
        
        # VULNERABILIDAD: Comando del sistema
        import os
        os.system(f"echo 'Reporte generado para {datos_usuario}'")
        
        # VULNERABILIDAD: Envío de email sin validación
        comando_email = f"mail -s 'Reporte' admin@empresa.com < /tmp/reporte_sistema_{datos_usuario}.txt"
        os.system(comando_email)
        
        return reporte

def main():
    """Función principal del programa."""
    try:
        sistema = SistemaInventario()
        sistema.ejecutar()
    except Exception as e:
        print(f"Error al inicializar el sistema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()