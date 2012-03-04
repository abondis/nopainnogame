<?php
define("FILELOG","move.log");
define("FORWARD","F");
define("BACKWARD","B");
define("TURN_LEFT","L");
define("TURN_RIGHT","R");

include 'lib.php';
 $url = 'http://bots.myrobots.com/channels/589/feed/last.json';
 $status = json_decode(file_get_contents($url));
 
 if( strlen(trim($status->field1)) == 0 ) {
 	die('nothing to do');
 }
 
 $log = array(
 	'direction'=>$status->field1, 
 	'value' => $status->field2, 
 	'isHit' => $status->field3, 
 	'timestamp' => time()
 );
 $log = json_encode($log);
 file_put_contents(FILELOG, $log."\r\n", FILE_APPEND);
 
 $orderDirection = FORWARD;
 $orderValue = 0;
 
 // Collision !
 if($isHit) {
 	$lastmove = getlastmove();
 	
 	$orderDirection = TURN_LEFT;
 	$orderValue = 1;
 	
 	// si le robot a tourne de 90degree
 	if( $lastmove['direction'] == TURN_LEFT && $lastmove['rotation'] == 1) {
 		$orderValue = 2; 		
 	}
 	
 } else {
 	
 	$orderDirection = FORWARD;
 	$orderValue = 0;
 	
 }

 $url = 'http://bots.myrobots.com/update?key=1647186ED7164FCE&field4='.$orderDirection.'&field5='.$orderValue.'&field6=0';
 file_get_contents($url);
 
 echo '<h1>DEBUG</h1>';
 echo '<pre>';
 var_dump($status);
 echo '</pre>';
 
 echo '<ul>ORDER';
 echo '<li>DIRECTION = '.$orderDirection.'</li>';
 echo '<li>VALUE = '.$orderValue.'</li>';
 echo '</UL>';
 
 
 ?>