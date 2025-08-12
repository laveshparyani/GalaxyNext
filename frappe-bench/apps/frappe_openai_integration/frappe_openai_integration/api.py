from openai import OpenAI
import frappe
from frappe import _
from frappe.utils import now


def get_openai_settings():
    """
    Fetch OpenAI settings.
    """
    return frappe.get_single("OpenAI Integration Settings")


def get_openai_response(prompt):
    try:
        settings = get_openai_settings()
        client = OpenAI(api_key=settings.api_key)
        response = client.chat.completions.create(
            model=settings.model, messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("OpenAI API Error"))
        return _("Sorry, I could not process your request at this time.")


@frappe.whitelist()
def ask_openai(prompt):
    answer = get_openai_response(prompt)
    return answer


@frappe.whitelist()
def save_chat_message(prompt, response):
    # Save the conversation linked with the logged in user
    doc = frappe.get_doc(
        {
            "doctype": "OpenAI Prompt Log",
            "user": frappe.session.user,
            "timestamp": now(),
            "prompt_message": prompt,
            "response_message": response,
        }
    )
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return True


@frappe.whitelist()
def get_chat_history():
    # Fetch saved chat messages for current user
    chats = frappe.get_all(
        "OpenAI Prompt Log",
        filters={"user": frappe.session.user},
        fields=["name", "prompt_message", "response_message", "timestamp"],
        order_by="creation asc",
        limit_page_length=10,
    )
    return chats


@frappe.whitelist()
def clear_chat_history():
    chats = frappe.get_all(
        "OpenAI Prompt Log", filters={"user": frappe.session.user}, fields=["name"]
    )
    for chat in chats:
        frappe.delete_doc("OpenAI Prompt Log", chat.name, force=True)
    return "success"
