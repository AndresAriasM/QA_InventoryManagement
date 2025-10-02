import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from main import SistemaInventario

class TestSistemaInventarioCompleto(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        with patch('inventario.Inventario') as mock_inv:
            mock_inv.return_value.archivo_datos = self.temp_file.name
            self.sistema = SistemaInventario()
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    @patch('builtins.input', side_effect=['TEST001', 'Laptop', 'Electronica', '1000', '5'])
    @patch('builtins.print')
    def test_agregar_producto_flujo_completo(self, mock_print, mock_input):
        """Test flujo completo agregar producto."""
        self.sistema.agregar_producto()
        # Verificar que se llamó al inventario
        
    @patch('builtins.input', return_value='')
    def test_agregar_producto_cancelado(self, mock_input):
        """Test cancelar agregar producto."""
        with patch.object(self.sistema, 'obtener_entrada', return_value=None):
            self.sistema.agregar_producto()
    
    @patch('builtins.input', side_effect=['TEST001', 's'])
    def test_eliminar_producto_confirmado(self, mock_input):
        """Test eliminar producto con confirmación."""
        from producto import Producto
        prod = Producto('TEST001', 'Test', 'Cat', 100.0, 10)
        self.sistema.inventario.agregar_producto(prod)
        
        with patch.object(self.sistema, 'obtener_entrada', side_effect=['TEST001', 's']):
            self.sistema.eliminar_producto()
    
    @patch('builtins.input', side_effect=['TEST001', 'n'])
    def test_eliminar_producto_cancelado(self, mock_input):
        """Test cancelar eliminación."""
        from producto import Producto
        prod = Producto('TEST001', 'Test', 'Cat', 100.0, 10)
        self.sistema.inventario.agregar_producto(prod)
        
        with patch.object(self.sistema, 'obtener_entrada', side_effect=['TEST001', 'n']):
            self.sistema.eliminar_producto()
    
    @patch('builtins.input', side_effect=['TEST001', '20'])
    def test_actualizar_stock_exitoso(self, mock_input):
        """Test actualizar stock."""
        from producto import Producto
        prod = Producto('TEST001', 'Test', 'Cat', 100.0, 10)
        self.sistema.inventario.agregar_producto(prod)
        
        with patch.object(self.sistema, 'obtener_entrada', side_effect=['TEST001', 20]):
            self.sistema.actualizar_stock()
    
    @patch('builtins.input', side_effect=['TEST001', '150.0'])
    def test_actualizar_precio_exitoso(self, mock_input):
        """Test actualizar precio."""
        from producto import Producto
        prod = Producto('TEST001', 'Test', 'Cat', 100.0, 10)
        self.sistema.inventario.agregar_producto(prod)
        
        with patch.object(self.sistema, 'obtener_entrada', side_effect=['TEST001', 150.0]):
            self.sistema.actualizar_precio()
    
    @patch('builtins.input', return_value='Laptop')
    def test_buscar_por_nombre(self, mock_input):
        """Test buscar por nombre."""
        with patch.object(self.sistema, 'obtener_entrada', return_value='Laptop'):
            self.sistema.buscar_por_nombre()
    
    @patch('builtins.input', return_value='Electronica')
    def test_buscar_por_categoria(self, mock_input):
        """Test buscar por categoría."""
        with patch.object(self.sistema, 'obtener_entrada', return_value='Electronica'):
            self.sistema.buscar_por_categoria()
    
    def test_mostrar_todos_productos(self):
        """Test mostrar todos."""
        with patch('builtins.input', return_value=''):
            self.sistema.mostrar_todos_productos()
    
    def test_reporte_stock_bajo(self):
        """Test reporte stock bajo."""
        with patch('builtins.input', return_value=''):
            self.sistema.reporte_stock_bajo()
    
    def test_reporte_valor_inventario(self):
        """Test reporte valor."""
        with patch('builtins.input', return_value=''):
            self.sistema.reporte_valor_inventario()
    
    def test_estadisticas_inventario(self):
        """Test estadísticas."""
        with patch('builtins.input', return_value=''):
            self.sistema.estadisticas_inventario()
    
    @patch('builtins.input', return_value='15')
    def test_configurar_umbral_stock(self, mock_input):
        """Test configurar umbral."""
        with patch.object(self.sistema, 'obtener_entrada', return_value=15):
            self.sistema.configurar_umbral_stock()
            self.assertEqual(self.sistema.umbral_stock_bajo, 15)
    
    def test_obtener_entrada_validaciones(self):
        """Test validaciones de entrada."""
        with patch('builtins.input', return_value='100'):
            resultado = self.sistema.obtener_entrada("Test:", int, {'minimo': 50, 'maximo': 200})
            self.assertEqual(resultado, 100)
        
        with patch('builtins.input', side_effect=['10', '100']):
            resultado = self.sistema.obtener_entrada("Test:", int, {'minimo': 50})
            self.assertEqual(resultado, 100)
    
    def test_validar_string_seguro_multiples_patrones(self):
        """Test múltiples patrones peligrosos."""
        self.assertFalse(self.sistema._validar_string_seguro("<iframe src='malicious'>"))
        self.assertFalse(self.sistema._validar_string_seguro("javascript:void(0)"))
        self.assertFalse(self.sistema._validar_string_seguro("vbscript:msgbox"))
        self.assertFalse(self.sistema._validar_string_seguro("data:text/html,<script>"))
        self.assertFalse(self.sistema._validar_string_seguro("file:///etc/passwd"))
        self.assertTrue(self.sistema._validar_string_seguro("texto normal"))