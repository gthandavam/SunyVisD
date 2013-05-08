<?php

function top10concepts($text) {
	return array(
		array('Breed-specific legislation', 21.413992572402),
		array('Dog', 21.288740778337),
		array('Dingo', 20.071396561365),
		array('Dog meat', 19.276514333065),
		array('Australian Cattle Dog', 18.996457036782),
		array('Dog training', 18.823445019563),
		array('Dog health', 18.80728402844),
		array('Dog breed', 18.502844414966),
		array('Dogs in warfare', 18.358541557236),
		array('Greater Swiss Mountain Dog', 18.149876307073)
	);
}

function relatedness($text1, $text2) {
	return 3.141592653589;
}

// use SQLITE3_OPEN_READONLY
// http://www.php.net/manual/en/sqlite3.open.php

// 'SELECT concept, SUM(tfidf) AS tfidfs FROM inverted_index AS ii JOIN concepts AS cs ON ii.concept_id = cs.id WHERE word_id IN (SELECT id FROM words WHERE word IN(' .
// implode(', ', array_map(function ($w) { return "'" . SQLite3::escapeString($w) . "'"; }, $words)) .
// ')) GROUP BY concept_id ORDER BY tfidfs DESC LIMIT 10'

?>