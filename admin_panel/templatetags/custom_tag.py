from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# @register.simple_tag
# def pagination(request):

#     per_page = request.GET.get("per_page", "10")

#     html = f"""
#     <select name="per_page"
#             class="form-select form-select-sm"
#             style="width:120px"
#             onchange="window.location='?per_page='+this.value">

#         <option value="10" {'selected' if per_page=='10' else ''}>10</option>
#         <option value="25" {'selected' if per_page=='25' else ''}>25</option>
#         <option value="50" {'selected' if per_page=='50' else ''}>50</option>
#         <option value="100" {'selected' if per_page=='100' else ''}>100</option>

#     </select>
#     """

#     return mark_safe(html)

@register.simple_tag
def pagination(page_obj):
    html = """<select class="form-select form-select-sm" style="width:150px" onchange="window.location=this.value">"""
    for i in range(1, page_obj.paginator.num_pages + 1):
        selected = ""
        if i == page_obj.number:
            selected = "selected"
        html += f"""
        <option value="?page={i}" {selected}>
            Page {i}
        </option>
        """
    html += "</select>"
    return mark_safe(html)