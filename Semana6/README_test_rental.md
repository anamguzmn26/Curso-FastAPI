# Tests Rent a Car - Guzmán Martínez

## Cobertura Esperada: >80 %

### Tests Implementados:

- ✅ test_create_alquiler – Crear alquiler con datos válidos
- ✅ test_get_alquiler_not_found – Manejo de alquiler inexistente
- ✅ test_regla_negocio_fechas – Validar que fecha_fin > fecha_inicio
- ✅ test_update_alquiler – Actualizar precio de un alquiler existente
- ✅ test_delete_alquiler – Eliminar un alquiler y verificar que no existe

### Casos de Prueba Específicos de Rent a Car:

1. Validar que `fecha_fin` sea posterior a `fecha_inicio`
2. Validar que `precio_dia` sea positivo
3. Validar que se incluya seguro obligatorio según políticas de la empresa
4. Actualizar datos de un alquiler existente
5. Eliminar un alquiler y comprobar que no puede ser consultado
