module "portal" {
  source  = "./modulo_ficha"
  nombre  = var.nombre_aplicacion
  entorno = var.entorno
}

module "ayuda" {
  source  = "./modulo_ficha"
  nombre  = "portal-ayuda"
  entorno = var.entorno
}
