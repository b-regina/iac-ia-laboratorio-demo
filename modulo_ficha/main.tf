resource "terraform_data" "ficha" {
  input = {
    nombre    = var.nombre
    entorno   = var.entorno
    etiquetas = {
      proyecto    = "nexo-portal"
      entorno     = var.entorno
      responsable = var.responsable
    }
  }
}
