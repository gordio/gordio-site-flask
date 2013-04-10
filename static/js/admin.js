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
function init_title()
{
	var title = document.getElementById('title');

	title.onblur = function() {
		var slug = document.getElementById('slug');

		if (!slug.value) {
			slug.value = slugify(this.value);
		}
	}
}
