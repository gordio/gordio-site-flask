window.addEventListener('load', function() {
        Hyphenator.config({
            'defaultlanguage': 'ru',
            'classname': 'page',
            'donthyphenateclassname': 'header',
            'intermediatestate': 'visible',
            'displaytogglebox': true,
            'minwordlength': 4,
            'useCSS3hyphenation': true
        });
        // Hyphenator.run();
        var blocks = document.getElementsByTagName('p');
        for (var i = 0; i < blocks.length; i++) {
            blocks[i].style.textAlign = 'justify';
            Hyphenator.hyphenate(blocks[i], 'ru');
        }
    }
);
