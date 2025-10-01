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
import logging
from typing import Optional
from producto import Producto
from inventario import Inventario, SecurityError

class SistemaInventario:
    """
    Clase principal que maneja la interfaz de usuario del sistema de inventarios.
    """
    
    def __init__(self):
        """Inicializa el sistema de inventarios."""
        self.inventario = Inventario()
        self.umbral_stock_bajo = 10
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola de forma segura."""
        import subprocess
        import shlex
        
        try:
            if os.name == 'nt':
                # Windows - usar subprocess de forma segura
                subprocess.run(['cls'], shell=False, check=True)
            else:
                # Unix/Linux - usar subprocess de forma segura
                subprocess.run(['clear'], shell=False, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback seguro - solo imprimir líneas en blanco
            print('\n' * 50)
    
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
    
    def obtener_entrada(self, mensaje: str, tipo=str, validaciones=None) -> any:
        """
        Obtiene entrada del usuario con validación y sanitización de seguridad.
        
        Args:
            mensaje (str): Mensaje a mostrar al usuario
            tipo: Tipo de dato esperado (str, int, float)
            validaciones (dict): Diccionario con validaciones adicionales
            
        Returns:
            any: Valor ingresado por el usuario
        """
        if validaciones is None:
            validaciones = {}
            
        while True:
            try:
                entrada = input(mensaje)
                
                # Sanitización de entrada
                entrada_sanitizada = self._sanitizar_entrada(entrada)
                
                if tipo == str:
                    valor = entrada_sanitizada.strip()
                    if not valor:
                        print("Error: No se puede ingresar un valor vacío.")
                        continue
                    
                    # Validación adicional de seguridad para strings
                    if not self._validar_string_seguro(valor):
                        print("Error: La entrada contiene caracteres no permitidos.")
                        continue
                        
                elif tipo == int:
                    valor = int(entrada_sanitizada)
                elif tipo == float:
                    valor = float(entrada_sanitizada)
                else:
                    valor = entrada_sanitizada
                
                # Aplicar validaciones adicionales
                if 'minimo' in validaciones and valor < validaciones['minimo']:
                    print(f"Error: El valor debe ser mayor o igual a {validaciones['minimo']}.")
                    continue
                    
                if 'maximo' in validaciones and valor > validaciones['maximo']:
                    print(f"Error: El valor debe ser menor o igual a {validaciones['maximo']}.")
                    continue
                    
                if 'longitud_minima' in validaciones and len(str(valor)) < validaciones['longitud_minima']:
                    print(f"Error: El valor debe tener al menos {validaciones['longitud_minima']} caracteres.")
                    continue
                    
                if 'longitud_maxima' in validaciones and len(str(valor)) > validaciones['longitud_maxima']:
                    print(f"Error: El valor no puede tener más de {validaciones['longitud_maxima']} caracteres.")
                    continue
                
                return valor
                
            except ValueError:
                print("Error: Por favor ingrese un valor válido.")
            except KeyboardInterrupt:
                print("\nOperación cancelada.")
                return None
    
    def _sanitizar_entrada(self, entrada: str) -> str:
        """
        Sanitiza la entrada del usuario para prevenir inyecciones.
        
        Args:
            entrada: Entrada del usuario
            
        Returns:
            str: Entrada sanitizada
        """
        if not isinstance(entrada, str):
            return str(entrada)
        
        # Remover caracteres de control peligrosos
        caracteres_peligrosos = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', 
                                '\x08', '\x0b', '\x0c', '\x0e', '\x0f', '\x10', '\x11', '\x12', 
                                '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', 
                                '\x1b', '\x1c', '\x1d', '\x1e', '\x1f']
        
        entrada_sanitizada = entrada
        for char in caracteres_peligrosos:
            entrada_sanitizada = entrada_sanitizada.replace(char, '')
        
        # Limitar longitud máxima
        if len(entrada_sanitizada) > 1000:
            entrada_sanitizada = entrada_sanitizada[:1000]
        
        return entrada_sanitizada
    
    def _validar_string_seguro(self, texto: str) -> bool:
        """
        Valida que un string sea seguro y no contenga patrones peligrosos.
        
        Args:
            texto: Texto a validar
            
        Returns:
            bool: True si es seguro, False si contiene patrones peligrosos
        """
        if not isinstance(texto, str):
            return False
        
        # Patrones peligrosos a detectar
        patrones_peligrosos = [
            r'<script.*?>.*?</script>',  # Scripts HTML
            r'javascript:',              # JavaScript
            r'vbscript:',               # VBScript
            r'on\w+\s*=',              # Event handlers
            r'data:text/html',         # Data URLs
            r'file://',                 # File URLs
            r'ftp://',                  # FTP URLs
            r'\.\./',                   # Path traversal
            r'\.\.\\',                  # Path traversal Windows
            r'<iframe',                 # iFrames
            r'<object',                 # Objects
            r'<embed',                  # Embeds
            r'<form',                   # Forms
            r'<input',                  # Inputs
            r'<meta',                   # Meta tags
            r'<link',                   # Link tags
            r'<style',                  # Style tags
            r'expression\s*\(',         # CSS expressions
            r'url\s*\(',                # CSS URLs
            r'@import',                 # CSS imports
            r'<.*?>',                   # HTML tags básicos
        ]
        
        import re
        texto_lower = texto.lower()
        
        for patron in patrones_peligrosos:
            if re.search(patron, texto_lower, re.IGNORECASE):
                return False
        
        return True
    
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
                logging.FileHandler('sistema_errors.log'),
                logging.StreamHandler()
            ]
        )
        
        # Log solo información segura
        logging.error(f"{mensaje}: {type(error).__name__}")
    
    def agregar_producto(self):
        """Permite agregar un nuevo producto al inventario."""
        print("\n--- AGREGAR PRODUCTO ---")
        
        # Validar ID del producto
        id_producto = self.obtener_entrada("ID del producto: ", str, {
            'longitud_minima': 1,
            'longitud_maxima': 50
        })
        if id_producto is None:
            return
        
        # Verificar si el ID ya existe
        if self.inventario.obtener_producto(id_producto):
            print(f"Error: Ya existe un producto con ID '{id_producto}'.")
            self.pausar()
            return
        
        # Validar nombre del producto
        nombre = self.obtener_entrada("Nombre del producto: ", str, {
            'longitud_minima': 1,
            'longitud_maxima': 100
        })
        if nombre is None:
            return
        
        # Validar categoría
        categoria = self.obtener_entrada("Categoría: ", str, {
            'longitud_minima': 1,
            'longitud_maxima': 50
        })
        if categoria is None:
            return
        
        # Validar precio
        precio = self.obtener_entrada("Precio: $", float, {
            'minimo': 0.01,
            'maximo': 999999.99
        })
        if precio is None:
            return
        
        # Validar cantidad
        cantidad = self.obtener_entrada("Cantidad en stock: ", int, {
            'minimo': 0,
            'maximo': 999999
        })
        if cantidad is None:
            return
        
        # Crear y agregar el producto
        try:
            producto = Producto(id_producto, nombre, categoria, precio, cantidad)
            
            if self.inventario.agregar_producto(producto):
                print(f"\n✓ Producto '{nombre}' agregado exitosamente.")
            else:
                print("\n✗ Error al agregar el producto.")
        except Exception as e:
            print(f"\n✗ Error al crear el producto: {e}")
        
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
                print("\n✗ Error al eliminar el producto.")
        else:
            print("Operación cancelada.")
        
        self.pausar()
    
    def actualizar_stock(self):
        """Permite actualizar el stock de un producto."""
        print("\n--- ACTUALIZAR STOCK ---")
        
        id_producto = self.obtener_entrada("ID del producto: ", str, {
            'longitud_minima': 1,
            'longitud_maxima': 50
        })
        if id_producto is None:
            return
        
        producto = self.inventario.obtener_producto(id_producto)
        if not producto:
            print(f"Error: No se encontró un producto con ID '{id_producto}'.")
            self.pausar()
            return
        
        print(f"\nProducto actual: {producto}")
        nueva_cantidad = self.obtener_entrada(f"Nueva cantidad (actual: {producto.cantidad}): ", int, {
            'minimo': 0,
            'maximo': 999999
        })
        if nueva_cantidad is None:
            return
        
        try:
            if self.inventario.actualizar_stock(id_producto, nueva_cantidad):
                print(f"\n✓ Stock actualizado exitosamente a {nueva_cantidad} unidades.")
            else:
                print("\n✗ Error al actualizar el stock.")
        except Exception as e:
            print(f"\n✗ Error al actualizar el stock: {e}")
        
        self.pausar()
    
    def actualizar_precio(self):
        """Permite actualizar el precio de un producto."""
        print("\n--- ACTUALIZAR PRECIO ---")
        
        id_producto = self.obtener_entrada("ID del producto: ", str, {
            'longitud_minima': 1,
            'longitud_maxima': 50
        })
        if id_producto is None:
            return
        
        producto = self.inventario.obtener_producto(id_producto)
        if not producto:
            print(f"Error: No se encontró un producto con ID '{id_producto}'.")
            self.pausar()
            return
        
        print(f"\nProducto actual: {producto}")
        nuevo_precio = self.obtener_entrada(f"Nuevo precio (actual: ${producto.precio:.2f}): $", float, {
            'minimo': 0.01,
            'maximo': 999999.99
        })
        if nuevo_precio is None:
            return
        
        try:
            if self.inventario.actualizar_precio(id_producto, nuevo_precio):
                print(f"\n✓ Precio actualizado exitosamente a ${nuevo_precio:.2f}.")
            else:
                print("\n✗ Error al actualizar el precio.")
        except Exception as e:
            print(f"\n✗ Error al actualizar el precio: {e}")
        
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
            except (ValueError, TypeError, AttributeError) as e:
                print(f"\nError de datos: {e}")
                self.pausar()
            except (OSError, IOError, PermissionError) as e:
                print("\nError de sistema: No se pudo acceder a los archivos necesarios.")
                self.pausar()
            except Exception as e:
                # Log del error sin exponer información sensible
                self._log_error_seguro("Error inesperado en el sistema", e)
                print("\nError inesperado del sistema. Contacte al administrador.")
                self.pausar()

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