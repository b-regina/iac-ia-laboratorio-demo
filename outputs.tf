output "resumen" {
  description = "Fichas previstas para el caso ficticio"
  value = {
    portal = module.portal.resumen
    ayuda  = module.ayuda.resumen
  }
}
