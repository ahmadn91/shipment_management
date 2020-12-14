# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Shipment(models.Model):
    _name="shipment.shipment"
    _inherit = 'mail.thread'
    _rec_name="partner_id"
    """ Logistic Details """
    partner_id = fields.Many2one("res.partner",required=True)
    dispatch_date = fields.Date(string="Dispatch Date",required=True)


   
    
    awb_bol = fields.Many2many("shipment.awb",string="AWB/BOL")
    poe_arrival_date = fields.Date(string="POE Arrival Date")
    no_of_trucks = fields.Char(string="Number of Trucks")
    london_notif = fields.Char(string="London Notification")
    legalized_docs_recieved = fields.Char(string="Legalized Docs Recieved")
    legalized_docs_given = fields.Char(string="Legalized Docs given")
    abu_gharib_arrival_Date = fields.Many2many(string="Abu Gharib Arrival Date",comodel_name="shipment.dates",relation="abg_arr_dates_rel",column1="shipment_dates_abg_arr",column2="dates_shipment_abg_arr")
    abu_gharib_departure_Date = fields.Many2many(string="Abu Gharib Departure Date",comodel_name="shipment.dates",relation="abg_dep_dates_rel",column1="shipment_dates_abg_dep",column2="dates_shipment_abg_dep")
    poe = fields.Many2one('shipment.poe', string='Port of Entry')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    clearence_company = fields.Many2many(comodel_name="clearence.company",relation="shipment_clearence_rel",column1="shipment_clearence",column2="clearence_shipment",string="Clearence Company")


    

    

    """ Financial Details """
    admin_expenses = fields.Float(string="Administrative Expenses")
    admin_expenses_date = fields.Date(string="Administrative Expenses Date")
    tc_invoice= fields.Many2many(comodel_name="tc.invoice",relation="tc_shipment_rel",column1="tc_shipment",column2="shipment_tc",string="TC Invoice")
    tc_invoice_date = fields.Date(string="TC Invoice Date",related="tc_invoice.date")
    tc_invoice_value = fields.Float(string="TC Invoice Value",related="tc_invoice.value")
    percentage = fields.Float(string="Percentage",compute="calculate_percentage")
    tax_paid = fields.Float(string="Tax Paid")
    customs_paid = fields.Float(string="Customs Paid")
    total = fields.Float(string="Total",compute="calculate_total")
    total_percentage = fields.Float(string="Total Percentage",compute="calc_total_percentage")
    # shipment_value = fields.Float(string="Shipment Value")
    container_dumurrage = fields.Float(string="Container Dumurrage")
    truck_dumurrage = fields.Float(string="Truck Dumurrage")
    state=fields.Selection([("draft","Draft"),("upcoming","Upcoming"),("at airport now","At airpot now"),("arrived in w.h + paid inv.","Arrived in W.H. + paid inv."),("cancelled","Cancelled")],string="Status",default="draft",required=True)
    shipping_line = fields.Char(string="Shipping Line")
    unloading_date_to_truck = fields.Date(string="Unloading Date to Truck in POE")
    legalized_doc_date = fields.Date(string="Legalized Docs Collection Date")
    containers= fields.Char(string="Containers")
    """ Shipment Line Items """
    
    shipment_line = fields.One2many("shipment.invoice","conn",string="Shipment Line Items")
    
    purchase_proxy = fields.Many2many(comodel_name="purchase.order",relation="proxy_purchase_rel",column1="pur_pro",cloumn2="pro_pur",string="Purchase Orders",related="shipment_line.rel_purchase_orders")
    
    
    @api.constrains("tc_invoice","shipment_line")
    def calculate_percentage(self):
        for rcd in self:
            total_tc=0
            total_shipment=0
            if rcd.tc_invoice:
                for item in rcd.tc_invoice:
                    total_tc+=item.value
            if rcd.shipment_line:
                for item in rcd.shipment_line:
                    total_shipment += item.shipment_value
            if total_tc !=0 and total_shipment !=0:
                rcd.percentage = total_tc / total_shipment
            else:
                rcd.percentage = False
    @api.constrains("tc_invoice","admin_expenses")
    def calculate_total(self):
        for rcd in self:
            total_tc = 0
            if rcd.tc_invoice:
                for item in rcd.tc_invoice:
                    total_tc += item.value
            rcd.total = total_tc + rcd.admin_expenses
            


    @api.constrains("total","shipment_line")
    def calc_total_percentage(self):
        for rcd in self:
            total_shipment=0
            if rcd.shipment_line:
                for item in rcd.shipment_line:
                    total_shipment += item.shipment_value
                if rcd.total !=0 and total_shipment !=0:
                    rcd.total_percentage = rcd.total / total_shipment 
                else:
                    rcd.total_percentage = False

        

    def escalate(self):
        if self.state =="draft":
            self.state="upcoming"
        elif self.state=="upcoming":
            self.state="at airport now"
        elif self.state=="at airport now":
            self.state = "arrived in w.h + paid inv."

    def cancel(self):
        self.state = "cancelled"


    


