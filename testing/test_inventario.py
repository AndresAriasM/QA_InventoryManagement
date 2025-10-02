import unittest
import os
import tempfile
import json
from datetime import datetime
from producto import Producto
from inventario import Inventario

class TestProducto(unittest.TestCase):
    """
    Tests para la clase Producto.
    """
    
    def setUp(self):
        """
        Configuración inicial para cada test.
        """
        self.producto = Producto("TEST001", "Producto Test", "Categoria Test", 100.0, 10)
    
    def test_crear_producto(self):
        """
        Test para crear un producto básico.
        """
        self.assertEqual(self.producto.id, "TEST001")
        self.assertEqual(self.producto.nombre, "Producto Test")
        self.assertEqual(self.producto.categoria, "Categoria Test")
        self.assertEqual(self.producto.precio, 100.0)
        self.assertEqual(self.producto.cantidad, 10)
        self.assertIsInstance(self.producto.fecha_actualizacion, datetime)
    
    def test_actualizar_precio(self):
        """
        Test para actualizar precio de producto.
        """
        nuevo_precio = 150.0
        self.producto.actualizar_precio(nuevo_precio)
        self.assertEqual(self.producto.precio, nuevo_precio)
        self.assertIsInstance(self.producto.fecha_actualizacion, datetime)
    
    def test_actualizar_stock(self):
        """
        Test para actualizar stock de producto.
        """
        nueva_cantidad = 20
        self.producto.actualizar_stock(nueva_cantidad)
        self.assertEqual(self.producto.cantidad, nueva_cantidad)
        self.assertIsInstance(self.producto.fecha_actualizacion, datetime)
    
    def test_calcular_valor_total(self):
        """
        Test para calcular valor total del producto.
        """
        valor_esperado = 100.0 * 10
        self.assertEqual(self.producto.calcular_valor_total(), valor_esperado)
    
    def test_calcular_descuento_seguro(self):
        """
        Test para calcular descuento de forma segura.
        """
        # Test descuento válido
        precio_con_descuento = self.producto.calcular_descuento_seguro(20.0)
        self.assertEqual(precio_con_descuento, 80.0)
        
        # Test descuento 0%
        precio_sin_descuento = self.producto.calcular_descuento_seguro(0.0)
        self.assertEqual(precio_sin_descuento, 100.0)
        
        # Test descuento 100%
        precio_gratis = self.producto.calcular_descuento_seguro(100.0)
        self.assertEqual(precio_gratis, 0.0)
    
    def test_calcular_descuento_invalido(self):
        """
        Test para descuentos inválidos.
        """
        with self.assertRaises(ValueError):
            self.producto.calcular_descuento_seguro(-10.0)
        
        with self.assertRaises(ValueError):
            self.producto.calcular_descuento_seguro(150.0)
    
    def test_procesar_datos_producto_optimizado(self):
        """
        Test para procesamiento optimizado de datos.
        """
        parametros = {"factor": 1.5, "categoria": "test"}
        resultado = self.producto.procesar_datos_producto_optimizado(parametros)
        
        self.assertIn('producto_id', resultado)
        self.assertIn('valor_total', resultado)
        self.assertIn('parametros_aplicados', resultado)
        self.assertIn('fecha_procesamiento', resultado)
        self.assertEqual(resultado['producto_id'], "TEST001")
        self.assertEqual(resultado['parametros_aplicados'], parametros)
    
    def test_procesar_datos_parametros_invalidos(self):
        """
        Test para parámetros inválidos en procesamiento.
        """
        with self.assertRaises(TypeError):
            self.producto.procesar_datos_producto_optimizado("parametros_invalidos")
    
    def test_to_dict(self):
        """
        Test para conversión a diccionario.
        """
        producto_dict = self.producto.to_dict()
        
        self.assertEqual(producto_dict['id'], "TEST001")
        self.assertEqual(producto_dict['nombre'], "Producto Test")
        self.assertEqual(producto_dict['categoria'], "Categoria Test")
        self.assertEqual(producto_dict['precio'], 100.0)
        self.assertEqual(producto_dict['cantidad'], 10)
        self.assertIn('fecha_actualizacion', producto_dict)
    
    def test_from_dict(self):
        """
        Test para creación desde diccionario.
        """
        producto_data = {
            'id': 'TEST002',
            'nombre': 'Producto Test 2',
            'categoria': 'Categoria Test 2',
            'precio': 200.0,
            'cantidad': 5,
            'fecha_actualizacion': '2024-01-01T12:00:00'
        }
        
        producto = Producto.from_dict(producto_data)
        
        self.assertEqual(producto.id, 'TEST002')
        self.assertEqual(producto.nombre, 'Producto Test 2')
        self.assertEqual(producto.categoria, 'Categoria Test 2')
        self.assertEqual(producto.precio, 200.0)
        self.assertEqual(producto.cantidad, 5)
        self.assertIsInstance(producto.fecha_actualizacion, datetime)

