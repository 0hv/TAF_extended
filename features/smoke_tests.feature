@ecommerce
Feature: E-commerce platform testing

    Background:
        Given I am on the "<platform>" version of the e-commerce application

    @B2C
    Scenario Outline: B2C - Business-to-Consumer platform testing
        When I land on the homepage
        Then I should see an intuitive user interface
        And I should be able to use a powerful search engine
        And I should see product recommendations based on my preferences
        And I should be able to interact with the shopping cart
        And I should see secure payment options
        And I should be able to manage my user account
        And I should see product reviews and ratings
        And I should be able to track my orders
        And I should see loyalty or reward programs
        And I should receive notifications and alerts

        Examples:
            | platform |
            | web      |
            | mobile   |

    @B2B
    Scenario Outline: B2B - Business-to-Business platform testing
        When I land on the B2B section
        Then I should see role-based access features
        And I should see personalized pricing options
        And I should be able to place bulk orders and see volume discounts
        And I should see a detailed product catalog
        And I should be able to request a quote
        And I should see B2B payment systems
        And I should be able to manage multi-user accounts
        And I should see integration options with ERP systems

        Examples:
            | platform |
            | web      |
            | mobile   |

    @C2C
    Scenario Outline: C2C - Consumer-to-Consumer platform testing
        When I land on the C2C section
        Then I should be able to list my products
        And I should see a seller rating and review system
        And I should be able to chat or message other users
        And I should see an escrow system for payments
        And I should see secure payment options for C2C transactions
        And I should be able to report and see moderation options for listings

        Examples:
            | platform |
            | web      |
            | mobile   |

    @API
    Scenario: API testing for data interfacing
        Given I have access to the e-commerce API
        When I request data for the homepage
        Then I should receive all the necessary data to display on the interface