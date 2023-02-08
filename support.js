/* SUPPORT.txt HTML widget

Use inside <body>, like:
	
	<script async src="support.js" data-url="/path/to/SUPPORT.txt"></script>

This fetches and parses SUPPORT.txt, and adds the information to the page.  You can change how soon the "warning" symbol is displayed (default is less than 180 days):

	<script [...] data-warning-days="365"></script>

You can customise the display with a simple template:

	<div id="support-info">
		...
	</div>
	<script [...] data-template="support-info"></script>
	
If the element referenced by `data-template` is a <template>, the content is inserted before the <script>.
*/
(script => {
	/* Parses SUPPORT.txt into an object like:
		{
			maintainers: [
				{
					name: "...",
					email: "...@..." (or null),
					date: "YYYY-MM-DD",
					icon: "{emoji}"
				},
				...
			],
			sections: [
				{
					name: "section",
					maintainers: [... as above ...]
				},
				...
			],
			icon: "{emoji}"
		}
	*/
	function parseSupportTxt(text) {
		let support = {
			maintainers: [],
			sections: []
		};
		let current = support;

		text.split('\n').forEach(function (line) {
			line = line.replace(/#.*/, '').trim();
			if (line.endsWith(":")) {
				current = {
					name: line.substr(0, line.length - 1),
					maintainers: []
				};
				support.sections.push(current);
			} else if (/^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\s/.test(line)) {
				let name = line.substr(10).trim(), email = null;
				name = name.replace(/<.*>/, e => {
					email = e;
					return ''
				}).trim();
				current.maintainers.push({
					date: line.substr(0, 10),
					name: name,
					email: email
				});
			}
		});
		return support;
	}
	
	/* Simple display template.
		Use `data-name="key"` to recurse into a sub-object, or repeat the elements of a list.
		Use {{key}} to replace text or attribute values. */
	function fillTemplate(node, object, childrenOnly) {
		if (!childrenOnly && node.dataset && node.dataset.name) {
			let name = node.dataset.name;
			let value = (name == "") ? object : object[name];
			if (Array.isArray(value)) {
				let parent = node.parentNode;
				value.forEach(item => {
					let clone = node.cloneNode(true);
					fillTemplate(clone, item, true);
					parent.insertBefore(clone, node);
				});
				parent.removeChild(node);
			} else if (value != null) {
				fillTemplate(node, value, true);
			}
		} else {
			if (node.childNodes) {
				for (let i = node.childNodes.length - 1; i >= 0; --i) {
					fillTemplate(node.childNodes[i], object);
				}
			}
			if (typeof node.nodeValue == "string") {
				node.nodeValue = node.nodeValue.replace(/\{\{(.*?)\}\}/g, (m, name) => {
					let value = object[name];
					return (value != null) ? value : "";
				});
			}
			if (node.attributes) {
				for (let i = 0; i < node.attributes.length; ++i) {
					fillTemplate(node.attributes[i], object);
				}
			}
		}
	}

	let today = (new Date).toISOString().substr(0, 10);
	let soonDays = parseFloat(script.dataset.warningDays) || 180;
	let soon = (new Date(Date.now() + soonDays*86400000)).toISOString().substr(0, 10);

	fetch(script.dataset.url)
		.then(r => r.text())
		.then(parseSupportTxt)
		.then(support => {
			// give each maintainer an "icon" field
			function emojiForDate(date) {
				if (date < today) return "\u274C";
				if (date < soon) return "\u26A0\uFE0F";
				return "\u2705";
			}
			let earliest = soon;
			support.maintainers.forEach(m => {
				m.icon = emojiForDate(m.date);
				if (m.date < earliest) earliest = m.date;
			});
			support.icon = emojiForDate(earliest);
			support.sections.forEach(section => {
				section.maintainers.forEach(m => {
					m.icon = emojiForDate(m.date);
					if (earliest < today && m.date >= today) {
						support.icon = "\u26A0\uFE0F";
					}
				});
			});

			let template = document.getElementById(script.dataset.template) || document.querySelector("template#support");
			if (!template) { // default template
				template = document.createElement("details");
				template.innerHTML = `
					<summary>{{icon}} Support</summary>
					<ul>
						<li data-name="maintainers">
							{{icon}} {{date}} <strong>{{name}}</strong> {{email}}
						</li>
						<li data-name="sections">
							<strong>{{name}}:</strong>
							<ul>
								<li data-name="maintainers">
									{{icon}} {{date}} <strong>{{name}}</strong> {{email}}
								</li>
							</ul>
						</li>
					</ul>`;
				script.parentNode.insertBefore(template, script);
			}
			if (template.tagName == 'TEMPLATE' && template.content) {
				let clone = template.content.cloneNode(true);
				fillTemplate(clone, support);
				script.parentNode.insertBefore(clone, script);
			} else {
				fillTemplate(template, support);
			}
		})
		.catch(console.error);
})(document.currentScript);
