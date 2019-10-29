# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date


class Agenda(models.Model): 
    _name = 'centro.agenda'
    _rec_name = 'descripcion'
    
    fecha = fields.Datetime(string='Fecha y hora', required=True)
    descripcion = fields.Text(string='Descripción', required=True)

class Agenda_especialista(models.Model): 
    _name = 'centro.agenda_especialista'
    _rec_name = 'descripcion'
    
    fecha = fields.Datetime(string='Fecha y hora', required=True)
    descripcion = fields.Text(string='Descripción', required=True)


class Receta(models.Model):
    _name = 'centro.receta'
    _rec_name = 'observacion'

    observacion = fields.Text(string="Observaciones", required=True)
    paciente_id = fields.Many2one(
        comodel_name='centro.paciente', string='Paciente', required=True)
    especialista_id = fields.Many2one(
        comodel_name='centro.especialista', string='Especialista', required=True)
    consulta_id = fields.Many2one(
        comodel_name='centro.consulta', string='Consulta', required=True)

class Consulta(models.Model):
    _name = 'centro.consulta'
    _rec_name = 'det_diagnostico'

    fecha = fields.Datetime(string="Fecha", required=True)
    det_diagnostico = fields.Text(string="Diagnóstico", required=True)
    estado = fields.Selection(
        [('atendido', 'Atendido'), ('noatendido', 'No Atendido')], required=True)
    reserva_id = fields.Many2one(
        comodel_name='centro.reserva', string='Reserva', required=True)
    paciente_id = fields.Many2one(
        comodel_name='centro.paciente', string='Paciente', required=True)
    receta_ids = fields.One2many(comodel_name='centro.receta', inverse_name='consulta_id', string='Recetas', required=True)
       
    
class Especialista(models.Model):
    _name = 'centro.especialista'
    _rec_name = 'nombre_es'

    rut_es = fields.Char(string='Rut', size=10, required= True)
    nombre_es = fields.Char(string='Nombre', size=50, required=True)

    especialidad_id = fields.Many2one(
        comodel_name='centro.especialidad', inverse_name='especialista_id', required=True)
    reserva_ids = fields.One2many(comodel_name='centro.reserva',
                                  inverse_name='especialista_id', string='Reservas', required=True)
    receta_ids = fields.One2many(comodel_name='centro.receta', inverse_name='especialista_id', string='Recetas', required=True)
    total_reserva = fields.Integer(compute ='_total_reserva', string= "Total de Reservas")

    @api.constrains ('rut_es') #VALIDAR RUT DEL ESPECIALISTA
    def validacion(self):
        cont=0 
        cont_num=0
        cont_guion=0
        buscar=self.rut_es
        while cont<len(buscar):
            if buscar[cont]=='0' or buscar[cont]=='1' or buscar[cont]=='2' or buscar[cont]=='3' or buscar[cont]=='4' or buscar[cont]=='5' or buscar[cont]=='6' or buscar[cont]=='7' or buscar[cont]=='8' or buscar[cont]=='9' or buscar[cont]=='K' or buscar[cont]=='k':
                cont_num+=1
            if buscar[cont]=='-':
                cont_guion+=1   
            cont+=1
        if cont_num<8 or cont_guion!=1:
            raise ValidationError('Rut incorrecto, ingrese nuevamente')
    

    @api.constrains ('nombre_es') #VALIDAR NOMBRE DEL ESPECIALISTA
    def validacion_nombre_e(self):
        cont=0 
        cont_num=0
        buscar=self.nombre_es
        while cont<len(buscar):
            if buscar[cont]=='0' or buscar[cont]=='1' or buscar[cont]=='2' or buscar[cont]=='3' or buscar[cont]=='4' or buscar[cont]=='5' or buscar[cont]=='6' or buscar[cont]=='7' or buscar[cont]=='8' or buscar[cont]=='9':
                cont_num=1
            cont+=1
        if cont_num==1:
            raise ValidationError('Nombre incorrecto, sólo ingresar carácteres válidos, intente nuevamente') 
    
    @api.one #KPI: CALCULAR EL NÙMERO DE RESERVAS POR ESPECIALISTA
    @api.depends('reserva_ids')
    def _total_reserva(self):
        self.total_reserva=len(self.reserva_ids)


class Especialidad(models.Model):
    _name = 'centro.especialidad'
    _rec_name = 'nombre_e'

    nombre_e = fields.Char(string='Especialidad', size=50, required=True)
    especialista_ids = fields.One2many(
        comodel_name='centro.especialista', inverse_name='especialidad_id', string='Especialista', required=True)
    total_especialista = fields.Integer(compute ='_total_especialista', string= "Total de Especialistas")
    
    @api.one #KPI: CALCULAR EL NÙMERO DE ESPECIALISTAS POR ESPECIALIDAD
    @api.depends('especialista_ids')
    def _total_especialista(self):
        self.total_especialista=len(self.especialista_ids)

class Reserva(models.Model):
    _name = 'centro.reserva'
    _rec_name = 'fecha'
  

    fecha = fields.Datetime(string="Fecha y Hora", required=True)
    estado = fields.Selection(
        [('pendiente', 'Pendiente'), ('realizada', 'Realizada'),('cancelada', 'Cancelada')], required=True)
    paciente_id = fields.Many2one(
        comodel_name='centro.paciente', string='Paciente', required=True)
    especialista_id = fields.Many2one(
        comodel_name='centro.especialista', string='Especialista', required=True)
    consulta_ids = fields.One2many(comodel_name='centro.consulta',
                                   inverse_name='reserva_id', string='Consultas', required=True)

