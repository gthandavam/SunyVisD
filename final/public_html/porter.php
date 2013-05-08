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
		# fix $this->b[$this->j+$length+1:-1] to use substr
		$this->b = substr($this->b, 0, $this->j + 1) . $s . $this->b[$this->j+$length+1:-1]
		$this->k = $this->j + $length;
	}

################################################################################

    def r(self, s):
        """r(s) is used further down."""
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        """step1ab() gets rid of plurals and -ed or -ing. e.g.

           caresses  ->  caress
           ponies    ->  poni
           sties     ->  sti
           tie       ->  tie        (--NEW--: see below)
           caress    ->  caress
           cats      ->  cat

           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        """
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                if self.j == 0:
                    self.k = self.k - 1
                # this line extends the original algorithm, so that
                # 'flies'->'fli' but 'dies'->'die' etc
                else:
                    self.k = self.k - 2
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1

        if self.ends("ied"):
            if self.j == 0:
                self.k = self.k - 1
            else:
                self.k = self.k - 2
        # this line extends the original algorithm, so that
        # 'spied'->'spi' but 'died'->'die' etc

        elif self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):   self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
        """step1c() turns terminal y to i when there is another vowel in the stem.
        --NEW--: This has been modified from the original Porter algorithm so that y->i
        is only done when y is preceded by a consonant, but not if the stem
        is only a single consonant, i.e.

           (*c and not c) Y -> I

        So 'happy' -> 'happi', but
          'enjoy' -> 'enjoy'  etc

        This is a much better rule. Formerly 'enjoy'->'enjoi' and 'enjoyment'->
        'enjoy'. Step 1c is perhaps done too soon; but with this modification that
        no longer really matters.

        Also, the removal of the vowelinstem(z) condition means that 'spy', 'fly',
        'try' ... stem to 'spi', 'fli', 'tri' and conflate with 'spied', 'tried',
        'flies' ...
        """
        if self.ends("y") and self.j > 0 and self.cons(self.k - 1):
            self.b = self.b[:self.k] + 'i' + self.b[self.k+1:]

    def step2(self):
        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):   self.r("ate")
            elif self.ends("tional"):  self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):      self.r("ence")
            elif self.ends("anci"):    self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):       self.r("ble") # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):
                if self.m() > 0:                     # --NEW--
                    self.setto("al")
                    self.step2()
            elif self.ends("fulli"):   self.r("ful") # --NEW--
            elif self.ends("entli"):   self.r("ent")
            elif self.ends("eli"):     self.r("e")
            elif self.ends("ousli"):   self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):   self.r("ize")
            elif self.ends("ation"):   self.r("ate")
            elif self.ends("ator"):    self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):     self.r("al")
            elif self.ends("iveness"): self.r("ive")
            elif self.ends("fulness"): self.r("ful")
            elif self.ends("ousness"): self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):     self.r("al")
            elif self.ends("iviti"):   self.r("ive")
            elif self.ends("biliti"):  self.r("ble")
        elif self.b[self.k - 1] == 'g': # --DEPARTURE--
            if self.ends("logi"):
                self.j = self.j + 1     # --NEW-- (Barry Wilkins)
                self.r("og")
        # To match the published algorithm, delete this phrase

    def step3(self):
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
        if self.b[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.b[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'): pass
            elif self.ends("ou"): pass
            # takes care of -ous
            else: return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k-1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k -1

    def stem_word(self, p, i=0, j=None):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed
        is from p[i] to p[j] inclusive. Typically i is zero and j is the
        offset to the last character of a string, (p[j+1] == '\0'). The
        stemmer adjusts the characters p[i] ... p[j] and returns the new
        end-point of the string, k. Stemming never increases word length, so
        i <= k <= j. To turn the stemmer into a module, declare 'stem' as
        extern, and delete the remainder of this file.
        """
        ## --NLTK--
        ## Don't print results as we go (commented out the next line)
        #print p[i:j+1]
        if j is None:
            j = len(p) - 1

        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i

        if self.b[self.k0:self.k+1] in self.pool:
            return self.pool[self.b[self.k0:self.k+1]]

        if self.k <= self.k0 + 1:
            return self.b # --DEPARTURE--

        # With this line, strings of length 1 or 2 don't go through the
        # stemming process, although no mention is made of this in the
        # published algorithm. Remove the line to match the published
        # algorithm.

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k+1]

    def adjust_case(self, word, stem):
        lower = word.lower()

        ret = ""
        for x in xrange(len(stem)):
            if lower[x] == stem[x]:
                ret += word[x]
            else:
                ret += stem[x]

        return ret

    def stem(self, word):
        stem = self.stem_word(word.lower(), 0, len(word) - 1)
        return self.adjust_case(word, stem)

################################################################################

}

?>