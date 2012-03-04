<?php
function getlastmove() {
	$file = FILELOG;
	$data = file($file);
	$line = $data[count($data)-1];
	$j = json_decode($line);
	return $j;
} 