## Django Food Delivery Application

### Project Overview

FoodHub is an online food delivery platform where customers can place instant orders,  
and authorized staff can manage the entire business operations via a simple dashboard.

### Key Features

- **Fast Ordering**  
  Customers can browse menus and place orders without the barrier of a signup process.

- **Dynamic Menu & Cart**  
  A user-friendly interface for browsing food categories, managing shopping cart items, and viewing real-time price calculations.

- **Secure Payment Integration**  
  Reliable transaction processing via PayPal REST API, enabling customers to pay securely with credit cards or PayPal accounts.

- **Centralized Staff Dashboard**  
  A restricted management area dedicated to restaurant operations, accessible only by authenticated Admin and Staff users.

- **Restaurant Management**  
  Full control over the restaurant's offerings and the ability for staff to track and update order statuses (e.g., marking orders as shipped) once they are ready for delivery.

### Technology Stack

#### Backend
- **Framework:** Django (Python-based web framework)
- **Authentication & User Management:** Django-Allauth  
- **Form Rendering:** Django Crispy Forms

#### Frontend
- **Customer Side:** Bootstrap 5  
- **Restaurant Side:** MDBootstrap 5 + Django Crispy Forms  
- **Technologies:** HTML5, CSS3, JavaScript

#### Payment Gateway
- **PayPal REST API Integration** via JavaScript SDK for secure checkout and payment processing

#### Database
- **SQLite** (Relational database used for development and local data storage)

