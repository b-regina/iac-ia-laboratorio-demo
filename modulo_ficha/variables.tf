variable "nombre" {
  description = "Nombre ficticio de la ficha"
  type        = string

  validation {
    condition     = startswith(var.nombre, "portal-")
    error_message = "El nombre del modulo debe comenzar por portal-."
  }
}

variable "entorno" {
  description = "Entorno ficticio de la ficha"
  type        = string

  validation {
    condition     = contains(["desarrollo", "pruebas", "integracion"], var.entorno)
    error_message = "El entorno del modulo debe ser desarrollo, pruebas o integracion."
  }
}
