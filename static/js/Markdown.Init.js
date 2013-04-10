(function() {
	// When using more than one `textarea` on your page, change the following line to match the one you’re after
	var textarea = document.getElementsByTagName('textarea')[0];
	var preview = document.createElement('div');
	var convert = new Markdown.getSanitizingConverter().makeHtml;

	// Continue only if the `textarea` is found
	if (textarea) {
		preview.id = 'preview';
		// Insert the preview `div` after the `textarea`
		textarea.parentNode.insertBefore(preview, textarea.nextSibling);
		// instead of `onkeyup`, consider using `oninput` where available: http://mathiasbynens.be/notes/oninput
		textarea.onkeyup = function() {
			preview.innerHTML = convert(eTextarea.value);
		}
		// Trigger the `onkeyup` event
		textarea.onkeyup.call(eTextarea);
	}
}());
