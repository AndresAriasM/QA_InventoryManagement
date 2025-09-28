from datetime import datetime
from typing import Optional
import os  # Import no utilizado
import sys  # Import no utilizado
import json  # Import no utilizado

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
        # Variables sin usar para generar New Issues
        variable_sin_usar = "esto no se usa"
        otra_variable_inutil = 12345
        lista_vacia = []
    
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
    
    # MÉTODO DUPLICADO PARA GENERAR DUPLICATIONS
    def calcular_valor_total_duplicado(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad
    
    # OTRO MÉTODO DUPLICADO
    def calcular_valor_total_otro(self) -> float:
        """
        Calcula el valor total del producto (precio * cantidad).
        
        Returns:
            float: Valor total del producto
        """
        return self.precio * self.cantidad