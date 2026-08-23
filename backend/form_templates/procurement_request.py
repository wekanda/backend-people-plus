PROCUREMENT_REQUEST = {
    "name": "PROCUREMENT REQUEST FORM",
    "key": "procurement_request",
    "category": "Procurement & Stores",
    "description": "Procurement request form with itemised cost table.",
    "fields": [
        {"name": "prc_no", "label": "PRC No.", "type": "text", "required": False},
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "location", "label": "Location", "type": "text", "required": False, "default": "Head Office"},
        {"name": "project", "label": "Project", "type": "text", "required": False, "default": "Operations"},
        {"name": "budget_line", "label": "Budget Line", "type": "text", "required": False},
        {"name": "available_budget", "label": "Available Budget", "type": "number", "required": False},
        {"name": "item1_description", "label": "Item 1 Description", "type": "text", "required": False},
        {"name": "item1_qty", "label": "Item 1 Quantity", "type": "number", "required": False},
        {"name": "item1_unit", "label": "Item 1 Unit", "type": "text", "required": False},
        {"name": "item1_cost", "label": "Item 1 Estimated Cost", "type": "number", "required": False},
        {"name": "item2_description", "label": "Item 2 Description", "type": "text", "required": False},
        {"name": "item2_qty", "label": "Item 2 Quantity", "type": "number", "required": False},
        {"name": "item2_unit", "label": "Item 2 Unit", "type": "text", "required": False},
        {"name": "item2_cost", "label": "Item 2 Estimated Cost", "type": "number", "required": False},
        {"name": "item3_description", "label": "Item 3 Description", "type": "text", "required": False},
        {"name": "item3_qty", "label": "Item 3 Quantity", "type": "number", "required": False},
        {"name": "item3_unit", "label": "Item 3 Unit", "type": "text", "required": False},
        {"name": "item3_cost", "label": "Item 3 Estimated Cost", "type": "number", "required": False},
        {"name": "requested_by", "label": "Requested By", "type": "text", "required": True},
        {"name": "requested_designation", "label": "Requested By (Designation)", "type": "text", "required": False, "default": "Procurement Unit"},
        {"name": "reviewed_by", "label": "Reviewed By", "type": "text", "required": False},
        {"name": "reviewed_designation", "label": "Reviewed By (Designation)", "type": "text", "required": False, "default": "Accountant"},
        {"name": "approved_by", "label": "Approved By", "type": "text", "required": False},
        {"name": "approved_designation", "label": "Approved By (Designation)", "type": "text", "required": False, "default": "Ag. Head of Finance & Operations"},
    ],
    "template": """
<h1>PROCUREMENT REQUEST</h1>
<p><span class="bold">PRC No:</span> {h(prc_no, '........')}</p>
<table class="info">
<tr><td class="k"><span class="bold">Date:</span></td><td>{h(date)}</td>
    <td class="k"><span class="bold">Location:</span></td><td>{h(location)}</td></tr>
<tr><td class="k"><span class="bold">Project:</span></td><td>{h(project)}</td>
    <td class="k"><span class="bold">Budget line:</span></td><td>{h(budget_line)}</td></tr>
<tr><td class="k"><span class="bold">Available budget:</span></td><td>{hm(available_budget)}</td></tr>
</table>
<table class="bordered">
<tr><th style="width:8%"><span class="bold">ITEM NO</span></th><th><span class="bold">DESCRIPTION</span></th><th style="width:10%"><span class="bold">QUANTITY</span></th><th style="width:10%"><span class="bold">UNIT</span></th><th style="width:16%"><span class="bold">ESTIMATED COST</span></th></tr>
<tr><td>1.</td><td>{h(item1_description)}</td><td>{h(item1_qty)}</td><td>{h(item1_unit)}</td><td class="center">{hm(item1_cost)}</td></tr>
<tr><td>2.</td><td>{h(item2_description)}</td><td>{h(item2_qty)}</td><td>{h(item2_unit)}</td><td class="center">{hm(item2_cost)}</td></tr>
<tr><td>3.</td><td>{h(item3_description)}</td><td>{h(item3_qty)}</td><td>{h(item3_unit)}</td><td class="right"><span class="bold">{hm(item_total)}</span></td></tr>
</table>
<p class="spacer-sm"> </p>
<p><span class="bold">Requested by:</span> {h(requested_by)} &nbsp;<span class="bold">Signature:</span> {sign_dots} &nbsp;<span class="bold">Date:</span> {sign_dots}</p>
<p>{h(requested_designation)}</p>
<p class="spacer-sm"> </p>
<p><span class="bold">Reviewed by:</span> {h(reviewed_by)} &nbsp;<span class="bold">Signature:</span> {sign_dots} &nbsp;<span class="bold">Date:</span> {sign_dots}</p>
<p>{h(reviewed_designation)}</p>
<p class="spacer-sm"> </p>
<p><span class="bold">Approved by:</span> {h(approved_by)} &nbsp;<span class="bold">Signature:</span> {sign_dots} &nbsp;<span class="bold">Date:</span> {sign_dots}</p>
<p>{h(approved_designation)}</p>
""",
}