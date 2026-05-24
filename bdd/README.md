“Why Page Object Model?”

Answer:

Page Object Model improves code reusability,
maintainability, and reduces duplicate code.
Each webpage is stored separately as a class.



Mention these confidently:

Selenium with Pytest
BDD using Behave
Explicit waits
Page Object Model
HTML Reporting
Screenshot capture
Logging
Data-driven testing
Git version control



Add HTML Report

Run:

pytest --html=reports/report.html



Add Logging

Example:

logger.info("Opening Home Decor category")
logger.error("Product not found")




Automation Testing Framework for Myntra Home Module
Using Selenium, Pytest, Behave, and Python

🧭 Your Updated E2E Flow (Correct Design)

🛒 PART 1: Product Journey
Open Myntra
Hover → Home & Living
Select Aromas & Candles
Open product
Add to bag
Open cart

💳 PART 2: Checkout Flow
Click Place Order
Redirect → Login page
Enter mobile number: 9760076422
Tick checkbox
Click Continue

⏳ PART 3: OTP WAIT (IMPORTANT)
WAIT for manual OTP entry
User completes OTP manually
Continue button triggers login success
🔁 PART 4: BACK TO PRODUCT FLOW
Redirect back to Myntra product/cart context
Again click Place Order
Click Continue to order



pytest -v --alluredir=reports/allure-results



allure generate reports/allure-results -o reports/allure-report --clean

allure open reports/allure-report




11:09:50 | INFO | ========== PYTEST E2E STARTED ==========
11:09:50 | INFO | Opening Myntra website
11:09:54 | INFO | Home page title verified: Online Shopping for Women, Men, Kids Fashion & Lifestyle - Myntra
11:09:54 | INFO | Hovering on Home & Living menu
11:10:06 | INFO | Submenu item not yet found by LINK_TEXT; continuing anyway
11:10:06 | INFO | Selecting Aromas & Candles category
11:10:12 | INFO | Category page URL verified: https://www.myntra.com/aroma-oil-diffusers-aroma-oils-air-freshener-handheld-air-fresheners-home-fragrances-home-fragrance-set-candles
11:10:12 | INFO | Category heading verified: Aroma Oil Diffusers Oils Air Freshener Handheld Fresheners Home Fragrances Fragrance Set Candles
11:10:12 | INFO | Opening first product
11:10:13 | INFO | New tab verified
11:10:13 | INFO | Switching to product tab
11:10:16 | INFO | Adding product to bag
11:10:27 | INFO | Bag count indicator not found; continuing
11:10:27 | INFO | Opening shopping bag
11:10:32 | INFO | Verifying product in cart
11:10:32 | INFO | Cart verification successful
11:10:32 | INFO | Clicking PLACE ORDER
11:10:36 | INFO | Login/Checkout page verified: https://www.myntra.com/login?referer=/checkout/cart
11:10:36 | INFO | Entering mobile number
11:10:39 | INFO | Waiting for OTP flow (manual step – up to 30 s)
11:11:09 | INFO | Second CONTINUE clicked
11:11:38 | INFO | OTP completed successfully
11:11:40 | INFO | Final cart verified with 4 product(s)
11:11:40 | INFO | ========== TEST PASSED ==========
