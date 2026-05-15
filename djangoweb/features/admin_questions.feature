Feature: Admin moderation of proposed questions

  Scenario: Admin aprova
    Given existe un admin "admin1" con password "admin12345"
    And existe un usuario "user4" con password "pass12345"
    And existe una proposed question de "user4" con texto "Pregunta per aprovar"
    When hago login como "admin1" con password "admin12345"
    And voy a "/admin-panel/questions/"
    And apruebo la pregunta pendiente
    Then la pregunta hauria d'estar aprovada

  Scenario: Admin rebutja
    Given existe un admin "admin2" con password "admin12345"
    And existe un usuario "user5" con password "pass12345"
    And existe una proposed question de "user5" con texto "Pregunta per rebutjar"
    When hago login como "admin2" con password "admin12345"
    And voy a "/admin-panel/questions/"
    And voy a rebutjar la pregunta pendiente
    And escribo la nota de rechazo "No encaixa amb el joc"
    And envio el formulario
    Then la pregunta hauria d'estar rebutjada amb la nota "No encaixa amb el joc"