/* Transform text into a URL slug: spaces turned into dashes, remove non alnum */
function slugify(text)
{
	text = text
	.replace(/[^-a-zA-Z0-9\s]+/ig, '') // Remove all bad symbols
	.toLowerCase()
	.trim()
	.replace(/\s{2,}/g, ' ') // Remove double spaces
	.replace(/\s/gi, '-');   // Replace space with dashes
	return text;
}


/* Init form element: make slug for title, if slug is empty */
window.addEventListener('load', function() {
	var title = document.getElementById('title');
	if (title === 'null') {
		return;
	}

	var slug = document.getElementById('slug');
	slug.useredited = false;
	slug.onchange = function(e) {
		this.useredited = true;
		this.onchange = null;
	}

	title.onchange = function() {
		if (!slug.value) {
			slug.value = slugify(this.value);
		} else if (!slug.useredited) {
			slug.value = slugify(this.value);
		}
	}
});