class ShipmentInvoices(models.Model):

    _name="shipment.invoice"
    _rec_name="invoice"
    conn = fields.Integer()
    invoice = fields.Many2one("account.move",string="Invoice")
    due_date = fields.Date(related="invoice.invoice_date",string="Invoice Due Date")
    rel_purchase_orders = fields.Many2many(comodel_name="purchase.order",relation="shipment_purchase_rel",column1="shipment_pur",column2="pur_shipment",string="Purchase Orders")
    # purchase_orders_ref = fields.Char(string="Reference",compute="purchase_reference_calc")
    rel_products = fields.Many2many(comodel_name="product.product",relation="shipment_product_rel",column1="shipment_pro",column2="pro_shipment",string="Related Products")
    warehouse_arr_dates = fields.Many2many(comodel_name="shipment.dates",relation="shipment_dates_rel",column1="shipment_dates",column2="dates_shipment",string="Warehouse Arrival Dates")
    licenses = fields.Many2many("license.license",string="Related Licenses")
    qty = fields.Many2many("shipment.quant",string="Quantity")
    gross_weight = fields.Float(string="Gross Weight")
    shipment_value = fields.Float(string="Shipment Value")
    pallets_cartons = fields.Char(string="Pallets/Cartons")
    notes=fields.Char(string="notes")


    # @api.depends("rel_purchase_orders")
    # def purchase_reference_calc(self):
    #     refs=[]
    #     for item in self:
    #         for po in item.rel_purchase_orders:
    #             po_object = self.env["purchase.order"].search([("name","=",po.name)])
    #             refs.append(po_object.partner_ref)
    #     self.purchase_orders_ref = '-'.join(refs)


class ShipmentLineDates(models.Model):
    _name="shipment.dates"
    _rec_name = "date"
    date = fields.Date(string="Date")


class ShipmentPoe(models.Model):
    _name="shipment.poe"
    _rec_name="name"

    #conn=fields.Integer()
    name=fields.Char(string="Port of Entry")



class ClearenceCompany(models.Model):
    _name="clearence.company"
    _rec_name="name"

    name=fields.Char(string="Name")


class TcInvoice(models.Model):
    _name="tc.invoice"
    _rec_name = "number"

    number = fields.Char(string="Invoice Number")
    date = fields.Date(string="Invoice Date")
    value = fields.Float(string="Invoice Value")


class ShipmentProductQuantity(models.Model):
    _name="shipment.quant"
    _rec_name = "quantity"

    quantity = fields.Integer(string="Quantity")


class AwbBol(models.Model):
    _name="shipment.awb"
    _rec_name = "number"
    number = fields.Char(string="AWB/BOL")




class AccountMoveExt(models.Model):
    _inherit="account.move"


    @api.model
    def name_get(self):
        result = []
        for record in self:
            if self.env.user.has_group('shipment_management.shipment_inv_pur_ref_show'):
                record_name = record.ref
                result.append((record.id, record_name))
            else:
                record_name = record.name
                result.append((record.id, record_name))
        return result

            
class PurchaseOrderExt(models.Model):

    _inherit="purchase.order"


    @api.model
    def name_get(self):
        result = []
        for record in self:
            if self.env.user.has_group('shipment_management.shipment_inv_pur_ref_show') :
                record_name = record.partner_ref
                result.append((record.id, record_name))
            else:
                record_name = record.name
                result.append((record.id, record_name))
        return result


