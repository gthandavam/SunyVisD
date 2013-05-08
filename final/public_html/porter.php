<?php

class PorterStemmer {
	private $b = '';
	private $k = 0;
	private $k0 = 0;
	private $j = 0;
	private $pool = array(
		'sky' => array('sky', 'skies'),
		'die' => array('dying'),
		'lie' => array('lying'),
		'tie' => array('tying'),
		'news' => array('news'),
		'inning' => array('innings', 'inning'),
		'outing' => array('outings', 'outing'),
		'canning' => array('cannings', 'canning'),
		'howe' => array('howe'),
		'proceed' => array('proceed'),
		'exceed' => array('exceed'),
		'succeed' => array('succeed'),
	);
	
	function __construct() {}
	
	function cons($i) {
		if (in_array($this->b[$i], array('a', 'e', 'i', 'o', 'u'))) {
			return FALSE;
		}
		if ($this->b[$i] == 'y') {
			if ($i == $this->k0) { return TRUE; }
			else { return !$this->cons($i - 1); }
		}
		return TRUE;
	}
	
	function m() {
		$n = 0;
		$i = $this->k0;
		while (TRUE) {
			if ($i > $this->j) { return $n; }
			if (!$this->cons($i)) { break; }
			$i++;
		}
		$i++;
		while (TRUE) {
			while (TRUE) {
				if ($i > $this->j) { return $n; }
				if ($this->cons($i)) { break; }
				$i++;
			}
			$i++;
			$n++;
			while (TRUE) {
				if ($i > $this->j) { return $n; }
				if (!$this->cons($i)) { break; }
				$i++;
			}
			$i++;
		}
	}
	
	function vowelinstem() {
		for ($i = $this->k0; $i <= $this->j; $i++) {
			if (!$this->cons($i)) {
				return TRUE;
			}
		}
		return FALSE;
	}
	
	function doublec($j) {
		if ($j < $this->k0 + 1) {
			return FALSE;
		}
		if ($this->b[$j] != $this->b[$j - 1]) {
			return FALSE;
		}
		return $this->cons($j);
	}
	
