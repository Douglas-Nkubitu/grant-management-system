from __future__ import unicode_literals
import frappe
from frappe.utils.data import cint

def get_context(context):
    context.gms_settings = frappe.get_single("Grant Management Settings")
    if not context.gms_settings.enable_gms_portal:
        frappe.local.flags.redirect_location = '/'
        raise frappe.Redirect

    page = frappe.form_dict.page
    pagination = paginate('Grant Call', page)
    context.active_grant_list = pagination.get('active_grant_list')
    context.prev = pagination.get('prev')
    context.next = pagination.get('next')
    context.no_cache = 1
   
def paginate(doctype, page=0):
    page_length = cint(frappe.db.get_single_value('Grant Management Settings', 'grant_call_per_page'))or 20
    prev, next = 0, 0
    date = frappe.utils.nowdate()
    query = f"""SELECT * FROM `tab{doctype}` WHERE docstatus = 1 AND published = 1 AND closing_date >= '{date}'  ORDER BY modified DESC """
       

    if(page):
        page = int(page)
        active_grant_list = frappe.db.sql(query+f"""LIMIT {(page*page_length)-page_length}, {page_length};""", as_dict=True)
        next_set = frappe.db.sql(query+f"""LIMIT {page*page_length}, {page_length};""", as_dict=True)
        if(next_set):
            prev, next = page-1, page+1
        else:
            prev, next = page-1, 0
    else:
        count = frappe.db.sql(f"""SELECT COUNT(name) as count FROM `tab{doctype}` WHERE docstatus = 1 AND published = 1 AND closing_date >= '{date}';""", as_dict=True)[0].count
        if(count > page_length):
            prev, next = 0, 2
        else:
            pass
        active_grant_list = frappe.db.sql(query+f"""LIMIT {page_length};""", as_dict=True)
    return {
        'active_grant_list': active_grant_list,
        'prev': prev,
        'next': next,
    }
