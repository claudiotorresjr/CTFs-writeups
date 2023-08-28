<?php

if($_SERVER['REQUEST_METHOD'] == "POST"){
    $data = json_decode(file_get_contents("php://input"));

    $classe = $data->classe;
    $funcao = $data->funcao;
    $arg = $data->arg;

    $instancia = new $classe();
    $d = call_user_func_array([$instancia, $funcao], $arg);
    echo $d;
    echo "\n";
}else{
    highlight_file(__FILE__);
}
?>