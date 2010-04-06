<html>
<head>
<title>Herald: pre-alpha</title>
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
	</div>
	<div class="span-18">
	<h2>Add new post, id:{{id}}</h2>
	<form action='/post/do' method='POST'>
	<span style="visibility:hidden"><input type='text' name='id' value='{{id}}' /></span>
	<b>Title:</b><input type='text' name='title' />
	<b>Content:</b><textarea name='content'></textarea>
	<b>Date:</b><input type='text' name='timestamp' value='{{timestamp}}' />
	<input type='submit' name='save' value='save' />
	</form>
	</div>
	<div class='span-6 last'>
		
	</div>
</div>
</body>
