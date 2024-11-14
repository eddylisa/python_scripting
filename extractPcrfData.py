

import csv
import xml.etree.ElementTree as ET
import re
import sys

def extract_to_csv(xml_file_path, csv_file_name):
    with open(xml_file_path, 'r') as xml_file:
        xml_content = xml_file.read()

    if not re.match(r'^\s*<\s*\w+.*?>.*?</\s*\w+\s*>', xml_content):
        xml_content = f'<root>{xml_content}</root>'

    root = ET.fromstring(xml_content)

    headers = ["BillingDay", "IMSI", "Custom2","Custom3", "Custom1", "Custom8", "TotalVolume", "QuotaName", "MSISDN", "CID"]

    with open(csv_file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

        num_extracted_lines=0

        for record in root:
            billing_day = ""
            imsi = ""
            custom2 = ""
            custom3 = ""
            custom1 = ""
            custom8 = ""
            total_volume = ""
            quota_name = ""
            msisdn = ""
            cid = ""

            billing_day_element = record.find(".//field[@name='BillingDay']")
            if billing_day_element is not None:
                billing_day = billing_day_element.text

            imsi_element = record.find(".//field[@name='IMSI']")
            if imsi_element is not None:
                imsi = imsi_element.text

            custom2_element = record.find(".//field[@name='Custom2']")
            if custom2_element is not None:
                custom2 = custom2_element.text

            custom3_element = record.find(".//field[@name='Custom3']")
            if custom3_element is not None:
                custom3 = custom3_element.text

            custom1_element = record.find(".//field[@name='Custom1']")
            if custom1_element is not None:
                custom1 = custom1_element.text

            custom8_element = record.find(".//field[@name='Custom8']")
            if custom8_element is not None:
                custom8 = custom8_element.text

            total_volume_element = record.find(".//totalVolume")
            if total_volume_element is not None:
                total_volume = total_volume_element.text

            quota_name_element = record.find(".//quota[@name]")
            if quota_name_element is not None:
                quota_name = quota_name_element.get("name")

            msisdn_element = record.find(".//field[@name='MSISDN']")
            if msisdn_element is not None:
                msisdn = msisdn_element.text

            cid_element = record.find(".//quota[@cid]")
            if cid_element is not None:
                cid = cid_element.text

            row_data = [billing_day, imsi, custom2,custom3, custom1, custom8, total_volume, quota_name, msisdn, cid]
            writer.writerow(row_data)

            num_extracted_lines += 1  
        print(f"\nNumber of lines extracted : {num_extracted_lines}\n")

if __name__ == '__main__':
    try:
        file_path = input("Enter the path of the XML file: ")
        csv_name = input("Enter the desired CSV file name: ")
    except IndexError:
        sys.exit("Two arguments are required: XML path and save file name.")
        
    
    extract_to_csv(file_path, csv_name)
   

# ===============================================================
# import csv
# import xml.etree.ElementTree as ET
# import re
# import sys

# def prefix_large_numbers(value):
#     """Prefix the value with a single quote if it is a large number."""
#     if value and value.isdigit() and len(value) > 10:  # Assuming large numbers have more than 10 digits
#         return f"'{value}"
#     return value

# def extract_to_csv(xml_file_path, csv_file_name):
#     with open(xml_file_path, 'r') as xml_file:
#         xml_content = xml_file.read()

#     # Wrap the content in a root tag if it's not wrapped
#     if not re.match(r'^\s*<\s*\w+.*?>.*?</\s*\w+\s*>', xml_content):
#         xml_content = f'<root>{xml_content}</root>'

#     root = ET.fromstring(xml_content)

#     headers = ["BillingDay", "IMSI", "Custom2", "Custom3", "Custom1", "Custom8", "TotalVolume", "QuotaName", "MSISDN", "CID"]

#     with open(csv_file_name, 'w', newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerow(headers)

#         num_extracted_lines = 0

#         for record in root:
#             billing_day = ""
#             imsi = ""
#             custom2 = ""
#             custom3 = ""
#             custom1 = ""
#             custom8 = ""
#             total_volume = ""
#             quota_name = ""
#             msisdn = ""
#             cid = ""

#             billing_day_element = record.find(".//field[@name='BillingDay']")
#             if billing_day_element is not None:
#                 billing_day = billing_day_element.text

#             imsi_element = record.find(".//field[@name='IMSI']")
#             if imsi_element is not None:
#                 imsi = imsi_element.text

#             custom2_element = record.find(".//field[@name='Custom2']")
#             if custom2_element is not None:
#                 custom2 = custom2_element.text

#             custom3_element = record.find(".//field[@name='Custom3']")
#             if custom3_element is not None:
#                 custom3 = custom3_element.text

#             custom1_element = record.find(".//field[@name='Custom1']")
#             if custom1_element is not None:
#                 custom1 = custom1_element.text

#             custom8_element = record.find(".//field[@name='Custom8']")
#             if custom8_element is not None:
#                 custom8 = custom8_element.text

#             total_volume_element = record.find(".//totalVolume")
#             if total_volume_element is not None:
#                 total_volume = total_volume_element.text

#             quota_name_element = record.find(".//quota[@name]")
#             if quota_name_element is not None:
#                 quota_name = quota_name_element.get("name")

#             msisdn_element = record.find(".//field[@name='MSISDN']")
#             if msisdn_element is not None:
#                 msisdn = msisdn_element.text

#             cid_element = record.find(".//quota[@cid]")
#             if cid_element is not None:
#                 cid = cid_element.text

#             # Process row data, prefixing large numbers with a single quote
#             row_data = [
#                 prefix_large_numbers(billing_day),
#                 prefix_large_numbers(imsi),
#                 prefix_large_numbers(custom2),
#                 prefix_large_numbers(custom3),
#                 prefix_large_numbers(custom1),
#                 prefix_large_numbers(custom8),
#                 prefix_large_numbers(total_volume),
#                 prefix_large_numbers(quota_name),
#                 prefix_large_numbers(msisdn),
#                 prefix_large_numbers(cid)
#             ]

#             writer.writerow(row_data)
#             num_extracted_lines += 1  
        
#         print(f"\nNumber of lines extracted: {num_extracted_lines}\n")

# if __name__ == '__main__':
#     try:
#         file_path = input("Enter the path of the XML file: ")
#         csv_name = input("Enter the desired CSV file name: ")
#     except IndexError:
#         sys.exit("Two arguments are required: XML path and save file name.")
        
#     extract_to_csv(file_path, csv_name)






