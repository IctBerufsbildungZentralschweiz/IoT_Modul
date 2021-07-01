<?php
$output = shell_exec('pgrep -f python3 /');
if ($output == null)
    echo "Script is not running";
else
    echo "script is running"
echo "<pre>$output</pre>";
?>