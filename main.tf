locals {
  catalogo = {
    portal = var.nombre_aplicacion
    ayuda  = "portal-ayuda"
  }
}

module "fichas" {
  for_each = local.catalogo
  source   = "./modulo_ficha"
  nombre   = each.value
  entorno  = var.entorno
}
