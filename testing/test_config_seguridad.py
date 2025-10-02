import unittest
import os
from config_seguridad import ConfiguracionSeguridad


class TestConfiguracionSeguridad(unittest.TestCase):
    
    def setUp(self):
        self.config = ConfiguracionSeguridad()

    # --- Pruebas de clave segura ---
    def test_obtener_clave_segura_longitud(self):
        """Debe generar una clave segura de 64 caracteres (32 bytes)."""
        clave = self.config.obtener_clave_segura()
        self.assertEqual(len(clave), 64)

    def test_obtener_clave_segura_hex_valido(self):
        """La clave generada debe ser hexadecimal válido."""
        clave = self.config.obtener_clave_segura()
        try:
            int(clave, 16)  # Verifica que puede convertirse desde hex
        except ValueError:
            self.fail("La clave generada no es hexadecimal válido.")

    def test_obtener_clave_segura_aleatoriedad(self):
        """Dos claves consecutivas no deben ser iguales."""
        clave1 = self.config.obtener_clave_segura()
        clave2 = self.config.obtener_clave_segura()
        self.assertNotEqual(clave1, clave2)

    # --- Pruebas de hash ---
    def test_hash_seguro_con_salt(self):
        """El hash debe ser reproducible si el salt es fijo."""
        texto = "password123"
        salt = "abc123"
        hash1 = self.config.hash_seguro(texto, salt)
        hash2 = self.config.hash_seguro(texto, salt)
        self.assertEqual(hash1, hash2)

    def test_verificar_hash_invalido(self):
        """Debe devolver False si el hash no tiene el formato esperado."""
        self.assertFalse(self.config.verificar_hash("texto", "hashsinformato"))

    # --- Pruebas de validación de entrada ---
    def test_validar_entrada_segura_texto_normal(self):
        self.assertTrue(self.config.validar_entrada_segura("texto normal"))

    def test_validar_entrada_segura_caracteres_peligrosos(self):
        self.assertFalse(self.config.validar_entrada_segura("<script>"))
        self.assertFalse(self.config.validar_entrada_segura("or 1=1;"))

    def test_validar_entrada_segura_demasiado_larga(self):
        """Debe rechazar entradas que excedan el tamaño máximo permitido."""
        entrada = "a" * (self.config.configuraciones['max_input_length'] + 1)
        self.assertFalse(self.config.validar_entrada_segura(entrada))

    def test_validar_entrada_segura_tipo_invalido(self):
        """Debe rechazar entradas que no son cadenas."""
        self.assertFalse(self.config.validar_entrada_segura(12345))
        self.assertFalse(self.config.validar_entrada_segura(None))

    # --- Pruebas de sanitización ---
    def test_sanitizar_entrada_tags(self):
        """Debe escapar correctamente los tags HTML."""
        entrada = "<b>Texto</b>"
        resultado = self.config.sanitizar_entrada(entrada)
        self.assertEqual(resultado, "&amp;lt;b&amp;gt;Texto&amp;lt;/b&amp;gt;")

    def test_sanitizar_entrada_caracteres_control(self):
        """Debe remover caracteres de control."""
        entrada = "texto\x01\x02seguro"
        resultado = self.config.sanitizar_entrada(entrada)
        self.assertEqual(resultado, "textoseguro")

    def test_sanitizar_entrada_exceso_longitud(self):
        """Debe truncar entradas que exceden el límite."""
        max_length = self.config.configuraciones['max_input_length']
        entrada = "a" * (max_length + 50)
        resultado = self.config.sanitizar_entrada(entrada)
        self.assertEqual(len(resultado), max_length)

    def test_sanitizar_entrada_no_string(self):
        """Debe convertir tipos no string a cadena."""
        resultado = self.config.sanitizar_entrada(12345)
        self.assertEqual(resultado, "12345")

    # --- Pruebas de configuración ---
    def test_obtener_configuracion_existente(self):
        """Debe obtener una configuración existente."""
        valor = self.config.obtener_configuracion("max_file_size")
        self.assertEqual(valor, 10485760)

    def test_obtener_configuracion_inexistente(self):
        """Debe devolver el valor por defecto si no existe la clave."""
        valor = self.config.obtener_configuracion("clave_inexistente", "default")
        self.assertEqual(valor, "default")

    def test_configuracion_sobreescrita_por_entorno(self):
        """Debe tomar la configuración desde variables de entorno."""
        os.environ["MAX_FILE_SIZE"] = "2048"
        nueva_config = ConfiguracionSeguridad()
        self.assertEqual(nueva_config.obtener_configuracion("max_file_size"), 2048)
        del os.environ["MAX_FILE_SIZE"]  # limpiar variable de entorno


if __name__ == "__main__":
    unittest.main()
