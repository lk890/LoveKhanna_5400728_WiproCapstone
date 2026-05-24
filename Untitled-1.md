11:39:53 | INFO | ========== PYTEST E2E STARTED ==========
11:39:53 | INFO | Opening Myntra website
11:39:57 | INFO | ✅ ASSERT PASSED: Page title contains 'Myntra' → 'Online Shopping for Women, Men, Kids Fashion & Lifestyle - Myntra'
11:39:57 | INFO | Hovering on Home & Living menu
11:39:58 | INFO | ✅ ASSERT PASSED: 'Aromas & Candles' submenu item is visible in dropdown
11:39:59 | INFO | Selecting Aromas & Candles category
11:40:03 | INFO | ✅ ASSERT PASSED: Category URL contains expected keyword → 'https://www.myntra.com/aroma-oil-diffusers-aroma-oils-air-freshener-handheld-air-fresheners-home-fragrances-home-fragrance-set-candles'
11:40:03 | INFO | ✅ ASSERT PASSED: Page <h1> heading contains expected keyword → 'Aroma Oil Diffusers Oils Air Freshener Handheld Fresheners Home Fragrances Fragrance Set Candles'
11:40:03 | INFO | Opening first product
11:40:04 | INFO | ✅ ASSERT PASSED: New product tab opened → total tabs: 2
11:40:04 | INFO | Switching to product tab
11:40:06 | INFO | ✅ ASSERT PASSED: 'Add to Bag' button is visible and clickable on product page
11:40:06 | INFO | Adding product to bag
11:40:17 | INFO | Bag count indicator not found; continuing
11:40:17 | INFO | Opening shopping bag
11:40:21 | INFO | Verifying product in cart
11:40:21 | INFO | ✅ ASSERT PASSED: Product is present in shopping cart
11:40:21 | INFO | Clicking PLACE ORDER
11:40:25 | INFO | ✅ ASSERT PASSED: Redirected to Login/Checkout page → 'https://www.myntra.com/login?referer=/checkout/cart'
11:40:25 | INFO | Entering mobile number
11:40:29 | INFO | Waiting for OTP flow (manual step – up to 30 s)
11:40:59 | INFO | ✅ ASSERT PASSED: Second CONTINUE button found and clicked after OTP
11:41:14 | INFO | ✅ ASSERT PASSED: OTP completed, redirected to checkout/cart → 'https://www.myntra.com/checkout/cart?loggedIn=true'
11:41:16 | INFO | ✅ ASSERT PASSED: Final cart contains 4 product(s) after login
11:41:16 | INFO | ========== TEST PASSED ==========
11:41:20 | INFO | ========== START TEST: table_lamps ==========
11:41:23 | INFO | ✅ ASSERT PASSED: Title contains 'Myntra' → 'Online Shopping for Women, Men, Kids Fashion & Lifestyle - Myntra'
11:41:25 | INFO | ✅ ASSERT PASSED: Home & Living nav menu is visible after hover
11:41:28 | INFO | ✅ ASSERT PASSED: Category URL contains 'tablelamp' → https://www.myntra.com/tablelamp
11:41:28 | INFO | ========== TEST COMPLETED: table_lamps ==========
11:41:32 | INFO | ========== START TEST: cups_mugs ==========
11:41:36 | INFO | ✅ ASSERT PASSED: Title contains 'Myntra' → 'Online Shopping for Women, Men, Kids Fashion & Lifestyle - Myntra'
11:41:38 | INFO | ✅ ASSERT PASSED: Home & Living nav menu is visible after hover
11:41:43 | INFO | ✅ ASSERT PASSED: Category URL contains 'cups-and-mugs' → https://www.myntra.com/cups-and-mugs
11:41:43 | INFO | Sort dropdown clicked for option: Price: High to Low
11:41:43 | INFO | ✅ ASSERT PASSED: Sort dropdown list is visible
11:41:44 | INFO | ✅ ASSERT PASSED: Sort 'Price: High to Low' applied — page still active at https://www.myntra.com/cups-and-mugs?sort=price_desc
11:41:44 | INFO | ========== TEST COMPLETED: cups_mugs ==========
11:41:48 | INFO | ========== START TEST: door_mats ==========
11:41:50 | INFO | ✅ ASSERT PASSED: Title contains 'Myntra' → 'Online Shopping for Women, Men, Kids Fashion & Lifestyle - Myntra'
11:41:52 | INFO | ✅ ASSERT PASSED: Home & Living nav menu is visible after hover
11:41:58 | INFO | ✅ ASSERT PASSED: Category URL contains 'doormats' → https://www.myntra.com/doormats
11:41:58 | INFO | ✅ ASSERT PASSED: Brand checkbox 'Aura' found in DOM
11:42:00 | INFO | Brand filter 'Aura' label clicked via JS
11:42:01 | INFO | ✅ ASSERT PASSED: Brand 'Aura' checkbox is now checked/selected
11:42:01 | INFO | ========== TEST COMPLETED: door_mats ==========
11:42:05 | INFO | ========== START TEST: bathroom_accessories ==========
11:42:08 | INFO | ✅ ASSERT PASSED: Title contains 'Myntra' → 'Online Shopping for Women, Men, Kids Fashion & Lifestyle - Myntra'
11:42:10 | INFO | ✅ ASSERT PASSED: Home & Living nav menu is visible after hover
11:42:15 | INFO | ✅ ASSERT PASSED: Category URL contains 'bathroom-accessories' → https://www.myntra.com/bathroom-accessories
11:42:15 | INFO | Sort dropdown clicked for option: Popularity
11:42:15 | INFO | ✅ ASSERT PASSED: Sort dropdown list is visible
11:42:16 | INFO | ✅ ASSERT PASSED: Sort 'Popularity' applied — page still active at https://www.myntra.com/bathroom-accessories?sort=popularity
11:42:16 | INFO | ========== TEST COMPLETED: bathroom_accessories ==========
11:42:20 | INFO | ========== START TEST: organisers_negative ==========
11:42:23 | INFO | ✅ ASSERT PASSED: Title contains 'Myntra' → 'Online Shopping for Women, Men, Kids Fashion & Lifestyle - Myntra'
11:42:25 | INFO | ✅ ASSERT PASSED: Home & Living nav menu is visible after hover
11:42:30 | INFO | ✅ ASSERT PASSED: Category URL contains 'organisers' → https://www.myntra.com/organisers
11:42:33 | INFO | Checking absence of invalid filters on organisers page
11:42:44 | INFO | ✅ ASSERT PASSED: 'Bed Size' filter correctly absent
11:42:54 | INFO | ✅ ASSERT PASSED: 'Small' filter option correctly absent
11:42:54 | INFO | ========== TEST COMPLETED: organisers_negative ==========
11:42:58 | INFO | ========== START TEST: bedsheets_negative ==========
11:43:03 | INFO | ✅ ASSERT PASSED: Title contains 'Myntra' → 'Online Shopping for Women, Men, Kids Fashion & Lifestyle - Myntra'
11:43:05 | INFO | ✅ ASSERT PASSED: Home & Living nav menu is visible after hover
11:43:10 | INFO | ✅ ASSERT PASSED: Category URL contains 'bedsheets' → https://www.myntra.com/bedsheets
11:43:10 | INFO | Sort dropdown opened for negative check
11:43:20 | INFO | ✅ ASSERT PASSED: Invalid sort option 'free' correctly absent from dropdown
11:43:20 | INFO | ========== TEST COMPLETED: bedsheets_negative ==========
