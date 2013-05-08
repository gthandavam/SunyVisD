<?php

error_reporting(E_ALL | E_STRICT);
ini_set('display_errors', TRUE);
set_time_limit(600);

require_once 'porter.php';
require_once 'tfidf.php';

$error = NULL;
$top = NULL;
$top_n = 10;
$similarity = NULL;

if (array_key_exists('action', $_POST) && $_POST['action'] == 'Submit') {
	$text1 = trim(preg_replace('/[^A-Za-z0-9 ]/', '', $_POST['text1']));
	$text2 = trim(preg_replace('/[^A-Za-z0-9 ]/', '', $_POST['text2']));
	if (empty($text1)) {
		$error = 'Please enter a word or phrase!';
	}
	elseif (empty($text2)) {
		$top_n = intval($_POST['topn']);
		if ($top_n <= 0) { $top_n = 10; }
		$top = top_concepts($text1, $top_n);
	}
	else {
		$similarity = relatedness($text1, $text2);
	}
}

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
<?php if (!is_null($error)): ?>
<p class="error"><?=htmlentities($error) ?></p>
<?php elseif (!is_null($top)): ?>
<p class="success">The top <strong><?=$top_n ?></strong> closest related concepts to <strong>&ldquo;<?=htmlentities($text1) ?>&rdquo;</strong> are:</p>
<ol>
<?php foreach ($top as $pair): ?>
<?php list($concept, $tfidf) = $pair; ?>
<li class="success"><strong><a href="https://en.wikipedia.org/wiki/<?=htmlentities($concept) ?>"><?=htmlentities($concept) ?></a></strong> <em>(TF-IDF score = <?=$tfidf ?>)</em></li>
<?php endforeach; ?>
</ol>
<?php elseif (!is_null($similarity)): ?>
<p class="success">The semantic relatedness of <strong>&ldquo;<?=htmlentities($text1) ?>&rdquo;</strong> and <strong>&ldquo;<?=htmlentities($text2) ?>&rdquo;</strong> is <strong><?=$similarity ?></strong>.</p>
<?php endif; ?>
<?php if (!is_null($top) || !is_null($similarity)): ?>
<p class="success"><em>Total query time: <?=$query_time ?>s</em></p>
<?php endif; ?>
<form id="tfidf" action="<?=htmlentities($_SERVER['PHP_SELF']) ?>" method="post">
<p>Enter a single word or phrase to find its closest <select id="topn" name="topn">
	<option value="1">1</option>
	<option value="5">5</option>
	<option value="10" selected="selected">10</option>
	<option value="20">20</option>
	<option value="50">50</option>
</select> Wikipedia concepts.</p>
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
