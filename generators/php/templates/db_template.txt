<?php
class DB {
    private static $_instance = null;
    private $_pdo,
            $_query,
            $_error = false,
            $_results,
            $_count = 0;

    private function __construct() {
        try {
            $this->_pdo = new PDO('mysql:host=' . Config::get('mysql/host') . ';dbname=' . Config::get('mysql/db'),
                                   Config::get('mysql/username'), Config::get('mysql/password'));
        } catch(PDOException $e) {
            die($e->getMessage());
        }
    }

    public static function getInstance() {
        if(!isset(self::$_instance)) {
            self::$_instance = new DB();
        }
        return self::$_instance;
    }

    public function query($sql, $params = array()) {
        $this->_error = false;
        if($this->_query = $this->_pdo->prepare($sql)) {
            $x = 1;
            if(count($params)) {
                foreach($params as $param) {
                    $this->_query->bindValue($x, $param);
                    $x++;
                }
            }

            if($this->_query->execute()) {
                $this->_results = $this->_query->fetchAll(PDO::FETCH_OBJ);
                $this->_count = $this->_query->rowCount();
            } else {
                $this->_error = true;
            }
        }
        return $this;
    }

    public function action($action, $table, $where = array(), $joinCondition = array(), $orderBy = array()) {
        if(count($where == 3)) {
            $operators = array('=', '<', '>', '<=', '>=', 'REGEXP');

            $sql = "$action FROM $table WHERE ";
            $values = array();

            foreach($where as $condition => $parts) {

                $field      = $parts[0];
                $operator   = $parts[1];
                $value      = $parts[2];

                if(in_array($operator, $operators)) {
                    $sql .= "$field $operator ?";
                }

                if($parts != end($where)) {
                    $sql .= " AND ";
                }

                $values[] = $value;
            }

            if(!empty($joinCondition)) {

                if(!empty($where)) {
                        $sql .= " AND ";
                }

                foreach($joinCondition as $condition => $parts) {

                    $column1 = $parts[0];
                    $column2 = $parts[1];

                    $sql .= "$column1 = $column2";

                }
            }

            if(!empty($orderBy)) {
                $sql .= " ORDER BY ";

                foreach($orderBy as $column) {
                    $sql .= "$column";

                    if($column != end($orderBy)) {
                        $sql .= ", ";
                    }
                }
            }

            if(!$this->query($sql, $values)->error()) {
                return $this;
            }
        }
        return false;
    }

    public function insert($table, $fields = array()) {
        $keys = array_keys($fields);
        $values = null;
        $x = 1;

        foreach($fields as $field) {
            $values .= '?';
            if($x < count($fields)) {
                $values .= ', ';
            }
            $x++;
        }

        $sql = "INSERT INTO {$table} (`" . implode('`, `', $keys) . "`) VALUES ({$values})";

        if(!$this->query($sql, $fields)->error()) {
            return true;
        }
        return false;
    }

    public function get($table, $where) {
        return $this->action('SELECT *', $table, $where);
    }

    public function getAll($table) {
        $sql = "SELECT * FROM {$table}";

        if(!$this->query($sql)->error()){
            return $this;
        }
    }

    public function delete($table, $where) {
        return $this->action('DELETE', $table, $where);
    }

    public function update($table, $primaryKey, $fields) {
        $set = '';
        $x = 1;

        foreach($fields as $name => $value) {
            $set .= "{$name} = ?";
            if($x < count($fields)) {
                $set .= ', ';
            }
            $x++;
        }

        $sql = "UPDATE {$table} SET {$set} WHERE {$primaryKey}";
        $debug = fopen('debugfile.txt', 'w');
        fwrite($debug, var_export($sql, true));
        fclose($debug);

        if(!$this->query($sql, $fields)->error()) {
            return true;
        }
        return false;
    }

    public function results() {
        return $this->_results;
    }

    public function first() {
        return $this->results()[0];
    }

    public function count() {
        return $this->_count;
    }

    public function error() {
        return $this->_error;
    }
}