from odoo import models, fields

class BibliotecaLibro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro de la biblioteca'

    name = fields.Char(string='Título', required=True)
    autor = fields.Char(string='Autor', default='Manuel')
    fecha = fields.Date(string='Fecha de publicación')

