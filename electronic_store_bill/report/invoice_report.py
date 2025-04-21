from odoo import models
from datetime import datetime
import pytz


class ClassInvoiceXlsx(models.AbstractModel):
    _name = 'report.booking_custom.report_commission_worksheet_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, commission):
        emp_header_no_border = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bold': 1})
        emp_header_no_border.set_font_name('Times New Roman')
        emp_header = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': 1})
        emp_header.set_font_name('Times New Roman')
        c_text = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        c_text.set_font_name('Times New Roman')
        l_text = workbook.add_format({'align': 'left', 'valign': 'vcenter'})
        l_text.set_font_name('Times New Roman')
        for obj in commission:

            sheet = workbook.add_worksheet(
                'Hoa hồng %s' % obj.name.replace('/', '.'))

            row = 0
            sheet.merge_range('A1:I1', 'Danh sách hoa hồng trong %s' %
                              obj.name, emp_header_no_border)
            sheet.merge_range('A3:B3', 'Tên: %s' %
                              obj.commission_user_id.name)
            sheet.merge_range('C3:D3', 'Tổng tiền: %s' %
                              obj.amount)
            sheet.merge_range('E3:F3', 'Đơn vị: %s' %
                              obj.currency_id.name)
            sheet.set_column("A:A", 10)
            sheet.set_column("B:B", 15)
            sheet.set_column("C:C", 25)
            sheet.set_column("D:D", 20)
            sheet.set_column("E:E", 20)
            sheet.set_column("F:F", 20)
            sheet.set_column("G:G", 15)
            sheet.set_column("H:H", 35)
            row += 5
            sheet.write(row, 0, 'Mã', emp_header)
            sheet.write(row, 1, 'Hợp đồng phương tiện', emp_header)
            sheet.write(row, 2, 'Số tiền', emp_header)
            sheet.write(row, 3, 'Đơn vị', emp_header)
            sheet.write(row, 4, 'Trạng thái', emp_header)
            sheet.write(row, 5, 'Đội bán hàng', emp_header)
            sheet.write(row, 6, 'Tài liệu nguồn', emp_header)
            sheet.write(row, 7, 'Ngày tạo', emp_header)
            row += 1
            i = 1
            for commission_line in obj.sales_commission_line:
                user_tz = self.env.user.tz
                to_usertz = pytz.timezone(user_tz) or pytz.utc
                if commission_line.date:
                    start_date_local = commission_line.date.astimezone(
                        to_usertz)
                    start_date_str = start_date_local.strftime(
                        "%m/%d/%Y, %H:%M:%S")
                sheet.write(row, 0, commission_line.name, l_text)
                sheet.write(
                    row, 1, commission_line.vehicle_contract_id.reference_no, l_text)
                sheet.write(row, 2, commission_line.amount, l_text)
                sheet.write(row, 3, commission_line.currency_id.name, l_text)
                sheet.write(row, 4, commission_line.state, l_text)
                sheet.write(row, 5, commission_line.sales_team_id.name, l_text)
                sheet.write(row, 6, commission_line.origin, l_text)
                sheet.write(row, 7, start_date_str, l_text)
                row += 1
                i += 1
