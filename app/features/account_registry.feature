Feature: Account registry
Scenario: User is able to create a new account
    Given Number of accounts in registry equals: "0"
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909876"
    Then Number of accounts in registry equals: "1"
    And Account with pesel "89092909876" exists in registry

# Scenario: User is able to create a second account
   Given Number of accounts in registry equals: "1"
   When I create an account using name: "dave", last name: "grohl", pesel: "70032312345"
   Then Number of accounts in registry equals: "2"
   And Account with pesel "70032312345" exists in registry

Scenario: User is able to update name of already created account
    Given Account with pesel "89092909876" exists in registry
    When I update "name" of account with pesel: "89092909876" to "russell"
    Then Account with pesel "89092909876" has "name" equal to "russell"

# Scenario: User is able to update surname of already created account
    Given Account with pesel "89092909876" exists in registry
    When I update "surname" of account with pesel: "89092909876" to "hendrix"
    Then Account with pesel "89092909876" has "surname" equal to "hendrix"

Scenario: User is able to delete already created account
    Given Account with pesel "89092909876" exists in registry
    When I delete account with pesel: "89092909876"
    Then Account with pesel "89092909876" does not exist in registry
    And Number of accounts in registry equals: "1"

# Scenario: User is able to delete last account
    Given Account with pesel "70032312345" exists in registry
    When I delete account with pesel: "70032312345"
    Then Number of accounts in registry equals: "0"
    And Account with pesel "89092909876" does not exist in registry