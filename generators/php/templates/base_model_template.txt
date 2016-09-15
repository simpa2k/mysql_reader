<?php

require_once('core/init.php');

/**
 *
 * Base class for models
 *
 */

abstract class BaseModel {

    private $db;

    public function __construct() {

        $this->db = DB::getInstance();
        
    }

    public function getDB() {

        return $this->db;

    }

    public abstract function get($where);

    public abstract function getAll();
}
