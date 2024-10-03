// Avoid `console` errors in browsers that lack a console.


// Place any jQuery/helper plugins in here.
(function ($) {

	// Equal Height
	$.fn.equalHeight = function (options) {
		var maxHeight = 0;
		var defaults = {
			selector: $('.equalHeight')
		};
		options = $.extend(defaults, options);

		$(this).each(function () {
			$(this).find(defaults.selector).each(function () {
				if ($(this).height() > maxHeight) {
					maxHeight = $(this).height();
				}
			});
			$(this).find(defaults.selector).height(maxHeight);
		});

		return this;
	}

	// Equal Width
	$.fn.equalWidth = function (options) {
		var maxWidth = 0;
		var defaults = {
			selector: $('.equalWidth')
		};
		options = $.extend(defaults, options);

		$(this).each(function () {
			$(this).find(defaults.selector).each(function () {
				if ($(this).width() > maxWidth) {
					maxWidth = $(this).width();
				}
			});
			$(this).find(defaults.selector).width(maxWidth);
		});

		return this;
	}

	if ($(window).width() > 767) {
		$('.equalHeightWrapper').equalHeight({
			selector: $('.equalHeight')
		});
	}


	function Utils() {

	}

	Utils.prototype = {
		constructor: Utils,
		isElementInView: function (element, fullyInView) {
			var pageTop = $(window).scrollTop();
			var pageBottom = pageTop + $(window).height();
			var elementTop = $(element).offset().top;
			var elementBottom = elementTop + $(element).height();

			if (fullyInView === true) {
				return ((pageTop < elementTop) && (pageBottom > elementBottom));
			} else {
				return ((elementTop <= pageBottom) && (elementBottom >= pageTop));
			}
		}
	};

	var Utils = new Utils();

	function isIE() {
		var ua = navigator.userAgent;
		var is_ie = ua.indexOf("MSIE ") > -1 || ua.indexOf("Trident/") > -1;

		return is_ie;
	}

	isIE();

	if (isIE()) {
		cssVars({
			onlyLegacy: false,
			include: 'link[href="assets/css/style.css"],style',
			onComplete: function (cssText, styleNode) {}
		});
	}

	var _document = $(document);

	_document.on("contextmenu", function (e) {
		if (e.target.nodeName != "INPUT" && e.target.nodeName != "TEXTAREA")
			e.preventDefault();
	});

	

})(jQuery);