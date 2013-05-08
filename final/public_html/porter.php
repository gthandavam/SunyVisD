<?php

class PorterStemmer {
	private $b = "";
	private $k = 0;
	private $k0 = 0;
	private $j = 0;
	private $pool = array(
		"sky" => array("sky", "skies"),
		"die" => array("dying"),
		"lie" => array("lying"),
		"tie" => array("tying"),
		"news" => array("news"),
		"inning" => array("innings", "inning"),
		"outing" => array("outings", "outing"),
		"canning" => array("cannings", "canning"),
		"howe" => array("howe"),
		"proceed" => array("proceed"),
		"exceed" => array("exceed"),
		"succeed" => array("succeed"),
	);
	
	function __construct() {}
	
	function cons($i) {
		if (in_array($this->b[$i], array('a', 'e', 'i', 'o', 'u'))) {
			return FALSE;
		}
		if ($this->b[$i] == 'y') {
			if ($i == $this->k0) {
				return TRUE;
			}
			else {
				return !$this->cons($i - 1);
			}
		}
		return TRUE;
	}
	
	function m() {
		$n = 0;
		$i = $this->k0;
		while (TRUE) {
			if ($i > $this->j) {
				return $n;
			}
			if (!$this->cons($i)) {
				break;
			}
			$i++;
		}
		$i++;
		while (TRUE) {
			while (TRUE) {
				if ($i > $this->j) {
					return $n;
				}
				if ($this->cons($i)) {
					break;
				}
				$i++;
			}
			$i++;
			$n++;
			while (TRUE) {
				if ($i > $this->j) {
					return $n;
				}
				if (!$this->cons($i)) {
					break;
				}
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
		if ($i == 1) { return !$this->cons(0) && $this->cons(1); }
		if (!$this->cons($i) || $this->cons($i - 1) || !$this->cons($i - 2) { return FALSE; }
		$ch = $this->b[$i];
		return !in_array($ch, array('w', 'x', 'y'));
	}
	
	function ends($s) {
		$length = strlen($s);
		if ($s[$length - 1] != $this->b[$this->k]) {
			return FALSE;
		}
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
		$this->b = substr($this->b, 0, $this->j + 1) . $s . $this->b[$this->j+$length+1:-1] ####
		$this->k = $this->j + $length;
	}
	
	function r($s) {
        """r(s) is used further down."""
        if self.m() > 0:
            self.setto(s)
}

?>