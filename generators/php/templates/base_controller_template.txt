<?php

require_once 'core/init.php';

abstract class BaseController {

    private $model;
    private $operators = array('gt' => '>',
                               'gte' => '>=',
                               'lt' => '<',
                               'lte' => '<=');

    public function __construct($model) {

        $this->model = $model;

    }

    protected function getModel() {

        return $this->model;

    }

    protected function translateOperator($operator) {

        if(array_key_exists($operator, $this->operators)) {

            return $this->operators[$operator];

        } else {

            return $operator;

        }

    }

    public function handleQuery($request) {

        if($request->parameters) {

            $results = $this->model->get($this->formatParameters($request->parameters));
            return $results;

        } else {

            return $this->model->getAll();

        }

    }
    
    /*
     * The following method is used to parse the request
     * parameters and present them in a format that's readable as
     * sql where-conditions to the database wrapper. 
     * However, due to lack of time there are some inconsistencies
     * in what format the database wrapper expects where conditions to be in
     * for different types of operations.
     * Currently the request parameters must be formatted when inserting
     * and when deleting but not when updating.
     */

    protected function formatParameters($parameters) {

        $where = array();

        foreach($parameters as $parameterName => $parameter) {

            $parameterParts = explode('=', $parameter);

            if(sizeof($parameterParts) == 1) {
                $where[] = array($parameterName, '=', $parameterParts[0]);
            } else {
                $where[] = array($parameterName, $this->translateOperator($parameterParts[0]), $parameterParts[1]);
            }

        }

        return $where;

    }

    protected function filterParameters($whiteListedParameters, $parameters) {
       $filteredParameters = array(); 
        
       foreach($whiteListedParameters as $whiteListedKey) {
           foreach($parameters as $key => $value) {
               if($whiteListedKey == $key) {
                 $filteredParameters[$key] = $value;
               }
           }
       } 
       return $filteredParameters; 
    }
    
    private function unsetAuthenticationParameters(&$request) {
        if(isset($request->parameters['username'])) {
            unset($request->parameters['username']);
        }
        
        if(isset($request->parameters['token'])) {
            unset($request->parameters['token']);
        }
    }

    public function checkToken($requestParameters) {
        $usernameAndToken = $this->filterParameters(array('username', 'token'), $requestParameters);

        $db = $this->model->getDB();

        if($db->get('users', $this->formatParameters($usernameAndToken))->results() != null) {
            return true;
        } else {
            http_response_code(401);
        }
    }

    public abstract function post($request);
    public abstract function put($request);
    public abstract function delete($request);
    
    public function postAction($request) {
       if($this->checkToken($request->parameters)) {
           $this->unsetAuthenticationParameters($request);
           $this->post($request);
       } 
    }
    
    public function putAction($request) {
        $debug = fopen('debug.txt', 'w');
        fwrite($debug, var_export($request->parameters, true));
        fclose($debug);
        if($this->checkToken($request->parameters)) {
            $this->unsetAuthenticationParameters($request);
            $this->put($request);
        } 
        
    }
    
    public function deleteAction($request) {
        if($this->checkToken($request->parameters)) {
            $this->unsetAuthenticationParameters($request);
            $this->delete($request);
        } 
        
    }

}
