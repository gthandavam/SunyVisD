<?php

$stemmer = new PorterStemmer();

$db_path = '/home/remy/Desktop/tfidf-d80-t1.75-indexed.db';
$db = new SQLite3($db_path, SQLITE3_OPEN_READONLY);

$query_time = 0;

function stem3($word) {
	global $stemmer;
	return $stemmer->stem($stemmer->stem($stemmer->stem($word)));
}

function top_concepts($text, $n = 10) {
	global $db, $query_time;
	$words = array_filter(array_map('stem3', preg_split('/\s+/', $text)));
	$concept_ids = array();
	$concepts = array();
	$sql = 'SELECT concept, SUM(tfidf) AS tfidfs FROM inverted_index AS ii JOIN concepts AS cs ON ii.concept_id = cs.id WHERE word_id IN (SELECT id FROM words WHERE word IN(';
	$sql .= implode(',', array_map(function ($w) { return "'$w'"; }, $words));
	$sql .= ')) GROUP BY concept_id ORDER BY tfidfs DESC LIMIT ' . $n;
	$time_start = microtime(true);
	$result = $db->query($sql);
	$time_end = microtime(true);
	$query_time = $time_end - $time_start;
	$top = array();
	while ($row = $result->fetchArray()) {
		$concept = $row['concept'];
		$tfidfs = $row['tfidfs'];
		$top[] = array($concept, $tfidfs);
	}
	return $top;
}

function relatedness($text1, $text2) {
	global $db, $query_time;
	$words1 = array_filter(array_map('stem3', preg_split('/\s+/', $text1)));
	$sql1 = 'SELECT concept_id, SUM(tfidf) AS tfidfs FROM inverted_index AS ii WHERE word_id IN (SELECT id FROM words WHERE word IN(';
	$sql1 .= implode(',', array_map(function ($w) { return "'$w'"; }, $words1));
	$sql1 .= ')) GROUP BY concept_id';
	$time_start = microtime(true);
	$result = $db->query($sql1);
	$time_end = microtime(true);
	$query_time = $time_end - $time_start;
	$vector1 = array();
	while ($row = $result->fetchArray()) {
		$concept_id = $row['concept_id'];
		$tfidfs = $row['tfidfs'];
		$vector1[$concept_id] = $tfidfs;
	}
	$words2 = array_filter(array_map('stem3', preg_split('/\s+/', $text2)));
	$sql2 = 'SELECT concept_id, SUM(tfidf) AS tfidfs FROM inverted_index AS ii WHERE word_id IN (SELECT id FROM words WHERE word IN(';
	$sql2 .= implode(',', array_map(function ($w) { return "'$w'"; }, $words2));
	$sql2 .= ')) GROUP BY concept_id';
	$time_start = microtime(true);
	$result = $db->query($sql2);
	$time_end = microtime(true);
	$query_time += $time_end - $time_start;
	$vector2 = array();
	while ($row = $result->fetchArray()) {
		$concept_id = $row['concept_id'];
		$tfidfs = $row['tfidfs'];
		$vector2[$concept_id] = $tfidfs;
	}
	$dot = 0;
	$mag1 = 0;
	$mag2 = 0;
	foreach ($vector1 as $concept_id => $tfidfs1) {
		$mag1 += $tfidfs1 * $tfidfs1;
		if (array_key_exists($concept_id, $vector2)) {
			$tfidfs2 = $vector2[$concept_id];
			$dot += $tfidfs1 * $tfidfs2;
			$mag2 += $tfidfs2 * $tfidfs2;
		}
	}
	foreach ($vector2 as $concept_id => $tfidfs2) {
		if (!array_key_exists($concept_id, $vector1)) {
			$mag2 += $tfidfs2 * $tfidfs2;
		}
	}
	$mag1 = sqrt($mag1);
	$mag2 = sqrt($mag2);
	return $dot / ($mag1 * $mag2);
}

?>