class TestInventario(unittest.TestCase):
    """
    Tests para la clase Inventario.
    """
    
    def setUp(self):
        """
        Configuración inicial para cada test.
        """
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        self.inventario = Inventario(self.temp_file.name)
        self.producto1 = Producto("TEST001", "Producto 1", "Categoria A", 100.0, 10)
        self.producto2 = Producto("TEST002", "Producto 2", "Categoria B", 200.0, 5)
        self.producto3 = Producto("TEST003", "Producto 3", "Categoria A", 50.0, 20)
    
    def tearDown(self):
        """
        Limpieza después de cada test.
        """
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_agregar_producto(self):
        """
        Test para agregar producto al inventario.
        """
        # Agregar producto exitosamente
        resultado = self.inventario.agregar_producto(self.producto1)
        self.assertTrue(resultado)
        self.assertIn("TEST001", self.inventario.productos)
        
        # Intentar agregar producto duplicado
        resultado_duplicado = self.inventario.agregar_producto(self.producto1)
        self.assertFalse(resultado_duplicado)
    
    def test_eliminar_producto(self):
        """
        Test para eliminar producto del inventario.
        """
        # Agregar producto primero
        self.inventario.agregar_producto(self.producto1)
        
        # Eliminar producto existente
        resultado = self.inventario.eliminar_producto("TEST001")
        self.assertTrue(resultado)
        self.assertNotIn("TEST001", self.inventario.productos)
        
        # Intentar eliminar producto inexistente
        resultado_inexistente = self.inventario.eliminar_producto("INEXISTENTE")
        self.assertFalse(resultado_inexistente)
    
    def test_obtener_producto(self):
        """
        Test para obtener producto por ID.
        """
        self.inventario.agregar_producto(self.producto1)
        
        # Obtener producto existente
        producto_obtenido = self.inventario.obtener_producto("TEST001")
        self.assertIsNotNone(producto_obtenido)
        self.assertEqual(producto_obtenido.id, "TEST001")
        
        # Obtener producto inexistente
        producto_inexistente = self.inventario.obtener_producto("INEXISTENTE")
        self.assertIsNone(producto_inexistente)
    
    def test_actualizar_stock(self):
        """
        Test para actualizar stock de producto.
        """
        self.inventario.agregar_producto(self.producto1)
        
        # Actualizar stock exitosamente
        resultado = self.inventario.actualizar_stock("TEST001", 15)
        self.assertTrue(resultado)
        self.assertEqual(self.inventario.productos["TEST001"].cantidad, 15)
        
        # Actualizar stock de producto inexistente
        resultado_inexistente = self.inventario.actualizar_stock("INEXISTENTE", 10)
        self.assertFalse(resultado_inexistente)
    
    def test_actualizar_precio(self):
        """
        Test para actualizar precio de producto.
        """
        self.inventario.agregar_producto(self.producto1)
        
        # Actualizar precio exitosamente
        resultado = self.inventario.actualizar_precio("TEST001", 150.0)
        self.assertTrue(resultado)
        self.assertEqual(self.inventario.productos["TEST001"].precio, 150.0)
        
        # Actualizar precio de producto inexistente
        resultado_inexistente = self.inventario.actualizar_precio("INEXISTENTE", 100.0)
        self.assertFalse(resultado_inexistente)
    
    def test_buscar_por_nombre(self):
        """
        Test para buscar productos por nombre.
        """
        self.inventario.agregar_producto(self.producto1)
        self.inventario.agregar_producto(self.producto2)
        
        # Búsqueda exacta
        resultados_exactos = self.inventario.buscar_por_nombre("Producto 1")
        self.assertEqual(len(resultados_exactos), 1)
        self.assertEqual(resultados_exactos[0].id, "TEST001")
        
        # Búsqueda parcial
        resultados_parciales = self.inventario.buscar_por_nombre("Producto")
        self.assertEqual(len(resultados_parciales), 2)
        
        # Búsqueda sin resultados
        resultados_vacios = self.inventario.buscar_por_nombre("Inexistente")
        self.assertEqual(len(resultados_vacios), 0)
    
    def test_buscar_por_categoria(self):
        """
        Test para buscar productos por categoría.
        """
        self.inventario.agregar_producto(self.producto1)
        self.inventario.agregar_producto(self.producto2)
        self.inventario.agregar_producto(self.producto3)
        
        # Búsqueda por categoría
        resultados_categoria_a = self.inventario.buscar_por_categoria("Categoria A")
        self.assertEqual(len(resultados_categoria_a), 2)
        
        resultados_categoria_b = self.inventario.buscar_por_categoria("Categoria B")
        self.assertEqual(len(resultados_categoria_b), 1)
        
        # Búsqueda sin resultados
        resultados_vacios = self.inventario.buscar_por_categoria("Categoria C")
        self.assertEqual(len(resultados_vacios), 0)
    
    def test_obtener_todos_productos(self):
        """
        Test para obtener todos los productos.
        """
        self.inventario.agregar_producto(self.producto1)
        self.inventario.agregar_producto(self.producto2)
        
        todos_productos = self.inventario.obtener_todos_productos()
        self.assertEqual(len(todos_productos), 2)
    
    def test_productos_bajo_stock(self):
        """
        Test para obtener productos con stock bajo.
        """
        self.inventario.agregar_producto(self.producto1)  # cantidad: 10
        self.inventario.agregar_producto(self.producto2)  # cantidad: 5
        self.inventario.agregar_producto(self.producto3)  # cantidad: 20
        
        # Productos con stock menor a 15
        productos_bajo = self.inventario.productos_bajo_stock(15)
        self.assertEqual(len(productos_bajo), 2)
        
        # Productos con stock menor a 5
        productos_muy_bajo = self.inventario.productos_bajo_stock(5)
        self.assertEqual(len(productos_muy_bajo), 0)
    
    def test_calcular_valor_total_inventario(self):
        """
        Test para calcular valor total del inventario.
        """
        self.inventario.agregar_producto(self.producto1)  # 100 * 10 = 1000
        self.inventario.agregar_producto(self.producto2)  # 200 * 5 = 1000
        
        valor_total = self.inventario.calcular_valor_total_inventario()
        self.assertEqual(valor_total, 2000.0)
    
    def test_calcular_valor_inventario_con_descuentos(self):
        """
        Test para calcular valor con descuentos.
        """
        self.inventario.agregar_producto(self.producto1)  # precio: 100
        self.inventario.agregar_producto(self.producto2)  # precio: 200
        
        # Test con umbral 150
        valor_con_descuentos = self.inventario.calcular_valor_inventario_con_descuentos(
            umbral_precio=150.0, factor_alto=1.1, factor_bajo=0.9
        )
        # producto1 (100): 100 * 0.9 = 90
        # producto2 (200): 200 * 1.1 = 220
        # Total: 90 + 220 = 310
        self.assertEqual(valor_con_descuentos, 310.0)
    
    def test_calcular_valor_inventario_parametros_invalidos(self):
        """
        Test para parámetros inválidos en cálculo de valor.
        """
        with self.assertRaises(ValueError):
            self.inventario.calcular_valor_inventario_con_descuentos(umbral_precio=-10.0)
        
        with self.assertRaises(ValueError):
            self.inventario.calcular_valor_inventario_con_descuentos(factor_alto=-1.0)
    
    def test_generar_analisis_completo_inventario(self):
        """
        Test para análisis completo del inventario.
        """
        self.inventario.agregar_producto(self.producto1)
        self.inventario.agregar_producto(self.producto2)
        
        analisis = self.inventario.generar_analisis_completo_inventario()
        
        self.assertIn('resumen', analisis)
        self.assertIn('estadisticas', analisis)
        self.assertIn('analisis_stock', analisis)
        self.assertIn('productos_clasificados', analisis)
        self.assertIn('reportes', analisis)
        self.assertIn('optimizaciones', analisis)
        self.assertIn('recomendaciones', analisis)
        
        self.assertEqual(analisis['resumen']['total_productos'], 2)
    
    def test_generar_analisis_parametros_invalidos(self):
        """
        Test para parámetros inválidos en análisis.
        """
        with self.assertRaises(ValueError):
            self.inventario.generar_analisis_completo_inventario(umbral_precio_alto=-10.0)
        
        with self.assertRaises(ValueError):
            self.inventario.generar_analisis_completo_inventario(umbral_stock_bajo=-5)
    
    def test_persistencia_datos(self):
        """
        Test para verificar la persistencia de datos.
        """
        # Agregar productos
        self.inventario.agregar_producto(self.producto1)
        self.inventario.agregar_producto(self.producto2)
        
        # Crear nuevo inventario que cargue los datos
        nuevo_inventario = Inventario(self.temp_file.name)
        
        # Verificar que los datos se cargaron correctamente
        self.assertEqual(len(nuevo_inventario.productos), 2)
        self.assertIn("TEST001", nuevo_inventario.productos)
        self.assertIn("TEST002", nuevo_inventario.productos)

    def test_generar_reporte_stock_bajo(self):
        """Test generación de reporte de stock bajo."""
        self.inventario.agregar_producto(self.producto1)
        self.inventario.agregar_producto(self.producto2)
        
        reporte = self.inventario.generar_reporte_stock_bajo(15)
        self.assertIn("REPORTE", reporte)
        self.assertIn("TEST001", reporte)

    def test_generar_estadisticas(self):
        """Test generación de estadísticas."""
        self.inventario.agregar_producto(self.producto1)
        self.inventario.agregar_producto(self.producto2)
        
        estadisticas = self.inventario.generar_estadisticas()
        self.assertIn("ESTADÍSTICAS", estadisticas)
        self.assertIn("Total de productos: 2", estadisticas)

    def test_obtener_producto_mas_caro(self):
        """Test obtener producto más caro."""
        self.inventario.agregar_producto(self.producto1)  # 100.0
        self.inventario.agregar_producto(self.producto2)  # 200.0
        
        mas_caro = self.inventario.obtener_producto_mas_caro()
        self.assertEqual(mas_caro.id, "TEST002")

    def test_calcular_promedio_precios_por_categoria(self):
        """Test cálculo de promedio por categoría."""
        self.inventario.agregar_producto(self.producto1)
        self.inventario.agregar_producto(self.producto3)
        
        promedios = self.inventario.calcular_promedio_precios_por_categoria()
        self.assertIn("Categoria A", promedios)

