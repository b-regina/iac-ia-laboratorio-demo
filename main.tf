locals {
  catalogo = {
    portal   = var.nombre_aplicacion
    ayuda    = "portal-ayuda"
    informes = "portal-informes"
  }
}

module "fichas" {
  for_each = local.catalogo
  source   = "./modulo_ficha"
  nombre   = each.value
  entorno  = var.entorno
}
