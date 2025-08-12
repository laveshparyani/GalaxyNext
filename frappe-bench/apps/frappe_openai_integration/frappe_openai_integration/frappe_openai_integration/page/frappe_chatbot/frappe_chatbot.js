frappe.pages['frappe-chatbot'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Frappe Chat Assistant',
		single_column: true
	});

	frappe.require('/assets/frappe_openai_integration/css/chatbot.css');

	// Add full-width classes
	let chat_area = $('<div>', { id: 'chat-area', class: 'chat-area' }).appendTo(page.main);
	let input_wrapper = $('<div>', { class: 'input-wrapper' }).appendTo(page.main);

	let input = $('<input>', {
		type: 'text',
		placeholder: 'Type your message...',
		class: 'chat-input'
	}).appendTo(input_wrapper);

	let send_btn = $('<button>', {
		text: 'Send',
		class: 'send-btn'
	}).appendTo(input_wrapper);

	let clear_btn = $('<button>', {
		text: 'Clear Chat History',
		class: 'clear-btn'
	}).appendTo(input_wrapper);

	// Load chat history
	load_chat_history();

	function load_chat_history() {
		frappe.call({
			method: "frappe_openai_integration.api.get_chat_history",
			callback: function(r) {
				if (r.message) {
					chat_area.empty();
					r.message.forEach(chat => {
						add_message(chat.prompt_message, 'user');
						add_message(chat.response_message, 'bot');
					});
				}
			}
		});
	}

	// Send on button or Enter
	send_btn.on('click', send_message);
	input.on('keypress', function(e) {
		if (e.which === 13) send_message();
	});

	function add_message(content, sender = 'user') {
		const wrapper = $('<div>', { class: `msg-wrapper ${sender}` });
		const avatar = $('<div>', { class: 'avatar' }).html(sender === 'user' ? '🧑' : '🤖');
		const bubble = $('<div>', {
			class: `chat-bubble ${sender}`,
			text: content
		});

		sender === 'user' ? wrapper.append(bubble).append(avatar) : wrapper.append(avatar).append(bubble);

		chat_area.append(wrapper);
		chat_area.scrollTop(chat_area[0].scrollHeight);
	}

	function send_message() {
		const val = input.val().trim();
		if (!val) return;
		add_message(val, 'user');
		input.val('');

		// Typing indicator
		let typing = $('<div>', { class: 'typing-indicator', text: '🤖 is typing...' }).appendTo(chat_area);
		chat_area.scrollTop(chat_area[0].scrollHeight);

		frappe.call({
			method: "frappe_openai_integration.api.ask_openai",
			args: { prompt: val },
			callback: function(r) {
				typing.remove();
				if (r.message) {
					add_message(r.message, 'bot');
					save_chat(val, r.message);
				}
			}
		});
	}

	function save_chat(prompt, response) {
		frappe.call({
			method: "frappe_openai_integration.api.save_chat_message",
			args: { prompt, response }
		});
	}

	clear_btn.on('click', function () {
		frappe.confirm('Are you sure you want to clear the chat history?', () => {
		frappe.call({
			method: "frappe_openai_integration.api.clear_chat_history",
			callback: function (r) {
			if (r.message === "success") {
				chat_area.empty();
				frappe.msgprint("Chat history cleared!");
			}
			}
		});
		});
	});

};