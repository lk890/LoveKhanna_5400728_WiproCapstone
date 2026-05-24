Feature: Myntra Home Module End To End Testing


Scenario: End to end order placement with login

  Given user launches Myntra website
  When user hovers on Home and Living menu
  And user selects Aromas and Candles category
  And user opens first product
  And user adds product to shopping bag
  And user clicks place order
  And user enters mobile number and logs in
  And user completes OTP manually
  
  Then product should be visible in cart