class TestIntegracion(unittest.TestCase):
    """
    Tests de integración del sistema completo.
    """
    
    def setUp(self):
        """
        Configuración para tests de integración.
        """
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.inventario = Inventario(self.temp_file.name)
    
    def tearDown(self):
        """
        Limpieza después de cada test.
        """
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_flujo_completo_inventario(self):
        """
        Test del flujo completo del sistema.
        """
        # 1. Agregar productos
        producto1 = Producto("PROD001", "Laptop", "Electrónicos", 1000.0, 5)
        producto2 = Producto("PROD002", "Mouse", "Electrónicos", 25.0, 50)
        producto3 = Producto("PROD003", "Libro", "Libros", 15.0, 100)
        
        self.assertTrue(self.inventario.agregar_producto(producto1))
        self.assertTrue(self.inventario.agregar_producto(producto2))
        self.assertTrue(self.inventario.agregar_producto(producto3))
        
        # 2. Verificar productos agregados
        self.assertEqual(len(self.inventario.productos), 3)
        
        # 3. Buscar por categoría
        electronicos = self.inventario.buscar_por_categoria("Electrónicos")
        self.assertEqual(len(electronicos), 2)
        
        # 4. Actualizar stock
        self.assertTrue(self.inventario.actualizar_stock("PROD001", 3))
        self.assertEqual(self.inventario.productos["PROD001"].cantidad, 3)
        
        # 5. Calcular valor total
        valor_total = self.inventario.calcular_valor_total_inventario()
        valor_esperado = (1000.0 * 3) + (25.0 * 50) + (15.0 * 100)
        self.assertEqual(valor_total, valor_esperado)
        
        # 6. Productos bajo stock
        productos_bajo = self.inventario.productos_bajo_stock(10)
        self.assertEqual(len(productos_bajo), 1)  # Solo PROD001
        
        # 7. Eliminar producto
        self.assertTrue(self.inventario.eliminar_producto("PROD003"))
        self.assertEqual(len(self.inventario.productos), 2)
    
    def test_manejo_errores(self):
        """
        Test para manejo de errores.
        """
        # Intentar agregar producto con ID duplicado
        producto1 = Producto("TEST001", "Producto 1", "Categoria", 100.0, 10)
        producto2 = Producto("TEST001", "Producto 2", "Categoria", 200.0, 5)
        
        self.assertTrue(self.inventario.agregar_producto(producto1))
        self.assertFalse(self.inventario.agregar_producto(producto2))
        
        # Intentar operaciones con productos inexistentes
        self.assertFalse(self.inventario.actualizar_stock("INEXISTENTE", 10))
        self.assertFalse(self.inventario.actualizar_precio("INEXISTENTE", 100.0))
        self.assertFalse(self.inventario.eliminar_producto("INEXISTENTE"))


if __name__ == '__main__':
    unittest.main()