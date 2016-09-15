<?php

require_once 'core/init.php';

/**
 *
 * Base class for controller classes
 *
 */

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

    /**
     *
     * Method for translating operators
     * from the format used in RESTful
     * requests to those used in the database.
     *
     * @param string $operator An operator in RESTful format
     * to be translated to a traditional arithmetic operator.
     *
     */

    protected function translateOperator($operator) {

        if(array_key_exists($operator, $this->operators)) {

            return $this->operators[$operator];

        } else {

            return $operator;

        }

    }

    /**
     *
     * Method for determining if
     * a request should be routed to
     * a model's get() or getAll() method.
     *
     * @param Request $request A request object.
     *
     */

    public function handleQuery($request) {

        if($request->parameters) {

            $results = $this->model->get($this->formatParameters($request->parameters));
            return $results;

        } else {

            return $this->model->getAll();

        }

    }
    
    /**
     *
     * Method used to parse the request
     * parameters of a request object and present them in a format that
     * the database wrapper in turn can translate to sql.
     * However, due to lack of time there are some inconsistencies
     * in what format the database wrapper expects where conditions to be in
     * for different types of operations.
     * Currently the request parameters must be formatted when inserting
     * and when deleting but not when updating.
     *
     * @param mixed[] $parameters Request parameters to be formatted.
     *
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

    /**
     *
     * Method to pick out certain parameters of interest
     * from an array.
     *
     * @param string[] $whiteListedParameters An array containing the parameters to be picked out.
     * @param mixed[] $parameters An array of parameters to be filtered.
     *
     */

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

    /**
     *
     * Method to remove authentication parameters
     * from a request. This method is necessary due to the fact that
     * this api expects authentication information to be passed as part
     * of the json representing the database object. Usually this information
     * is provided in the HTTP header, and if that had been the case this
     * wouldn't be necessary.
     *
     * @param Request &$request The addres of a request object to be modified.
     *
     */

    private function unsetAuthenticationParameters(&$request) {
        if(isset($request->parameters['username'])) {
            unset($request->parameters['username']);
        }
        
        if(isset($request->parameters['token'])) {
            unset($request->parameters['token']);
        }
    }

    /**
     *
     * Method to check an authentication token.
     *
     * @param mixed[] $requestParameters An array of parameters containing
     * a username and a token to be checked.
     *
     */

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

    /**
     *
     * Method to handle a post request. Requires authentication.
     *
     * @param Request $request A post request to be handled.
     *
     */

    public function postAction($request) {
       if($this->checkToken($request->parameters)) {
           $this->unsetAuthenticationParameters($request);
           $this->post($request);
       } 
    }

    /**
     *
     * Method to handle a put request. Requires authentication.
     *
     * @param Request $request A put request to be handled.
     *
     */

    public function putAction($request) {
        if($this->checkToken($request->parameters)) {
            $this->unsetAuthenticationParameters($request);
            $this->put($request);
        } 
        
    }

    /**
     *
     * Method to handle a delete request. Requires authentication.
     *
     * @param Request $request A delete request to be handled.
     *
     */

    public function deleteAction($request) {
        if($this->checkToken($request->parameters)) {
            $this->unsetAuthenticationParameters($request);
            $this->delete($request);
        } 
        
    }

}
