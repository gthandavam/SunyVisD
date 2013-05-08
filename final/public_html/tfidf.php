<?php

$stemmer = new PorterStemmer();

$db_path = '/home/remy/Desktop/tfidf-d80-t2.5-indexed.db';
$db = new SQLite3($db_path, SQLITE3_OPEN_READONLY);

function stem3($word) {
	global $stemmer;
	return $stemmer->stem($stemmer->stem($stemmer->stem($word)));
}

function top10concepts($text) {
	global $db;
	$words = array_filter(array_map('stem3', preg_split('/\s+/', $text)));
	$concept_ids = array();
	$concepts = array();
	$sql = 'SELECT concept, SUM(tfidf) AS tfidfs FROM inverted_index AS ii JOIN concepts AS cs ON ii.concept_id = cs.id WHERE word_id IN (SELECT id FROM words WHERE word IN(';
	$sql .= implode(',', array_map(function ($w) { return "'$w'"; }, $words));
	$sql .= ')) GROUP BY concept_id ORDER BY tfidfs DESC LIMIT 10';
	$time_start = microtime(true);
	$result = $db->query($sql);
	$time_end = microtime(true);
	$query_time = $time_end - $time_start;
	$top10 = array();
	while ($row = $result->fetchArray()) {
		$concept = $row['concept'];
		$tfidfs = $row['tfidfs'];
		$top10[] = array($concept, $tfidfs);
	}
	return $top10;
}

function relatedness($text1, $text2) {
	return 3.141592653589;
}

?>
