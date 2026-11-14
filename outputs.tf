output "resumen" {
  description = "Catalogo de fichas ficticias previsto para este entorno"
  value = {
    for clave, ficha in module.fichas : clave => ficha.resumen
  }
}