class Paciente(models.Model):
    _name = 'centro.paciente'
    _rec_name = 'nombre'

    rut = fields.Char(string='Rut', size=10, required=True)
    domicilio = fields.Char(string='Domicilio', size=50, required=True)
    nombre = fields.Char(string='Nombre', size=50, required=True)
    det_prevision = fields.Selection([('fonasa', 'Fonasa'), ('isapre', 'Isapre'), (
        'particular', 'Particular')], string='Previsión', required=True)
    fecha_nac = fields.Date(string='Fecha de Nacimiento', required=True)
    det_grupo_sangre = fields.Selection([('onegativo', 'O-'), ('opositivo', 'O+'), ('anegativo', 'A-'), ('apositivo', 'A+'), (
        'bnegativo', 'B-'), ('bpositivo', 'B+'), ('abnegativo', 'AB-'), ('abpositivo', 'AB+')], string='Grupo de Sangre', required=True)
    email = fields.Char(string='Correo Electronico', size=50, required=True)
    det_alergia = fields.Char(string='Alergias', required=True)
    celular = fields.Char(string='Celular', size=9, required=True)
    det_vacuna = fields.Char(string='Vacunas', required=True)
    reserva_ids = fields.One2many(comodel_name='centro.reserva',
                                  inverse_name='paciente_id', string='Reservas', required=True)
    receta_ids = fields.One2many(
        comodel_name='centro.receta', inverse_name='paciente_id', string='Recetas', required=True)
    consulta_ids = fields.One2many(
        comodel_name='centro.consulta', inverse_name='paciente_id', string='Consulta', required=True)
    edad = fields.Integer(compute ='_cal_age')
    total_receta = fields.Integer(compute ='_total_receta', string= 'Total de Recetas')
    total_consulta = fields.Integer(compute ='_total_consulta', string= 'Total de Consultas')
    total_reservap = fields.Integer(compute ='_total_reservap', string= 'Total de Reservas')
    

    @api.depends('fecha_nac') #CALCULAR EDAD
    @api.one
    def _cal_age(self):
        if self.fecha_nac:
            years = relativedelta(date.today(), self.fecha_nac).years
            self.edad = int(years)  

    @api.constrains ('rut') #VALIDAR RUT DEL PACIENTE
    def validacion(self):
        cont=0 
        cont_num=0
        cont_guion=0
        buscar=self.rut
        while cont<len(buscar):
            if buscar[cont]=='0' or buscar[cont]=='1' or buscar[cont]=='2' or buscar[cont]=='3' or buscar[cont]=='4' or buscar[cont]=='5' or buscar[cont]=='6' or buscar[cont]=='7' or buscar[cont]=='8' or buscar[cont]=='9' or buscar[cont]=='K' or buscar[cont]=='k':
                cont_num+=1
            if buscar[cont]=='-':
                cont_guion+=1   
            cont+=1
        if cont_num<8 or cont_guion!=1:
            raise ValidationError('Rut incorrecto, ingrese nuevamente')

    @api.constrains ('celular') #VALIDAR CELULAR DEL PACIENTE
    def validacion_celular(self):
        cont=0 
        cont_let=0
        buscar=self.celular
        while cont<len(buscar):
            if buscar[cont]=='0' or buscar[cont]=='1' or buscar[cont]=='2' or buscar[cont]=='3' or buscar[cont]=='4' or buscar[cont]=='5' or buscar[cont]=='6' or buscar[cont]=='7' or buscar[cont]=='8' or buscar[cont]=='9':
                cont_let=1
            else:
                raise ValidationError('Celular incorrecto, por favor ingrese sólo carácteres válidos, intente nuevamente') 
            cont+=1
 

    @api.constrains ('nombre') #VALIDAR NOMBRE DEL PACIENTE
    def validacion_nombre(self):
        cont=0 
        cont_num=0
        buscar=self.nombre
        while cont<len(buscar):
            if buscar[cont]=='0' or buscar[cont]=='1' or buscar[cont]=='2' or buscar[cont]=='3' or buscar[cont]=='4' or buscar[cont]=='5' or buscar[cont]=='6' or buscar[cont]=='7' or buscar[cont]=='8' or buscar[cont]=='9':
                cont_num=1
            cont+=1
        if cont_num==1:
            raise ValidationError('Nombre incorrecto, sólo ingresar carácteres válidos, intente nuevamente') 

    @api.one #KPI: CALCULAR EL NÙMERO DE RECETAS POR PACIENTE
    @api.depends('receta_ids')
    def _total_receta(self):
        self.total_receta=len(self.receta_ids)
    
    @api.one #KPI: CALCULAR EL NÙMERO DE CONSULTAS POR PACIENTE
    @api.depends('consulta_ids')
    def _total_consulta(self):
        self.total_consulta=len(self.consulta_ids)
    
    @api.one #KPI: CALCULAR EL NÙMERO DE RESERVAS POR PACIENTE
    @api.depends('reserva_ids')
    def _total_reservap(self):
        self.total_reservap=len(self.reserva_ids)
    
    @api.constrains ('fecha_nac')
    def validarfecha(self):
        nac=self.fecha_nac
        hoy = fields.Date.today()
        if nac>hoy:
            raise ValidationError('La fecha de nacimiento no corresponde, por favor ingresar sólo datos válidos, intente nuevamente ') 