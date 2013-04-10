// Automatic load scripts from link objects
// Example usage:
// <link type="text/javascript" href="js/core.js" onload="core.init();">
// <script async src="js/loader.js"></script>

function load(url, callback) {
	var req = new XMLHttpRequest();
	req.open('get', url, true);

	req.onreadystatechange = function() {
		if(req.readyState === 4 && req.status === 200) {
			var se = document.createElement('script');
			se.async = true;
			document.getElementsByTagName('head')[0].appendChild(se);
			se.text = req.responseText;
			return callback();
		}
	}
	req.send();
}


(function() {
	var s = document.getElementsByTagName('link');
	for (var i = 0; i < s.length; i++) with({i: i}) {
		// Load type="text/javascript" or if href ended with .js
		if (s[i].getAttribute("type") == "text/javascript" || /\.js$/.test(s[i].href)) {
			load(s[i].href, function() {eval(s[i].getAttribute("onload"))});
		}
	}
})();
