import unittest
from unittest.mock import patch, MagicMock
from main import SistemaInventario

class TestSistemaInventario(unittest.TestCase):
    
    def setUp(self):
        self.sistema = SistemaInventario()
    
    def test_inicializacion(self):
        """Test que el sistema se inicializa correctamente."""
        self.assertIsNotNone(self.sistema.inventario)
        self.assertEqual(self.sistema.umbral_stock_bajo, 10)
    
    @patch('builtins.input', return_value='TEST001')
    def test_obtener_entrada_string(self, mock_input):
        """Test obtener entrada de tipo string."""
        resultado = self.sistema.obtener_entrada("Test: ", str)
        self.assertEqual(resultado, 'TEST001')
    
    @patch('builtins.input', return_value='100')
    def test_obtener_entrada_int(self, mock_input):
        """Test obtener entrada de tipo int."""
        resultado = self.sistema.obtener_entrada("Número: ", int)
        self.assertEqual(resultado, 100)
    
    def test_sanitizar_entrada(self):
        """Test sanitización de entrada."""
        # La sanitización de main solo quita caracteres de control, no HTML
        entrada_con_control = "test\x00\x01normal"
        resultado = self.sistema._sanitizar_entrada(entrada_con_control)
        self.assertNotIn('\x00', resultado)
        self.assertEqual(resultado, "testnormal")
    
    def test_validar_string_seguro(self):
        """Test validación de strings seguros."""
        self.assertTrue(self.sistema._validar_string_seguro("texto normal"))
        self.assertFalse(self.sistema._validar_string_seguro("<script>"))
        self.assertFalse(self.sistema._validar_string_seguro("javascript:"))
    
    @patch('builtins.input', side_effect=['s'])
    @patch('builtins.print')
    def test_agregar_producto_completo(self, mock_print, mock_input):
        """Test flujo completo de agregar producto."""
        with patch.object(self.sistema, 'obtener_entrada', side_effect=[
            'TEST001', 'Producto Test', 'Categoria', 100.0, 10
        ]):
            self.sistema.agregar_producto()
            producto = self.sistema.inventario.obtener_producto('TEST001')
            self.assertIsNotNone(producto)

    def test_validar_string_seguro_casos(self):
        """Test múltiples casos de validación."""
        self.assertTrue(self.sistema._validar_string_seguro("texto123"))
        self.assertFalse(self.sistema._validar_string_seguro("test<iframe>"))
        self.assertFalse(self.sistema._validar_string_seguro("javascript:alert()"))