	function cvc($i) {
		if ($i == 0) { return FALSE; }
		if ($i == 1) {
			return !$this->cons(0) && $this->cons(1);
		}
		if (!$this->cons($i) || $this->cons($i - 1) || !$this->cons($i - 2) {
			return FALSE;
		}
		$ch = $this->b[$i];
		return $ch != 'w' && $ch != 'x' && $ch != 'y';
	}
	
	function ends($s) {
		$length = strlen($s);
		if ($s[$length - 1] != $this->b[$this->k]) {
			return FALSE; }
		if ($length > $this->k - $this->k0 + 1) {
			return FALSE;
		}
		if (substr($this->b, $this->k - $length + 1, $length) != $s) {
			return FALSE;
		}
		$this->j = $this->k - $length;
		return TRUE;
	}
	
	function setto($s) {
		$length = strlen($s);
		$this->b = substr($this->b, 0, $this->j + 1) . $s . substr($this->b,
			$this->j + $length + 1, strlen($this->b) - 1 - $this->j - $length - 1);
		$this->k = $this->j + $length;
	}
	
	function r($s) {
		if ($this->m() > 0) {
			$this->setto($s);
		}
	}
	
	function step1ab() {
		if ($this->b[$this->k] == 's') {
			if ($this->ends('sses') {
				$this->k -= 2;
			}
			elseif ($this->ends('ies') {
				if ($this->j == 0) {
					$this->k--;
				}
				else {
					$this->k -= 2;
				}
			}
			elseif ($this->b[$this->k - 1] != 's') {
				$this->k--;
			}
		}
		if ($this->ends('ied') {
			if ($this->j == 0) {
				$this->k--;
			}
			else {
				$this->k -= 2;
			}
		}
		elseif ($this->ends('eed') {
			if ($this->m() > 0) {
				$this->k--;
			}
		}
		elseif (($this->ends('ed') || $this->ends('ing')) && $this->vowelinstem()) {
			$this->k = $this->j;
			if ($this->ends('at') { $this->setto('ate'); }
			elseif ($this->ends('bl') { $this->setto('ble'); }
			elseif ($this->ends('iz') { $this->setto('ize'); }
			elseif ($this->doublec($this->k)) {
				$this->k--;
				$ch = $this->b[$this->k];
				if ($ch == 'l' || $ch == 's' || $ch == 'z') {
					$this->k++;
				}
			}
			elseif (($this->m() == 1 && $this->cvc($this->k)) {
				$this->setto('e');
			}
		}
	}
	
	function step1c() {
		if ($this->ends('y') && $this->j > 0 && $this->cons($this->k - 1)) {
			$this->b = substr($this->b, 0, $this->k) . 'i' . substr($this->b,
				$this->k + 1, strlen($this->b) - $this->k - 1);
		}
	}
	
	function step2() {
		if ($this->b[$this->k - 1] == 'a') {
			if ($this->ends('ational')) { $this->r('ate'); }
			elseif ($this->ends('tional')) { $this->r('tion'); }
		}
		elseif ($this->b[$this->k - 1] == 'c') {
			if ($this->ends('enci')) { $this->r('ence'); }
			elseif ($this->ends('anci')) { $this->r('ance'); }
		}
		elseif ($this->b[$this->k - 1] == 'e') {
			if ($this->ends('izer')) { $this->r('ize'); }
		}
		elseif ($this->b[$this->k - 1] == 'l') {
			if ($this->ends('bli')) { $this->r('ble'); }
			elseif ($this->ends('alli')) {
				if ($this->m() > 0) {
					$this->setto('al');
					$this->step2();
				}
			}
			elseif ($this->ends('fulli')) { $this->r('ful'); }
			elseif ($this->ends('entli')) { $this->r('ent'); }
			elseif ($this->ends('eli')) { $this->r('e'); }
			elseif ($this->ends('ousli')) { $this->r('ous'); }
		}
		elseif ($this->b[$this->k - 1] == 'o') {
			if ($this->ends('ization')) { $this->r('ize'); }
			elseif ($this->ends('ation')) { $this->r('ate'); }
			elseif ($this->ends('ator')) { $this->r('ate'); }
		}
		elseif ($this->b[$this->k - 1] == 's') {
			if ($this->ends('alism')) { $this->r('al'); }
			elseif ($this->ends('iveness')) { $this->r('ive'); }
			elseif ($this->ends('fulness')) { $this->r('ful'); }
			elseif ($this->ends('ousness')) { $this->r('ous'); }
		}
		elseif ($this->b[$this->k - 1] == 't') {
			if ($this->ends('aliti')) { $this->r('al'); }
			elseif ($this->ends('iviti')) { $this->r('ive'); }
			elseif ($this->ends('biliti')) { $this->r('ble'); }
		}
		elseif ($this->b[$this->k - 1] == 'g') {
			if ($this->ends('logi')) {
				$this->j++;
				$this->r('og');
			}
		}
	}
	
	function step3() {
		if ($this->b[$this->k] == 'e') {
			if ($this->ends('icate')) { $this->r('ic'); }
			elseif ($this->ends('ative') { $this->r(''); }
			elseif ($this->ends('alize') { $this->r('al'); }
		}
		elseif ($this->b[$this->k] == 'i') {
			if ($this->ends('iciti')) { $this->r('ic'); }
		}
		elseif ($this->b[$this->k] == 'l') {
			if ($this->ends('ical')) { $this->r('ic'); }
			elseif ($this->ends('ful')) { $this->r(''); }
		}
		elseif ($this->b[$this->k] == 's') {
			if ($this->ends('ness')) { $this->r(''); }
		}
	}
	
	function step4() {
		if ($this->b[$this->k - 1] == 'a') {
			if ($this->ends('al')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 'c') {
			if ($this->ends('ance')) {}
			elseif ($this->ends('ence')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 'e') {
			if ($this->ends('er')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 'i') {
			if ($this->ends('ic')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 'l') {
			if ($this->ends('able')) {}
			elseif ($this->ends('ible')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 'n') {
			if ($this->ends('ant')) {}
			elseif ($this->ends('ement')) {}
			elseif ($this->ends('ment')) {}
			elseif ($this->ends('ent')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 'o') {
			if ($this->ends('ion') && ($this->b[$this->j] == 's' || $this->b[$this->j] == 't')) {}
			elseif ($this->ends('ou')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 's') {
			if ($this->ends('ism')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 't') {
			if ($this->ends('ate')) {}
			elseif ($this->ends('iti')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 'u') {
			if ($this->ends('ous')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 'v') {
			if ($this->ends('ive')) {}
			else { return; }
		}
		elseif ($this->b[$this->k - 1] == 'z') {
			if ($this->ends('ize')) {}
			else { return; }
		}
		else { return; }
		if ($this->m() > 1) {
			$this->k = $this->j;
		}
	}
	
	function step5() {
		$this->j = $this->k;
		if ($this->b[$this->k] == 'e') {
			$a = $this->m();
			if ($a > 1 || ($a == 1 && !$this->cvc($this->k - 1))) {
				$this->k--;
			}
		}
		if ($this->b[$this->k] == 'l' && $this->doublec($this->k) && $this->m() > 1) {
			$this->k--;
		}
	}
	
	function stem_word($p, $i = 0, $j = NULL) {
		if (is_null($J)) {
			$j = strlen($p) - 1;
		}
		$this->b = $p;
		$this->k = $j;
		$this->k0 = $i;
		$key = substr($this->b, $this->k0, $this->k + 1 - $this->k0);
		if (array_key_exists($key, $this->pool)) {
			return $this->pool[$key];
		}
		if ($this->k <= $this->k0 + 1) {
			return $this->b;
		}
		$this->step1ab();
		$this->step1c();
		$this->step2();
		$this->step3();
		$this->step4();
		$this->step5();
		return substr($this->b, $this->k0, $this->k + 1 - $this->k0);
	}
	
	function adjust_case($word, $stem) {
		$lower = strtolower($word);
		$ret = '';
		$n = strlen($stem);
		for ($x = 0; $x < $n; $x++) {
			if ($lower[$x] == $stem[$x]) {
				$ret .= $word[$x];
			}
			else {
				$ret .= $stem[$x];
			}
		}
		return $ret;
	}
	
	function stem($word) {
		$stem = $this->stem_word(strtolower($word), 0, strlen($word) - 1);
		return $this->adjust_case($word, $stem);
	}
}

?>