Feature: Proposed questions CRUD

  Scenario: Crear pregunta OK
    Given existe un usuario "user1" con password "pass12345"
    When hago login como "user1" con password "pass12345"
    And voy a "/questions/new/"
    And relleno el formulario de pregunta con texto "Aquesta és una pregunta de prova", categoria "party" y mecanica "repte"
    And envio el formulario
    Then debería ver "Pregunta enviada correctament i pendent de revisió."

  Scenario: Crear sin login
    When voy a "/questions/new/"
    Then debería ser redirigido al login

  Scenario: Editar propia
    Given existe un usuario "user2" con password "pass12345"
    And existe una proposed question de "user2" con texto "Pregunta pendent de user2"
    When hago login como "user2" con password "pass12345"
    And vaig a editar la meva pregunta
    And cambio el texto de la pregunta a "Pregunta editada correctament"
    And envio el formulario
    Then debería ver "Pregunta actualitzada correctament."

  Scenario: Eliminar propia
    Given existe un usuario "user3" con password "pass12345"
    And existe una proposed question de "user3" con texto "Pregunta a eliminar"
    When hago login como "user3" con password "pass12345"
    And vaig a eliminar la meva pregunta
    And confirmo la eliminacion
    Then debería ver "Pregunta eliminada correctament."

  Scenario: Editar d'un altre
    Given existe un usuario "owner1" con password "pass12345"
    And existe un usuario "intrus1" con password "pass12345"
    And existe una proposed question de "owner1" con texto "Pregunta privada del owner"
    When hago login como "intrus1" con password "pass12345"
    And vaig a editar la pregunta d'un altre usuari
    Then hauria de veure un error o redirecció