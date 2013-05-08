<?php

require_once 'porter.php';

?>

<!DOCTYPE html>

<html>

<head>
<meta charset="UTF-8">
<title>CSE 507: Explicit Semantic Analysis</title>
<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Droid+Sans:400,700">
<link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>

<div id="header">
<div class="central">
<h1>Explicit Semantic Analysis</h1>
</div>
</div>

<div id="content">
<div class="central">
<form id="tfidf" action="<?=htmlentities($_SERVER['PHP_SELF']) ?>" method="post">
<p>Enter a single word or phrase to find its closest 10 Wikipedia concepts.</p>
<p><input id="text1" name="text1" type="text" size="40"></p>
<p>Enter two to calculate their semantic relatedness based on their concept vectors.</p>
<p><input id="text2" name="text2" type="text" size="40"></p>
<p><input id="action" name="action" type="submit" value="Submit"></p>
</form>
</div>
</div>

<div id="footer">
<div class="central">
<p>Remy Oukaour, Ganesa Thandavam, Omar Khazamov<br>
CSE 507, Stony Brook University</p>
</div>
</div>

</body>

</html>
