<html>
<head>
<title>Herald: pre-alpha | {{title}}</title>
	<link rel="stylesheet" href="/static/css/style.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="/static/css/screen.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="/static/css/print.css" type="text/css" media="print">
	<link rel="stylesheet" href="/static/css/typography.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="/static/css/forms.css" type="text/css" media="screen, projection">
	<!--[if lt IE 8]>
		<link rel="stylesheet" href="/static/css/ie.css" type="text/css" media="screen, projection">
	<![endif]-->
</head>
<body>
<div class="container">
	<div class="span-24 last">
		<h1>Herald!</h1>
		<p>maxr: {{maxr}}</p>
	</div>
	<div class="span-18">
	% for post in posts:
		<p class='post'>{{post}}</p>
	% end
	</div>
	<div class="span-6 last">
		<h5>login</h5>
	</div>
	<div class="span-6 prepend-18 last">
	<h3>Menu</h3>
	% for item in menu:
		<p class='menu'>{{item}}</p>
	% end
	</div>
</div>
</body>
