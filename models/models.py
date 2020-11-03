# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Shipment(models.Model):
    _name="shipment.shipment"
    _rec_name="partner_id"
    """ Logistic Details """
    partner_id = fields.Many2one("res.partner",string="Vendor",required=True)
    dispatch_date = fields.Date(string="Dispatch Date",required=True)
    pallets_cartons = fields.Integer(string="Pallets/Cartons")
    awb_bol = fields.Integer(string="AWB/BOL")
    poe_arrival_date = fields.Date(string="POE Arrival Date")
    no_of_trucks = fields.Integer(string="Number of Trucks")
    london_notif = fields.Char(string="London Notification")
    legalized_docs_recieved = fields.Char(string="Legalized Docs Recieved")
    legalized_docs_given = fields.Char(string="Legalized Docs given")
    abu_gharib_arrival_Date = fields.Date(string="Abu Gharib Arrival Date")
    abu_gharib_departure_Date = fields.Date(string="Abu Gharib Departure Date")
    cleaning_co = fields.Char(string="Cleaning Company")
    poe = fields.Many2one('shipment.poe', string='Port of Entry')
    licenses = fields.Many2many("license.license",string="Related Licenses")

    

    """ Financial Details """
    admin_expenses = fields.Float(string="Administrative Expenses")
    admin_expenses_date = fields.Date(string="Administrative Expenses Date")
    tc_invoice_number = fields.Integer(string="TC Invoice Number")
    tc_invoice_date = fields.Date(string="TC Invoice Date")
    tc_invoice_value = fields.Integer(string="TC Invoice Value")
    percentage = fields.Float(string="Percentage")
    tax_paid = fields.Float(string="Tax Paid")
    customs_paid = fields.Float(string="Customs Paid")
    total = fields.Float(string="Total")
    total_percentage = fields.Float(string="Total Percentage")



    state=fields.Selection([("draft","Draft"),("upcoming","Upcoming"),("at airport now","At airpot now"),("arrived in w.h + paid inv.","Arrived in W.H. + paid inv."),("cancelled","Cancelled")],string="Status",default="draft",required=True)

    """ Shipment Line Items """
    
    shipment_line = fields.One2many("shipment.invoice","conn",string="Shipment Line Items")
    
    purchase_proxy = fields.Many2many(comodel_name="purchase.order",relation="proxy_purchase_rel",column1="pur_pro",cloumn2="pro_pur",string="Purchase Orders",related="shipment_line.rel_purchase_orders")



    






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
    rel_purchase_orders = fields.Many2many(comodel_name="purchase.order",relation="shipment_purchase_rel",column1="shipment_pur",column2="pur_shipment",string="Purchase Orders")
    rel_products = fields.Many2many(comodel_name="product.product",relation="shipment_product_rel",column1="shipment_pro",column2="pro_shipment",string="Related Products")
    warehouse_arr_dates = fields.Many2many(comodel_name="shipment.dates",relation="shipment_dates_rel",column1="shipment_dates",column2="dates_shipment",string="Warehouse Arrival Dates")



class ShipmentLineDates(models.Model):
    _name="shipment.dates"
    _rec_name = "date"
    date = fields.Date(string="Date")





class ShipmentPoe(models.Model):
    _name="shipment.poe"
    _rec_name="name"

    #conn=fields.Integer()
    name=fields.Char(string="Port of Entry")



