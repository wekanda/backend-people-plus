STORES_REQUISITION = {
    "name": "STORES REQUISITION FORM",
    "key": "stores_requisition",
    "category": "Procurement & Stores",
    "description": "Stores/issues requisition request and approval workflow.",
    "fields": [
        {"name": "requisition_no", "label": "Requisition No.", "type": "text", "required": False},
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "department", "label": "Department", "type": "text", "required": True},
        {"name": "location", "label": "Location", "type": "text", "required": False},
        {"name": "category", "label": "Category", "type": "select",
         "options": ["Office Supplies", "Stationery", "Equipment", "Furniture", "PPE", "Medical Supplies", "Other"],
         "required": False},
        {"name": "item1_description", "label": "Item 1 Description", "type": "text", "required": False},
        {"name": "item1_qty", "label": "Item 1 Quantity", "type": "number", "required": False},
        {"name": "item1_unit", "label": "Item 1 Unit", "type": "text", "required": False},
        {"name": "item1_remarks", "label": "Item 1 Remarks", "type": "text", "required": False},
        {"name": "item2_description", "label": "Item 2 Description", "type": "text", "required": False},
        {"name": "item2_qty", "label": "Item 2 Quantity", "type": "number", "required": False},
        {"name": "item2_unit", "label": "Item 2 Unit", "type": "text", "required": False},
        {"name": "item2_remarks", "label": "Item 2 Remarks", "type": "text", "required": False},
        {"name": "item3_description", "label": "Item 3 Description", "type": "text", "required": False},
        {"name": "item3_qty", "label": "Item 3 Quantity", "type": "number", "required": False},
        {"name": "item3_unit", "label": "Item 3 Unit", "type": "text", "required": False},
        {"name": "item3_remarks", "label": "Item 3 Remarks", "type": "text", "required": False},
        {"name": "requested_by", "label": "Requested By", "type": "text", "required": True},
        {"name": "requested_designation", "label": "Requester Designation", "type": "text", "required": False},
        {"name": "approved_by", "label": "Approved By", "type": "text", "required": False},
        {"name": "approved_designation", "label": "Approver Designation", "type": "text", "required": False, "default": "Head of Operations"},
        {"name": "issued_by", "label": "Issued By", "type": "text", "required": False},
        {"name": "received_by", "label": "Received By", "type": "text", "required": False},
    ],
    "template": """
<h1>STORES REQUISITION</h1>
<table class="info">
<tr><td class="k">Requisition No.</td><td>{h(requisition_no)}</td><td class="k">Date</td><td>{h(date)}</td></tr>
<tr><td class="k">Department</td><td>{h(department)}</td><td class="k">Location</td><td>{h(location)}</td></tr>
<tr><td class="k">Category</td><td>{h(category)}</td></tr>
</table>
<table class="bordered">
<tr><th>#</th><th>Item Description</th><th style="width:10%">Quantity</th><th style="width:10%">Unit</th><th>Remarks</th></tr>
<tr><td>1</td><td>{h(item1_description)}</td><td>{h(item1_qty)}</td><td>{h(item1_unit)}</td><td>{h(item1_remarks)}</td></tr>
<tr><td>2</td><td>{h(item2_description)}</td><td>{h(item2_qty)}</td><td>{h(item2_unit)}</td><td>{h(item2_remarks)}</td></tr>
<tr><td>3</td><td>{h(item3_description)}</td><td>{h(item3_qty)}</td><td>{h(item3_unit)}</td><td>{h(item3_remarks)}</td></tr>
</table>
<div class="spacer-sm"></div>
<p><span class="bold">Requested by:</span> {h(requested_by)} ({h(requested_designation)}) &nbsp;<span class="bold">Signature:</span> {sign_dots} &nbsp;<span class="bold">Date:</span> {sign_dots}</p>
<p class="spacer-sm"> </p>
<p><span class="bold">Approved by:</span> {h(approved_by)} ({h(approved_designation)}) &nbsp;<span class="bold">Signature:</span> {sign_dots} &nbsp;<span class="bold">Date:</span> {sign_dots}</p>
<p class="spacer-sm"> </p>
<p><span class="bold">Issued by (Stores):</span> {h(issued_by)} &nbsp;<span class="bold">Signature:</span> {sign_dots} &nbsp;<span class="bold">Date:</span> {sign_dots}</p>
<p><span class="bold">Received by:</span> {h(received_by)} &nbsp;<span class="bold">Signature:</span> {sign_dots} &nbsp;<span class="bold">Date:</span> {sign_dots}</p>
""",
}