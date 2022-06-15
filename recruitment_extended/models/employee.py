# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.http import request
from datetime import datetime



class EmergencyContact(models.Model):
    _name = "recruit.employee"
    _description = "Employee details"

    name = fields.Char(string="Name", size=50, track_visibility='always')
    address = fields.Char(string="Address", size=50, )
    phone = fields.Char(string="Phone", track_visibility='always')
    applicant_id = fields.Many2one('hr.applicant', string="Applicant")
    employee_id = fields.Many2one('hr.employee', string="Applicant")
    

class Applicant(models.Model):
    _inherit = 'hr.applicant'


    emergency_contact = fields.One2many(comodel_name="recruit.employee",inverse_name="applicant_id",string="Emergency Contact")
    education_info = fields.One2many(comodel_name="education.info",inverse_name="applicant_id",string="Education Info")

    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.display_name
            else:
                if not applicant.partner_name:
                    raise UserError(_('You must define a Contact Name for this applicant.'))
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'type': 'private',
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.partner_name or contact_name:
                employee = self.env['hr.employee'].create({
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id or False,
                    'job_title': applicant.job_id.name,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                            and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.phone or False,
                    'applicant_emergency_contact':applicant.emergency_contact or False,
                    'education_info': applicant.education_info or False,         
                            })
                           
                applicant.write({'emp_id': employee.id})
                if applicant.job_id:
                    applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                    applicant.job_id.message_post(
                        body=_('New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                        subtype="hr_recruitment.mt_job_applicant_hired")
                applicant.message_post_with_view(
                    'hr_recruitment.applicant_hired_template',
                    values={'applicant': applicant},
                    subtype_id=self.env.ref("hr_recruitment.mt_applicant_hired").id)

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        dict_act_window['context'] = {'form_view_initial_mode': 'edit'}
        dict_act_window['res_id'] = employee.id
        return dict_act_window

class Employee(models.Model):
    _inherit = 'hr.employee'

    applicant_emergency_contact = fields.One2many(comodel_name="recruit.employee",inverse_name="employee_id",string="Emergency Contact")
    education_info = fields.One2many(comodel_name="education.info",inverse_name="employee_id",string="Education Info" )

class EducationInfo(models.Model):
    _name = "education.info"
    _description = "Education Info details"

    institute = fields.Char(string="Institute", size=50)
    degree =  fields.Char(string="Degree", size=50)
    passing_year =  fields.Date(string="Passing Year", size=50)
    applicant_id = fields.Many2one('hr.applicant', string="Applicant")
    employee_id = fields.Many2one('hr.employee', string="Applicant")
    